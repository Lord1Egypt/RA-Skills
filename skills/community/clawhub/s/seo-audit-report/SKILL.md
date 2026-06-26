---
name: seo-audit-report
description: Run comprehensive SEO audits on any website and generate actionable reports. Use when the user asks to audit a website's SEO, check technical SEO issues, analyze on-page optimization, review meta tags, check page speed indicators, find broken links, analyze heading structure, or generate an SEO improvement plan. Outputs a scored report with prioritized recommendations.
---

# SEO Audit Report

Run full SEO audits from your agent and get actionable, scored reports.

## Quick Start

```bash
python3 scripts/seo_audit.py --url https://example.com
```

## Commands

### Full Audit
```bash
python3 scripts/seo_audit.py --url https://example.com --depth 3
```

Crawls up to `--depth` pages from the starting URL.

### Quick Check (single page)
```bash
python3 scripts/seo_audit.py --url https://example.com/page --quick
```

### Generate Report
```bash
python3 scripts/seo_audit.py --url https://example.com --output report.md
```

## What Gets Audited

### Technical SEO
- HTTPS enforcement and redirect chains
- Robots.txt presence and configuration
- Sitemap.xml detection and validation
- Canonical tag usage
- Mobile viewport meta tag
- Page load indicators (response time, content size)
- HTTP status codes across crawled pages

### On-Page SEO
- Title tag (presence, length, keyword usage)
- Meta description (presence, length, uniqueness)
- Heading hierarchy (H1-H6 structure)
- Image alt text coverage
- Internal/external link ratio
- Content length analysis
- Open Graph and Twitter Card tags

### Content Quality Signals
- Word count per page
- Heading-to-content ratio
- Duplicate title/description detection
- Thin content pages (<300 words)

### Link Health
- Broken internal links (4xx/5xx)
- Orphan pages (no internal links pointing to them)
- External link count and diversity

## Scoring

Each audit category is scored 0-100:

| Score | Rating | Meaning |
|-------|--------|---------|
| 90-100 | Excellent | No significant issues |
| 70-89 | Good | Minor improvements possible |
| 50-69 | Fair | Notable issues to address |
| 0-49 | Poor | Critical issues found |

Overall score is a weighted average:
- Technical: 35%
- On-Page: 35%
- Content: 15%
- Links: 15%

## Report Format

Reports are markdown with:
- Executive summary with overall score
- Category breakdowns with individual scores
- Prioritized issue list (Critical → Low)
- Specific fix recommendations per issue
- Comparison benchmarks

## Advanced

See `references/seo-checklist.md` for the complete 50+ point checklist used in audits.
