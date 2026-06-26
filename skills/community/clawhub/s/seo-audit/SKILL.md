---
name: seo-audit
description: |
  Audit a webpage's SEO and generate a scored report with actionable fixes.

  USE WHEN:
  - User provides a URL and asks to check/audit/review its SEO
  - User asks "how's my site's SEO?" or "what SEO issues does [URL] have?"
  - User wants to improve search rankings for a specific page
  - User asks to review meta tags, headings, or on-page optimization

  DON'T USE WHEN:
  - User wants keyword research or content strategy (that's research, not an audit)
  - User wants to track rankings over time (use a rank tracking tool)
  - User wants technical site-wide crawl analysis (this audits single pages, not full sites)
  - User wants Google Search Console or Analytics data (requires API access, not page scraping)
  - User wants to fix SEO issues (this diagnoses — fixing is a separate step)
  - User wants backlink analysis (requires third-party tools like Ahrefs/Moz)

  OUTPUTS: Markdown report with overall score (0-100), category breakdowns (Meta, Content, Technical, Performance), critical issues, warnings, and prioritized recommendations.

  INPUTS: A single URL to audit. Optionally: target keywords to check against.
---

# SEO Audit

Analyze any webpage for SEO issues and generate an actionable report.

## Workflow

1. Fetch the target URL using `web_fetch`
2. Analyze the HTML content for SEO factors (see checklist below)
3. Score each category (0-100)
4. Generate a formatted report with findings and recommendations
5. Save report as markdown file

## SEO Checklist

### Meta & Head (25 points)
- Title tag exists, 30-60 chars, contains target keywords
- Meta description exists, 120-160 chars, compelling
- Canonical URL present
- Open Graph tags (og:title, og:description, og:image)
- Twitter Card tags
- Favicon reference
- Language attribute on `<html>`

### Content Quality (25 points)
- Single H1 tag present
- Logical heading hierarchy (H1 → H2 → H3)
- Word count (minimum 300 for ranking)
- Image alt text coverage
- Internal links present
- External links present
- No broken heading structure

### Technical (25 points)
- Mobile viewport meta tag
- HTTPS (check URL scheme)
- Clean URL structure (no excessive params)
- Structured data / Schema.org markup
- No duplicate content signals
- robots meta tag check

### Performance Indicators (25 points)
- Total HTML size (flag if >100KB)
- Image count and alt coverage
- External resource count (CSS/JS files)
- Inline CSS volume (flag if excessive)
- Render-blocking resources estimate

## Report Format

```markdown
# SEO Audit Report: [URL]
**Date:** [date]
**Overall Score:** [X/100]

## Summary
[2-3 sentence overview]

## Scores
| Category | Score | Status |
|----------|-------|--------|
| Meta & Head | X/25 | ✅/⚠️/❌ |
| Content | X/25 | ✅/⚠️/❌ |
| Technical | X/25 | ✅/⚠️/❌ |
| Performance | X/25 | ✅/⚠️/❌ |

## Findings
### Critical Issues
...
### Warnings
...
### Passed
...

## Recommendations
[Prioritized action items]
```

## Scoring

- ✅ 80%+ of category points = Good
- ⚠️ 50-79% = Needs improvement
- ❌ Below 50% = Critical issues

## Common Mistakes to Avoid

- **Don't audit without fetching** — always fetch the actual page HTML, don't guess from the URL alone
- **Don't penalize single-page apps unfairly** — SPAs often have minimal HTML; note it but don't tank the score
- **Don't report Open Graph as "critical"** — it's important but not a ranking factor. Keep severity accurate.
- **Don't ignore context** — a personal blog doesn't need Schema.org markup the way an e-commerce site does. Tailor severity to the site type.
