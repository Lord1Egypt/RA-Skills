---
name: security-audit-owasp
version: 1.0.0
description: "Full OWASP, Nmap, Nikto vulnerability assessment for OpenClaw deployments. Scan your infrastructure, harden configs, and generate compliance reports."
license: MIT
tags: [security, owasp, nmap, nikto, vulnerability, audit, pentest, hardening, compliance, infrastructure]
source: el-rudo-larios/security-audit
trigger: "security audit vulnerability scan penetration test OWASP hardening"
metadata:
  openclaw:
    emoji: "🔒"
---

# Security Audit — OWASP, Nmap, Nikto

Comprehensive security auditing toolkit for OpenClaw deployments. Scan your infrastructure, identify vulnerabilities, and harden configs.

## What It Does

1. **Port Scanning** — Nmap service detection, OS fingerprinting, script scanning
2. **Web Vulnerability Assessment** — Nikto web server scans, OWASP Top 10 checks
3. **Infrastructure Hardening** — SSH config audit, firewall rules, exposed services
4. **Compliance Reports** — Structured JSON output, severity ratings, remediation steps

## Quick Start

```bash
# Full security audit
bash scripts/security-audit.sh --target 192.168.1.0/24 --output reports/

# Quick port scan
bash scripts/quick-audit.sh --target localhost
```

## Features

- Automated Nmap scans with service version detection
- Nikto web vulnerability assessment
- OWASP Top 10 checklist verification
- SSH hardening recommendations
- Firewall rule audit
- Structured JSON reports with severity ratings
- Remediation scripts for common findings

## Requirements

- OpenClaw 2.0+
- Nmap (apt install nmap)
- Nikto (apt install nikto)
- Python 3.10+

## License

MIT
