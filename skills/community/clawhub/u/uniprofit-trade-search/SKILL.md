---
name: uniprofit-trade-search
description: Search UniProfit trade intelligence data through the OpenClaw-compatible UniProfit API. Use when Codex or OpenClaw needs importer lookup, exhibition lead search, or purchase requirement search with a user-created `trade_search` API key.
metadata:
  openclaw:
    emoji: 🔍
    requires:
      env: ["UNIPROFIT_API_BASE_URL", "UNIPROFIT_TRADE_SEARCH_KEY"]
      bins: ["python"]
---

# UniProfit Trade Search

Use this skill to query UniProfit trade data from the OpenClaw runtime.

## Quick Start

Required environment variables:

- `UNIPROFIT_API_BASE_URL`
- `UNIPROFIT_TRADE_SEARCH_KEY`

Credential format:

```http
X-UniProfit-Key: {UNIPROFIT_TRADE_SEARCH_KEY}
```

Read only what you need:

- Read `references/api.md` for request and response formats.
- Read `references/query-patterns.md` when the user's search intent is vague.
- Read `references/error-handling.md` when an API call fails or returns no data.

## Protocol Contract

For runtime execution, follow this protocol exactly.

Use only these runtime endpoints:

- `GET {UNIPROFIT_API_BASE_URL}/openclaw/credential/me`
- `POST {UNIPROFIT_API_BASE_URL}/openclaw/search/query`

Execution checklist:

- send authentication with `X-UniProfit-Key`
- send search requests as `POST`
- send search requests with a JSON body
- keep `source`, `filters`, `page`, and `page_size` in the request body

Do not replace this skill with generic supplier-search or buyer-search endpoints.

Canonical runtime pattern:

1. validate the credential if needed with `GET /openclaw/credential/me`
2. build a query plan
3. execute search with `POST /openclaw/search/query`
4. summarize the current result window

Run `scripts/check_credential.py` if the credential may be missing or invalid.

## Use This Skill When

- the user wants overseas buyer or importer leads
- the user wants exhibition lead records
- the user wants procurement or sourcing requirement records
- the user wants structured trade search against UniProfit-owned datasets

Do not use this skill for:

- sending emails
- generating email drafts
- general web research outside UniProfit data

## Planning Rules

Prefer structured filters over broad searches.

Use a two-step workflow:

1. build an internal query plan
2. execute the query only if the plan is reliable enough

Do not turn every natural-language request directly into an API call.

Choose one source first:

- `importers` for importers or buyers
- `exhibition` for exhibition leads
- `requirements` for procurement demand

Use only supported filters for the chosen source:

- `importers`: `company_name`, `country_code`, `hs_code`, `hs_codes`, `date_period`, `is_verified`
- `exhibition`: `fair_name`, `state`, `company_name`, `procurement_category`, `contact_person`
- `requirements`: `country`, `purchase_title`, `purchasing_unit`, `keyword`, `min_amount`, `max_amount`, `currency`

Important:

- `importers` does not support `keyword`
- product keyword search should usually use `requirements`
- if the user wants buyer search by product on `importers`, prefer HS code first

Language strategy:

- first query with the user's original wording
- if the first query returns no result, allow one language-aware fallback that better matches the likely storage language of the chosen source
- do not immediately translate everything into English by default
- do not chain many multilingual retries

Do not send unsupported filters. The backend rejects them with `400`.

If the user does not specify a source, choose the best fit and state it briefly.

Before calling the API, decide these four items internally:

- recommended source
- recommended filters
- confidence level
- whether one critical field is still missing

If confidence is low, ask the user one short clarifying question instead of querying immediately.

If confidence is medium or high, query once with the best structured plan.

For product-style requests:

- product keyword + buyer intent: prefer `requirements` first unless the user already has HS code
- product keyword + explicit HS code: use `importers`
- company lookup: use `importers`
- fair or exhibitor lookup: use `exhibition`

## Execution Flow

1. Read the user request and infer buyer search, exhibition search, or demand search intent.
2. Build a query plan:
   - source
   - filters
   - confidence
   - missing critical field, if any
3. If one critical field is missing and the plan is weak, ask one short question.
4. Otherwise run `scripts/search_trade.py`, or make the same protocol call to `POST /openclaw/search/query` with `X-UniProfit-Key` and a JSON body.
5. If the first query returns no result, allow one fallback retry using the same source with a closer language match for that source.
6. Summarize the search source, filters, current window size, whether more results may exist, and the best leads.
7. If there are still no results, suggest one narrower or broader retry based on the same plan.

## Planning Heuristics

Prefer these planning rules:

- If the user says buyer / importer / customer and gives company-like terms, choose `importers`.
- If the user gives a fair name, exhibitor context, or exhibition lead request, choose `exhibition`.
- If the user gives product words without HS code, especially for demand discovery, choose `requirements`.
- If the user asks for buyers by product but only gives a plain product phrase, do not send `keyword` to `importers`.
- If the user asks for buyers by product and also gives HS code, use `importers` with `hs_code` or `hs_codes`.
- If the user gives only country + generic product phrase and no HS code, prefer one short clarifying question over a blind `importers` query.
- For `requirements`, keep the user's original country and product wording on the first attempt when the database is likely to store those fields in the same language.
- Use at most one language fallback after a zero-result first attempt. Example: keep `哈萨克斯坦 + 家居用品` first, then try one closer storage-language fallback such as `household` if needed.

## Output Style

Start with:

- source searched
- filters applied
- current window result count
- whether more results may exist

Then present the most actionable rows. Prioritize company name, geography, contact clues, and product relevance.

For `requirements` results, prefer showing:

- `purchase_title`
- `purchasing_unit`
- `email` when present
- `country`
- `deadline`
- `amount` and `currency` when present

Describe results as a current query window rather than a complete database count. If the runtime response includes `has_more`, explain that more matching results may exist and guide the user to narrow the filters for a more focused next step.

Preferred wording pattern:

- `This query returned {returned_count} results from {source}.`
- if `has_more = true`: `More matching results may be available beyond the current window. Narrow the filters to continue with a more focused search.`
- if `query_hint` exists: restate it as the next best search refinement suggestion

Do not dump raw JSON unless the user asks for it.
