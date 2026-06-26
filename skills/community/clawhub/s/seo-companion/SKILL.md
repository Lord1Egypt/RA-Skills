---
name: seo-companion
description: Deep SEO analysis and execution for on-page SEO, technical SEO, content strategy, local SEO, keyword research, and backlink risk/recommendations. Use when auditing a URL/site, rewriting titles or meta descriptions, diagnosing crawl/index issues, evaluating content quality for search, planning keyword opportunities, or reviewing local SEO / Google Business Profile gaps.
---

# SEO Companion

Use this skill to deliver rigorous, implementation-focused SEO help without drifting into vague marketing advice.

## Core operating rules

- Separate **facts**, **strong heuristics**, and **situational suggestions**.
- Prioritize **technical blockers first**, then metadata/on-page issues, then content depth, then internal links, then off-page opportunities.
- Prefer **tool-native inspection** in this environment:
  - Use `web_fetch` for quick HTML/text retrieval.
  - Use `browser` when rendered DOM, JS behavior, or screenshots matter.
  - Use the bundled audit script for repeatable extraction.
- Do not recommend black-hat tactics: no PBNs, bought reviews, cloaking, doorway pages, or spam link packages.
- Be explicit about uncertainty. Many SEO thresholds are heuristics, not laws.

## Request triage

Classify the request before answering:

1. **On-page SEO**
   - Titles, meta descriptions, H1/H2/H3 structure, canonicals, alt text, internal links.
   - Read `references/on-page.md`.

2. **Technical SEO**
   - Indexing, robots.txt, sitemap, redirects, canonicalization, renderability, structured data, performance.
   - Read `references/technical.md`.

3. **Content strategy / keyword work**
   - Keyword targeting, clustering, cannibalization, content briefs, content gaps.
   - Read `references/content-strategy.md`.

4. **Local SEO**
   - GBP, NAP consistency, local landing pages, reviews, citations.
   - Read `references/local-seo.md`.

5. **Link building / backlink evaluation**
   - Link quality, outreach ideas, risk flags, sustainable acquisition.
   - Read `references/link-building.md`.

6. **Full audit**
   - Run the bundled script first, then deepen with browser/manual inspection if needed.
   - Read `references/technical.md` and `references/on-page.md`.

## Runtime requirements and fallbacks

Preferred runtime for the bundled script:
- Python 3
- `requests`
- `beautifulsoup4` (`bs4`)

If those Python dependencies are missing:
- do **not** fail silently
- **ask before installing packages** in environments where package installation changes the system/runtime state
- if package installs are not approved or not appropriate, fall back to `web_fetch` for raw HTML/text inspection and `browser` for rendered-page inspection

The script is optional support tooling, not a hard requirement for using this skill.

## Target safety

Do not run the bundled script against private/internal targets unless the user explicitly intends that and the environment is trusted.

Treat these as blocked by default for routine SEO work:
- `localhost`
- loopback addresses
- private RFC1918 IP ranges
- link-local addresses
- obvious cloud metadata endpoints
- internal-only hostnames or intranet targets

For normal public-site SEO auditing, stick to public HTTP/HTTPS URLs.

## Standard workflow for a URL audit

1. Run the bundled script:

```bash
python3 scripts/audit_page.py <URL>
```

2. Review the structured output for:
   - title/meta quality
   - canonical presence
   - robots directives
   - heading counts
   - internal/external links
   - image alt gaps
   - structured data presence
   - robots.txt / sitemap availability

3. If the page is JS-heavy or the HTML output looks incomplete, inspect with `browser`.

4. Produce findings in this order:
   - **Critical blockers**
   - **High-impact improvements**
   - **Medium / nice-to-have fixes**
   - **What to do next**

## Output contracts

### Quick page audit
Use when the user wants a fast diagnosis for one page.

Include:
- summary table
- top 3–7 issues
- exact rewrites if applicable

### Full SEO teardown
Use when the user wants a deeper review.

Include:
- technical section
- on-page section
- content section
- internal linking / structure section
- local SEO section if relevant
- prioritized roadmap

### Metadata rewrite pack
Use when the user asks for titles, descriptions, or heading rewrites.

Include:
- 3–5 title options
- 2–3 meta description options
- suggested H1
- reasoning briefly tied to query intent / CTR / relevance

## Default thresholds

Treat these as **strong heuristics**, not absolute truths:

- Title tag: ideal ~50–60 chars
- Meta description: ideal ~120–156 chars
- H1 count: exactly 1 preferred
- Thin content risk: often under ~500–600 body words for pages intended to rank
- Strong content target: depends on intent and SERP, not a fixed word count

## Reporting style

When reporting, always:
- cite exact numbers where useful
- distinguish page-specific vs site-wide issues
- explain why something matters
- avoid fake certainty
- prefer actionable fixes over generic theory

## Reference map

Read only what you need:
- `references/on-page.md`
- `references/technical.md`
- `references/content-strategy.md`
- `references/local-seo.md`
- `references/link-building.md`
- `references/platform-playbooks.md`
- `references/canada-local.md`

## Bundled script

Use `scripts/audit_page.py` for repeatable extraction. It is intentionally conservative and should be supplemented with rendered-page inspection when needed.

If the script cannot run because Python dependencies are unavailable, continue with a manual audit using `web_fetch` and `browser` rather than treating the skill as unusable.
