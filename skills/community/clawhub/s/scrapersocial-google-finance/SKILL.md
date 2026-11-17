---
name: google-finance-api
version: 1.0.4
description: Google Finance data toolkit via ScraperSocial — live quotes, historical price candles and instrument search.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - google-finance
  - stocks
  - quotes
  - market-data
  - social-media
  - api
  - mcp
allowed-tools: Bash(node:*)
metadata:
  openclaw:
    primaryEnv: SCRAPERSOCIAL_KEY
    homepage: https://scrapersocial.com
    requires:
      env:
        - SCRAPERSOCIAL_KEY
    network:
      allow:
        - api.scrapersocial.com
    shell:
      only: scripts/*.js
---

# Google Finance API skill

Read public Google Finance data as clean JSON. This Google Finance API skill returns a current quote for an instrument, historical price candles, and search across tickers — at 1 credit per call, which makes it practical to poll a watchlist.

This skill wraps **3 live Google Finance endpoints** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- A user asks what a stock, index or currency pair is trading at.
- You need historical candles to chart or compute a return.
- You need to resolve a company name to a ticker symbol.

### Do not use this skill when

- **You are making trading or investment decisions on this data.** It is a convenience read of a public page, not an exchange feed. It is not licensed market data, may be delayed, and may be served from cache.
- **You need tick-level or real-time data.** Use a market data vendor.
- **You need fundamentals, filings or analyst estimates.** Not covered here.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 3 documented `/v1/google_finance/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_history.js` | List Google Finance history. | handle | 1 credit per candle |
| `get_quote.js` | Get Google Finance quote. | handle | 1 credit |
| `search.js` | List Google Finance search. | query | 1 credit per instrument |
| `call_endpoint.js` | Call any `/v1/google_finance/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/google-finance-api/scripts/get_quote.js AAPL
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/google_finance/history` | handle | candle | 1 credit per candle | yes |
| `/v1/google_finance/quote` | handle | quote | 1 credit | no |
| `/v1/google_finance/search` | query | instrument | 1 credit per instrument | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get a stock quote as JSON?

`get_quote.js` with the instrument handle, for 1 credit. Use `search.js` first if you only know the company name.

### Can I get historical prices?

Yes. `get_history.js` returns candles, charged 1 credit per candle returned, so set `--limit` deliberately.

### Is this real-time data?

No. Treat it as indicative. Responses may be cached; `--fresh` bypasses the cache at the same cost, but the underlying page is not an exchange feed.

### Is this an official Google API?

No. ScraperSocial is independent and not affiliated with Google.

## Links

- [Google Finance data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
