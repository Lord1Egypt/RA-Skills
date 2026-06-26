---
name: subdomain-takeover
description: Check subdomains for potential takeover vulnerabilities. Detects dangling DNS records pointing to unclaimed services (GitHub Pages, Heroku, AWS, etc.)
metadata: {"openclaw":{"emoji":"🏴","requires":{"bins":["bash","dig"]}}}
---

# Subdomain Takeover Checker

Detect dangling DNS records that could be hijacked. Checks if subdomains point to services that might be unclaimed.

## Quick Start

```bash
# Check a list of subdomains
bash {baseDir}/scripts/check-takeover.sh -l subdomains.txt

# Check single subdomain
bash {baseDir}/scripts/check-takeover.sh -d sub.example.com

# Passive DNS only (no HTTP verification)
bash {baseDir}/scripts/check-takeover.sh -l subdomains.txt --passive
```

## What It Checks

CNAME records pointing to known vulnerable services:
- GitHub Pages (*.github.io, *.github.com)
- Heroku (*.herokudns.com, *.herokuapp.com)
- AWS (*.amazonaws.com, *.s3.amazonaws.com, *.cloudfront.net)
- Azure (*.azurewebsites.net, *.cloudapp.azure.com)
- Shopify (*.myshopify.com)
- Fastly (*.fastly.net)
- Pantheon (*.pantheonsite.io)
- Surge (*.surge.sh)
- Tumblr (*.tumblr.com)
- WordPress (*.wordpress.com)
- Zendesk (*.zendesk.com)
- 50+ more services...

## Options

- `-l FILE` — File with subdomains (one per line)
- `-d DOMAIN` — Single subdomain to check
- `--passive` — DNS-only check (no HTTP requests)
- `--json` — JSON output
- `--timeout SECS` — DNS timeout (default: 5)
- `--output FILE` — Write results to file

## Output

```
=== Subdomain Takeover Scan ===
Scanning 50 subdomains...

⚠️  VULNERABLE:
  blog.example.com → example.github.io (GitHub Pages — claimable)
  old.example.com → example.herokuapp.com (Heroku — claimable)

✅ SAFE:
  api.example.com → cloudfront.net (AWS — active)
  www.example.com → A record (direct)

Summary: 2/50 potentially vulnerable
```

## Remediation

If a subdomain is vulnerable:
1. Remove the DNS record, OR
2. Reclaim the service (re-register the GitHub repo, Heroku app, etc.)
3. Set up monitoring to catch future dangles
