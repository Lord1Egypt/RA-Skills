# name-resolver

## Overview

Tier 0 preprocessor: converts user-supplied natural-language names (company names,
ticker variants, concept / sector / index names) into the canonical identifiers
downstream references need — `bare code` for assets, `collection symbol` for
collections. Resolves the OUT-OF-SCOPE gap previously declared in `industry-and-symbols.md`.

**Confidence bypass**: When you are very confident about the canonical identifier
for a well-known input (mainstream tickers, famous indices), you may pass the
identifier directly to downstream references without calling this preprocessor.
Default behavior — call the preprocessor. Bypass is an optimization for confidence,
not a routine shortcut.

## When to use / When not to use

**Use when**:
- User supplies a natural-language company name (e.g. "贵州茅台", "Apple", "腾讯")
- User supplies a concept / sector / index name (e.g. "白酒", "食品饮料", "沪深300", "中证500")
- You are not sufficiently confident in the canonical identifier

**Do NOT use when**:
- User already supplied a bare code (`600519`, `AAPL`, `000300.SH`) — pass through directly
- User input is a metric / financial indicator name — use `metric-resolver.md` instead

## Endpoint

| Method | Path | Purpose |
|---|---|---|
| POST | `$STOCKI_GATEWAY_URL/api/v1/match/assets` | NL company/ticker → bare code |
| POST | `$STOCKI_GATEWAY_URL/api/v1/match/collections` | NL concept/sector/index name → collection symbol |
| POST | `$STOCKI_GATEWAY_URL/api/v2/asset/get_symbols_from_collection` | collection symbol → stock list |

## §A match/assets — company name / ticker → bare code

### Input schema

```json
{
  "keys": ["贵州茅台"],
  "area": "cn",
  "type": "stock"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `keys` | List[str] | yes | One or more names/symbols/tickers to resolve. Each entry resolves independently. |
| `area` | string | yes | `cn` / `hk` / `us` / `crypto`. The endpoint is `(area, type)`-scoped. |
| `type` | string | yes | `stock` / `futures` / `etf` / `major_index` / `concept_index` / `crypto`. |

### Response shape

```json
{
  "success": true,
  "data": [{
    "query": "贵州茅台",
    "asset": {
      "name": "贵州茅台", "code": "600519",
      "symbol": "600519|ST|SSE", "exchange": "SSE",
      "type": "stock", "area": "cn", "description": "..."
    },
    "method": "precise",
    "confidence": "high",
    "alternatives": null,
    "status": "success"
  }],
  "error": null, "error_code": null, "message": null,
  "trace_id": "uuid"
}
```

**Use `asset.code`** for downstream `bare code` parameters (e.g. `realtime-quote.md` `symbols`,
`fundamentals-panel.md` `symbols`). Do NOT pass `asset.symbol` (the pipe-delimited form)
downstream — that is internal-only.

### Error / not-found shape

`success` is generally `true` even when no good match exists. Branch on `data[0].status`:
- `data[0].status == "not_found"` → no match (rare; usually KB miss returns `success:true` + `method=knn`)
- `data[0].status == "success"` + `method=knn` + low confidence → KB miss fallback, see Confidence handling

### Steps (LLM)

1. Decide `(area, type)` from user context (market, asset class)
2. POST to `$STOCKI_GATEWAY_URL/api/v1/match/assets`
3. Read `data[0].method` and `data[0].confidence` → consult Confidence handling section
4. Extract `data[0].asset.code` if accepted; pass to downstream reference

## §B match/collections — concept / sector / index name → collection symbol

### Input schema

```json
{
  "keys": ["中证500"],
  "area": "cn",
  "type": "index"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `keys` | List[str] | yes | NL collection names. **Note: this endpoint uses `keys` (list), not `name` (string).** |
| `area` | string | yes | `cn` / `hk` / `us` — see Availability matrix below |
| `type` | string | yes | `concept` / `sector` / `index` — see "Type hint vs returned type" below |

### Type hint vs returned type

**The request `type` is a hint, not a constraint.** The resolver searches the area's KB for the best
match across collection types. The returned `data[0].collection.type` may differ from the request type
if the KB does not have the requested type but has a close match in another type. Examples:

- request `(cn, sector, "食品饮料")` → KB has only the concept entry → returns `type=concept`
- request `(us, sector, "半导体")` → KB has only the concept entry → returns `type=concept`

**Caller responsibility**: always trust `data[0].collection.type` and pass that same `type` (not the
request's `type`) to §C `get_symbols_from_collection`. Mismatching the request type to §C will fail-loud
with `"行业不存在"` or `"invalid collection type"`.

### Availability matrix (downstream `§C` constraints)

Reflects the union of types that the KB has *some* entries for in each area. Not every NL name in
each cell will resolve — KB coverage is most complete in Chinese forms; English forms
(`Technology` / `Semiconductors` / `Finance`) often miss.

| `type` | cn | us | hk | crypto |
|---|---|---|---|---|
| `concept` | ✓ | partial(中文 only) | — | — |
| `index` | ✓ | — | ✓(see Quirks) | — |
| `sector` | ✓ | partial(中文 only) | partial(细分类,粗粒度 KB miss) | — |

When the resolver returns `status=not_found` or `method=knn confidence=low`, surface fail-loud per
Confidence handling — do not auto-fall-through to a downstream call with the fuzzy result.

### Response shape

```json
{
  "success": true,
  "data": [{
    "query": "中证500",
    "collection": {
      "type": "index", "name": "中证500", "area": "cn",
      "symbol": "000905.SH",
      "description": "中证小盘500指数 ..."
    },
    "method": "precise",
    "confidence": "high",
    "alternatives": null,
    "status": "success"
  }],
  "error": null, "trace_id": "uuid"
}
```

### Symbol form by area+type

The shape of `collection.symbol` varies and must be passed to §C verbatim:

| Area + Type | Symbol form | Example |
|---|---|---|
| cn:index | `<6-digit>.SH` / `<6-digit>.SZ` | `000905.SH` |
| cn:concept / cn:sector | canonical name string | `白酒` / `食品饮料` |
| hk:index | **pipe-delimited internal form** (NOT `.HI`) | `HSI\|IX\|HKEX` |
| hk:sector | canonical name string | `区域性银行` |
| us:sector | canonical name string | `半导体` (Chinese form when KB-matched) |

**Use `collection.symbol`** for `§C get_symbols_from_collection` input.

### Quirks

- **hk:index → constituents currently fails upstream** with a MySQL syntax error
  (server-side bug, tracked in `docs/superpowers/notes/2026-05-18-name-resolver-proxy-verify.md`).
  Until fixed: surface `unavailable` to the user rather than attempting §C for hk:index.

### Steps (LLM)

1. Determine `(area, type)` — check Availability matrix; if a cell is `—`, fail-loud
2. POST to `$STOCKI_GATEWAY_URL/api/v1/match/collections`
3. Consult Confidence handling for `method` / `confidence` decision
4. **Read `data[0].collection.type` (not the request `type`)** and use that for §C
5. Extract `data[0].collection.symbol` (verbatim) and pass to §C as `symbol`

## §C get_symbols_from_collection — collection symbol → stock list

### Input schema

```json
{
  "area": "cn",
  "symbol": "白酒",
  "type": "concept"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `area` | string | yes | `cn` / `us` / `hk` / `crypto` |
| `symbol` | string | yes | Collection name from `§B match/collections` `collection.symbol`. **Must NOT be empty / `"market"` / `"universe"` — those trigger an "all market" fallback that returns the full universe (~5000+ rows). Client-side guard: validate before calling.** |
| `type` | string | yes (when querying a collection) | `concept` / `sector` / `index`. **If missing, endpoint returns `{code:1, message:"invalid collection type"}` — this is the fail-loud anchor.** |
| `level` | int | no | Only for `type=sector`; default 1 (industry top level). |

### Response shape

```json
{
  "data": [{"code":"600519","name":"贵州茅台",...}, ...],
  "action": "success",
  "total_records": 19,
  "data_path": "data/asset_<hash>.csv",
  "data_description": "Retrieved 19 assets for area=cn, symbol=白酒 ..."
}
```

When `total_records > 500`, `data` becomes a CSV path string + `data_description` carries
the first 500 rows in markdown table. Out of band of inline data; downstream agents should
use `data_description` for the inline preview and not attempt to fetch the CSV path
from the gateway in this skill (runtime cannot retrieve external storage).

### Fail-loud anchors

| Trigger | Response | LLM action |
|---|---|---|
| missing `type` | `{code:1, message:"invalid collection type"}` | Stop, return error to user |
| invalid `area` | `{code:1, message:"不支持的市场区域: ..."}` | Stop |
| `symbol == ""` / `"market"` / `"universe"` | by-design returns full universe (looks like `action:success`) | **Client-side guard required**: validate `symbol` before calling. Do NOT rely on the gateway to error here. |

### Steps (LLM)

1. Validate `symbol ∉ {空, "market", "universe"}` — if invalid, fail-loud (do not call)
2. POST to `$STOCKI_GATEWAY_URL/api/v2/asset/get_symbols_from_collection`
3. Check `action == "success"` and `code != 1`; otherwise fail-loud
4. Read `data` (list) or `data_description` (markdown for >500 rows)
5. Extract bare codes for downstream reference; do NOT pass `symbol` (pipe-delim form) downstream

## Confidence handling

This is a guideline for interpreting `method` and `confidence` in §A/§B response.
**Do not treat the rules below as a closed decision table** — use them as intent
and apply judgment to the user's situation.

### Intent

- `method = "precise"` → trust the result, pass `asset.code` / `collection.symbol` to downstream
- `method = "knn"` with `confidence = "high"` → accept but surface uncertainty to the user
  in your own words (the upstream is reasonably sure, but flag the fuzzy origin so the user
  can correct if it was the wrong identification)
- `method = "knn"` with lower confidence (`low` / `medium` / unlisted) → fail-loud,
  ask the user to supply a ticker or verify the name
- any other `method` value → fail-loud + treat as unknown service state

`score` is internal-only — do NOT use it as a threshold (upstream `score` is bimodal
and degenerate in knn mode, no useful discrimination).

### Why knn ≠ "fuzzy match acceptable"

`method = "knn"` is **knowledge base miss fallback**, not a confidence-adjusted fuzzy
match. The upstream's KB does not have the input and returns the nearest neighbor.
Today's `knn` result may become tomorrow's `precise` as the upstream KB grows.
Do not lock in surface text that treats knn as a stable match.

### Example surface text (when accepting knn+high)

Intent — paraphrase as appropriate; **do not lock to this template**:

> "I'm reading『{user input}』as『{asset.name}』(`{asset.code}`). If that's not the
> company you meant, please give me a ticker and I'll re-run."

### Example surface text (when failing fail-loud)

Intent:

> "I couldn't find a confident match for『{user input}』in the known list. If you have
> a ticker, please supply it; otherwise verify the spelling or whether the company
> is listed."

### Internal-only fields

Never surface these in user-facing text:
- `asset.symbol` (pipe-delimited form, e.g. `600519|ST|SSE`)
- `confidence`, `score`, `method`, `trace_id`
- `data[0].asset.exchange` (use `asset.code` only)

## Response Fields — Raw → User-Facing Label

| Section | Raw key | EN label | CN label | Pass through? |
|---|---|---|---|---|
| §A asset | `asset.code` | Symbol | 代码 | ✓ to downstream `symbols` param |
| §A asset | `asset.name` | Company name | 公司名 | ✓ to user-facing text |
| §A asset | `asset.exchange` | Exchange | 交易所 | only if user explicitly asks |
| §A asset | `asset.symbol` | (internal) | — | ✗ **never** — pipe-delimited internal form |
| §A asset | `asset.description` | Description | 简介 | ✓ optional |
| §A | `method`, `score`, `confidence` | (internal) | — | ✗ never surface |
| §B collection | `collection.symbol` | Collection symbol | 集合代码 | ✓ to §C `symbol` param; for user-facing text, prefer the name |
| §B collection | `collection.name` | Collection name | 名称 | ✓ to user-facing text |
| §B collection | `collection.type` | Type | 类型 | ✓ if disambiguation needed |
| §B collection | `collection.description` | Description | 简介 | ✓ optional |
| §C | `data[*].code` | Symbol | 代码 | ✓ to downstream |
| §C | `data[*].name` | Name | 名称 | ✓ user-facing |
| §C | `data[*].symbol` | (internal) | — | ✗ never (pipe-delim) |
| §C | `data_description` | Markdown preview | 预览 | use for inline display when `total_records > 500` |
| envelope | `trace_id`, `error_code`, internal-only metadata | (internal) | — | ✗ never |

## Cross-ref

- After resolving an asset (`§A`), pass `asset.code` to:
  - `realtime-quote.md` for current price / fundamental snapshot
  - `fundamentals-panel.md` for time-series financials
  - `price-history.md` for OHLCV history
  - `consensus-and-target.md` for forecast/target
  - `financial-context.md` for composite analysis (cn/hk only)
- After resolving a collection (`§B`) → `§C get_symbols_from_collection` →
  for each stock, follow asset-flow above
- `industry-and-symbols.md` references this doc for the "collection name → constituents"
  reverse lookup that used to be out-of-scope
- For metric (financial indicator) resolution, see `metric-resolver.md` instead
