# realtime-quote

## Overview

Stocki gateway v3 realtime quote snapshot. Two endpoint shapes: `get_latest_quotes` takes multi-asset groups (mixed across markets in one call); `get_all_latest_quotes` returns the full single-market panel (5000+ records). The response carries `market_status` + `data_context.freshness`, telling the LLM whether the data is realtime or latest_close.

## Trigger Vocabulary

- 中文："现在多少钱 / 现价 / 涨多少 / 跌多少 / 涨停 / 跌停 / 开盘了吗 / 收盘价 / 实时行情 / 涨幅榜 / 跌幅榜 / 量能 / 茅台 PE 现在"
- 英文："real-time price / intraday quote / latest price / pct change / market open / today's gainers / day high / current PE"
- 边界：用户问"昨天交易日吗 / 下个交易日" → `market-calendar.md`。"过去一年涨多少 / K 线" → `price-history.md`。"PE 历史时序 / 5y 分位" → `fundamentals-panel.md` / `financial-context.md`。"今天开盘吗" 也可走本 skill（response 自带 `market_status`）。

## Endpoint

| Method | Path | Purpose |
|---|---|---|
| POST | `$STOCKI_GATEWAY_URL/api/v3/quotes/get_latest_quotes` | Specified symbols, multi-asset groups (mix markets in a single call) |
| POST | `$STOCKI_GATEWAY_URL/api/v3/quotes/get_all_latest_quotes` | Single area×asset_type full panel (5000+ records, 60s server-side cache) |

## Input schema

### A. `get_latest_quotes` (QuotesV2Request)

```json
{
  "assets": [
    {"symbols": ["600519"], "area": "cn", "asset_type": "stock"}    
  ],
  "include_fundamentals": true,
  "timeout": 5.0
}
```

| Field | Required | Description |
|---|---|---|
| `assets[*].symbols` | yes | bare code list (no exchange suffix) |
| `assets[*].area` | yes | `cn / hk / us / crypto` |
| `assets[*].asset_type` | yes | `stock / index / etf / futures / crypto` |
| `include_fundamentals` | no | when true, CN stock response carries PE/PB/ROE/gross-margin/EPS snapshot |
| `timeout` | no | seconds, default 5.0 |

`assets` may contain multiple groups, allowing **one cross-market pull** (cn:stock + hk:stock + us:stock + crypto:crypto).

### B. `get_all_latest_quotes` (QuotesV2SimpleRequest)

```json
{"area": "cn", "asset_type": "stock", "include_fundamentals": false}
```

Flat top-level, single area×asset_type full panel; multiple markets require multiple calls. With `include_fundamentals=true`, 5000+ records all carry fundamentals — payload is large, use with care.

## E2E examples

**(a) Happy path — single stock + fundamentals**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/quotes/get_latest_quotes" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"assets":[{"symbols":["600519"],"area":"cn","asset_type":"stock"}],"include_fundamentals":true}'
```
Expected: `data[0]` contains `pct_change / close / pre_close / volume / fundamentals.{pe_ttm, pb_mrq, ps_ttm, roe, gross_margin_qfa, eps_qfa, sales_yoy_qfa, ...}`.

**(b) Batch across markets — cn + hk + us in one call**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/quotes/get_latest_quotes" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"assets":[
    {"symbols":["600519"],"area":"cn","asset_type":"stock"},
    {"symbols":["00700"],"area":"hk","asset_type":"stock"},
    {"symbols":["AAPL"],"area":"us","asset_type":"stock"}
  ]}'
```
Expected: `data` list contains 3 records; `data_context` carries three freshness keys `cn:stock / hk:stock / us:stock`.

**(c) Full-market + top gainers (client-side sort)**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/quotes/get_all_latest_quotes" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"stock","include_fundamentals":false}'
```
Expected: `data` has 5000+ records; the LLM can sort client-side by `pct_change` and take top-N (one of the few cases where client-side processing is acceptable, since the server has no dedicated ranking endpoint).

**(d) Upstream error / invalid area**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/quotes/get_latest_quotes" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"assets":[{"symbols":["BAD"],"area":"invalid","asset_type":"stock"}]}'
```
Expected: 4xx / empty `data` / explanatory `message` field; the skill instructs the LLM to surface the server-side error message to the user.

## Response Fields — Raw → User-Facing Label

All `data[*].fundamentals.*` values are pipe-delim strings of shape `"<value>|<CN label>|<as_of_date>|<extra>"`. Extract: `split("|")[0]` for the numeric value, `[1]` for the embedded CN label (matches the CN label column below), `[2]` for the PIT date.

| Raw key | EN label | CN label | Note |
|---|---|---|---|
| `market_status.<area>` | Market status | 市场状态 | enum: open / pre_market / post_market / closed |
| `data_context.<area>:<asset_type>.freshness` | Data freshness | 数据时效 | enum: realtime / latest_close / previous_close; MUST be surfaced to the user |
| `data_context.<area>:<asset_type>.context` | Context description | 状态说明 | natural-language string from upstream; can render directly |
| `data[*].pct_change` | Percent change | 涨跌幅 | |
| `data[*].open` | Open | 开盘 | |
| `data[*].high` | High | 最高 | |
| `data[*].low` | Low | 最低 | |
| `data[*].close` | Close | 收盘 | |
| `data[*].pre_close` | Previous Close | 昨收 | |
| `data[*].volume` | Volume | 成交量 | |
| `data[*].time` | Timestamp | 时间 | |
| `data[*].fundamentals.pe_ttm` | PE (TTM) | 市盈率(TTM) | pipe-delim |
| `data[*].fundamentals.pb_mrq` | PB (MRQ) | 市净率(MRQ) | pipe-delim |
| `data[*].fundamentals.ps_ttm` | PS (TTM) | 市销率(TTM) | pipe-delim |
| `data[*].fundamentals.roe` | ROE | 净资产收益率 | pipe-delim |
| `data[*].fundamentals.gross_margin_qfa` | Gross Margin (QFA) | 毛利率(单季) | pipe-delim |
| `data[*].fundamentals.net_margin_qfa` | Net Margin (QFA) | 净利率(单季) | pipe-delim |
| `data[*].fundamentals.eps_qfa` | EPS (QFA) | 每股收益(单季) | pipe-delim |
| `data[*].fundamentals.sales_yoy_qfa` | Revenue YoY (QFA) | 营收同比(单季) | pipe-delim |
| `data[*].fundamentals.np_yoy_qfa` | Net Profit YoY (QFA) | 净利润同比(单季) | pipe-delim |
| `data[*].fundamentals.price_chg_5d` | 5-Day Price Change | 5日涨跌幅 | pipe-delim |
| `data[*].fundamentals.price_chg_20d` | 20-Day Price Change | 20日涨跌幅 | pipe-delim |

**Output discipline**: never pass raw key (`pe_ttm`, `gross_margin_qfa`, pipe-delim symbol like `AAPL|ST|USA`, source-tagged industry prefix 形如 `<src>-<category>`) to user-visible text. Agent picks EN or CN label based on the user's language. For fundamentals pipe-delim values: surface `split("|")[0]` as the number; the embedded `split("|")[1]` Chinese label can be used directly OR mapped to the EN label above.

## Cross-ref

- Historical OHLCV / interval returns → `price-history.md` (use `metrics=["adj_close"]` to compute cumulative returns)
- PE/PB historical time series / valuation percentile → `fundamentals-panel.md` or `financial-context.md` L1 (5y percentile)
- One-shot composite view (financials + valuation + business structure + consensus) → `financial-context.md`
- Plain trading-day / market-holiday lookup → `market-calendar.md` (if the user is already asking about quotes, the `market_status` in this skill's response is sufficient — don't make a second call)
