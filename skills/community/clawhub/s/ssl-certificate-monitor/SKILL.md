---
name: ssl-certificate-monitor
description: Monitor SSL certificates for expiration, security issues, and compliance across domains and subdomains.
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
      python:
        - cryptography
---

# SSL Certificate Monitor

## What This Does

A CLI tool to monitor SSL/TLS certificates for expiration dates, security issues, and basic compliance checks. Check single domains or multiple domains from a list, get detailed certificate information, and receive alerts before certificates expire.

Key features:
- **Check expiration dates** for SSL certificates on domains and subdomains
- **Detailed certificate info** - issuer, subject, serial number, signature algorithm
- **Security validation** - check certificate chain, basic trust validation
- **Batch monitoring** - check multiple domains from a file or list
- **Alert thresholds** - warn when certificates expire within specified days (default 30 days)
- **JSON output** - machine-readable output for integration with monitoring systems
- **Simple CLI interface** - easy to use in scripts or cron jobs
- **No external API required** - uses Python's SSL/TLS libraries

## When To Use

- You need to monitor SSL certificate expiration for your websites
- You want to automate certificate renewal reminders
- You're managing multiple domains and subdomains
- You need to validate certificate chain and basic security
- You want to integrate SSL monitoring into your DevOps pipeline
- You're auditing domains for certificate compliance
- You need to check certificates on internal servers or development environments

## Usage

Basic commands:

```bash
# Check a single domain
python3 scripts/main.py check example.com

# Check with custom port
python3 scripts/main.py check example.com --port 443

# Check multiple domains from a file (one domain per line)
python3 scripts/main.py batch domains.txt

# Set custom warning threshold (days before expiration)
python3 scripts/main.py check example.com --warning-days 14

# Output JSON for machine processing
python3 scripts/main.py check example.com --json

# Check certificate details (issuer, subject, algorithm, etc.)
python3 scripts/main.py details example.com

# Validate certificate chain and basic security
python3 scripts/main.py validate example.com
```

## Examples

### Example 1: Check single domain expiration

```bash
python3 scripts/main.py check example.com
```

Output:
```
✅ Domain: example.com:443
   Status: Valid
   Expires: 2026-06-15 23:59:59 UTC
   Days remaining: 101
   Issuer: Let's Encrypt Authority X3
   Subject: CN=example.com
   Algorithm: SHA256-RSA
```

### Example 2: Check with warning threshold

```bash
python3 scripts/main.py check example.com --warning-days 30
```

Output (if expiring within 30 days):
```
⚠️  Domain: example.com:443
   Status: Expiring soon
   Expires: 2026-03-10 23:59:59 UTC
   Days remaining: 4
   Issuer: Let's Encrypt Authority X3
   Subject: CN=example.com
   Algorithm: SHA256-RSA
   Warning: Certificate expires in 4 days
```

### Example 3: Batch check from file

```bash
python3 scripts/main.py batch domains.txt --warning-days 30
```

Output:
```
📋 Batch check results (5 domains):
✅ example.com: Valid (101 days remaining)
✅ api.example.com: Valid (95 days remaining)
⚠️  staging.example.com: Expiring soon (15 days remaining)
❌ internal.example.com: Invalid (Certificate expired 2 days ago)
❌ old.example.com: Connection failed (Timeout)

Summary: 3 valid, 1 expiring soon, 1 expired, 1 failed
```

### Example 4: JSON output for automation

```bash
python3 scripts/main.py check example.com --json
```

Output:
```json
{
  "domain": "example.com",
  "port": 443,
  "status": "valid",
  "expires_at": "2026-06-15T23:59:59Z",
  "days_remaining": 101,
  "issuer": "Let's Encrypt Authority X3",
  "subject": "CN=example.com",
  "algorithm": "SHA256-RSA",
  "serial_number": "0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
  "valid_from": "2025-06-16T00:00:00Z",
  "valid_to": "2026-06-15T23:59:59Z",
  "warning": false,
  "error": null
}
```

### Example 5: Certificate details

```bash
python3 scripts/main.py details example.com
```

Output:
```
📋 Certificate details for example.com:443

Subject: CN=example.com
Issuer: Let's Encrypt Authority X3
Serial: 0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6

Validity:
  Not before: 2025-06-16 00:00:00 UTC
  Not after:  2026-06-15 23:59:59 UTC
  Days remaining: 101

Signature:
  Algorithm: SHA256-RSA
  Key size: 2048 bits

Extensions:
  Subject Alternative Names: example.com, www.example.com
  Key Usage: Digital Signature, Key Encipherment
  Extended Key Usage: TLS Web Server Authentication
```

## Requirements

- Python 3.x
- `cryptography` library for certificate parsing (installed automatically or via pip)

Install missing dependencies:
```bash
pip3 install cryptography
```

## Limitations

- Only checks TLS certificates on standard ports (custom ports supported via --port)
- Requires network connectivity to target domains
- May be blocked by firewalls or network security policies
- Does not perform deep security audits (no revocation checking, weak cipher detection)
- No support for client certificate authentication
- Limited to standard TLS handshake (no SNI customization)
- May not work with self-signed certificates without custom trust stores
- No support for checking certificate transparency logs
- Rate limiting may affect checking many domains quickly
- No built-in notification system (output only)
- Does not check for mixed content or other web security issues
- No support for checking certificates in load balancers or CDNs directly
- Limited error handling for network timeouts or DNS failures
- No support for checking certificates in mobile apps or other non-web contexts

## Directory Structure

The tool works with domain lists as text files (one domain per line). No special configuration directories are required.

## Error Handling

- Connection timeouts show helpful error messages with retry suggestions
- DNS resolution failures suggest checking domain spelling
- Certificate validation errors show certificate details and validation issues
- Port connection failures suggest checking firewall rules or service status
- File not found errors suggest checking file paths and permissions

## Contributing

This is a skill built by the Skill Factory. Issues and improvements should be reported through the OpenClaw project.