---
name: rankizz-analyze-competitor
description: Analyze one competitor's organic-search footprint, ranking topics, strongest pages, content formats, backlinks, authority signals, positioning, and exploitable gaps. Use when a named domain repeatedly wins search results, appears in customer comparisons, or needs a focused SEO teardown. Rankizz is optional until live keyword, domain, SERP, or backlink evidence is needed.
---

# Analyze an SEO competitor

Turn competitor evidence into decisions for the user's site. Do not create a flattering summary or instructions to copy the competitor.

## Invoke Rankizz MCP tools

When using Rankizz through MCP, the initial tool list is intentionally compact. Call `search_tools` with a capability query or exact domain-tool name and set `includeSchemas: true` unless the arguments are already known. Invoke a discovered tool with `call_read_tool` when its `readOnlyHint` is `true`; use `call_tool` for every other tool. Pass the discovered name as `tool` and its original input object as `arguments`. REST callers continue to use the direct `/api/v1/tools/<tool-name>` endpoint.

## Confirm comparison context

Identify the competitor domain, user's site, target market and language, and business question. Normalize the domain and clarify whether subdomains should be included when it matters.

Inspect provided exports, public pages, sitemaps, and previous landscape research before making paid calls.

## Build an evidence stack

Use available local or public evidence for positioning, site structure, page types, authorship, structured data, internal linking, and content patterns.

Use Rankizz selectively:

- `get_domain_overview` for estimated organic footprint
- `get_ranked_keywords` for keyword, URL, rank, intent, and traffic rows
- `get_serp_results` for priority head-to-head searches
- `get_backlinks_overview` for profile summary
- `get_backlinks_profile` for a bounded sample of detailed referring pages
- `get_ahrefs_domain_rating` for cached directional DR
- `get_domain_keyword_suggestions` when appropriate to the project workflow

Hosted calls require at least 10 credits. Stop Rankizz calls on a low-credit response and link to `https://www.rankizz.com/billing`. Use a small evidence-led sequence rather than calling every tool by default.

## Check AI visibility when relevant

When the comparison includes AI answers, discover `research_ai_rank_tracking_prompt` with `search_tools` and `includeSchemas: true`, then use `call_tool` with the discovered name and arguments. Query one relevant prompt and only the requested providers: `chatgpt`, `google_ai_mode`, `perplexity`, `gemini`, or `claude`. Include `projectId`; use `countryCode` and `languageCode` for the comparison market. This is metered live research and does not save a prompt for later runs.

Inspect each provider's `status`. A successful tool call can contain provider errors; `UPSTREAM_UNAVAILABLE` means missing evidence, not zero visibility. Successful results contain a non-empty `answer`, `brandMentioned`, `mentions`, and `citations`. The citation list combines citation and source URLs; Google AI Mode may supply attached source links. Do not describe every listed source as an inline citation. A null `webSearchTriggered` means unknown. Preserve the prompt, provider, market, and `researchedAt` timestamp in the comparison.

## Analyze, then compare

Read [references/competitor-framework.md](references/competitor-framework.md).

Determine:

- where visibility is concentrated
- topics, intents, and page types that drive it
- which pages appear durable versus incidental
- content, product, brand, entity, and authority advantages
- backlink patterns supported by measured data
- weaknesses, stale areas, mismatched intents, or overextended topics
- gaps relevant to the user's strengths

Distinguish observed facts, provider estimates, and inferences. Never report an estimate as first-party analytics.

## Recommend differentiation

Recommend ways to serve the searcher better: clearer tools, better evidence, original data, stronger product experience, more focused intent, credible expertise, or underserved formats.

Do not reproduce copyrighted text, page structure, brand language, proprietary data, or outreach lists from the competitor.

## Deliver

Return an executive comparison, evidence table, keyword and page themes, authority findings, what to learn, what not to imitate, the strongest strategic gaps, and three prioritized actions for the user's site.

Include source dates and data limitations. Recommend a competitive-landscape study when one competitor is insufficient to represent the market.

For repeated comparisons, save the reviewed prompts with `add_ai_prompt`,
choose engines with `configure_ai_prompt_run`, and explicitly request
`run_ai_prompts`. Reuse the same UUID `runId` on retries and read the stored
result with `get_ai_prompt_run`; there is no automatic schedule.
