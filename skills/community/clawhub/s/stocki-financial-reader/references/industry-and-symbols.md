# industry-and-symbols

## Overview

Three query categories bundled together: (A) industry / SW classification (datareader/read `industry`); (B) index constituents (datareader/read `index_member`); (C) registry + company briefing (`market_symbol/get_symbols`). All responses are pass-through — do not post-process on the client side.

## Trigger Vocabulary

- 中文："茅台是什么行业 / 食品饮料板块 / 申万分类 / 沪深 300 成分 / 中证 500 都有哪些 / 茅台公司简介 / 注册地 / 股本变动 / 流通 A 股 / 解禁 / 上市日期"
- English: "industry of X / sector / SW classification / CSI300 constituents / company briefing / registration / shareholding change / IPO date / list date"
- Boundaries:
  - "白酒板块都有哪些 / AI 概念股都有哪些 / 沪深300 成分股" (sector / concept / index **name** → symbol list) → **走 `references/name-resolver.md` §B + §C 双步**: §B 把 NL collection 名 resolve 成 `collection.symbol`,§C `get_symbols_from_collection` 把 collection symbol 反查成股票列表。返回结果按本 reference 的 Response 纪律展示给用户(bare code + 中文名,不带 pipe-delim)。
  - "PE 最低 20 只 / ROE > 15%" → the stock-screening skill is **not yet delivered** (upstream limitation; tracked separately). Tell the user this capability is temporarily unavailable.
  - "茅台一键综合分析" → `financial-context.md`

## Endpoint

| Method | Path | Purpose |
|---|---|---|
| POST | `$STOCKI_GATEWAY_URL/api/v3/datareader/read` | `data_type=industry` — industry membership (trading-day time series) |
| POST | `$STOCKI_GATEWAY_URL/api/v3/datareader/read` | `data_type=share` — share structure (by change event) |
| POST | `$STOCKI_GATEWAY_URL/api/v3/datareader/read` | `data_type=index_member` — index constituents (trading-day time series) |
| POST | `$STOCKI_GATEWAY_URL/api/v2/market_symbol/get_symbols` | Registry + company briefing |

Availability matrix (measured 2026-05-08; re-check with `market-calendar.md` `/availability` before assuming a change):
- `cn/hk/us:stock × industry`
- `cn/hk:stock × share`
- `cn/hk:index × index_member`

## Input schema

### A. industry / share / index_member (datareader/read)

```json
{
  "area": "cn",
  "asset_type": "stock",
  "data_type": "industry",
  "symbols": ["600519"],
  "start_date": "2024-01-01",
  "end_date": "2026-05-08"
}
```

⚠️ **`start_date` + `end_date` are required** (upstream bug: missing dates return `"Internal error: NaTType does not support strftime"` with `suggestion=null`. The skill forces all 4 fields to be passed.)

- `industry` returns the industry tag per trading day (the label can change across years). For "current industry" → `end_date` = latest trading day, take the last record.
- `share` returns share-structure **change events** (not a daily panel). NA fills are normal.
- `index_member` is a **panel time-series** (one record per constituent per day). CSI 300 over one year ≈ 73K records → **far exceeds `inline_threshold` max 1000, must narrow query**. For "current constituents" only → `start_date` = `end_date` = latest trading day, set `inline_threshold = 400` (300 × 1.33 margin) → `len(data) == total_records == ~300` inline, no truncation. Longer ranges → narrow further or fail-loud per SKILL.md §Inline Threshold.
- `index_member` symbols must carry the exchange suffix (`"000300.SH"` / `"399006.SZ"` / `"HSI.HI"`).

⚠️ **inline_threshold (same body param as price/fundamental)**: pass when expected `total_records > 50` to avoid 50-row truncation. `index_member` single-day on ~300-stock indices (CSI 300 / HSI) → `inline_threshold = 400`; `industry` / `share` single-symbol queries are typically <50 rows so the default suffices. **Full decision rule: SKILL.md §Inline Threshold.**

### B. get_symbols

```json
{"area": "cn", "asset_type": "stock", "symbols": ["600519"], "detail": true}
```

| Field | Required | Description |
|---|---|---|
| `area / asset_type / symbols` | yes | bare code (no exchange suffix) |
| `detail` | no | when true, returns ~20 fields (CN) / ~47 fields (HK, including a longer briefing) |
| `for_match` | no | when true, returns match-friendly shape (used by symbol_resolver; skip in normal scenarios) |
| `list_since` | no | filter by list date (YYYY-MM-DD) |

## E2E examples

**(a) industry — cn single stock**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"stock","data_type":"industry","symbols":["600519"],"start_date":"2024-01-01","end_date":"2026-05-08"}'
```
Expected: `data[*] = {code, date, industry}`; the last record's `industry` = "食品饮料".

**(b) Multi-market batch — hk industry**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"hk","asset_type":"stock","data_type":"industry","symbols":["00700"],"start_date":"2024-01-01","end_date":"2026-05-08"}'
```

**(c) index_member — CSI 300 current constituents**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"index","data_type":"index_member","symbols":["000300.SH"],"start_date":"2026-05-07","end_date":"2026-05-07","inline_threshold":400}'
```
Expected: `data[*] = {code, date, index_code}`; `total_records ~300` and `len(data) == total_records` (no truncation because `inline_threshold = 400 ≥ 300`). **Survivorship bias**: the response only contains currently-listed constituents — it does NOT carry the historical add/drop trail.

**(d) get_symbols detail — company briefing**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v2/market_symbol/get_symbols" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"stock","symbols":["600519"],"detail":true}'
```
Expected: `data[0]` contains `name / comp_name / comp_name_eng / list_date / list_board / exch_market / briefing` (CN ~20 fields).

**(e) Upstream error pass-through — missing dates**:
```bash
curl -X POST "$STOCKI_GATEWAY_URL/api/v3/datareader/read" \
  -H "Authorization: Bearer $STOCKI_API_KEY" -H "Content-Type: application/json" \
  -d '{"area":"cn","asset_type":"stock","data_type":"industry","symbols":["600519"]}'
```
Expected: `{"action":"error","error":"Internal error: NaTType...","suggestion":null}`. The skill teaches the LLM: on this error, auto-retry once with a date range filled in; only surface to the user if it still fails.

## Response Fields — Raw → User-Facing Label

### data_type=industry (industry classification time series)

| Raw key | EN label | CN label | Note |
|---|---|---|---|
| `data[*].code` | Symbol code | 代码 | |
| `data[*].date` | Date | 日期 | |
| `data[*].industry` | Industry | 行业 | string may carry supplier prefix; see prefix-stripping rule below |

### data_type=share (shareholding change events)

| Raw key | EN label | CN label | Note |
|---|---|---|---|
| `data[*].code` | Symbol code | 代码 | |
| `data[*].date` | Date | 日期 | |
| `data[*].total_shares` | Total shares | 总股本 | |
| `data[*].float_shares` | Float shares | 流通股 | |
| `data[*].float_a_shares` | Float A shares | 流通 A 股 | |
| `data[*].non_tradable_shares` | Non-tradable shares | 非流通股 | |
| `data[*].free_float_a_shares` | Free-float A shares | 自由流通 A 股 | |
| `data[*].change_reason` | Change reason | 变动原因 | |
| `data[*].ann_date` | Announcement date | 公告日 | PIT-critical |
| `data[*].register_date` | Register date | 登记日 | |

NA values are normal — `share` is an event series, not a daily panel.

### data_type=index_member (index constituents time series)

| Raw key | EN label | CN label | Note |
|---|---|---|---|
| `data[*].code` | Constituent symbol | 成分股代码 | |
| `data[*].date` | Date | 日期 | |
| `data[*].index_code` | Index symbol | 指数代码 | suffix like `.SH` / `.SZ` / `.HI` — present to user with the index Chinese / English name, NOT the raw code |

### get_symbols detail=true (registry + briefing)

| Raw key | EN label | CN label | Note |
|---|---|---|---|
| `data[*].name` | Short name | 简称 | |
| `data[*].comp_name` | Company name (CN) | 全称 | |
| `data[*].comp_name_eng` | Company name (EN) | 英文名 | |
| `data[*].list_date` | List date | 上市日 | |
| `data[*].list_board` | List board | 上市板 | |
| `data[*].exch_market` | Exchange | 交易所 | |
| `data[*].category` | Category | 分类 | may carry supplier prefix; strip per the prefix rule below |
| `data[*].briefing` | Briefing | 公司简介 | render directly; HK may include longer prose |

### Common envelope

| Raw key | EN label | CN label | Note |
|---|---|---|---|
| `metadata.data_path` | CSV Path | CSV 路径 | triggered when `total_records > inline_threshold` (default 50). CSV not directly fetchable from the runtime — **prefer raising `inline_threshold` (max 1000) on the request** rather than relying on this path. |
| `metadata.warnings` | Warnings | 警告 | upstream errors / truncation; MUST be surfaced to the user |

**Industry-prefix discipline (flagship case)**: `data[*].industry` and `data[*].category` values may arrive with a source-tagged prefix 形如 `<src>-<category>`(e.g. 一段 source tag + 分隔符 + 分类名)。ALWAYS strip the prefix before showing the value to the user — surface only the classification itself ("食品饮料" / "Banking" / "计算机")。Leaking the source tag violates output discipline and locks the publish-form into a single upstream forever。LLM 按常识识别"前缀-分类名"模式即可,不依赖固定 vendor 清单。

**Index-name presentation rule**: never show `.SH / .SZ / .HI / .GI` suffixes to the user. Map `000300.SH` → "沪深300" / CSI 300; `399006.SZ` → "创业板指" / ChiNext; `HSI.HI` → "恒生指数" / Hang Seng Index; etc. Pick CN or EN per user's language.

**Output discipline**: never pass raw key (`float_a_shares`, `comp_name_eng`, `index_code` suffixes like `.SH / .SZ / .HI`, source-tagged industry prefix 形如 `<src>-<category>`) to user-visible text. Agent picks EN or CN label based on the user's language.

## Cross-ref

- For "concept / sector / index **name** → constituent stocks" lookup, use `name-resolver.md` §B + §C (resolve the collection name, then fetch constituents).
- "茅台 PE / 营收 / ROE" → `fundamentals-panel.md`
- "茅台业务结构 / segments" → `consensus-and-target.md` (revenue_breakdown) or `financial-context.md` L2
- "茅台一键综合分析" → `financial-context.md`
- High-PE screening / filtering by sector or concept → the stock-screening skill is **not yet delivered** (upstream limitation; tracked separately). For "top-30 highest-PE" style asks, suggest running a market-wide valuation pull and sorting client-side, or wait for stock-screening to land.
- Pure market status / trading-day queries → `market-calendar.md`
