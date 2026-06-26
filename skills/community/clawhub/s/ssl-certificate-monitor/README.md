# SSL Certificate Monitor

Monitor SSL/TLS certificates for expiration dates, security issues, and compliance across domains and subdomains.

## Features

- Check expiration dates for SSL certificates
- Detailed certificate information (issuer, subject, algorithm)
- Batch monitoring of multiple domains
- Alert thresholds for expiring certificates
- JSON output for machine processing
- Basic certificate chain validation

## Quick Start

```bash
# Check a single domain
python3 scripts/main.py check example.com

# Check multiple domains from a file
python3 scripts/main.py batch domains.txt --warning-days 30

# Get certificate details
python3 scripts/main.py details example.com
```

## Installation

This skill requires Python 3.x and the `cryptography` library:

```bash
pip3 install cryptography
```

## Usage Examples

### Check domain with custom warning threshold
```bash
python3 scripts/main.py check example.com --warning-days 14
```

### Output JSON for automation
```bash
python3 scripts/main.py check example.com --json
```

### Validate certificate chain
```bash
python3 scripts/main.py validate example.com
```

## File Format for Batch Checking

Create a text file with one domain per line:

```
example.com
api.example.com
staging.example.com
blog.example.com:8443
```

## Output

The tool provides color-coded output:
- ✅ Valid certificates
- ⚠️  Certificates expiring soon (within warning threshold)
- ❌ Expired or invalid certificates

## Limitations

- Network connectivity required
- Standard TLS handshake only
- No deep security audits
- No built-in notification system

## License

This skill is part of the OpenClaw Skill Factory portfolio.