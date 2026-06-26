# fundamentals-panel

## Overview

Stocki gateway v3 unifies the financial statements (3 statements) + derived indicators + valuation time series + market cap behind one endpoint: `/api/v3/datareader/read`, partitioned by `data_type`. **Key LLM decision**: first identify which of the 4 `data_type`s the user is asking about; if a specific metric is needed (instead of the default columns), decide whether to hit the high-frequency cheatsheet below or fall back to `metric-resolver.md`.

Underlying `/api/v3/datareader/read` requires `start_date` / `end_date` and returns multi-period panels for all 4 `data_type`s. For a single-point query use `realtime-quote` with `include_fundamentals=true` instead.

## Trigger Vocabulary

- 中文："营业收入 / 营业利润 / 净利润 / 毛利 / 总资产 / 净资产 / 资产负债率 / 经营现金流 / ROE / ROA / 毛利率 / 净利率 / 周转率 / 杠杆 / PE / 市盈率 / PB / 市净率 / PS / 市销率 / TTM / 总市值 / 流通市值 / 自由流通 / 解禁 / 单季 / 累计 / 年报 / 季报 / 半年报 / 三季报"
- English: "revenue / net income / gross profit / total assets / equity / debt ratio / OCF / ROE / ROA / margin / turnover / leverage / P/E / P/B / P/S / TTM / market cap / free float"
- Boundaries:
  - Consensus estimates / analyst target price / business segments → `consensus-and-target.md`
  - One-shot composite + 5y percentile → `financial-context.md` L1 (preferred for "analyze Moutai"-style questions)
  - "What's Moutai's PE right now?" — real-time single value → `realtime-quote.md` with `include_fundamentals=true` (one call covers it + carries freshness)
  - User's metric name is not in the cheatsheet below → call `metric-resolver.md` first to obtain the canonical symbol, then come back to this skill

## Endpoint

| Method | Path | data_type | Purpose |
|---|---|---|---|
| POST | `$STOCKI_GATEWAY_URL/api/v3/datareader/read` | `financial` | Three statements (income / balance / cashflow), **quarterly panel**, date = period end |
| POST | `$STOCKI_GATEWAY_URL/api/v3/datareader/read` | `indicator` | Derived indicators (ROE / turnover / leverage etc.), quarterly panel |
| POST | `$STOCKI_GATEWAY_URL/api/v3/datareader/read` | `market_cap` | Total / float market cap (`extra.total=true/false` controls scope) |
| POST | `$STOCKI_GATEWAY_URL/api/v3/datareader/read` | `valuation` | Valuation time series + 52w + share counts, **daily panel** |

Availability matrix (measured 2026-05-08; re-check with `market-calendar.md` `/availability` before assuming a change):
- `cn:stock × {financial, indicator, market_cap, valuation}` ✅
- `hk:stock × {financial, indicator, market_cap, valuation}` ✅
- `us:stock × market_cap` ✅; most other us combos are unavailable — pass server `error + warnings` through to the user

<!-- These sections document the upstream API payload contract; raw column keys (e.g. `oper_rev`) appear here intentionally and are not user-visible. -->
<!-- lint:disable rule=canonical-metric -->
## Input schema

```json
{
  "area": "cn",
  "asset_type": "stock",
  "data_type": "financial",
  "symbols": ["600519"],
  "metrics": ["oper_rev","net_profit"],
  "start_date": "2024-01-01",
  "end_date": "2025-12-31",
  "extra": {"report_type": "Q4", "daily": false}
}
```

| Field | Required | Description |
|---|---|---|
| `area / asset_type / data_type / symbols` | yes | Same as the v3 datareader common contract |
| `start_date / end_date` | **yes** | The docs say some `data_type`s ignore these, but in practice **omitting them crashes** (NaTType bug, see notes) |
| `metrics` | no | Omit → server returns the default column set; if passed → must be a column key from the Response Fields cheatsheet below (e.g. `oper_rev`). A semantic name like "ROE" / "营业收入" / "revenue" / "净资产收益率" yields a MySQL `Unknown column` error — resolve through `metric-resolver.md` first |
| `extra.report_type` | no | `Q1 / Q2 / Q3 / Q4 / Y` (financial / indicator) |
| `extra.daily` | no | true = **PIT daily frequency** (most recent report period announced as of that day); false = quarterly panel (default) |
| `extra.pit` | no | A different PIT flag from `daily`; mainly affects segments and is generally unused by this skill |
| `extra.total` | no | `market_cap`-only: true=total market cap (default share=total_shares), false=float (default share=float_a_shares). Measured: default share is `float_a_shares`, not total |
| `inline_threshold` | no | int, range `[1, 1000]`, default 50 (silently clamped). Pass when expected `total_records > 50` to avoid truncation; for fundamental/indicator estimate `N = symbols × report_periods` and set `min(ceil(N × 1.2), 1000)`. **Full decision rule: SKILL.md §Inline Threshold.** |

⚠️ **`extra.daily=true` failure handling**: the server returns a regular `error + suggestion`. The skill teaches the LLM to pass the error through to the user; **do not silently retry with daily=false** — this is a client-side convention, the gateway endpoint does not make decisions for the client.

## Mandatory two-step flow (when metrics is semantic, not a known column key)

The `metrics` field of `/api/v3/datareader/read` accepts only column keys from the Response Fields cheatsheet below (e.g. `oper_rev`, `waa_roe`, `roe_deducted`). A semantic name (Chinese "营业收入" / "净资产收益率" / colloquial English "revenue" / "net income") → the server's MySQL reports `Unknown column`, the response has `action=error`, and the user sees a failure with no obvious cause.

| Step | Action | Skip consequence |
|---|---|---|
| **1** | Scan the cheatsheet section below. Hit → take the key directly. **Miss** → cross-ref `metric-resolver.md` to query the registry and pick one | Skipping `metric-resolver` and passing a Chinese / colloquial name directly → guaranteed failure |
| **2** | Put the resolved key into `metrics=[...]` and call this skill | — |

> ⚠️ Omitting `metrics` is also legal (the server returns the default column set), but when the user explicitly names a metric you **must resolve** it — do not fall back to default columns and make the user pick.

## `use_ytd_value` 累计/单季陷阱 + CN/HK 默认相反(b1 caveat)

`/api/v3/datareader/read` 对**普通财务 metric**(`oper_rev` / `net_profit` / `waa_roe` 等)走 panel 查询时:

| 市场 | `use_ytd_value` 默认 | 含义 |
|---|---|---|
| CN | **`False`**(单季)| Q1 行 = Q1 单季 / Q2 行 = Q2 单季 / Q3 行 = Q3 单季 / Q4 行 = Q4 单季 |
| HK | **`True`**(累计)| Q1 行 = 3 个月累计 / Q2 行 = 6 个月累计 / Q3 行 = 9 个月累计 / Q4 行 = 12 个月累计 = 全年 |

LLM 路由决策:

- **用户问"全年 / 年报 / 累计营收"** → 必须显式传 `extra.use_ytd_value=true`(CN 必传,HK 默认即是)。否则 CN 拿到 Q4 单季当年报,数字差 ~4 倍。
- **用户问"Q4 单季营收"** → CN 走默认(False)直接拿到;HK 必须显式传 `use_ytd_value=false` + `report_type="Q4"`。
- **单季 metric(`q_*` 前缀)在 `data_type=financial` 下不可用** —— CN 拿单季营收 / 净利润直接用 `oper_rev` / `net_profit` 默认即可。**注意范围**:`q_*` 在 `data_type=indicator` 下**可用**(如 `q_roe_deducted`),caveat 边界**仅限 financial reader**,不要扩到 indicator。
- **`report_type` 参数是 HK-only**:CN reader **不解析**该字段(`Q1`/`Q2`/`Q3`/`Q4` 行由 panel 时间窗 + `use_ytd_value` 决定);HK 必须传以选报告期。

**LLM 路由这类 query 时必须显式声明累计/单季并传对应 `use_ytd_value`,不依赖隐式默认。** 向用户回复时只说"单季营收 / 全年累计营收 / 年报营收"等中文表述,**不**把 `oper_rev` / `q_*` / `use_ytd_value` / `report_type` 等 raw key / 参数名出现在 user-visible response。

## E2E examples

**(a) Happy path — financial Q4 statement items**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"stock","data_type":"financial","symbols":["600519"],"metrics":["oper_rev","net_profit"],"start_date":"2024-01-01","end_date":"2025-12-31","extra":{"report_type":"Q4"}}'
```
Expected: `data[*] = {code, date, report_period, oper_rev, net_profit, avail_date}`. **Note**: `avail_date` is the announcement date (a PIT-critical field), use it to tell the user when a report "became visible".

**(b) PIT daily=true — backtest preflight**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"stock","data_type":"valuation","symbols":["600519"],"start_date":"2025-01-01","end_date":"2025-03-31","extra":{"daily":true}}'
```
Expected: `total_records ~90` (one row per day, weekends included); each row carries the full valuation column set. `pe_ttm / pb_new` reflect the TTM valuation as seen by the market on that trading day.

**(c) Multi-market batch — cn vs hk statement comparison** (Rule 7 multi-market coverage):
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"hk","asset_type":"stock","data_type":"financial","symbols":["00700"],"start_date":"2024-01-01","end_date":"2025-12-31"}'
```

**(d) Upstream-error pass-through — us:stock:financial unavailable**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"us","asset_type":"stock","data_type":"financial","symbols":["AAPL"],"start_date":"2024-01-01","end_date":"2025-12-31"}'
```
Expected: `action=error`, `metadata.warnings` carries the reason. Pass warnings through to the user: suggest falling back to `data_type=market_cap` (the only us option that works) or switching to the `realtime-quote` fundamentals snapshot (if only the current value is needed).

**(e) Bad metric — demonstrating why metric-resolver is mandatory**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"stock","data_type":"indicator","symbols":["600519"],"metrics":["净资产收益率"],"start_date":"2024-01-01","end_date":"2025-12-31"}'
```
Expected: `metadata.warnings` contains `MySqlError ... Unknown column '净资产收益率' in 'field list'`. The skill teaches the LLM: on seeing this error → cross-ref `metric-resolver.md` to resolve "净资产收益率" / "ROE" into a recognized column key (`waa_roe`) and retry; **do not just tell the user "not found"**.

<!-- lint:enable -->

## Response Fields — Key → User-Facing Label

Each `data_type` has its own field set. The `Key` column below is both the **response field name** (what comes back in `data[i]`) and the form to pass into `metrics=[...]`. Cheatsheet hit → take the `Key` directly; miss → fall back to `metric-resolver.md` (per the two-step flow above).

### data_type=financial (quarterly panel)

| Key | EN label | CN label | Note |
|---|---|---|---|
| `oper_rev` | Total Revenue | 营业总收入 | unit: 元 |
| `net_profit` | Net Profit | 净利润 | unit: 元 |
| `net_profit_incl_min_int_inc` | Net Profit Incl. Minority | 净利润含少数股东 | unit: 元 |
| `less_oper_cost` | Operating Cost | 营业成本 | unit: 元 |
| `oper_profit` | Operating Profit | 营业利润 | unit: 元 |
| `tot_profit` | Total Profit | 利润总额 | unit: 元 |
| `tot_assets` | Total Assets | 总资产 | unit: 元 |
| `tot_liab` | Total Liabilities | 总负债 | unit: 元 |
| `tot_equity` | Total Equity | 所有者权益 | unit: 元 |
| `net_cash_flows_oper_act` | Net OCF | 经营活动现金流净额 | unit: 元 |
| `net_cash_flows_inv_act` | Net Investing CF | 投资活动现金流 | unit: 元 |

⚠️ Single-quarter revenue / net profit: do **not** try to pass a single-quarter variant key here — under `data_type=financial` they return `data=[]+error="No data found"`. Use `oper_rev` / `net_profit` + `extra.use_ytd_value=False` (CN default) instead. See b1 caveat above.

### data_type=indicator (quarterly panel)

| Key | EN label | CN label | Note |
|---|---|---|---|
| `waa_roe` | Weighted ROE | 加权平均净资产收益率 | percent |
| `roe_deducted` | Deducted ROE | ROE(扣非) | percent |
| `q_roe_deducted` | Single-Quarter Deducted ROE | 单季 ROE(扣非) | percent |
| `roa` | ROA | ROA | percent |
| `grossprofitmargin` | Gross Margin | 毛利率 | percent |
| `netprofitmargin` | Net Margin | 净利率 | percent |
| `debttoassets` | Debt-to-Assets | 资产负债率 | percent |
| `current` | Current Ratio | 流动比率 | ratio |
| `quick` | Quick Ratio | 速动比率 | ratio |

### data_type=valuation (daily panel — default columns suffice; do not pass `metrics`)

| Key | EN label | CN label | Note |
|---|---|---|---|
| `pe` | PE | 市盈率 | static |
| `pe_ttm` | PE (TTM) | 市盈率(TTM) | trailing-12-month |
| `pb_new` | PB | 市净率 | latest book value |
| `ps` | PS | 市销率 | static |
| `ps_ttm` | PS (TTM) | 市销率(TTM) | trailing-12-month |
| `pcf_ocf` | P/CF (OCF) | 市现率(经营现金流) | |
| `pcf_ocfttm` | P/CF (OCF TTM) | 市现率(经营现金流 TTM) | |
| `total_share` | Total Shares | 总股本 | |
| `float_a_share` | Float A Shares | 流通A股 | |
| `free_share` | Free-Float Shares | 自由流通股本 | |
| `size` | Total Market Cap | 总市值 | unit: 元 |
| `float_size` | Float Market Cap | 流通市值 | unit: 元 |
| `close` | Close Price | 收盘价 | for the trading day |
| `high_52week` | 52-Week High | 52周高 | |
| `low_52week` | 52-Week Low | 52周低 | |
| `net_assets` | Net Assets | 净资产 | unit: 元 |
| `oper_rev_ttm` | Revenue (TTM) | 营收(TTM) | unit: 元 |
| `net_profit_parent_comp_ttm` | Net Profit Parent (TTM) | 归母净利(TTM) | unit: 元 |
| `net_cash_flows_oper_act_ttm` | OCF (TTM) | 经营现金流(TTM) | unit: 元 |

### data_type=market_cap (daily)

| Key | EN label | CN label | Note |
|---|---|---|---|
| `code` | Symbol code | 代码 | |
| `date` | Date | 日期 | YYYY-MM-DD |
| `close` | Close Price | 收盘价 | |
| `share` | Shares | 股本 | `extra.total` controls scope; default `float_a_shares` (not total_shares) |
| `size` | Market Cap | 市值 | unit: 元; size = close × share |

### Common envelope fields (all data_type)

| Key | EN label | CN label | Note |
|---|---|---|---|
| `data[*].code` | Symbol code | 代码 | |
| `data[*].date` | Date | 日期 | |
| `data[*].report_period` | Report Period | 报告期 | financial / indicator only; format YYYY-MM-DD (period end) |
| `data[*].avail_date` | Announcement Date | 公告披露日 | PIT-critical; financial / indicator only |
| `metadata.data_path` | CSV Path | CSV 路径 | triggered when `total_records > inline_threshold` (default 50). CSV not directly fetchable from the runtime — **prefer raising `inline_threshold` (max 1000) on the request** rather than relying on this path. |
| `metadata.warnings` | Warnings | 警告 | upstream errors / truncation; MUST be surfaced to the user |

**Output discipline**: never pass any raw column key (e.g. `oper_rev`, `waa_roe`, `roe_deducted`, `pe_ttm`), pipe-delim symbol (`AAPL|ST|USA`), or source-tagged industry prefix 形如 `<src>-<category>` to user-visible text. For metrics not covered by the tables above, look up the key in `metric-resolver.md` and use its `name` field as the display label. Use readable units (e.g. "Revenue 2.3亿元 (+15% YoY)") rather than raw integers in 元. Agent picks EN or CN label based on the user's language.

## Cross-ref

- User says "analyze / composite / is it healthy / business structure" → `financial-context.md` L1/L2/L3 (one-shot composite, do not chain)
- "Market expectations / consensus / target price" → `consensus-and-target.md`
- User-given metric not in this cheatsheet → `metric-resolver.md` (pull the registry to pick the canonical symbol)
- "What's Moutai's PE now" / "What's Moutai's ROE now" — single value → `realtime-quote.md` with `include_fundamentals=true` (lighter + carries freshness)
- "How much did Moutai gain over the past year / price trend" → `price-history.md`
- "Since when is X's data available / availability" → `market-calendar.md`
