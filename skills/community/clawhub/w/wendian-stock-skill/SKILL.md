---
name: wendian-markethot-skill
description: This Skill is powered by the **Wendian Starmap (问象星图)** professional stock data analytics platform, exposing core market intelligence endpoints for **real-time quotes**, **K-line/OHLC bars**, **heatmaps**, and **sector rotation analytics**. It supports natural-language or direct API access to: 1) **Real-time market data** — heatmap snapshots (sector/stock heat), global index spot quotes, single-symbol and batch K-line data; 2) **Calendar & reference data** — trading calendar and stock basic info for screening, search, and business-logic gating; 3) **Heatmap & sector rotation (proprietary algorithms)** — sector/stock heat matrices, market-wide heat aggregate index, and per-stock concept heatmaps that visualize cross-sector rotation momentum; 4) **Concepts & constituents** — concept/theme list, batch concept constituents, and reverse lookup of a stock's concept memberships, supporting sector selection and linkage analysis. This skill provides authoritative, low-latency market and heat data for LLMs and applications, ideal for heatmap visualization, rotation analysis, and quantitative research workflows.
required_env_vars:
  - WENDIAN_MARKETHOT_APIKEY
credentials:
  - type: api_key
    name: WENDIAN_MARKETHOT_APIKEY
    description: API Key issued by Wendian Starmap (问象星图). Register a free account at https://markethot.wendian.net to obtain a complimentary API quota.
---

# Wendian Starmap Skill (`wendian-markethot-skill`)

**Wendian Starmap (问象星图)** is a professional stock data analytics application that delivers institutional-grade market intelligence — real-time quotes, multi-period K-line bars, proprietary heatmaps, sector rotation analytics, and curated strategy screeners.

This skill exposes those capabilities over **HTTPS**. The base URL is `https://markethot.wendian.net/app-api/member/skill-data`, and each endpoint is appended as a route under that prefix.

## Getting Started

1. **Register** a free account at [https://markethot.wendian.net](https://markethot.wendian.net) to receive a complimentary API quota.
2. **Obtain** your API Key from the member console.
3. **Store** the key in the `WENDIAN_MARKETHOT_APIKEY` environment variable.
4. **Authenticate** every request via the HTTP header `X-API-Key: <YOUR_API_KEY>`.
5. **Invoke** any of the routes below using either `GET` or `POST` as documented.

### Quick Examples

**Real-time heatmap snapshot**

```bash
curl -X GET 'https://markethot.wendian.net/app-api/member/skill-data/heatmap/realtime?limit=30&source=sector&type=volume' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY'
```

**Single-symbol K-line bars**

```bash
curl -X GET 'https://markethot.wendian.net/app-api/member/skill-data/bars?symbol=601179.SH&period=day&limit=100' \
  --header 'X-API-Key: YOUR_API_KEY'
```

**Batch K-line bars (POST)**

```bash
curl -X POST 'https://markethot.wendian.net/app-api/member/skill-data/batch_bars' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --data '{"symbol_list": ["601179.SH", "000001.SZ"], "period": "day", "limit": 100}'
```

---

## Heatmap Capabilities (Proprietary)

The defining differentiator of Wendian Starmap is its **heatmap and sector-rotation analytics**, built on proprietary algorithms that go beyond commodity market data:

- **The Problem It Solves.** Hundreds of sectors and thousands of equities move every session. Conventional change-percent leaderboards or sector lists fail to surface *who is taking the baton, who is fading, and how aggregate market heat is evolving*. What is missing is a `time × instrument` heat matrix paired with an aggregate trend curve.
- **What the Heatmap Delivers.** Volume, price, and related signals are quantified into a continuous **heat score**, then projected onto a **time series** and a **two-dimensional matrix** (rows = trading days, columns = sectors or stocks, color = heat). The matrix exposes rotation patterns at a glance, while the **market-wide aggregate heat index** highlights overall momentum and inflection points.
- **Typical Workflows.**
  - **Intraday.** Use `heatmap/realtime` to see which sectors or stocks are leading or expanding in volume right now — ideal for live heatmaps, leaderboards, or alerting.
  - **Post-close & research.** Use `heatmap` to retrieve the multi-day heat matrix for visualization, `heatmap/index` to inspect the aggregate market heat curve, and `heatmap/stock_concepts` to identify which concepts are propelling a given stock and which themes are rotating.

The heatmap suite (`heatmap/realtime`, `heatmap`, `heatmap/index`, `heatmap/stock_concepts`) is the **core proprietary capability** that distinguishes this skill from generic market-data feeds, purpose-built for sector rotation, heat ranking, and concept-linkage analytics.

---

## I. Real-time & Market Quotes

### 1. `GET /heatmap/realtime` — Real-time Heatmap Snapshot

**Purpose.** Returns a current-moment heat-ranked snapshot along a single dimension — either by *sector* or by *stock* — measured by volume heat or price heat.

**Use Cases.** Power intraday dashboards, leaderboards, and alerting that surface which sectors or stocks are currently leading or experiencing volume expansion, including average sector returns and individual stock changes.

**Query Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit`   | int  | No       | 30      | Maximum number of rows; `0` returns all. |
| `source`  | str  | No       | sector  | Data dimension: `sector` or `stock`. |
| `type`    | str  | No       | volume  | Heat metric: `volume` or `price`. |

---

### 2. `GET /global_index/spot` — Global Index Spot Quotes

**Purpose.** Real-time levels and changes for major global indices (e.g. Dow Jones, NASDAQ, S&P 500, Hang Seng).

**Use Cases.** Pre-market and post-market context for overseas conditions and sentiment; powers global-index dashboards and cross-market correlation studies with A-shares.

**Query Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `names`   | str  | No       | —       | Comma-separated index names (e.g. `Dow Jones,NASDAQ,S&P 500,Hang Seng`). Returns all when omitted. |

---

### 3. `GET /futures/main` — Domestic Futures Spot Snapshot

**Purpose.** Real-time snapshot of major mainland Chinese futures contracts: price, change, volume, open interest, and other core fields.

**Use Cases.** Monitor domestic futures markets, analyze commodity price trends, and infer supply/demand dynamics across associated industrial chains. Coverage spans the main contracts of SHFE (Shanghai Futures Exchange), DCE (Dalian Commodity Exchange), CZCE (Zhengzhou Commodity Exchange), GFEX (Guangzhou Futures Exchange), and CFFEX (China Financial Futures Exchange).

**Response Fields**

| Field | Type | Description |
|-------|------|-------------|
| `code`             | str   | Contract code (e.g. `AL0` for the continuous aluminum contract). |
| `name`             | str   | Contract name (e.g. *Aluminum Continuous*). |
| `price`            | float | Last traded price. |
| `change_pct`       | float | Percentage change. |
| `change_amount`    | float | Absolute price change. |
| `volume`           | float | Trade volume. |
| `turnover`         | float | Notional turnover (may be `null`). |
| `amplitude`        | float | Trading-day amplitude (%). |
| `high`             | float | Session high. |
| `low`              | float | Session low. |
| `open`             | float | Session open. |
| `prev_settle`      | float | Previous settlement. |
| `bid1`             | float | Best bid. |
| `ask1`             | float | Best ask. |
| `settlement`       | float | Current settlement price. |
| `position`         | float | Open interest. |
| `exchange`         | str   | Exchange code (e.g. `SHFE`). |
| `exchange_cn`      | str   | Localized exchange name. |
| `is_continuous`    | bool  | Whether the row represents a continuous contract. |
| `is_main_contract` | bool  | Whether the row represents the main contract. |

**Example**

```bash
curl -X GET 'https://markethot.wendian.net/app-api/member/skill-data/futures/main' \
  --header 'X-API-Key: YOUR_API_KEY'
```

---

### 4. `GET /futures/global` — International Futures Spot Snapshot

**Purpose.** Real-time snapshot of major international futures markets, covering energy, metals, agricultural, and financial commodities.

**Use Cases.** Track global commodity pricing, derive demand-side signals, and benchmark domestic counterparts. Coverage includes LME, CBOT, COMEX, NYMEX, and other leading international venues.

**Response Fields**

| Field          | Type   | Description |
|----------------|--------|-------------|
| `名称`         | str    | Contract name (e.g. *LME Aluminum 3M*). |
| `最新价`       | float  | Latest price in native currency. |
| `人民币报价`   | float  | Price converted to CNY. |
| `涨跌额`       | float  | Absolute change. |
| `涨跌幅`       | float  | Percentage change. |
| `开盘价`       | float  | Open. |
| `最高价`       | float  | High. |
| `最低价`       | float  | Low. |
| `昨日结算价`   | float  | Previous settlement. |
| `持仓量`       | float  | Open interest. |
| `买价`         | float  | Bid. |
| `卖价`         | float  | Ask. |
| `行情时间`     | str    | Quote time (HH:MM:SS). |
| `日期`         | str    | Quote date (YYYY-MM-DD). |

**Example**

```bash
curl -X GET 'https://markethot.wendian.net/app-api/member/skill-data/futures/global' \
  --header 'X-API-Key: YOUR_API_KEY'
```

---

### 5. `GET /bars` — K-line / OHLC Bars

**Purpose.** Retrieve K-line bars (open, high, low, close, volume, turnover, etc.) for a single instrument across configurable periods and time ranges, with pagination.

**Use Cases.** Drives charting, technical analysis, backtesting, and quantitative strategy research. Supports daily and intraday granularity for the freshest data.

**Query Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `symbol`  | str  | Yes      | —       | Instrument code, e.g. `601179.SH`. |
| `period`  | str  | No       | day     | Period: `1m` / `5m` / `15m` / `30m` / `1h` / `day` / `1w` / `1M`. |
| `start`   | str  | No       | —       | Start time: `yyyyMMdd`, `yyyyMMddHHMMSS`, or `yyyy-MM-dd`. |
| `end`     | str  | No       | —       | End time (same formats as `start`). |
| `limit`   | int  | No       | 100     | Bars per page (1–5000). |
| `offset`  | int  | No       | 0       | Pagination offset; `0` returns the most recent `limit` bars. |

---

### 6. `POST /batch_bars` — Batch K-line Bars

**Purpose.** Fetch K-line data for multiple instruments in a single request. The response is column-oriented per `code` (`open` / `high` / `low` / `close` / `volume` / `amount` / `trade_time` arrays), reducing round-trips and payload overhead.

**Use Cases.** Multi-stock comparisons, multi-pane charts, and portfolio-level monitoring across daily and intraday periods.

**Request Body (JSON)**

| Parameter      | Type        | Required | Default | Description |
|----------------|-------------|----------|---------|-------------|
| `symbol_list`  | list[str]   | Yes      | —       | Instrument codes, e.g. `["601179.SH", "000001.SZ"]`. |
| `period`       | str         | No       | day     | Period: `1m` / `5m` / `15m` / `30m` / `1h` / `day` / `1w` / `1M`. |
| `start`        | str         | No       | —       | Start time: `yyyyMMdd`, `yyyyMMddHHMMSS`, or `yyyy-MM-dd`. |
| `end`          | str         | No       | —       | End time (same formats as `start`). |
| `limit`        | int         | No       | 100     | Bars per page (1–5000). |
| `offset`       | int         | No       | 0       | Pagination offset. |

---

## II. Calendar & Reference Data

### 7. `GET /trade_cal` — Trading Calendar

**Purpose.** Query trading days and holidays for a given range, optionally filtered by exchange and trading status.

**Use Cases.** Determine whether a given date is a trading day, compute *the last N trading days*, exclude non-trading days from business logic, and drive front-end date pickers.

**Query Parameters**

| Parameter  | Type | Required | Default | Description |
|------------|------|----------|---------|-------------|
| `start`    | str  | No       | —       | Start date `yyyyMMdd`. |
| `end`      | str  | No       | —       | End date `yyyyMMdd`. |
| `exchange` | str  | No       | SSE     | Exchange code (defaults to SSE). |
| `is_open`  | int  | No       | —       | Filter: `1` for trading days only, `0` for holidays only; omit to return all. |

---

### 8. `GET /stock_basic` — Stock Reference Data

**Purpose.** Retrieve the static or quasi-static master list of equities (code, name, pinyin, etc.).

**Use Cases.** Backs the universe for screeners, search, and code autocompletion across front-end dropdowns and search boxes.

**Parameters.** None — `GET` without query parameters.

---

## III. Heatmap & Sector Rotation (Proprietary)

The heatmap suite is built on **proprietary algorithms** designed to make **cross-sector rotation momentum** observable: volume and price signals are quantified into a continuous heat score, then projected onto a time series and a two-dimensional matrix that exposes who is taking the baton and who is fading.

### 9. `GET /heatmap` — Heatmap Matrix

**Purpose.** Returns a heat matrix across multiple trading days × multiple instruments (`trade_dates × items` of `values`), keyed by either sector or stock.

**Use Cases.** Render heatmap visualizations where rows = time, columns = sector or stock, and color = heat — surfacing rotation and strength dynamics at a glance.

**Query Parameters**

| Parameter        | Type | Required | Default | Description |
|------------------|------|----------|---------|-------------|
| `end_date`       | str  | No       | —       | End date `yyyyMMdd`; defaults to the latest trading day. |
| `date_count`     | int  | No       | 30      | Number of trading days (rows): 1–365. |
| `columns_count`  | int  | No       | 30      | Number of concepts/stocks (columns), top-N by latest heat descending: 1–200. |
| `source`         | str  | No       | sector  | Dimension: `sector` or `stock`. |
| `heatmap_type`   | str  | No       | volume  | Heat metric: `volume` or `price`. |

---

### 10. `GET /heatmap/index` — Market Heat Aggregate Index

**Purpose.** Returns the aggregate time series of *market heat* (e.g. `mean_value` and `count` grouped by `type × source`) — interpretable as a single curve representing overall market heat.

**Use Cases.** Track the overall heat regime and identify inflection points.

**Query Parameters**

| Parameter    | Type | Required | Default | Description |
|--------------|------|----------|---------|-------------|
| `end_date`   | str  | No       | —       | End date `yyyyMMdd`; defaults to the latest trading day. |
| `date_count` | int  | No       | 30      | Number of trading days: 1–365. |
| `source`     | str  | No       | sector  | Dimension: `sector` or `stock`. |
| `type`       | str  | No       | volume  | Heat metric: `volume` or `price`. |

---

### 11. `GET /heatmap/stock_concepts` — Per-Stock Concept Heatmap

**Purpose.** For a given stock, returns the heat matrix of its associated concept sectors over a window of time (rows = dates, columns = the stock's concepts).

**Use Cases.** Diagnose which concepts are driving a stock and identify which themes are rotating; pair with the sector heatmap for cross-level (stock × sector) linkage analysis.

**Query Parameters**

| Parameter      | Type | Required | Default | Description |
|----------------|------|----------|---------|-------------|
| `symbol`       | str  | Yes      | —       | Stock code, e.g. `601012.SH`. |
| `end_date`     | str  | No       | —       | End date `yyyyMMdd`; defaults to today. |
| `date_count`   | int  | No       | 30      | Number of trading days: 1–365. |
| `heatmap_type` | str  | No       | volume  | Heat metric: `volume` or `price`. |

---

## IV. Concepts & Constituents

### 12. `GET /concepts` — Concept / Theme List

**Purpose.** Returns the list of all concept and theme sectors registered in the system (code, name, etc.).

**Use Cases.** Backs concept selectors, sector trees, and screening criteria; commonly paired with `heatmap` and `stock_concepts`.

**Query Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `source`  | str  | No       | all     | Provider: `ths` (Tonghuashun), `kpl` (Kaipanla), or `all`. |
| `type`    | str  | No       | —       | Concept type filter (effective for `ths` only). |

---

### 13. `POST /concepts/members` — Concept Constituents (Batch)

**Purpose.** Resolve the constituent equities for one or more concept sectors in a single request.

**Use Cases.** Populate "stocks within a concept" views, perform intra-concept screening or weighting, and pair with heatmap endpoints for sector–stock linkage analysis.

**Request Body (JSON)**

| Parameter | Type        | Required | Default | Description |
|-----------|-------------|----------|---------|-------------|
| `codes`   | list[str]   | Yes      | —       | List of concept codes. Codes are globally unique; `type` and `source` are not required. |

---

### 14. `GET /stock_concepts` — Concepts of a Stock (Reverse Lookup)

**Purpose.** Returns the list of concept sectors a given stock belongs to (stock → concept list).

**Use Cases.** Powers stock profile pages, tag rendering, and feeds the per-stock concept heatmap (`heatmap/stock_concepts`).

**Query Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `symbol`  | str  | Yes      | —       | Stock code, e.g. `601179.SH`. |
| `source`  | str  | No       | all     | Provider: `ths` / `kpl` / `all`. |

---

## V. Strategy Screening

### 15. `GET /strategy_select` — Strategy-based Stock Screener

**Purpose.** Surface equities matching curated technical strategies (e.g. *First-to-Second Limit-Up*, *Starlight*, *Steady-State*). Results refresh every trading day.

**Use Cases.** Provide ready-to-use, strategy-aligned stock pools that augment investment decisions with diverse technical viewpoints.

**Query Parameters**

| Parameter        | Type | Required | Default | Description |
|------------------|------|----------|---------|-------------|
| `date`           | str  | Yes      | —       | Trading date in `yyyyMMdd`. |
| `strategy_name`  | str  | No       | —       | Strategy identifier; omit to return all strategies. |

**Strategy Catalog**

| Strategy ID                  | Description |
|------------------------------|-------------|
| `yjer`                       | First-to-Second limit-up screener. |
| `xinghui_model`              | Starlight strategy. |
| `wdt`                        | Steady-state screener. |
| `san_zhouqi_gongzhen`        | Daily/Weekly/Monthly tri-cycle resonance. |
| `month_w_type`               | Monthly W-bottom pattern. |
| `min5_buy2`                  | 5-minute second-buy entry. |
| `ma89_squeeze`               | Multi-MA squeeze convergence. |
| `island_model`               | Island reversal pattern. |
| `bottom_zhongshu_fanzhuan`   | Bottom-pivot reversal. |

**Response Format.** The `data` field is an array; each element contains:

- `stock_code` — Stock code.
- `stock_name` — Stock name.
- `float_volume` — Free-float share count.
- `total_volume` — Total share count.
- `trade_date` — Trading date.
- `code_list` — Related codes.
- `concept_list` — Associated concepts.
- `rank_list` — Ranking signals.
- `strategy_name` — Originating strategy.

**Examples**

```bash
# All strategies for 2026-03-27
curl -X GET 'https://markethot.wendian.net/app-api/member/skill-data/strategy_select?date=20260327' \
  --header 'X-API-Key: YOUR_API_KEY'

# A specific strategy (First-to-Second limit-up)
curl -X GET 'https://markethot.wendian.net/app-api/member/skill-data/strategy_select?date=20260327&strategy_name=yjer' \
  --header 'X-API-Key: YOUR_API_KEY'
```

---

## Endpoint Summary

| Endpoint                     | Core Capability |
|------------------------------|-----------------|
| `heatmap/realtime`           | Real-time heat snapshot — live leaders and volume expansion. |
| `global_index/spot`          | Global index spot quotes — overseas market context. |
| `bars`                       | Single-symbol K-line — charting and strategy. |
| `batch_bars`                 | Multi-symbol K-line (column-oriented) — comparison and monitoring. |
| `trade_cal`                  | Trading calendar — *last N trading days* and similar logic. |
| `heatmap`                    | Sector/stock heat matrix — **visualizes rotation momentum** *(proprietary)*. |
| `heatmap/index`              | Aggregate market heat curve — overall regime. |
| `heatmap/stock_concepts`     | Per-stock concept heat matrix — concept rotation. |
| `stock_basic`                | Equity master data — screening and search. |
| `concepts`                   | Concept / theme list. |
| `concepts/members`           | Concept constituents (batch). |
| `stock_concepts`             | Reverse lookup of a stock's concepts. |
| `strategy_select`            | Strategy-based daily stock screener. |

The heatmap endpoints (`heatmap/realtime`, `heatmap`, `heatmap/index`, `heatmap/stock_concepts`) are powered by **proprietary algorithms** that visualize cross-sector rotation momentum — the differentiating capability of this skill versus generic market-data feeds.

---

## Operational Limits

- `date_count`, `limit`, and `columns_count` for heatmap and K-line endpoints are bounded; avoid overly broad ranges to prevent oversized responses or timeouts.
- For `batch_bars`, keep `symbol_list` reasonably small to avoid oversized request bodies.
- For full response schemas and field semantics, refer to the *Data API Reference* shipped with the project.

## Troubleshooting

If a response is empty or unexpected, verify that:

1. The base URL is `https://markethot.wendian.net/app-api/member/skill-data` and the route is correctly appended.
2. The `X-API-Key` header is present and contains a valid API Key.
3. Parameters comply with the tables above (types, ranges, formats).

Persistent issues should be escalated to Wendian Starmap (问象星图) support via [https://markethot.wendian.net](https://markethot.wendian.net).

---

## File-Output Convention

**⚠️ Mandatory.** All temporary artifacts produced by this skill **must** be written under `archive/wendian-markethot-skill/`. Violating this convention pollutes the workspace root and undermines maintainability.

### Directory Layout
```
archive/wendian-markethot-skill/
├── temp_*.py              # Temporary analysis scripts
├── temp_*.json            # Temporary data files
└── ...                    # Other related artifacts
```

### Naming Conventions
- **Temporary scripts:** `temp_<purpose>.py` (e.g. `temp_analysis.py`).
- **Temporary data:** `temp_<purpose>.json` (e.g. `temp_result.json`).
- **Reports:** `report_<type>_<date>.md`.

### Prohibited
- ❌ Do not create temporary files in the workspace root.
- ❌ Do not create temporary files inside `skills/wendian-markethot-skill/`.

### Required
- ✅ All generated files must reside under `archive/wendian-markethot-skill/`.
- ✅ Use clear, purpose-and-date-aware file names.

---

## Environment Configuration

Set the API Key environment variable before invoking this skill:

```bash
# Windows PowerShell
$env:WENDIAN_MARKETHOT_APIKEY="your_api_key_here"

# Linux / macOS
export WENDIAN_MARKETHOT_APIKEY="your_api_key_here"
```

## End-to-End Test

```bash
# Smoke-test the real-time heatmap snapshot (after setting the env var)
$apiKey = $env:WENDIAN_MARKETHOT_APIKEY
curl.exe -X GET "https://markethot.wendian.net/app-api/member/skill-data/heatmap/realtime?limit=5&source=sector&type=volume" -H "Content-Type: application/json" -H "X-API-Key: $apiKey"
```
