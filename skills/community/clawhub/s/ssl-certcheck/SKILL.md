---
name: ssl-certcheck
description: Check SSL/TLS certificates for any hostname — expiry dates, issuer, SANs, protocol version, cipher suite. Use when asked to check if a certificate is valid, see when a cert expires, inspect TLS details, or audit HTTPS security. Alerts on expired or soon-to-expire certs. Zero dependencies — pure Python ssl/socket.
---

# certcheck 🔒

SSL/TLS certificate inspector with expiry alerts.

## Commands

```bash
# Check one or more hosts
python3 scripts/certcheck.py github.com google.com openclaw.ai

# JSON output for scripting
python3 scripts/certcheck.py --json example.com

# Custom expiry warning threshold (default 30 days)
python3 scripts/certcheck.py --days 60 mysite.com

# Custom port
python3 scripts/certcheck.py -p 8443 internal.example.com
```

## Output
- ✅ Valid cert with >30 days remaining
- ⚠️ Cert expiring within threshold
- ❌ Expired or connection failed
- Shows: CN, issuer, expiry date + days left, TLS version, cipher, SANs

## Exit Codes
- 0: All certs healthy
- 1: One or more expired/expiring (useful for cron monitoring)
