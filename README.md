# TCPPortScanner
`tcp-port-scanner` — a lightweight Python script to scan TCP ports on target hosts. Designed for *authorized testing only* (use only on hosts you own or have explicit permission to test). Perfect for light pentesting, network security practice, or quick service checks.

---

## ✨ Key Features

* Parallel TCP port scanning using `ThreadPoolExecutor`.
* Flexible port range parsing: `1-1024`, `22,80,443`, or a combination.
* Adjustable number of threads for speed/load control.
* Per-connection timeout option for faster detection or more thorough scanning.
* Detects common service names (if available) via `socket.getservbyport`.
* Results can be saved to CSV.
* Lightweight — relies only on standard Python modules (no external dependencies).

---

## ❗ Important Warning (Read Before Use)

**Do not** use this script to scan or attack servers you do not own or do not have explicit permission for. Unauthorized port scanning can violate laws and service provider policies.

Use only for: hosts you own, lab environments, or targets explicitly permitted in writing.

---

## 📦 Requirements

* Python 3.7+ (recommended 3.8+)
* Only standard Python modules — no additional installation required.

---

## 🚀 Usage

Run the script from terminal/command prompt:

```bash
python port_scanner.py <target> [--ports PORTS] [--threads N] [--timeout S] [--output file.csv]
```

**Examples:**

```bash
# Scan 1-1024 on a target IP
python port_scanner.py 192.168.1.10 --ports 1-1024

# Scan specific ports and save results
python port_scanner.py example.com --ports 22,80,443,8080 --threads 50 --timeout 1.0 --output results.csv
```

---

## 🛠️ Options / Flags

* `host` : target hostname or IP address.
* `--ports` : port range or list (default `1-1024`). Example: `22,80,443,8000-8100`.
* `--threads` : number of parallel threads (default `50`). Max capped at 1000.
* `--timeout` : per-connection socket timeout in seconds. Default `0.8`.
* `--output` : optional CSV file path to save results.

---

## 📋 CSV Result Format

CSV contains columns:

```
host, ip, port, service
```

Example row:

```
example.com, 93.184.216.34, 80, http
```

---

## 🔍 Technical Overview

* DNS resolution via `socket.gethostbyname`.
* IP validation using `ipaddress.ip_address`.
* Port parser accepts single numbers, ranges `a-b`, and comma-separated combinations.
* Parallel scanning using `concurrent.futures.ThreadPoolExecutor`.
* Connection checked with `socket.connect_ex` (non-blocking with timeout).

---

## 🧰 Usage Tips & Performance

* Increasing `--threads` speeds up scans on responsive networks but increases resource load (and may trigger firewall alerts).
* For public Internet targets, use a higher timeout (e.g., `--timeout 1.0`) to avoid false negatives.
* For local networks, smaller timeout (`0.2-0.8`) is usually sufficient.

---

## 🐞 Troubleshooting

* **Cannot resolve hostname**: ensure DNS works or use direct IP.
* **Scan is slow / interrupted**: reduce thread count or increase timeout.
* **No open ports found despite services running**: try increasing timeout and verify that target firewall is not dropping connections.

---

## 💡 Development Ideas (Contributions)

* Add IPv6 support.
* Add UDP scan mode (with reliability caveats/permissions).
* Integrate banner grabbing for more accurate service identification.
* Stealth mode (throttling, random delay) for smoother testing.

Contributions accepted via Pull Requests — include test cases and change description.

---

## 🔐 SECURITY.md (Summary)

**Security policy for this project:**

* **Scope:** Script is for *authorized testing only*.
* **Vulnerability reporting:** If you find bugs that allow end-to-end exploitation, report via GitHub *issue* or email. Do not publish exploit details before patching.
* **Privacy & data:** Do not use the script to access or extract sensitive data without permission.
* **Dependency audit:** No external dependencies, so focus on audit of scanning logic and input validation.

---

## 📚 References / Further Reading

* Books & materials on *network scanning* and *ethical hacking*.
* Python documentation for `socket`, `concurrent.futures`, `ipaddress`.

---

## © License

License file is already available in the repository. Check `LICENSE` for full usage rights and limitations.

---

Thank you for using this script — hope it helps with your network security activities.
