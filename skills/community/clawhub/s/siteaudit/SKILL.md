---
name: siteaudit
description: Comprehensive website audit combining uptime check, TLS certificate inspection, and security headers grading in one command. Use when asked to audit a website, check site health, verify HTTPS setup, or get a full security overview of a domain. Reports response time, cert expiry, header grades, and flags issues. Zero dependencies — pure Python.
---

# siteaudit 🔍

All-in-one website health audit: uptime + TLS + security headers.

## Commands

```bash
# Audit one or more sites
python3 scripts/siteaudit.py github.com openclaw.ai example.com

# JSON output for automation/cron
python3 scripts/siteaudit.py --json mysite.com
```

## Checks Performed
1. **Uptime** — HTTP HEAD request, response time in ms, status code
2. **TLS Certificate** — expiry date, days remaining, issuer, protocol version
3. **Security Headers** — grades A-F based on 6 critical headers (HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy)

## Issue Detection
- ❌ Site DOWN (connection/5xx errors)
- ⚠️ Slow response (>2s)
- ❌ TLS errors
- ⚠️ Certificate expiring within 14 days
- ⚠️ Weak security headers (grade D or F)

## Exit Codes
- 0: All sites healthy
- 1: One or more issues detected
