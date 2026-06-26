# market-calendar

## Overview

Stocki gateway market status + trading calendar + data availability lookup. 5 GET endpoints, no body, all parameters via query string. Responses pass through to the user directly — no client-side post-processing.

## Trigger Vocabulary

- 中文："今天 A 股开盘吗 / 美股开了没 / 港股星期六开吗 / 昨天是不是交易日 / 下个交易日 / 交易日历 / 五一假期 / 数据有没有 / X 能查到吗"
- 英文："is the market open / trading day today / next trading day / market calendar / availability / does the gateway have X"
- Boundary: "Is Moutai open?" → go to `realtime-quote.md` (the response already carries `market_status`, saving one call).

## Endpoint

| Method | Path | Purpose |
|---|---|---|
| GET | `$STOCKI_GATEWAY_URL/api/v3/market/status` | Current market status (is_trading / last_trading_date / timezone) |
| GET | `$STOCKI_GATEWAY_URL/api/v3/market/trading_days` | Trading days within a date range |
| GET | `$STOCKI_GATEWAY_URL/api/v3/market/nearest_trading_date` | Nearest trading day ≥ the given date (inclusive) |
| GET | `$STOCKI_GATEWAY_URL/api/v3/market/next_trading_date` | Next trading day > the given date (exclusive) |
| GET | `$STOCKI_GATEWAY_URL/api/v3/availability` | Data availability matrix (which area×asset_type×data_type are queryable) |

## Input schema

| Endpoint | Required query | Description |
|---|---|---|
| `/market/status` | `area` ∈ {`all`, `cn`, `hk`, `us`, `crypto`} | `area=all` returns all 4 markets in one call |
| `/market/trading_days` | `begin_date`, `end_date`, `area` | `area` does not accept `all`, single market only; dates in YYYY-MM-DD |
| `/market/nearest_trading_date` | `date`, `area` | Single market |
| `/market/next_trading_date` | `date`, `area` | Single market |
| `/availability` | none | Returns the full matrix in one shot |

The `crypto` market is open 7×24 (response is always `is_trading: true`); `/availability` currently shows `crypto:crypto:price` as `{available: false, reason: ...}`.

## E2E examples

**(a) Happy path — fetch all-market status in one call**:
```bash
curl -X GET "$STOCKI_GATEWAY_URL/api/v3/market/status?area=all" \
  -H "Authorization: Bearer $STOCKI_API_KEY"
```
Expected: `{"cn":{"status":"post_market","is_trading":false,"last_trading_date":"2026-05-07","timezone":"Asia/Shanghai"}, "hk":{...},"us":{...},"crypto":{...}}`. Possible `status` values: `open / pre_market / post_market / closed`.

**(b) Cross-market batch — date-range trading days + single-day next (cn and us called separately)**:
```bash
curl -X GET "$STOCKI_GATEWAY_URL/api/v3/market/trading_days?begin_date=2026-05-01&end_date=2026-05-15&area=cn" \
  -H "Authorization: Bearer $STOCKI_API_KEY"

curl -X GET "$STOCKI_GATEWAY_URL/api/v3/market/next_trading_date?date=2026-05-08&area=us" \
  -H "Authorization: Bearer $STOCKI_API_KEY"
```
Expected (cn): `{"area":"cn","trading_days":["2026-05-06","2026-05-07",...],"count":8}`; US is similar.

**(c) Upstream error passthrough — unknown area**:
```bash
curl -X GET "$STOCKI_GATEWAY_URL/api/v3/market/status?area=invalid" \
  -H "Authorization: Bearer $STOCKI_API_KEY"
```
Expected: 4xx + JSON `{"detail":"..."}` or similar error; the skill instructs the LLM to surface the detail to the user without re-wrapping.

**(d) availability sample**:
```bash
curl -X GET "$STOCKI_GATEWAY_URL/api/v3/availability" \
  -H "Authorization: Bearer $STOCKI_API_KEY"
```
Expected: `{"datareader":{"cn:stock:price":true,"crypto:crypto:price":{"available":false,"reason":"..."},...},"quotes":{...},"probed_at":"..."}`.

## Response Fields — Raw → User-Facing Label

### `/market/status`

| Raw key | EN label | CN label | Note |
|---|---|---|---|
| `is_trading` | Is trading | 交易中 | bool; true = market currently open |
| `status` | Status | 状态 | enum: open / pre_market / post_market / closed |
| `last_trading_date` | Last trading date | 最近交易日 | YYYY-MM-DD; the most recent completed trading day |
| `timezone` | Timezone | 时区 | IANA tz id; show users a common name ("北京时间" / "美东时间" / "港时" / "UTC") |

### `/market/trading_days`

| Raw key | EN label | CN label | Note |
|---|---|---|---|
| `area` | Market | 市场 | echoed back |
| `trading_days` | Trading days | 交易日列表 | list of YYYY-MM-DD strings in the queried window |
| `count` | Count | 数量 | len(trading_days) |

### `/market/nearest_trading_date` and `/market/next_trading_date`

| Raw key | EN label | CN label | Note |
|---|---|---|---|
| `nearest_trading_date` | Nearest trading date | 最近交易日 | ≥ the given date (inclusive); applies to `/nearest_trading_date` only |
| `next_trading_date` | Next trading date | 下个交易日 | > the given date (exclusive); applies to `/next_trading_date` only |

### `/availability`

| Raw key | EN label | CN label | Note |
|---|---|---|---|
| `datareader.<area>:<asset_type>:<data_type>` | Availability flag | 可用性标志 | value is either `true` OR `{"available": false, "reason": "..."}`; handle both shapes |
| `quotes.<area>:<asset_type>` | Quotes availability | 行情可用性 | same shape rule |
| `probed_at` | Probed at | 探测时间 | ISO timestamp of last availability probe |

**Status enum presentation**: translate `status` enum for the user — `open` → "交易中" / "Open"; `pre_market` → "盘前" / "Pre-market"; `post_market` → "盘后" / "Post-market"; `closed` → "休市" / "Closed".

**Availability key presentation**: never echo the colon-joined raw key (`cn:stock:price`) to the user. Map to a phrase: `cn:stock:price` → "A 股价格数据" / "CN stock price data"; `crypto:crypto:price` → "加密货币价格数据" / "Crypto price data"; `hk:index:price` → "港股指数价格数据" / "HK index price data"; etc.

**Timezone presentation**: `timezone` field is an IANA tz id (`Asia/Shanghai` / `America/New_York` / `Asia/Hong_Kong` / `UTC`). Surface the common name to the user — "北京时间" / "美东时间" / "港时" / "UTC" — not the raw IANA id.

**Date presentation**: `last_trading_date` / `nearest_trading_date` / `next_trading_date` are YYYY-MM-DD strings; format as natural-language date when surfacing ("5 月 7 日" / "May 7").

**Output discipline**: never pass raw key (`is_trading`, `last_trading_date`, the colon-joined availability key like `cn:stock:price`, IANA tz id like `Asia/Shanghai`) to user-visible text. Agent picks EN or CN label based on the user's language.

## Cross-ref

- "Is Moutai open?" / "current price and also market status" → `realtime-quote.md` (response carries `market_status` + `data_context.<area>.freshness`)
- "When does X data start / how far back can I look?" → this skill's `/availability` only tells you **whether** data is queryable, **not the start date**; for the start date, call `price-history.md` or `fundamentals-panel.md` directly and inspect the actual date range in the response
- Crypto historical price unavailable → this skill's `/availability` flags `available:false`, but the concrete error passthrough is handled by `price-history.md`
