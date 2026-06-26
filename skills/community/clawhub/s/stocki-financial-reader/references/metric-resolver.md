# metric-resolver

## Overview

The stocki gateway's metric registry covers four markets: cn / hk / us / crypto. The HTTP layer **does NOT do fuzzy matching** — the LLM pulls the registry and picks from `name (CN)` / `symbol` / `synomnyms` / `description` itself. This is an intermediate step: once you have the canonical `symbol`, call `/api/v3/datareader/read` with `metrics=[...]`. The registry record count drifts with upstream patches; when you need a sense of scale, hit `kb_meta.record_counts` for the live number — do not freeze counts in the docs.

> ⚠️ The crypto area exposes only OHLCV basics (`open/high/low/close/volume/amount/rtn`) and not financial metrics. For the crypto case, **do not use this skill** — pass the fixed column names directly to datareader/read.

## When to use / When not to use

**Use this skill when**:
- The user mentions a semantic metric name like "ROE / 净资产收益率 / 毛利率 / 营收同比 / EPS / 自由现金流 / 速动比率 / 财务杠杆"
- You know the data_type (fundamentals / indicator / valuation, etc.) but are unsure of the canonical column name

**Do NOT use this skill when**:
- `realtime-quote` with `include_fundamentals=true` already returns a server-prepacked snapshot — use it directly, no resolution needed
- `price-history` uses fixed common columns (`metrics=["close","adj_close","open","high","low","volume"]`) — pass them directly
- `fundamentals-panel` / `consensus-and-target` ship their own high-frequency cheatsheets (~30 metrics). If your metric is on the cheatsheet, take the canonical name directly; **only on miss** do you fall back to this skill
- `market-calendar` / `industry-and-symbols` / `financial-context` do not accept a `metrics` parameter

## Endpoint

| Method | Path | Purpose |
|---|---|---|
| POST | `$STOCKI_GATEWAY_URL/api/v2/market_metric/get_metrics` | Pull the metric registry (filter by area / asset_type / kind) |

<!-- This file IS the canonical metric mapping source; canonical names below are intentional and request-side only, not user-visible output. -->
<!-- lint:disable rule=canonical-metric -->
## Input schema

```json
{
  "area": "cn",
  "asset_type": "stock",
  "kind": "profitability_and_earnings_quality",
  "limit": 50,
  "offset": 0
}
```

| Field | Required | Description |
|---|---|---|
| `area` | no | `cn / hk / us / crypto`; omitted = all. **crypto is OHLCV only; do not use this skill for crypto.** |
| `asset_type` | no | `stock` (cn/hk/us) / `crypto` (crypto area) |
| `kind` | no | category filter; 13 kinds listed below |
| `limit` / `offset` | no | pagination |

**13 `kind` values**: `balance_sheet`, `income_statement`, `cashflow_statement`, `valuation_multiples`, `profitability_and_earnings_quality`, `growth`, `solvency`, `per_share_metrics`, `capital_structure`, `market_data`, `cash_flow`, `operating_efficiency`, `capitalization`.

**User semantics → recommended `kind` filter** (narrows the scan):
- "营收 / 利润 / 成本 / 三表科目" / "revenue / profit / cost / statement items" → `kind=income_statement` or `cashflow_statement` or `balance_sheet`
- "ROE / ROA / 利润率 / 周转率" / "ROE / ROA / margin / turnover" → `kind=profitability_and_earnings_quality`
- "PE / PB / PS / EV/EBITDA" → `kind=valuation_multiples`
- "营收同比 / 利润增速 / 同比" / "YoY revenue / profit growth" → `kind=growth`
- "速动比率 / 资产负债率 / 利息保障" / "quick ratio / debt-to-assets / interest coverage" → `kind=solvency`
- "EPS / 每股净资产 / 每股现金流" / "EPS / book value per share / cashflow per share" → `kind=per_share_metrics`
- "市值 / 流通股 / 总股本" / "market cap / float shares / total shares" → `kind=capitalization`

## E2E examples

**(a) User asks for "ROE" → look under profitability**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v2/market_metric/get_metrics" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"stock","kind":"profitability_and_earnings_quality"}'
```
The LLM scans `response.data` for records whose `name` contains "ROE" / "净资产收益率". Candidates: `waa_roe` (加权平均净资产收益率) / `roe_deducted` (扣非) / `q_roe_deducted` (单季扣非) / `yoyroe` (同比增长率). A bare "ROE" usually means `waa_roe` (the most common one); only switch if the user explicitly says "扣非 / 单季 / 同比" or the English equivalent.

**(b) User asks for "营业收入" → look under income_statement**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v2/market_metric/get_metrics" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"stock","kind":"income_statement","limit":20}'
```
Scan `name` for "营业收入" / "revenue" → `oper_rev` (营业总收入). Default to `oper_rev`. For CN 单季营收 use `oper_rev` + `extra.use_ytd_value=False` (CN 默认即是); see `fundamentals-panel.md` b1 caveat.

**(c) HK metric — user asks for "派息率" / dividend payout**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v2/market_metric/get_metrics" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"hk","asset_type":"stock"}'
```
Locally grep `name` / `description` / `synomnyms` for "派息" / "dividend".

## Response Fields — Raw → User-Facing Label

Each record carries 18 fields:
- `symbol` — **mapped short name** (lowercase, e.g. `oper_rev` / `waa_roe` / `roe_deducted` / `q_eps`). This is what you put into `metrics=[...]` on `/api/v3/datareader/read`.
- `name` — CN display name (the primary battleground for user-semantic matching)
- `area` / `asset_type` / `kind` — classification
- `period` — `daily / quarter / yearly` — determines how `extra.report_type` is filled at query time
- `table` — underlying data-layer identifier with entity-type suffix (形如 `*Income` / `*Valuation` / `*CashFlow` / `*Indicator` 等);按后缀模式 imply `data_type` routing(`*Income` → financial, `*Valuation` → valuation, etc.)
- `unit / displayUnit` — unit (万元 / % / 元)
- `synomnyms` — synonyms (mostly empty, but a hit catches colloquial names)
- `description` — English gloss
- `is_derived` — whether the metric is derived
- `v3_alias` — v3 alias (mostly null)

If `response.kb_meta.source_drift` is non-empty, surface a note to the user: "the registry is out of sync with the underlying source; results may be stale".

## Selection logic (how the LLM should pick)

1. **Prefer exact `name` match** (the user's phrase appears literally in the record's `name`)
2. **Next: `description` / `synomnyms` contains** the user's phrase or a near-synonym
3. **Multiple candidates → pick by time granularity**:
   - "latest / TTM" → choose `period=daily` or a `name` containing "TTM"
   - "quarterly / single-quarter" → choose `name` containing "单季" or `symbol` starting with `q_`
   - "annual / full year" → choose `name` containing "全年" or the unmodified main variant

**单季前缀适用域边界**:`q_*` 系列(mapped 短名前缀)仅在 `data_type=indicator` 下可用(如 `q_roe_deducted` / `q_eps`,2026-05-13 实测可拉数据);`data_type=financial` 不接受任何单季 metric 直接传入——CN 单季营收 / 净利润直接用 `oper_rev` / `net_profit` + `extra.use_ytd_value=False`(CN 默认即是);参见 `fundamentals-panel.md` b1 caveat。

4. **Special qualifiers**:
   - "扣非" / "deducted" → `name` contains "扣除非经常" or `symbol` contains `_deducted`
   - "稀释" / "diluted" → `name` contains "稀释" or `symbol` contains `_diluted`
   - "母公司 / 归母" / "parent company" → `name` contains "归属于母公司"

**c1: EPS 默认选 Basic,显式说 diluted 才换**(cn/hk 一致):

| 市场 | BASIC | DILUTED | 单季 EPS |
|---|---|---|---|
| CN | `eps_basic` | `eps_diluted`(+ `eps_diluted2` 期末摊薄)| `q_eps` |
| HK | `eps_basic` | `eps_diluted`(+ `eps_diluted2` / `eps_diluted3` 期末摊薄变体)| **无**(hk registry 不提供单季 EPS,L2 已锁) |

规则:

- 用户说 "EPS / 每股收益":**cn/hk 一律默认 BASIC**(`eps_basic`)
- 用户明说 "稀释 / diluted / 摊薄":用 DILUTED 主变体(`eps_diluted`);若用户说"期末摊薄"再换 `eps_diluted2` 变体
- 用户说 "单季 EPS":cn 用 `q_eps`;**hk 需 fail-loud**:告知用户"hk 不提供单季 EPS,请确认是否要全年 BASIC"——**不要静默 fallback 到全年 BASIC 当作单季返回**

**不要猜**:有歧义时按本表退而向用户列 2 个候选(`BASIC` vs `DILUTED`),让用户确认;不假设"BASIC 总是对的"。

5. If you cannot narrow to a unique answer → list 2-3 candidates for the user to confirm. **Do not guess.**

<!-- lint:enable -->

## Output discipline (this skill IS the mapping source)

This skill's core output IS the raw → user-facing mapping table; downstream skills apply the output discipline based on what this skill returns.

- **`symbol` field — the mapped short name** (e.g. `oper_rev` / `waa_roe` / `roe_deducted`). Used ONLY as a downstream `metrics=[...]` request parameter for `/api/v3/datareader/read`; **never enters user replies**.
- **`name` field (CN-friendly display name)** — this is the label to show to the user
- When presenting multiple candidates, surface `name + description`; **do not let the user see `symbol`** (except in debug or when the user explicitly asks for the canonical column name)
- The `table` field in each record carries an underlying data-layer identifier (entity-type suffix pattern like `*Income` / `*Valuation`) — this is a debug field, **never shown to the user**
- Downstream skills (`fundamentals-panel`, `consensus-and-target`, future `stock-screening` / `backtest`) consistently surface `name` rather than `symbol` to the user

## Cross-ref

- Once resolved, take the canonical symbol → `fundamentals-panel.md` (financial / indicator / valuation / market_cap data_type)
- Consensus-related fields (`con_or` / `con_np` / `con_eps`) are already canonical → no resolution needed; go straight to `consensus-and-target.md`
- Valuation snapshot (current PE/PB/ROE) → `realtime-quote.md` with `include_fundamentals=true`; do not use this skill
- Sector / company-name resolution ("茅台" → `600519`) → **OUT-OF-SCOPE** (this batch of skills assumes the user supplies a symbol; asset resolution would require `match_asset` which the HTTP layer does not expose — fall back to `/api/v2/market_symbol/get_symbols` and pick manually)
