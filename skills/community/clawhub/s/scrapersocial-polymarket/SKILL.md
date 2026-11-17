---
name: polymarket-api
version: 1.0.4
description: Polymarket data toolkit via ScraperSocial — prediction market listings and current odds as clean JSON.
license: MIT-0
author: ScraperSocial
homepage: https://scrapersocial.com
repository: https://github.com/nikhonit/social-media-api-skills
tags:
  - polymarket
  - prediction-markets
  - odds
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

# Polymarket API skill

Read public Polymarket data as clean JSON. This Polymarket API skill has a single endpoint: search markets by query and get back the listings with their current odds, at 1 credit per market. Prediction market prices are a genuinely useful forecast signal, and this is a cheap way to put them in front of an agent.

This skill wraps **1 live Polymarket endpoint** from the [ScraperSocial](https://scrapersocial.com) API. Public data only, returned as clean JSON.

## When to use this skill

- A user asks what the market thinks the odds of an event are.
- You want a forecast signal to compare against commentary or polling.
- You are tracking how odds on a question move over time.

### Do not use this skill when

- **You are placing trades.** This is read-only and is not trading infrastructure. Nothing here executes orders, and the odds may be cached rather than live.
- **You are presenting odds as fact.** They are a market price, not a prediction from an authority — say so when you surface them.
- **You need order book depth or historical series.** One endpoint, current listings only.

## Setup

```bash
export SCRAPERSOCIAL_KEY=sk_live_...   # https://scrapersocial.com/app/keys
```

Signing up at [scrapersocial.com/signup](https://scrapersocial.com/signup) includes 100 free credits, no card required.

## Permissions and scope

These scripts do exactly three things and nothing else: read one environment variable (`SCRAPERSOCIAL_KEY`), send HTTPS requests to `https://api.scrapersocial.com` (the host is a constant in the code, not configurable), and print JSON. They run as `node scripts/<name>.js` with no other shell use, no file writes and no persistence. `call_endpoint.js` accepts only the 1 documented `/v1/polymarket/` paths in the table below and refuses anything else before a request is made.

## Scripts

| Script | What it does | Input | Credits |
|---|---|---|---|
| `get_markets.js` | List Polymarket markets. | query | 1 credit per market |
| `call_endpoint.js` | Call any `/v1/polymarket/` endpoint directly | path + params | varies |

Every script also accepts `--limit`, `--cursor`, `--fields`, `--format` and `--fresh`. `--limit` is clamped to 50: above that the API returns an async job instead of data.

## Example

```bash
node skills/polymarket-api/scripts/get_markets.js "election"
```

Every response uses the same envelope:

```json
{ "data": {}, "meta": { "count": 20, "next_cursor": "..." }, "request_id": "a18e4ef88ad4b00b" }
```

`meta` appears on paginated endpoints only. Keep `request_id` — support traces calls with it.

## Endpoints

| Endpoint | Input | Returns | Credits | Paginated |
|---|---|---|---|---|
| `/v1/polymarket/markets` | query | market | 1 credit per market | yes |

Costs shown per item for paginated endpoints, per call otherwise. Failed calls are not charged.

## FAQ

### How do I get prediction market odds?

`get_markets.js` with a query returns matching markets and their odds, 1 credit per market.

### Are the odds live?

They may be served from cache. Pass `--fresh` to bypass it at the same credit cost, but treat the result as indicative rather than an execution price.

### Can I trade through this?

No. Read-only. Use Polymarket directly for anything transactional.

### Is this an official Polymarket API?

No. ScraperSocial is independent and not affiliated with Polymarket.

## Links

- [Polymarket data on ScraperSocial](https://scrapersocial.com)
- [All 33 platform skills](https://github.com/nikhonit/social-media-api-skills)
- [OpenAPI spec](https://scrapersocial.com/openapi.json) · [llms.txt](https://scrapersocial.com/llms.txt)

## Disclaimer

ScraperSocial is an independent product and is not affiliated with, endorsed by, or sponsored by any platform named in this repository. All product names, logos and brands are property of their respective owners. These skills return only publicly available data.
