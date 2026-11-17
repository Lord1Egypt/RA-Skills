# Stock contract exchange ranking

`POST https://api.rootdata.com/open/skill/stock_leaderboard`

Send `Authorization: Bearer {ROOTDATA_SKILL_KEY}`, `Content-Type: application/json`, and optionally `language: cn` (default: `en`).
Success envelope: `{"result":200,"data":...}`. Fields without source data can be null or absent.

Uses the latest published stock-contract leaderboard snapshot. Percentage fields are formatted strings; absent depth/spread data is not zero.

## Request body

Use `{}`; this endpoint has no query parameters.

## Response fields

| Field | Type | Meaning |
|---|---|---|
| `rank` | int | Rank |
| `exchange` | string | Exchange identifier |
| `score` | decimal | Overall score (0-100) |
| `contract_count` | int | Number of valid stock contracts |
| `open_interest_change_pct` | string | 24h open interest change rate (percentage, e.g. "3.10%"; null when no comparable historical data) |
| `turnover_24h_change_pct` | string | 24h turnover change rate (percentage; null when no comparable historical data) |
| `weighted_depth_2pct_usd` | decimal | Weighted ±2% depth (USD) |
| `spread_pct` | string | Turnover-weighted average spread (percentage) |
| `funding_rate_pct` | string | 24h funding rate (percentage) |
| `maker_fee_rate` | string | Maker fee rate (single value or range, e.g. "0.0200%" or "0.0200% - 0.0400%") |
| `taker_fee_rate` | string | Taker fee rate (single value or range) |
| `margin` | string | Margin settlement currency (e.g. USDT; multiple currencies separated by /) |
| `max_leverage` | int | Maximum leverage multiplier |
