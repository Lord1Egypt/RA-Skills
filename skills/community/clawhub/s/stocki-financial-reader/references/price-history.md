# price-history

## Overview

Stocki gateway v3 unified historical-price query, via `POST /api/v3/datareader/read` with `data_type=price`. Supports single stock / multi-stock batch / index / ETF / futures. **Adjustment-price semantics** is the first pitfall of this skill: OHLCV is unadjusted by default; for cross-ex-date comparison you must explicitly pass `metrics=["adj_close"]`.

## Trigger Vocabulary

- 中文："历史价 / 历史走势 / 月线 / 周线 / 日 K / K 线 / 过去一年涨 / 三年回报 / 区间收益 / OHLCV / 成交量 / 收盘价 / 后复权 / 前复权 / adj_close / 累计收益"
- English: "price history / OHLCV / candle / weekly chart / yearly return / cumulative return / adjusted close / forward return"
- Boundaries:
  - Realtime / intraday / movers leaderboard → `realtime-quote.md` (response carries `data_context.freshness`)
  - PE / PB / ROE historical time series → `fundamentals-panel.md`
  - Valuation history percentile (5y) → `financial-context.md` L1
  - Strategy backtest performance → backtest skill **not yet delivered** (upstream limitation, tracked separately). For pure-arithmetic, no-strategy questions like "how much did CSI 300 equal-weight gain in one year", this skill can take head and tail of `metrics=["adj_close"]`; for backtests with strategy / rebalancing / stop-loss, tell the user it is currently unavailable.

## Endpoint

| Method | Path | Purpose |
|---|---|---|
| POST | `$STOCKI_GATEWAY_URL/api/v3/datareader/read` | `data_type=price` historical OHLCV / adjusted |

Availability matrix (re-check with `market-calendar.md` `/availability` before assuming a change; currently known working combinations):
- `cn/hk/us:stock × price`
- `cn:etf × price`
- `cn:futures × price`
- `cn:index / hk:index / us:index × price`
- `crypto:crypto:price` is currently **unavailable** (response passes through server `error + warnings`; do not pretend it works)

## Input schema

```json
{
  "area": "cn",
  "asset_type": "stock",
  "data_type": "price",
  "symbols": ["600519"],
  "metrics": ["open","high","low","close","volume"],
  "start_date": "2026-04-01",
  "end_date": "2026-04-30"
}
```

| Field | Required | Description |
|---|---|---|
| `area` | yes | `cn / hk / us / crypto` |
| `asset_type` | yes | `stock / index / etf / futures / crypto` |
| `data_type` | yes | fixed `"price"` |
| `symbols` | yes | list; stocks use bare code ("600519"); **indexes carry exchange suffix** ("000300.SH" / "399006.SZ" / "HSI.HI") |
| `metrics` | no | defaults to the full OHLCV set; for cumulative return you must explicitly pass `["adj_close"]` |
| `start_date / end_date` | yes | YYYY-MM-DD |
| `inline_threshold` | no | int, range `[1, 1000]`, default 50 (silently clamped). Pass when expected `total_records > 50` to avoid 50-row truncation; estimate `N = symbols × trading_days × metrics` and set `min(ceil(N × 1.2), 1000)`. **Full decision rule: SKILL.md §Inline Threshold.** |

⚠️ **Adjusted-price is mandatory for cross-ex-date math**: default `metrics` does not include adjusted prices. **For cumulative return / cross-ex-date comparison → you must pass `metrics=["adj_close"]`** (works for CN/HK; US `adj_close` is occasionally NA → fall back to `close` but the LLM must explicitly tell the user precision is limited).

## ⚠️ Futures continuous-contract roll-over warning (required for asset_type=futures)

`cn:futures × price` returns the **main-contract (XXmain) continuous series**, which contains **non-market-driven** price jumps on contract switch days (a calendar spread of 1–5% between the old contract's last-day close and the new contract's first-day close).

- ❌ **Do not** compute daily return as `(close_t / close_{t-1}) - 1` directly — roll days will contaminate the series and long-horizon cumulative returns will be wildly wrong.
- ❌ **Do not** use head-vs-tail `close` to compute an N-year cumulative return — the roll-day jump does not cancel.
- ✅ Short-horizon analysis that does not cross a roll day can use `close` normally.
- ✅ Return series that crosses roll days: use the `pct_change` carried in the response (when available); or on the client side identify days with a sharp drop in `oi` (open interest) as a roll signal and exclude them.
- ✅ Long-horizon cumulative return / backtest: v3 currently does **not** expose a separately adjusted continuous series. Tell the user the result contains roll-over noise — do not pretend it is precise.

Typical roll nodes: the few trading days before contract expiry; financial futures (IF/IC/IH) roll monthly; commodity futures (I/CF etc.) roll per product-specific rules.

## E2E examples

**(a) Happy path — cn single-stock monthly OHLCV**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"stock","data_type":"price","symbols":["600519"],"metrics":["open","high","low","close","volume"],"start_date":"2026-04-01","end_date":"2026-04-30"}'
```
Expected: `data[*] = {code, date, open, high, low, close, volume}`, ~22 trading days.

**(b) Batch + long window + adj_close (cumulative-return scenario)**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"stock","data_type":"price","symbols":["600519","000858"],"metrics":["adj_close"],"start_date":"2025-05-01","end_date":"2026-05-01","inline_threshold":600}'
```
Expected: `total_records ~484` (2 stocks × 242 trading days). **`inline_threshold = 600` is set explicitly** (484 × 1.2 margin per SKILL.md §Inline Threshold) so `len(data) == total_records == 484` and the 50-row truncation does not apply. To compute a 1-year cumulative return → take per-stock last `adj_close` / first `adj_close` - 1. **Do not use `close` for 1-year comparisons** (ex-date events will introduce series jumps).

**(c) Multi-market — us / hk index comparison**:
```bash
# us SPY index proxy
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"us","asset_type":"index","data_type":"price","symbols":["SPX.GI"],"metrics":["close"],"start_date":"2025-05-01","end_date":"2026-05-01"}'

# hk Hang Seng
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"hk","asset_type":"index","data_type":"price","symbols":["HSI.HI"],"metrics":["close"],"start_date":"2025-05-01","end_date":"2026-05-01"}'
```
Note: us single-stock response also carries redundant fields like `pre_close / change / pct_change / amount` (spec does not force consumption; take as needed).

**(d) Upstream-error pass-through — crypto unavailable**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"crypto","asset_type":"crypto","data_type":"price","symbols":["BTCUSDT"],"start_date":"2026-04-01","end_date":"2026-04-30"}'
```
Expected: `{"action":"error","data":[],"metadata":{"warnings":["fetch failed: Missing config: database_url - crypto. "]}}` — the skill teaches the LLM to pass `metadata.warnings` through to the user and state plainly "crypto historical price is currently unavailable from the data source"; do not fabricate.

## Response Fields — Raw → User-Facing Label

| Raw key | EN label | CN label | Note |
|---|---|---|---|
| `data[*].code` | Symbol code | 代码 | bare code for stocks/ETFs; index includes exchange suffix |
| `data[*].date` | Date | 日期 | YYYY-MM-DD |
| `data[*].open` | Open | 开盘 | |
| `data[*].high` | High | 最高 | |
| `data[*].low` | Low | 最低 | |
| `data[*].close` | Close | 收盘 | NOT adjusted; do not use for cross-ex-date comparisons |
| `data[*].volume` | Volume | 成交量 | |
| `data[*].amount` | Turnover | 成交额 | US stocks only |
| `data[*].pre_close` | Previous Close | 昨收 | US stocks only |
| `data[*].change` | Price change | 涨跌额 | US stocks only |
| `data[*].pct_change` | Percent change | 涨跌幅 | US stocks; also valid for futures roll-aware return |
| `data[*].adj_close` | Adjusted Close | 复权收盘价 | MUST use for cumulative-return / cross-ex-date comparisons (CN/HK reliable; US occasionally NA — fallback to close with explicit precision caveat) |
| `data[*].oi` | Open interest | 持仓量 | futures only; roll-day signal (sharp drop = roll) |
| `total_records` | Total rows | 总行数 | expected ≈ N_symbols × N_trading_days |
| `metadata.data_path` | CSV path | CSV 路径 | triggered when `total_records > inline_threshold` (default 50). CSV not directly fetchable from the runtime — **prefer raising `inline_threshold` (max 1000) on the request** rather than relying on this path. |
| `metadata.elapsed_ms` | Elapsed (ms) | 耗时(毫秒) | |
| `metadata.row_count` | Row count | 行数 | |
| `metadata.symbol_requested` | Requested symbols | 请求标的 | |
| `metadata.symbol_returned` | Returned symbols | 返回标的 | |
| `metadata.missing_symbols` | Missing symbols | 缺失标的 | symbols asked for but no data returned |
| `metadata.warnings` | Warnings | 警告 | upstream-fetch failure / data-source issues; MUST be surfaced to the user |

**Index symbol presentation rule**: never show suffix `.SH / .SZ / .HI / .GI` to the user. Map to display name instead: `000300.SH` → "沪深300" / CSI 300; `399006.SZ` → "创业板指" / ChiNext; `HSI.HI` → "恒生指数" / Hang Seng Index; `SPX.GI` → "标普500" / S&P 500. Pick CN or EN display per user's language.

**Futures roll-over discipline**: when surfacing return / cumulative-pnl figures for `asset_type=futures`, explicitly note any roll-overs in the window — never silently use raw `close` head-vs-tail to claim a long-horizon return.

**Output discipline**: never pass raw key (`adj_close`, `pct_change`, pipe-delim symbol like `AAPL|ST|USA`, source-tagged industry prefix 形如 `<src>-<category>`) to user-visible text. Agent picks EN or CN label based on the user's language.

## Cross-ref

- Realtime intraday → `realtime-quote.md`
- Valuation time series (PE/PB/PS) → `fundamentals-panel.md`
- Combined 5y percentile → `financial-context.md` L1
- Strategy backtest → not yet delivered (upstream limitation, tracked separately)
- BTC/ETH historical price → this skill passes the `crypto:crypto:price` unavailable error through (does not pretend it works); for crypto realtime, use `realtime-quote.md` (freshness may be `latest_close`)
