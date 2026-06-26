# consensus-and-target

## Overview

Packages 3 related data_types: (A) `consensus_forecast` — sell-side consensus estimates; (B) `target_price` — broker-merged target price; (C) `revenue_breakdown` — primary-business segment composition. All go through `/api/v3/datareader/read`, covered only for `cn:stock`. Default columns are sufficient (no need to route through metric-resolver).

## Trigger Vocabulary

- 中文："市场对 X 预期 / 卖方预期 / 一致预期 / 隐含 PE / 隐含 PB / 分析师上调 / 下调 / 业绩预测 / 目标价 / 券商目标价 / 主营业务 / 业务分部 / 分产品 / 分地区 / 分渠道 / 营收构成 / 占比"
- English: "consensus forecast / sell-side estimate / target price / implied PE / implied valuation / segment / revenue breakdown / by product / by region"
- Boundaries:
  - Historical realised financials ("revenue of the past 4 quarters") → `fundamentals-panel.md`
  - One-shot composite "give me an overview of Moutai" → `financial-context.md` L1 (includes a lite consensus block)
  - Need the full 9–16 field segments + by_dimension grouping for business structure → `financial-context.md` L2/L3 (**avoid calling this skill plus financial-context twice**)
  - "What is PE right now / PE time series" → `fundamentals-panel.md` (valuation)

## Endpoint

| Method | Path | data_type | Purpose |
|---|---|---|---|
| POST | `$STOCKI_GATEWAY_URL/api/v3/datareader/read` | `consensus_forecast` | Sell-side consensus, multi con_year × multi date snapshots |
| POST | `$STOCKI_GATEWAY_URL/api/v3/datareader/read` | `target_price` | Broker-merged target-price time series |
| POST | `$STOCKI_GATEWAY_URL/api/v3/datareader/read` | `revenue_breakdown` | Primary-business segments (by channel / product / region dimension) |

## Input schema

### A. consensus_forecast

```json
{
  "area": "cn",
  "asset_type": "stock",
  "data_type": "consensus_forecast",
  "symbols": ["600519"],
  "start_date": "2026-01-01",
  "end_date": "2026-04-30",
  "extra": {"con_years": [2026, 2027]}
}
```

| Field | Required | Description |
|---|---|---|
| `start_date / end_date` | yes | Snapshot date range; server defaults to a 90-day lookback cap (observed: omitting still works, but the behaviour is undocumented) |
| `extra.con_years` | no | list[int]; pull multiple con_years in one call; omit = all fiscal years with data |
| `inline_threshold` | no | int, range `[1, 1000]`, default 50 (silently clamped). Pass when expected `total_records > 50` to avoid truncation; consensus is sparse — estimate `N = symbols × posted_days_in_window` and set `min(ceil(N × 1.5), 1000)`. **Full decision rule: SKILL.md §Inline Threshold.** |

Multiple `date` snapshots = consensus-revision trajectory (track `con_eps / con_np_yoy` evolution for the same con_year).

### B. target_price

```json
{
  "area": "cn",
  "asset_type": "stock",
  "data_type": "target_price",
  "symbols": ["600519"],
  "start_date": "2026-01-01",
  "end_date": "2026-04-30"
}
```

Returns only the merged `con_target_price`. Use multiple dates to see upgrades / downgrades.

### C. revenue_breakdown

```json
{
  "area": "cn",
  "asset_type": "stock",
  "data_type": "revenue_breakdown",
  "symbols": ["600519"],
  "start_date": "2024-01-01",
  "end_date": "2025-01-01",
  "extra": {"report_periods": ["20241231"]}
}
```

⚠️ **`extra.report_periods` is required** (list[str] YYYYMMDD; sourced from `dataLoader_v2/estimate/revenue_breakdown.py` "REQUIRED").
⚠️ **`start_date / end_date` are also required** (verified 2026-05-08: the old spec said "ignored" — formally they do not participate in time filtering, but omitting them still triggers a NaTType crash. Pass placeholders, e.g. start = 1 Jan of the earliest report_periods year / end = 1 Jan of the year after the latest report_periods; see notes §11).
⚠️ **`metrics` is also ignored** (safer to omit; passing any metric does not filter columns — the response is always 17 columns).

Typical cross-year / cross-half-year `report_periods`: `["20231231","20240630","20241231"]`; supply multiple year-ends to inspect annual trends.

## E2E examples

**(a) consensus_forecast — single stock latest consensus**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"stock","data_type":"consensus_forecast","symbols":["600519"],"start_date":"2026-04-01","end_date":"2026-04-30","extra":{"con_years":[2026]}}'
```
Expected: `data[*] = {code, date, stock_name, con_year, con_or, con_np, con_eps, con_pe, con_pb, con_peg, con_roe, con_or_yoy, con_np_yoy}`. **Units**: `con_or / con_np` in 万元 (ten-thousand yuan); `con_pe / con_pb / con_peg / con_roe` dimensionless; `con_or_yoy / con_np_yoy` percent.

**(b) Revision trajectory — multi-date snapshots tracking consensus evolution**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"stock","data_type":"consensus_forecast","symbols":["600519"],"start_date":"2026-01-01","end_date":"2026-04-30","extra":{"con_years":[2026]}}'
```
Take `con_eps / con_np_yoy` at each date; the time-series change = analyst upgrade / downgrade trajectory. Note: the server defaults to a 90-day lookback, longer ranges get truncated.

**(c) target_price — target-price time series**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"stock","data_type":"target_price","symbols":["600519"],"start_date":"2026-01-01","end_date":"2026-04-30"}'
```
Expected: `data[*] = {code, date, stock_name, con_target_price}` (unit: yuan). Compare against current close → implied upside.

**(d) revenue_breakdown — primary-business segments**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"stock","data_type":"revenue_breakdown","symbols":["600519"],"start_date":"2024-01-01","end_date":"2025-01-01","extra":{"report_periods":["20241231"]}}'
```
Expected: `data[*]` with 17 fields: `code / date / ann_dt / currency / segment / segment_type / segment_itemcode / sales / sales_percentage / sales_yoy / profit / profit_percentage / profit_yoy / cost / cost_percentage / cost_yoy / gross_profit_margin / gross_profit_margin_yoy`. `segment_type` ∈ `channel / product / region / industry`; to group by dimension, client-side group-by `segment_type`. `ann_dt` is the announcement disclosure date (PIT-critical).

**(e) Upstream error pass-through — revenue_breakdown missing report_periods**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"stock","data_type":"revenue_breakdown","symbols":["600519"],"start_date":"2024-01-01","end_date":"2025-01-01"}'
```
Expected: `action=error`; the skill teaches the LLM that on seeing this error it should automatically retry once with `extra.report_periods` added (typically the most recent 4 annual / semi-annual reports, e.g. `["20231231","20240630","20241231"]`), and only surface the error to the user if the retry still fails.

## Response Fields — Raw → User-Facing Label

### data_type=consensus_forecast (consensus across analysts)

| Raw key | EN label | CN label | Note |
|---|---|---|---|
| `data[*].code` | Symbol code | 代码 | |
| `data[*].date` | Snapshot date | 快照日期 | |
| `data[*].stock_name` | Stock name | 股票名称 | |
| `data[*].con_year` | Forecast year | 预测财年 | int |
| `data[*].con_or` | Consensus Revenue | 一致预期营收 | unit: 万元 |
| `data[*].con_np` | Consensus Net Profit | 一致预期净利润 | unit: 万元 |
| `data[*].con_eps` | Consensus EPS | 一致预期 EPS | unit: 元 |
| `data[*].con_pe` | Consensus PE | 一致 PE | implied; dimensionless |
| `data[*].con_pb` | Consensus PB | 一致 PB | implied; dimensionless |
| `data[*].con_peg` | Consensus PEG | 一致 PEG | implied; dimensionless |
| `data[*].con_roe` | Consensus ROE | 一致 ROE | percent |
| `data[*].con_or_yoy` | Revenue YoY (consensus) | 营收同比预期 | percent |
| `data[*].con_np_yoy` | Net Profit YoY (consensus) | 净利同比预期 | percent |

### data_type=target_price (merged sell-side target)

| Raw key | EN label | CN label | Note |
|---|---|---|---|
| `data[*].code` | Symbol code | 代码 | |
| `data[*].date` | Snapshot date | 快照日期 | |
| `data[*].stock_name` | Stock name | 股票名称 | |
| `data[*].con_target_price` | Consensus Target Price | 一致目标价 | unit: 元; compare to current close for implied upside/downside |

### data_type=revenue_breakdown (segment composition)

| Raw key | EN label | CN label | Note |
|---|---|---|---|
| `data[*].code` | Symbol code | 代码 | |
| `data[*].date` | Date | 日期 | |
| `data[*].ann_dt` | Announcement Date | 公告披露日 | PIT-critical |
| `data[*].currency` | Currency | 币种 | |
| `data[*].segment` | Segment name | 分部名称 | strip 形如 `<src>-<category>` 的来源前缀 if present |
| `data[*].segment_type` | Segment type | 分部维度 | enum: channel / product / region / industry |
| `data[*].segment_itemcode` | Segment item code | 分部代码 | |
| `data[*].sales` | Sales | 销售额 | unit: 元 |
| `data[*].sales_percentage` | Sales share | 销售占比 | percent |
| `data[*].sales_yoy` | Sales YoY | 销售同比 | percent |
| `data[*].profit` | Profit | 利润 | unit: 元 |
| `data[*].profit_percentage` | Profit share | 利润占比 | percent |
| `data[*].profit_yoy` | Profit YoY | 利润同比 | percent |
| `data[*].cost` | Cost | 成本 | unit: 元 |
| `data[*].cost_percentage` | Cost share | 成本占比 | percent |
| `data[*].cost_yoy` | Cost YoY | 成本同比 | percent |
| `data[*].gross_profit_margin` | Gross Margin | 毛利率 | percent |
| `data[*].gross_profit_margin_yoy` | Gross Margin YoY | 毛利率同比 | percentage points |

### Common envelope

| Raw key | EN label | CN label | Note |
|---|---|---|---|
| `metadata.data_path` | CSV Path | CSV 路径 | triggered when `total_records > inline_threshold` (default 50). CSV not directly fetchable from the runtime — **prefer raising `inline_threshold` (max 1000) on the request** rather than relying on this path. |
| `metadata.warnings` | Warnings | 警告 | upstream errors / truncation; MUST be surfaced to the user |

**Target-price presentation discipline**: when comparing `con_target_price` to current close, surface "implied upside +X%" / "implied downside −X%" prose rather than echoing the raw field name.

**Segment-prefix discipline**: if `segment` values carry 形如 `<src>-<category>` 的来源前缀, strip the prefix before showing to the user (same rule as `industry-and-symbols.md`).

**Output discipline**: never pass raw key (`con_or`, `con_target_price`, `segment_type`, pipe-delim symbol like `AAPL|ST|USA`, source-tagged industry prefix 形如 `<src>-<category>`) to user-visible text. Agent picks EN or CN label based on the user's language.

## Cross-ref

- Composite + L2 segments + L3 full consensus 138-record time series → `financial-context.md` (avoid calling this skill plus financial-context twice)
- Historical three-statement financials / valuation / metrics → `fundamentals-panel.md`
- Company industry / sector mapping → `industry-and-symbols.md`
- Current PE realtime value → `realtime-quote.md` `include_fundamentals=true`
