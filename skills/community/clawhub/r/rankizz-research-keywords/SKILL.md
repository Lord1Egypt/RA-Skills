---
name: rankizz-research-keywords
description: Find, evaluate, and prioritize organic-search keyword opportunities from a site's products, audience problems, existing pages, exports, Search Console data, SERPs, or optional Rankizz metrics. Use before creating or refreshing content, planning landing pages, or deciding which searches are worth targeting. Rankizz is optional until live volume, difficulty, intent, or SERP evidence is needed.
---

# Research keywords

Build a decision-ready opportunity set, not a large unfiltered keyword dump.

## Invoke Rankizz MCP tools

When using Rankizz through MCP, the initial tool list is intentionally compact. Call `search_tools` with a capability query or exact domain-tool name and set `includeSchemas: true` unless the arguments are already known. Invoke a discovered tool with `call_read_tool` when its `readOnlyHint` is `true`; use `call_tool` for every other tool. Pass the discovered name as `tool` and its original input object as `arguments`. REST callers continue to use the direct `/api/v1/tools/<tool-name>` endpoint.

## Establish context

Read existing SEO project context, site pages, briefs, and supplied exports before asking questions. Determine:

- target site, product, or topic
- audience and conversion goal
- target country and language
- existing page or new-content use case
- branded terms, irrelevant meanings, and exclusions

Ask only for missing details that would materially change the market or intent.

## Generate candidates locally first

Use available evidence without Rankizz when it is sufficient:

- product and service language from the site
- audience tasks, pains, comparisons, and objections
- supplied keyword, Search Console, analytics, or advertising exports
- related terms and questions found in public pages or accessible search results
- existing page headings and internal-search language

Normalize whitespace and obvious duplicates while retaining the original phrase and source. Do not invent search volume, difficulty, CPC, traffic, or rank.

## Use Rankizz only for missing live evidence

If Rankizz is connected and quantitative prioritization is useful:

1. Resolve a project with `list_projects`.
2. Use `list_saved_keywords` before paying to re-research known terms.
3. Use `research_keywords` for 1–5 high-value seed topics.
4. Use `get_keyword_metrics` to hydrate a known candidate list in one batch.
5. Use `get_serp_results` only for ambiguous intent or final-priority terms in standard web search.
6. For local intent, use `get_local_serp_results` to inspect Google Maps or Local Finder results. Pass a DataForSEO `locationCode` only when overriding the project's market; do not pass latitude or longitude.
7. Use `get_google_business_questions` only when Google Business Profile Q&A evidence will change the keyword or content decision. It also defaults to the project's market when `locationCode` is omitted.
8. Use `get_search_console_performance` when a connected site may already have striking-distance queries.

Hosted calls require at least 10 credits. If access reports a low balance, stop Rankizz calls, link to `https://www.rankizz.com/billing`, and complete the qualitative portion without fabricated metrics.

State why a credit-using call is needed, prefer batching, and avoid repeating fresh research already returned in the session. Ask before enabling any higher-cost refinement option.

## Evaluate opportunities

Read [references/research-method.md](references/research-method.md). Evaluate fit before volume:

- business and audience relevance
- search intent and expected page type
- conversion proximity
- evidence of demand
- difficulty and SERP strength when available
- current site authority and topical coverage
- existing ranking page or cannibalization risk
- confidence and data freshness

Treat provider metrics as estimates, not guarantees. Do not discard a strategically important low-volume term solely because its reported volume is small or unavailable.

## Deliver

Return:

1. a concise market and intent summary
2. 10–25 prioritized opportunities when enough evidence exists
3. a longer candidate table grouped into target now, validate, later, and exclude
4. SERP or metric caveats
5. the next recommended action

For each prioritized keyword include phrase, intent, recommended page type, relevance, volume/KD/CPC when actually available, current page if any, rationale, confidence, and source date.

Ask before calling `save_keywords` or applying tags. Never persist a discarded or unreviewed bulk list automatically.
