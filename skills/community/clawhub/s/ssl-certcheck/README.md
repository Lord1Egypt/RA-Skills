# certcheck 🔒

SSL/TLS certificate checker. Inspect cert expiry, issuer, SANs, protocol, and cipher for any hostname. Alerts on expired or soon-to-expire certificates. Zero dependencies.

## Usage
```bash
python3 certcheck.py github.com google.com
python3 certcheck.py --json example.com
python3 certcheck.py --days 60 mysite.com  # warn if <60 days
```
