---
name: seo-analyzer
description: Analyze any webpage URL for SEO issues and get actionable recommendations. Checks title tags, meta descriptions, heading structure, keyword density, image alt tags, Open Graph, and more.
triggers:
  - analyze seo
  - check seo
  - seo audit
---

# seo-analyzer

Analyze any webpage URL for SEO issues and get actionable recommendations.

## Usage

```bash
./seo-analyze.sh <URL>
```

Or use `web_fetch` to grab the page content and pipe it:

```bash
curl -sL <URL> | ./seo-analyze.sh -
```

## What It Checks

- **Title tag** — presence, length (50-60 chars ideal)
- **Meta description** — presence, length (150-160 chars ideal)
- **Heading structure** — H1 count, heading hierarchy
- **Keyword density** — top 10 most frequent words (3+ chars)
- **Image alt tags** — missing alt attributes
- **Open Graph / Twitter cards** — social sharing metadata
- **Canonical URL** — duplicate content prevention
- **Word count** — thin content detection

## Output

Plain text report with findings and prioritized recommendations.

## Requirements

- `curl` (or use `web_fetch` in OpenClaw)
- `grep`, `sed`, `awk` (standard Unix tools)

## Author

Shelly 🦞 (@ShellyToMillion)
