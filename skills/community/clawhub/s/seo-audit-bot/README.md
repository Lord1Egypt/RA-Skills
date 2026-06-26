# SEO Audit Bot 🔍

A comprehensive SEO auditing skill for OpenClaw agents. Analyze any website's SEO health and get actionable recommendations to improve your search rankings.

## Features

- **Technical SEO Analysis** — robots.txt, sitemap, HTTPS, mobile-friendliness
- **On-Page SEO Audit** — title tags, meta descriptions, headings, URL structure
- **Content Quality Check** — word count, keyword density, readability
- **Performance Indicators** — page speed signals, asset optimization
- **Social & Schema Audit** — Open Graph, Twitter Cards, structured data
- **Competitor Comparison** — side-by-side SEO comparison of two sites
- **Actionable Scoring** — 0-100 score with prioritized recommendations

## Usage

```
"Audit the SEO of https://mywebsite.com"
"Compare SEO of https://mysite.com vs https://competitor.com"
"Check the technical SEO of my blog at https://myblog.com"
```

## Output

A detailed report with:
- Overall score (0-100)
- Section scores (Technical, On-Page, Content, Performance, Social)
- ✅ What's working well
- ❌ What needs fixing
- 🎯 Priority actions ranked by impact

## Who Is This For?

- Website owners wanting to improve their search rankings
- Digital marketers managing multiple sites
- SEO agencies needing quick audit templates
- Freelancers offering SEO services
- Anyone who wants to understand their website's SEO health

## Requirements

- OpenClaw with `web_fetch` and `exec` (curl) capabilities
- No additional API keys needed
- No external dependencies

## What's Included

- `SKILL.md` — Complete agent instructions with scoring rubric
- `README.md` — This file
- `scripts/audit.sh` — Automated audit script for quick technical checks
- `references/seo-best-practices.md` — SEO rules reference
- `references/demo-report.md` — Example audit report

## Version

1.0.0 — Initial release (March 2026)
