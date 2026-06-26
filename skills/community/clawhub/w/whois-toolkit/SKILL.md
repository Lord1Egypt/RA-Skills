---
name: whois-toolkit
description: Domain WHOIS lookup toolkit for querying registrar, creation/expiry dates, nameservers, status, and registrant info. Use when looking up domain ownership, checking domain expiry dates, monitoring domain renewals, or investigating domain registration details. Supports all major TLDs. No external dependencies or API keys required.
---

# WHOIS Toolkit

Query WHOIS data for any domain — registrar, dates, nameservers, expiry warnings.

## Quick Start

```bash
# Basic WHOIS lookup
python3 scripts/whois_lookup.py example.com

# Multiple domains at once
python3 scripts/whois_lookup.py example.com example.org example.io

# JSON output
python3 scripts/whois_lookup.py example.com --json

# Expiry check only (great for monitoring)
python3 scripts/whois_lookup.py example.com example.org --expiry-only

# Show raw WHOIS response
python3 scripts/whois_lookup.py example.com --raw

# Use a specific WHOIS server
python3 scripts/whois_lookup.py example.com --server whois.verisign-grs.com
```

## Features

- Structured parsing: registrar, dates, nameservers, status, organization
- Expiry warnings: color-coded alerts at 30, 90 day thresholds
- Multi-domain batch queries
- Raw WHOIS passthrough mode
- Built-in WHOIS server mapping for 25+ TLDs
- Zero dependencies (uses raw socket queries)

## Flags

- `--json` — Machine-readable JSON output
- `--raw` — Include raw WHOIS response text
- `--expiry-only` — Show only domain and expiry date
- `--server <host>` — Override the WHOIS server
