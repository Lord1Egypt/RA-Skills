# financial-context

## Overview

Stocki gateway one-shot composite view: a single call returns 11 sections (`meta` / `valuation` with 5y percentiles / `income` / `balance_sheet` / `cashflow` / `indicator` / `consensus` / `segments` / `field_descriptions` / `_source_map` / `history`). `layer` ∈ {1, 2, 3} controls depth. **The `metrics` parameter is NOT accepted** — the column set is decided server-side.

## Trigger Vocabulary

- 中文："分析一下 / 综合分析 / 看下基本面 / X 贵不贵 / X 财务健康 / 业务结构 / 哪条业务增长最快 / 主营拆解 / 销售涨利润跌为什么 / 多角度 / 一键 / 深度追因 / 5 年分位 / 历史分位"
- English: "analyze X / fundamentals overview / financial context / valuation percentile / business segments / why revenue up profit down"
- Boundaries:
  - Single-field time series ("PE history / revenue over 8 quarters") → `fundamentals-panel.md`
  - Sell-side estimates / target price only (no financial cross-check) → `consensus-and-target.md`
  - Realtime price + current PE only → `realtime-quote.md`
  - Company industry / sector / listing date → `industry-and-symbols.md`
  - **L1 already answers "analyze Moutai" — DO NOT instinctively jump to `fundamentals-panel.md` and chain multiple calls.**

## Endpoint

| Method | Path | Purpose |
|---|---|---|
| POST | `$STOCKI_GATEWAY_URL/api/v3/financial_context/cn` | A-share composite single-stock view |
| POST | `$STOCKI_GATEWAY_URL/api/v3/financial_context/hk` | HK composite single-stock view |

## Input schema

```json
{
  "symbol": "600519",
  "layer": 1,
  "current_date": "2026-05-08",
  "pit": false
}
```

| Field | Required | Description |
|---|---|---|
| `symbol` | yes | bare code ("600519" / "00700"), no exchange suffix |
| `layer` | yes | `1 / 2 / 3`, depth (see table below) |
| `current_date` | no | YYYY-MM-DD, PIT cutoff; omitted = server uses today (server tz) |
| `pit` | no | true = segments strictly filtered by `ann_dt <= current_date`; default false (friendlier for realtime analysis) |

⚠️ **Do NOT pass `inline_threshold` to this endpoint.** `/api/v3/financial_context/{cn,hk}` returns a composite dict (`valuation` / `income` / `balance_sheet` / `cashflow` / `indicator` / `consensus` / `segments` / `field_descriptions` / ...), not a paginated `data` list — the parameter is silently ignored. `inline_threshold` only applies to `/api/v3/datareader/read` (see SKILL.md §Inline Threshold).

## Layer differences

| Layer | Segments detail | Consensus records | Suitable for |
|---|---|---|---|
| 1 | stub (only `available_at_layer=2` + `dimensions[]`) | ≤ 2 (current_fy + next_fy) | "analyze Moutai / is Moutai expensive" generic composite view |
| 2 | 9-field records + `by_dimension` grouping | ≤ 3 | "Moutai business structure / which segment is growing fastest" |
| 3 | 16-field records (cost / profit / yoy cross-validation) | **132+ records, full time series** | "Why is Moutai revenue up but profit down / consensus revision trajectory" |

⚠️ **L3 already contains the complete consensus time series — do not call `consensus-and-target.md` again.**

## E2E examples

**(a) L1 composite analysis — "analyze Moutai"**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/financial_context/cn" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"symbol":"600519","layer":1}'
```
Expected: 11 sections. Key fields:
- `meta.{symbol, name, area, report_period, report_date, query_date, data_freshness}`
- `valuation` with 5y percentiles (后缀 `percentile_5y` 的字段;实际字段名以响应为准) — use this when the user asks "is it expensive"
- `income / balance_sheet / cashflow / indicator` are each a dict containing the latest report-period values + YoY + QoQ

**(b) L2 business structure — "which Moutai segment grows fastest"**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/financial_context/cn" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"symbol":"600519","layer":2}'
```
Expected: `segments.data` ≥ 5 records (one per segment), each with 9 fields (`ann_dt, currency, segment, segment_type, sales, sales_percentage, sales_yoy, profit_percentage, gross_profit_margin`) + `segments.by_dimension` containing `channel / product / region / industry` groups.

**(c) L3 consensus time series — "in the last 3 months have analysts revised Moutai up or down"**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/financial_context/cn" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"symbol":"600519","layer":3}'
```
Expected: `consensus` ≥ 100 records (ascending by date) + `segments.data` with the richer 16-field shape. **Do NOT additionally call `consensus-and-target.md`.**

**(d) Multi-market — hk Tencent**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/financial_context/hk" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"symbol":"00700","layer":1}'
```
Expected: action=success, `meta` contains `name_eng` "TENCENT". Note: when hk `data_freshness.indicator_is_fallback=true`, indicator data used the previous-period fallback — surface to the user as "indicators are one period behind financials".

**(e) Upstream error pass-through — symbol does not exist**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/financial_context/cn" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"symbol":"999999","layer":1}'
```
Expected: HTTP **200** + `{"action":"error","error":"...","symbol":"...","suggestion":"..."}`(此 endpoint 用 envelope 而非 HTTP status 表达错误)。**判错按 `action == "error"`,不要按 status code**。skill 把 `error` 和 `suggestion` 透传给用户,并建议先用 `industry-and-symbols.md` `get_symbols` 确认 symbol 存在。

## Response Shape

Single JSON object. 11 stable top-level sections (cn/hk × L1/L2/L3 全部 6 组合实测齐全):

| Section | Semantics |
|---|---|
| `meta` | 元信息:symbol / name / area / report_period / `data_freshness.*` (PIT critical,含 `indicator_is_fallback` flag) |
| `valuation` | 估值:当期 PE/PB/PS/PCF + 5y 分位(`valuation` 段里 key 后缀含 `percentile_5y` 的字段即是);字段集随市场/股票浮动 |
| `income` / `balance_sheet` / `cashflow` | 三表(最新报告期)dict + YoY + QoQ |
| `indicator` | 财务指标(ROE / margins / turnover 等);可能 fallback 到上一期(看 `meta.data_freshness.indicator_is_fallback`) |
| `consensus` | 一致预期:L1 ≤2 records (current_fy + next_fy) / L2 ≤3 / L3 ≥100 (full time series, ascending by date) |
| `segments` | 业务分部:**cn 为 dict** (L1 stub 仅 `available_at_layer=2` + `dimensions[]`; L2 9-field records + `by_dimension` 按 `channel/product/region/industry` 分组; L3 16-field 加 cost/profit/cost_yoy 等);**hk 始终为 null**(L1/L2/L3 均无) |
| `field_descriptions` | **CN 标签权威源**:dict 形式 raw key → 中文 gloss;len 随 layer 增长(cn ~43/127/212, hk ~34/114/193) |
| `_source_map` | **debug only, NEVER 给用户**:内部 routing metadata,无 user-facing 契约,格式随版本可能变 |
| `history` | 预留, 当前未使用 |

### Field 解读纪律

具体字段名随**市场 / 股票 / layer / 报告期**浮动:实测 cn `valuation.dividend_yield` 有 hk 同位置无;hk 银行 `valuation` 多 `float_share / net_assets / turnover / oper_rev_ttm` 等扩展字段。**不要按硬编码字段清单消费**:

- **CN 标签源**:取 `field_descriptions[raw_key]`,缺时按英文 raw key 含义意译,不直接吐 raw key
- **5y 分位**:`valuation` 段里 key 含 `percentile_5y` 后缀的字段即是;不假定固定前缀
- **缺字段**:不假装存在,告诉用户该期无此项
- **路由判断**:看 section 是否存在 / 是否空,不看具体字段名

### 已知陷阱(必须主动告知用户)

**HK 无 currency 信号(数据缺口必须主动告知)** —— hk `income / balance_sheet / cashflow / valuation` 各 dict **无 `currency` 字段**;且 hk `segments` 字段**始终为 `null`**(layer 1/2/3 均测过——不同于 cn 端 layer ≥ 2 segments.data 实存且带 currency=CNY)。**HK 端没有任何 currency 信号可取**——LLM 必须按公司归属 / 股票类型推断币种:

- H 股内地公司(如腾讯 00700、中广核电力 01816)按 IFRS 用 **RMB** 报表
- 本港公司(如汇丰 00005)用 **HKD**
- 跨上市公司(如东方海外 00316)可能用 **USD**

**展示数值时必须标注币种**;若不确定,显式告知用户"币种基于公司归属推断,请核对最新年报披露",**不要默认 HKD**——默认 HKD 给 H 股内地公司会出大错(RMB 与 HKD 相差近 10% + 长期趋势)。

**Segments YoY 口径陷阱(数据缺口必须主动告知)** —— `segments.data[*].sales_yoy` 在公司**并购 / 分拆 / 业务线重组**的当期可能产生**非业务原因**的数字断层。当 `|sales_yoy|` 异常(如 > 200% 或 < -50%)或某 segment 名前期有当期无 / 前期无当期有,展示给用户时**必须主动提示** "该 segment 同比可能因口径变化(并购 / 分拆 / 重组),请核对当期公告",**不要直接解读为业务剧变**。数据层无法自动识别"是否口径变化"——只能识别"数字异常 / segment 名变更"作为触发信号。最终解读需用户自行核对公告;LLM 的职责是 surface 触发信号,**不**默认按业务逻辑下结论。

**Indicator fallback** —— `meta.data_freshness.indicator_is_fallback=true`(hk 常见)表示指标用了上一期 fallback。主动告知用户"指标数据较财报落后一期"。

### Routing & 5y-window 约束

**5y 窗口排他性**:本 endpoint 仅暴露固定 5 年分位字段(`valuation` 段 `percentile_5y` 后缀)。**不**计算任意窗口分位。用户问 3y / 10y / 自定义窗口 → fall back to `fundamentals-panel.md` 拉 `data_type=valuation` 原始日频序列 client-side 计算,并明确告知用户"基于原始序列估算"。

**Routing discipline**:L1 已经能回答 generic "analyze X" / "is X expensive" / "X fundamentals" prompts。**不要**习惯性 chain `fundamentals-panel.md` 多 endpoint 回答这类问题。

### Output Discipline(endpoint 特异)

总纪律见 SKILL.md `## Output Discipline`。fin-context 额外:

- `_source_map` / `_source` / 任何下划线开头字段 —— debug only,内部 routing metadata,无 user-facing 契约且格式随版本可能变,**绝不**进用户文本
- segment 文本带形如 `<src>-<category>` 的来源前缀 —— 剥掉前缀再展示(同 `industry-and-symbols.md`)
- CN 标签源:优先 `field_descriptions[raw_key]`,无对应时按 raw key 英文含义意译,不直接吐 raw key
- 顶级 section 名 CN 速查:`meta` → 元信息;`valuation` → 估值;`income` → 利润表;`balance_sheet` → 资产负债表;`cashflow` → 现金流量表;`indicator` → 财务指标;`consensus` → 一致预期;`segments` → 业务分部;`field_descriptions` → 字段说明;`_source_map` → 数据源映射(debug);`history` → 历史

## Cross-ref

- Single-stock price trajectory → `price-history.md`
- Single-field time series (PE history / ROE 4-quarter trend) → `fundamentals-panel.md`
- Full consensus time series → use this skill's **L3**, not `consensus-and-target.md` (avoid duplicate calls)
- Realtime price + current PE → `realtime-quote.md`
- Industry mapping / company profile → `industry-and-symbols.md`
- us single-stock returns HTTP 404 on v3 (no payload). Route through `market-calendar.md` `/availability` to check liveness before calling.
