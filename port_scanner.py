#!/usr/bin/env python3
"""
Simple TCP Port Scanner (for authorized testing only).

Usage examples:
  python port_scanner.py 192.168.1.10 --ports 1-1024
  python port_scanner.py example.com --ports 22,80,443,8080 --threads 50 --timeout 1.0 --output results.csv

Always scan only hosts you own or have explicit permission to test.
"""

import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from ipaddress import ip_address
import csv
import sys

def parse_ports(ports_str):
    ports = set()
    for part in ports_str.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            try:
                a, b = part.split('-', 1)
                a, b = int(a), int(b)
                if a > b:
                    a, b = b, a
                ports.update(range(max(1, a), min(65535, b) + 1))
            except ValueError:
                print(f"[WARN] Ignoring invalid port range: '{part}'", file=sys.stderr)
        else:
            try:
                p = int(part)
                if 1 <= p <= 65535:
                    ports.add(p)
                else:
                    print(f"[WARN] Ignoring out-of-range port: {p}", file=sys.stderr)
            except ValueError:
                print(f"[WARN] Ignoring invalid port: '{part}'", file=sys.stderr)
    return sorted(ports)

def scan_port(host, port, timeout):
    """Return tuple (port, True/False, service_name_or_empty)"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            res = s.connect_ex((host, port))
            if res == 0:
                # Try get common service name
                try:
                    svc = socket.getservbyport(port, "tcp")
                except Exception:
                    svc = ""
                return (port, True, svc)
            else:
                return (port, False, "")
    except Exception:
        return (port, False, "")

def main():
    parser = argparse.ArgumentParser(description="Simple TCP Port Scanner (authorized testing only).")
    parser.add_argument("host", help="Target hostname or IP address")
    parser.add_argument("--ports", default="1-1024", help="Ports to scan, e.g. '1-1024' or '22,80,443,8000-8100'")
    parser.add_argument("--threads", type=int, default=50, help="Number of concurrent threads (default: 50)")
    parser.add_argument("--timeout", type=float, default=0.8, help="Socket timeout in seconds (default: 0.8)")
    parser.add_argument("--output", help="Optional CSV output file (path) to save results")
    args = parser.parse_args()

    # Resolve host to IP
    try:
        target_ip = socket.gethostbyname(args.host)
    except Exception as e:
        print(f"[!] Could not resolve host {args.host}: {e}", file=sys.stderr)
        return

    try:
        ip_address(target_ip)  # validate
    except Exception:
        print(f"[!] Resolved address {target_ip} is invalid.", file=sys.stderr)
        return

    ports = parse_ports(args.ports)
    if not ports:
        print("[!] No valid ports to scan.", file=sys.stderr)
        return

    print(f"Target: {args.host} ({target_ip})")
    print(f"Ports: {len(ports)} ports ({ports[0]}-{ports[-1]})")
    print(f"Threads: {args.threads}, Timeout: {args.timeout}s")
    print("Starting scan...\n")

    start = datetime.now()
    open_ports = []

    # Limit threads to sensible max
    max_threads = min(max(1, args.threads), 1000)

    try:
        with ThreadPoolExecutor(max_workers=max_threads) as ex:
            futures = { ex.submit(scan_port, target_ip, p, args.timeout): p for p in ports }
            for fut in as_completed(futures):
                port = futures[fut]
                try:
                    portnum, is_open, svc = fut.result()
                    if is_open:
                        print(f"[OPEN]  Port {portnum:5d}  Service: {svc or '-'}")
                        open_ports.append((portnum, svc))
                except Exception as e:
                    print(f"[ERROR] port {port}: {e}", file=sys.stderr)
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user (Ctrl+C). Shutting down...", file=sys.stderr)
    except Exception as e:
        print(f"[!] Unexpected error during scan: {e}", file=sys.stderr)

    elapsed = datetime.now() - start
    print("\nScan finished in", str(elapsed).split('.')[0])
    print(f"Open ports found: {len(open_ports)}")
    for p, s in open_ports:
        print(f" - {p}  {s or ''}")

    if args.output:
        try:
            with open(args.output, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["host", "ip", "port", "service"])
                for p, s in open_ports:
                    writer.writerow([args.host, target_ip, p, s])
            print(f"Results saved to {args.output}")
        except Exception as e:
            print(f"[!] Could not save results: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
