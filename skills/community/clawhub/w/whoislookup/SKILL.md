---
name: whoislookup
description: Look up domain WHOIS registration info — registrar, creation date, expiry date, nameservers, and domain status. Use when asked to check who owns a domain, when a domain expires, find nameservers, or get domain registration details. Supports com/net/org/io/dev/app/ai/co and 10+ more TLDs. Zero dependencies — pure Python stdlib.
---

# whoislookup 🔍

Domain WHOIS lookup with parsed output. Queries WHOIS servers directly via socket.

## Commands

```bash
# Look up one or more domains
python3 scripts/whoislookup.py github.com openclaw.ai

# Raw WHOIS response
python3 scripts/whoislookup.py --raw example.com

# Parsed JSON output
python3 scripts/whoislookup.py --json github.com

# Custom WHOIS server
python3 scripts/whoislookup.py --server whois.verisign-grs.com example.com
```

## Output Fields
- Registrar name
- Created / Expires / Updated dates
- Nameservers (up to 4)
- Domain status (EPP codes)

## Supported TLDs
com, net, org, io, dev, app, ai, co, me, xyz, info, uk, de, fr, eu, ca, au — auto-detects WHOIS server. Falls back to whois.nic.{tld} for others.
