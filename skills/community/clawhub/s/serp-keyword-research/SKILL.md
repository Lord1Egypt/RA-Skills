---
name: serp-keyword-research
description: Runs SERP and keyword research via Crawlora — Google, Bing, Brave, DuckDuckGo, Yahoo, Baidu, Yandex, selected Qwant/Startpage suggestions, and Google Trends. Use for localized search snapshots, autocomplete ideas, or trend context; it does not provide universal keyword volume.
---

# SERP & keyword research

Capture search-engine result samples and keyword/trend signals as normalized
JSON from the Crawlora API. Baidu and Yandex add localized result surfaces;
Qwant and Startpage currently contribute autocomplete suggestions only.

## When to use this skill

- "What ranks for <query> on Google / Bing?" / "snapshot the SERP for …".
- "Keyword ideas / autocomplete for …" (suggest endpoints).
- "Is <topic> trending?" / "interest over time / by region for <keyword>."
- "Related and rising queries for …" (Google Trends).
- SEO/SERP monitoring, keyword discovery, or trend research.

## Setup (one-time)

- Get a free Crawlora API key (2,000 credits/mo, no card) at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`. Missing/invalid key → `401`.

## How it works

1. **SERP** — Google search is `POST /google/search` with flat `keyword`,
   `language`, and `country` fields. Bing, Brave, DuckDuckGo, Yahoo, Baidu,
   and Yandex use `GET` with `q`. Search results are provider-specific samples:
   preserve each engine's market/language settings, result order, and retrieval
   time; do not treat ranks from different engines as a common position metric.
   On a `503` challenge, record the failure and use another engine only when it
   fits the requested market.
2. **Verticals** — news/videos/images per engine (`/google/news`, `/bing/videos`,
   `/duckduckgo/news`, `/duckduckgo/image`, `/duckduckgo/video`, `/duckduckgo/shopping`, …).
3. **Keyword ideas** — autosuggest: `GET /google/suggest?q=...`, `/bing/suggest`,
   `/brave/suggest`, `/baidu/suggest`, `/yandex/suggest`, `/qwant/suggest`, and
   `/startpage/suggest`. Suggestions are query ideas in the source's ranking
   order, not search-volume estimates or proof of audience demand.
4. **Trends** — Google Trends `POST` endpoints:
   `/google/trends/explore/interest-over-time`, `/interest-by-region`,
   `/related-topics`, `/rising-queries`, `/top-queries` (body: `{"keywords":[...]}`),
   plus `GET /google/trends/trending` for what's hot now.

Full endpoint list, methods, and params: [`reference/endpoints.md`](reference/endpoints.md).

## Calling the API

```sh
# GET search engines + suggest:
scripts/crawlora.sh /bing/search q="web scraping api" | jq '.'
scripts/crawlora.sh /brave/search q="web scraping api" | jq '.'
scripts/crawlora.sh /duckduckgo/search q="web scraping api" | jq '.'
scripts/crawlora.sh /yahoo-search/search q="web scraping api" | jq '.'
scripts/crawlora.sh /baidu/search q="web scraping api"
scripts/crawlora.sh /yandex/search q="web scraping api"
scripts/crawlora.sh /google/suggest q="web scraping" | jq '.'
scripts/crawlora.sh /qwant/suggest q="web scraping"
scripts/crawlora.sh /startpage/suggest q="web scraping"

# POST endpoints take a JSON body (note -X POST):
scripts/crawlora.sh -X POST /google/search '{"keyword":"web scraping api","language":"en","country":"us"}' | jq '.'
scripts/crawlora.sh -X POST /google/trends/explore/interest-over-time '{"keywords":["web scraping"]}' | jq '.'
```

Use `scripts/crawlora.sh` for all requests; it keeps the API key out of command-line arguments.


## Endpoint reference

See [`reference/endpoints.md`](reference/endpoints.md) for every search and
suggestion endpoint this skill uses (method, path, params, and description).

## Examples

- **SERP snapshot:** `POST /google/search` (and `/bing/search`) for a target query;
  record the ranked result titles/URLs to track positions over time.
- **Keyword expansion:** seed term → `/google/suggest` → for each suggestion,
  `POST /google/trends/explore/rising-queries` to find momentum.
- **Trend check:** `POST /google/trends/explore/interest-over-time` with
  `{"keywords":["electric bikes","e-bikes"]}` and compare the series.

## Notes & limits

- **Credits / pay-on-success:** billed only on `2xx`; free tier 2,000 credits/mo.
  Key at [https://crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- **Public data only** — public search results; respect each engine's terms.
- Search result lists are not full-index exports. Baidu/Yandex, Qwant/Startpage,
  and English-language providers have different locale and result semantics;
  keep samples separate and do not infer universal rank, traffic, or demand.
- **Security:** key lives in `CRAWLORA_API_KEY` only — never hardcode, query-param, or commit it.
- Search endpoints may return `503` when the engine serves a challenge page —
  retry or switch engines (Google ↔ Bing ↔ Brave). Google search is rate-limited
  to ~1 req/s (`429` on excess).
