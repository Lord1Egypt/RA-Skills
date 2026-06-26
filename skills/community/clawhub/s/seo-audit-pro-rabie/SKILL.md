---
name: seo-audit-pro
description: Full SEO audit and content brief generator for any website URL. Use when users ask to audit a website's SEO, check technical SEO issues, analyze on-page SEO, generate a content brief, find SEO problems, or get an SEO report. Produces a structured report covering technical health, on-page factors, Core Web Vitals, content gaps, and ready-to-use content briefs for target keywords. Triggers on phrases like "audit my site", "check SEO", "SEO report for", "content brief for", "what's wrong with my site's SEO", "improve my rankings".
---

# SEO Audit Pro

Generate a comprehensive SEO audit + content brief for any website or URL.

## Workflow

1. **Run the audit script** to collect technical + on-page signals:
   ```bash
   python3 scripts/seo_audit.py <url> [--keyword "target keyword"]
   ```
   The script outputs a JSON report. Read it fully before writing the report.

2. **Generate the audit report** using the structure in `references/report-template.md`.

3. **If a keyword was provided**, append a Content Brief section using `references/content-brief-template.md`.

4. **Score the site** using the scoring rubric in `references/scoring.md` and include a summary score card at the top.

## Output Format

- Lead with a **Score Card** (Overall /100, broken into 4 categories)
- Use clear headers: Technical SEO, On-Page SEO, Content Analysis, Recommendations
- End with a **Priority Action List** (top 5 fixes, ordered by impact)
- If keyword provided: append a full **Content Brief**
- Deliver as markdown — format for readability

## Key Principles

- Be specific: cite exact URLs, status codes, missing tags, file sizes
- Prioritize by impact: critical issues first
- Be actionable: every finding must have a fix recommendation
- Content briefs must include: search intent, outline, word count, internal link suggestions, meta title/description drafts
