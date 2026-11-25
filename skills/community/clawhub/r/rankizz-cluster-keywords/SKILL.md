---
name: rankizz-cluster-keywords
description: Cluster an existing keyword list by search intent and likely page need, then map clusters to current or proposed URLs while flagging cannibalization, consolidation, and weak-fit terms. Use when the user already has keywords but needs a content map, page plan, or tagging structure. Rankizz is optional unless fresh metrics, saved keywords, or SERP similarity evidence is needed.
---

# Cluster keywords into a page map

Turn a keyword set into defensible page decisions. Do not group terms only because they share words.

## Invoke Rankizz MCP tools

When using Rankizz through MCP, the initial tool list is intentionally compact. Call `search_tools` with a capability query or exact domain-tool name and set `includeSchemas: true` unless the arguments are already known. Invoke a discovered tool with `call_read_tool` when its `readOnlyHint` is `true`; use `call_tool` for every other tool. Pass the discovered name as `tool` and its original input object as `arguments`. REST callers continue to use the direct `/api/v1/tools/<tool-name>` endpoint.

## Prepare the input

Accept CSV, spreadsheet, Markdown, JSON, copied text, saved Rankizz keywords, or a prior research result. Preserve:

- original keyword
- volume, difficulty, CPC, rank, or intent when supplied
- source and retrieval date
- existing tags or proposed page

Normalize casing and whitespace for comparison without destroying the original values. Separate branded, irrelevant, wrong-market, and malformed terms before clustering.

## Build evidence locally

Use the site's existing URL inventory, navigation, sitemap, or supplied page list to understand current page purposes. Rankizz is not required for semantic and intent clustering when the input already contains enough context.

For ambiguous or high-value groups, use live SERP similarity if available. Similar wording does not prove the same intent; different wording does not prove separate pages.

## Use Rankizz conditionally

When connected:

- call `list_saved_keywords` to load a reviewed project set
- call `get_keyword_metrics` once for important terms missing metrics
- call `get_serp_results` in batches for ambiguous clusters
- call `get_site_explorer_inventory` to map clusters to known site URLs
- call `get_ranked_keywords` or Search Console tools when existing performance affects the mapping

Rankizz-hosted calls require at least 10 credits. On a low-credit response, stop cloud calls, link to `https://www.rankizz.com/billing`, and continue with available inputs.

Do not save keywords, replace tags, or reorganize project data without explicit confirmation.

## Decide page boundaries

Follow [references/clustering-rules.md](references/clustering-rules.md).

For each cluster, decide whether to:

- map to one existing page
- improve or consolidate existing pages
- create one new page
- split into multiple page intents
- retain for validation
- exclude

Prefer the searcher's expected page and task over a mechanically convenient taxonomy.

## Deliver

Return:

1. a clustering summary and evidence limitations
2. the proposed page map
3. cannibalization and consolidation findings
4. excluded or uncertain terms with reasons
5. a prioritized creation or refresh queue

Each cluster must include primary keyword, secondary terms, intent, recommended page type, target URL or proposed slug, aggregate demand only when mathematically valid, evidence, and confidence.

Do not sum duplicate or close-variant volume as if every value were independent. Do not claim SERP similarity unless SERPs were actually compared.
