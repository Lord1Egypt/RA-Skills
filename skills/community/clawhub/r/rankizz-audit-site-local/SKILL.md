---
name: rankizz-audit-site-local
description: Audit a public website for technical SEO, on-page content, structured data, GEO readiness, and AEO readiness using only the agent's local browser, shell, filesystem, and network resources. Use when the user requests a local, offline-capable, no-account, no-credit, or non-Rankizz site audit. Rankizz MCP and API access are not required.
---

# Audit a site locally

Audit with evidence available to the current agent. Do not require Rankizz, an API key, or paid provider data.

## Establish scope

Use an explicit Quick or Full request without asking again. Otherwise ask the user to choose:

- **Quick:** homepage, robots, sitemap, and up to 10 representative pages.
- **Full:** a user-approved, bounded crawl budget and optional path scope.

Treat the target as permission to retrieve public pages for analysis, not permission to bypass authentication, bot controls, rate limits, or access restrictions.

## Choose available resources

Prefer existing site files or crawl exports when the user provides them. Otherwise use the safest available browser or HTTP tool.

When Python 3 and outbound network access are available, run the bundled crawler from the skill directory:

```sh
python3 scripts/crawl_site.py https://example.com --max-pages 10 --output site-audit.json
```

For a larger confirmed scope, change `--max-pages`. Use `--path-prefix /docs/` to stay inside a section. The script respects robots.txt, stays on the starting hostname, limits request rate, rejects credential-bearing URLs, and blocks private-network targets unless `--allow-private-network` is explicitly set.

If scripts cannot run, reproduce the same bounded workflow with the agent's browser or shell. If the environment has no network access, ask for HTML files, a crawl export, or a sitemap instead of pretending the site was inspected.

Read [references/audit-checklist.md](references/audit-checklist.md) before interpreting results and [references/report-contract.md](references/report-contract.md) before writing the report.

## Inspect evidence

Retrieve in this order when available:

1. start URL
2. `robots.txt`
3. declared sitemaps and `/sitemap.xml`
4. representative navigation, product/service, category, article, about, contact, and FAQ pages
5. internally discovered pages within the confirmed budget

Check response outcomes, indexability directives, canonicals, titles, descriptions, headings, visible text, images, internal links, structured data, social metadata, and page-type consistency.

Use Lighthouse, browser performance tools, or a user-provided performance export only when available. Label performance `not assessed` when it was not measured. Do not substitute response time for Core Web Vitals.

## Bound conclusions

HTML and crawl evidence cannot prove rankings, keyword demand, backlinks, traffic, conversions, index coverage, or AI citations. State when those data sources are absent.

Evaluate GEO and AEO as content and structure readiness, not as guaranteed visibility. Separate direct observations from reasonable inferences.

Do not treat every short page, noindex page, canonical, redirect, or missing description as an error without considering page purpose.

## Deliver the report

Return a concise chat recap plus a Markdown or HTML report when file creation is available. Generate PDF or DOCX only on request and only with an appropriate document tool.

Include:

1. exact coverage and limitations
2. dimension statuses
3. three highest-value actions
4. consolidated findings with URL evidence
5. page-level examples
6. what is already working
7. a remediation sequence
8. a suggested re-check

Never include a finding without evidence. Never invent a metric to make the report appear complete.
