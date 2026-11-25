# Rankizz roadmap tool sequence

Use the smallest evidence sequence that answers the decision. Hosted MCP and REST calls require at least 10 credits before execution.

## Required setup

1. `list_projects`: resolve `projectId`, domain, location code, and language code.
2. `get_ahrefs_domain_rating`: first diagnostic; cached one day and uses no research credits.

## Authority evidence

- `get_backlinks_overview`: summary plus top referring domains; usually about 50 credits for a domain.
- `get_backlinks_profile`: one bounded detailed page; use only for anchors, link status, spam/authority signals, or page-level evidence.

Prefer referring-domain quality and relevance over raw backlink count. The overview already contains the referring-domain total; do not call the detailed profile merely to repeat it.

## First-party traction

- `get_search_console_performance`
  - Start with `dimensions: ["query", "page"]` and `dateRange: "last_28_days"` or a supported 90-day range.
  - Use `dataState: "final"` for stable comparisons.
  - Filter striking-distance positions client-side; the API cannot filter by position.
  - Read-only and no research credits.
- `get_google_analytics_organic_landing_pages`
  - Use a complete 28-day window first.
  - Inspect sessions, engagement, key events, transactions, revenue, and concentration.
  - Read-only and no research credits.
- `get_site_explorer_page`: optional exact-page combined view for a URL already in the persisted sitemap.

If a connection is missing, keep the missing source visible in the report. Do not translate an unavailable connection into zero traffic.

## Directional market evidence

- `get_domain_overview`: estimated organic traffic, organic keyword count, backlinks, and referring domains; cached 12 hours.
- `research_keywords`: 1–5 seeds and up to the supported result limit per seed.
- `get_keyword_metrics`: hydrate a reviewed batch with volume, KD, intent, CPC, and trends.
- `get_serp_results`: live top 20 for 1–10 queries. It does not return pages 3–4.
- `find_serp_competitors`: recurring domains across an already reviewed keyword set.
- `get_domain_keyword_suggestions`: one competitor's ranking keyword opportunities after its overview.
- `get_ranked_keywords`: detailed domain or page keyword, URL, rank, volume, intent, and estimated traffic rows.

## Cost controls

- State the purpose before a paid call.
- Reuse results and cache windows within the session.
- Batch keyword metrics and SERP requests.
- Do not enrich every competitor. Shortlist proof/peer domains first.
- Do not enable clickstream refinement unless close-variant precision changes the decision; it can double keyword research cost.
- Stop immediately on low-credit or payment-required responses.
