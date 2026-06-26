---
name: subdomain-enum
description: Enumerate subdomains for any domain using DNS brute-force and certificate transparency logs (crt.sh). Use when a user needs to discover subdomains, perform reconnaissance, audit attack surface, find forgotten or exposed services, or map the infrastructure of a domain. No API keys required. Supports custom wordlists, concurrent threads, and JSON output.
---

# Subdomain Enumerator

Discover subdomains for any domain using two complementary techniques: DNS brute-force resolution and certificate transparency log mining via crt.sh.

## Quick Start

```bash
python3 scripts/subenum.py example.com
```

## Commands

```bash
# Basic enumeration (built-in wordlist + crt.sh)
python3 scripts/subenum.py example.com

# Custom wordlist
python3 scripts/subenum.py example.com --wordlist /path/to/wordlist.txt

# Faster with more threads
python3 scripts/subenum.py example.com --threads 20

# DNS only (skip crt.sh)
python3 scripts/subenum.py example.com --no-crtsh

# JSON output
python3 scripts/subenum.py example.com --json

# Save results to file
python3 scripts/subenum.py example.com --output subdomains.txt

# Verbose progress
python3 scripts/subenum.py example.com -v
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--wordlist, -w` | built-in (~120 words) | Custom wordlist file |
| `--threads, -t` | `10` | Concurrent DNS resolution threads |
| `--timeout` | `15` | HTTP timeout for crt.sh query |
| `--no-crtsh` | off | Skip certificate transparency lookup |
| `--json` | off | Output as JSON |
| `--output, -o` | — | Write results to file |
| `--verbose, -v` | off | Show progress during scan |

## Techniques

1. **DNS Brute-force** — Resolves `{word}.{domain}` against DNS for each word in the wordlist. Returns IP addresses for live subdomains.
2. **Certificate Transparency (crt.sh)** — Queries public CT logs for certificates issued to `*.domain`, revealing subdomains that may not respond to DNS but have had TLS certificates.

## Dependencies

```bash
pip install requests
```

## Notes

- Built-in wordlist covers common subdomains (www, api, mail, staging, etc.)
- For comprehensive scans, use a larger wordlist (e.g., SecLists DNS wordlists)
- Results are deduplicated across sources
- Use responsibly — only scan domains you own or have authorization to test
