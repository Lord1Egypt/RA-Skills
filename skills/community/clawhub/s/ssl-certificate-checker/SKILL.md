---
name: ssl-certificate-checker
description: Check SSL/TLS certificate details including expiration date, issuer, validity, cipher suites, and security warnings for any domain. Use when verifying HTTPS security, monitoring certificate expiry, or troubleshooting SSL issues.
---

# SSL Certificate Checker

Analyze SSL/TLS certificates for any domain to verify security configuration and monitor expiration.

## When to Use

- Checking SSL certificate expiration dates
- Verifying certificate chain and issuer
- Troubleshooting HTTPS connection issues
- Auditing website security configuration
- Monitoring certificates before renewal

## When NOT to Use

- Penetration testing (this is read-only)
- Internal network certificates (use dedicated tools)
- Certificate installation (this only checks, doesn't install)

## Examples

### Basic Certificate Check

```bash
# Check certificate for a domain
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | openssl x509 -noout -dates -subject -issuer

# Get detailed certificate information
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -text