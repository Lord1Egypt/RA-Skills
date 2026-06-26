---
name: recon-quick
description: Fast OSINT and reconnaissance presets using bbot and nmap. One-command subdomain enumeration, port scanning, and web fingerprinting for bug bounty recon.
metadata: {"openclaw":{"emoji":"🔍","requires":{"bins":["bbot","nmap"]},"install":[{"id":"bbot","kind":"pipx","packages":["bbot"],"label":"Install bbot via pipx"}]}}
---

# Recon Quick — Fast OSINT Presets

One-command recon using bbot and nmap. Preset workflows for common bug bounty recon tasks.

## Prerequisites

```bash
pipx install bbot
# nmap: apt install nmap / brew install nmap
```

## Quick Start

```bash
# Full subdomain enumeration + web probe
python3 {baseDir}/scripts/recon.py target.com --preset full

# Just subdomains
python3 {baseDir}/scripts/recon.py target.com --preset subdomains

# Quick port scan top 100
python3 {baseDir}/scripts/recon.py target.com --preset ports
```

## Presets

| Preset | What it does | Time |
|--------|-------------|------|
| `subdomains` | Subdomain enum via bbot | 2-10 min |
| `ports` | Top 100 ports + service detection | 1-5 min |
| `web` | HTTP probe + tech fingerprint | 2-5 min |
| `full` | Subdomains + ports + web + nuclei | 10-30 min |
| `passive` | Passive recon only (DNS, certs, APIs) | 1-3 min |

## Options

- `--preset PRESET` — Recon preset (default: subdomains)
- `--output DIR` — Output directory (default: `./recon-output`)
- `--json` — Output as JSON
- `--threads N` — Thread count (default: 10)
- `--wordlist FILE` — Custom wordlist for subdomain brute
- `--proxy URL` — Proxy for web requests

## Output Structure

```
recon-output/
├── target.com/
│   ├── subdomains.txt      # Discovered subdomains
│   ├── live-hosts.txt       # Alive HTTP services
│   ├── ports.txt            # Open ports
│   ├── tech-fingerprints.txt # Detected technologies
│   ├── nuclei-findings.txt  # Vulnerability scan results
│   └── full-report.json     # Everything combined
```

## Integration with Bug Bounty

```bash
# Run recon, generate report
python3 recon.py target.com --preset full --output ./bounties/target
bb-report-template --type recon --target target.com -o report.md
```

## Notes

- bbot handles rate limiting and scope validation automatically
- Nuclei findings are informational — manual verification required
- Always check program scope before scanning
- Use `--proxy socks5://127.0.0.1:9050` for Tor
