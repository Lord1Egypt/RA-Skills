---
name: uexx-data-cloud
description: Use this skill when the user wants to query cryptocurrency market data, sentiment, ETF flows, funding rates, OI, long/short ratios, or asks to use UEXX Data Cloud. The skill automatically obtains or reuses a Free API Key and returns direct answers from the cached market data service instead of teaching API usage by default.
metadata:
  short-description: Query crypto market cached data
---

# UEXX Data Cloud

UEXX Data Cloud is a cryptocurrency market data cache API for quantitative research, market monitoring, and trading systems. It provides cached global market data, selected symbol-level history, automatic historical backfill, and Free/PRO access levels.

Use this skill to answer user questions directly from UEXX data. Do **not** default to API tutorials. Only show curl/Python code when the user explicitly asks how to integrate the API.

## Default Workflow

1. Understand the user's data question.
2. If needed, run `scripts/query.py` with the appropriate intent and symbol.
3. The script automatically obtains or reuses a Free Key via `POST /api/v1/free-key`.
4. Read the JSON result and answer in natural language.
5. Mention data time/cache age when useful.

## Supported Intents

- `fear-greed`: fear and greed index, market sentiment
- `altcoin-season`: altcoin season index
- `funding-rate`: symbol funding rate, e.g. BTC/ETH
- `oi`: symbol open interest
- `long-short`: symbol account long/short ratio

Default symbol is `BTCUSDT` when the user asks a symbol-level question without a symbol.

## Scripts

Use Python 3.

```bash
python scripts/query.py fear-greed
python scripts/query.py altcoin-season
python scripts/query.py funding-rate --symbol BTC
python scripts/query.py oi --symbol ETH
python scripts/query.py long-short --symbol BTCUSDT
python scripts/list_catalog.py
```

## Answer Style

Return the value and interpretation, not raw JSON.

Example:

> 今日恐慌贪婪指数为 72，处于 Greed 区间。数据更新时间为 2026-05-19，缓存约 2 分钟前刷新。市场情绪偏乐观，但这不是单独的买入信号。

For unavailable or PRO-only data, say what is available on Free and suggest PRO only when relevant.

## API Usage Requests

If the user explicitly asks for API integration, provide:

- Base URL: `https://bbs.uexx.com`
- Free Key endpoint: `POST /api/v1/free-key`
- Auth header: `X-API-Key: <key>`
- Relevant endpoint and a short curl/Python example.

See `references/api_catalog.md` for available data categories and endpoint mapping.
