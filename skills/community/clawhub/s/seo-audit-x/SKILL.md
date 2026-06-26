---
name: seo-audit
description: Comprehensive SEO audit and optimization for any website or URL. Use when asked to audit a site's SEO, analyze on-page optimization, check technical SEO issues, review meta tags/headings/content structure, assess page speed factors, identify keyword opportunities, generate SEO reports, or suggest actionable improvements for search rankings. Triggers on phrases like "audit my site", "check SEO", "improve rankings", "SEO report", "optimize for search", "keyword analysis", "meta tags", "fix SEO issues".
---

# SEO Audit Skill

Deliver a thorough, actionable SEO audit for any URL or domain. Output should be immediately useful — not generic advice.

## Workflow

### 1. Gather Target
Ask for the URL if not provided. Optionally ask for: target keywords, competitors to benchmark against, and priority pages.

### 2. Fetch & Analyze Pages
Use `web_fetch` to retrieve page content. Analyze:
- **Title tag**: Present? Length (50–60 chars ideal)? Contains primary keyword?
- **Meta description**: Present? Length (150–160 chars ideal)? Compelling CTA?
- **H1/H2/H3 structure**: Single H1? Keyword-rich headings? Logical hierarchy?
- **Content quality**: Word count, keyword density (1–2%), readability, duplicate content signals
- **Internal linking**: Anchor text quality, orphan pages, link depth
- **Image alt text**: Present on all images?
- **URL structure**: Clean, keyword-rich, no excessive parameters?
- **Schema markup**: Present? Appropriate type?

### 3. Technical Signals (infer from page source)
- Page load indicators (inline CSS vs external, render-blocking scripts)
- Mobile viewport meta tag
- Canonical tags
- robots meta tag
- HTTPS
- Structured data (JSON-LD)

### 4. Keyword Analysis
Use `web_search` to:
- Identify what the page currently ranks for (search `site:domain.com`)
- Find keyword gaps vs competitors
- Suggest 5–10 target keywords with estimated intent (informational/transactional/navigational)

### 5. Competitor Benchmarking (if competitors provided)
Fetch top competitor pages for same keywords. Compare: title structure, content length, heading strategy, backlink signals (visible in SERPs).

### 6. Generate Report
Use the report template in `references/report-template.md`. Sections:
- Executive Summary (3–5 bullet critical issues)
- Score card (0–100 across 5 dimensions)
- On-Page Analysis
- Technical SEO
- Keyword Opportunities
- Quick Wins (fix in <1 hour)
- Long-Term Roadmap

### 7. Run the Audit Script (optional, for bulk analysis)
```bash
python3 scripts/seo_audit.py --url <URL> [--competitors url1,url2] [--keywords kw1,kw2]
```

See `references/scoring-rubric.md` for how scores are calculated.
See `references/checklist.md` for the full 50-point audit checklist.
