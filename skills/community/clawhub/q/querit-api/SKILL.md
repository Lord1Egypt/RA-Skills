---
name: querit-api
description: Build and debug Querit.ai search API integrations - POST /v1/search for live web results, POST /v1/contents for clean page text. Use when Querit, querit.ai, api.querit.ai, or QUERIT_API_KEY appears; when writing or reviewing code that calls a web search or page-extraction API from an app, RAG pipeline, or agent and Querit is the provider. Not for running a one-off search - if the Querit MCP server is connected, call its tools instead.
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    requires:
      anyBins: [python3, curl]
    primaryEnv: QUERIT_API_KEY
    envVars:
      - name: QUERIT_API_KEY
        required: true
        description: "Querit API key, created on the Querit platform's API Key management page."
    homepage: https://www.querit.ai
---

# Querit API

Querit is a web retrieval system built for LLM consumption. Two endpoints, both `POST`, both JSON, both authenticated the same way:

- `https://api.querit.ai/v1/search` - ranked web results with snippets and optional page text
- `https://api.querit.ai/v1/contents` - crawl 1-10 URLs and return their content

This skill is for building and debugging an integration - code that will run in the user's own application. To simply retrieve something for the current task, use the Querit MCP server's `querit_search` and `querit_contents` tools if they are connected, rather than writing a script here.

## Authentication

```
Authorization: Bearer <QUERIT_API_KEY>
Content-Type: application/json
```

Keys are created on the Querit platform's API Key management page. Read the key from the `QUERIT_API_KEY` environment variable - never hardcode it, never log it, never write it to a file that could be committed. When a user pastes a key into the conversation, use it for the call at hand and suggest they export it instead:

```bash
export QUERIT_API_KEY="..."   # or the agent's own scoped config
```

If the user has no key, point them at https://www.querit.ai to sign up, and at https://www.querit.ai/en/playground to try queries before writing code.

## Workflow

### 1. Verify the key and the endpoint first

`scripts/querit_smoke.py` uses only the Python standard library:

```bash
python3 scripts/querit_smoke.py --search "what does salesforce do"
python3 scripts/querit_smoke.py --contents https://example.com
python3 scripts/querit_smoke.py --search "openclaw skills" --need-content --count 5
```

It reads `QUERIT_API_KEY`, prints HTTP status, latency, result count, a normalized preview of each hit, and per-URL crawl status, and never prints the key. `--raw` dumps the untouched JSON. Prove the credential works before touching the user's codebase, so a bad key does not get debugged through their application stack.

### 2. Pick the endpoint

| The user needs | Endpoint |
|---|---|
| Find pages for a query | `/v1/search` |
| Find pages and ground an answer on their text | `/v1/search` with `needContent: true` |
| Full text of URLs the user already has | `/v1/contents` |
| Reliable text for every search hit | `/v1/search`, then `/v1/contents` on the URLs |

The last two rows are the decision that matters. `needContent: true` returns `sentence[]` only for results whose text was already available, and the field is simply absent otherwise. If every top result must have text, search then fetch, because `/v1/contents` reports per-URL success or failure explicitly.

### 3. Choose parameters

A request with every filter branch populated:

```json
{
  "query": "quantum computing breakthroughs",
  "count": 10,
  "needContent": true,
  "filters": {
    "languages": { "include": ["english"] },
    "geo": { "countries": { "include": ["united states"] } },
    "timeRange": { "date": "d7" },
    "sites": { "include": ["arxiv.org"] }
  }
}
```

Languages and countries are lowercase full names, not ISO codes. `timeRange.date` is a relative window (`d7`, `w2`, `m3`, `y1`) or an absolute `2026-08-01to2026-08-10`. `references/search-api.md` has the full value sets, the plan caps, and when each filter is worth applying; `references/contents-api.md` does the same for `format`, `crawlTimeout`, and `extrasMeta`.

### 4. Write the integration

`references/python-integration.md` has the SDK call, a REST client with retry and a QPS limiter, batch chunking for contents, and result normalization for RAG. For other languages, build against the request and response tables in `references/search-api.md` and `references/contents-api.md`.

Four field-level details that break naive parsers, whatever the language:

- `results.result` is nested one level deeper than most search APIs. Iterating `results` yields dict keys, not hits.
- `sentence` is absent, not empty, when a result has no text. Every field in a result is optional.
- `snippet` can contain HTML fragments. Sanitize before rendering or sending to a model.
- On `/v1/contents`, `results` and `statuses` are joined by `id`, not by position, and partial batches return 200.

### 5. Handle failures

`references/troubleshooting.md` covers 400, 401, 403, 429, timeouts, and the several ways a 200 carries nothing useful. The two that surprise people: 403 is usually per-endpoint subscription rather than a bad key, and 429 needs a client-side limiter rather than more retries.

## References

- `references/search-api.md` - `/v1/search`: request and response contract, accepted filter values, when to apply each.
- `references/contents-api.md` - `/v1/contents`: contract, the `results`/`statuses` pairing, choosing `format` and `crawlTimeout`.
- `references/troubleshooting.md` - error codes, empty responses, and isolating the failing layer.
- `references/python-integration.md` - SDK usage, a REST client with retry and rate limiting, batch concurrency, normalizing results.

Official docs: https://www.querit.ai/en/docs/overview/about
