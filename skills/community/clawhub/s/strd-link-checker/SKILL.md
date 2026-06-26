---
name: link-checker
description: Check all links in a website's HTML files and report broken, redirected, and slow links. Supports internal links, external links, and affiliate link identification. Use after publishing content to verify nothing is broken, or as part of a regular site health audit. Particularly useful for affiliate content where broken product links mean lost commissions.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl", "python3"] },
        "install": [],
      },
  }
---

# Link Checker

Validate links in HTML files and report issues: broken links (404/500), redirects, slow responses, and affiliate link status.

## What This Skill Does

- Scans all HTML files in a given directory
- Checks each link (internal + external) for HTTP status
- Identifies broken (4xx/5xx), redirected (3xx), and slow links (>5s)
- Groups links by type: internal, external, affiliate
- Outputs a clean markdown report sorted by severity

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SITE_DIR` | Yes | — | Directory containing HTML files to scan |
| `LINK_CHECK_TIMEOUT` | No | `10` | Max seconds to wait per link |
| `AFFILIATE_DOMAINS` | No | see below | Comma-separated affiliate domains to flag |

Default affiliate domains: `amazon.com,hostname/s/aspx,godaddy.com,bluehost.com,digitalocean.com,heroku.com,shopify.com,awin1.com,ref=`

## Scripts

### check.sh — Full Link Audit

```bash
./scripts/check.sh [directory]
```

Output: markdown report with broken links, redirects, slow links, and affiliate links found.

### quick.sh — Fast Scan (broken links only)

```bash
./scripts/quick.sh [directory]
```

Only reports 4xx/5xx status links. Skips affiliate and slow link checks.

### affiliate.sh — Affiliate Link Report

```bash
./scripts/affiliate.sh [directory]
```

Lists all affiliate links and whether they're reachable. Critical for revenue site maintenance.

## Output Format

```
# Link Checker Report — [site name]
Generated: [timestamp]

## Summary
- Total links checked: N
- Broken: N  🔴
- Redirected: N  🟡
- Slow (>5s): N  🟠
- Affiliate: N  ✅

## Broken Links (4xx/5xx)  🔴
[file] [line] [url] — [status]

## Redirects  🟡
[file] [url] → [destination]

## Slow Links (>5s)  🟠
[file] [url] — [response_time]

## Affiliate Links  ✅
[file] [url]
```

## Example Usage

```bash
# Check all articles
SITE_DIR=./site ./scripts/check.sh

# Fast broken-link only
./scripts/quick.sh ./site/articles/

# Affiliate link audit
AFFILIATE_DOMAINS="amazon.com,digitalocean.com,bluehost.com" ./scripts/affiliate.sh ./site
```

## Notes

- External links are checked with HEAD requests (faster than GET)
- Broken link reports are prioritized by severity (5xx worse than 4xx)
- Affiliate links are flagged but marked ✅ to confirm they're present
- Run this after any major content update to catch broken links before Google does
