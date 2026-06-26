---
name: tickerdb
version: 0.1.2
description: Connect your agent to pre-computed market context that improves reasoning and reduces token usage.
metadata:
  openclaw:
    emoji: "📈"
    requires:
      env:
        - TICKERDB_KEY
    primaryEnv: TICKERDB_KEY
    homepage: "https://tickerdb.com"
user-invocable: true
---

# TickerDB - Market context for agents.

[TickerDB](https://tickerdb.com) provides pre-computed market context that improves reasoning and reduces token usage.

## First Run Setup

If the `TICKERDB_KEY` environment variable is not set, walk the user through account setup before doing anything else:

1. Ask for their email address and let them know: "This will sign you into your existing TickerDB account, or create a new one if you don't have one yet."
2. Call `POST https://api.tickerdb.com/auth` with `{ "email": "<their email>" }`.
3. Tell them to check their inbox for a 6-digit code.
4. Once they provide the code, call `POST https://api.tickerdb.com/auth/verify` with `{ "email": "<their email>", "code": "<their code>" }`.
5. The response contains an `apiKey` field for new accounts. Show the user their key and ask: "I've got your API key — would you like me to save it?" If they confirm, OpenClaw persists it automatically. If no `apiKey` in the response (existing account), direct them to https://tickerdb.com/dashboard to retrieve their key.

Once authenticated, continue through onboarding in order:

**Step 1 — Watchlist**
Ask: "What tickers would you like to add to your watchlist? You can give me a list of stock symbols, crypto (e.g. BTCUSD), or ETFs."
After they provide tickers, call `GET /v1/summary/{ticker}` for each one to confirm they're valid and give a brief one-line summary of each.

**Step 2 — Daily Report**
Ask: "Would you like me to set up a daily morning report for these tickers? Each morning I can brief you on key metrics — trend changes, support zone, abnormal volume, and any notable signals."

---

TickerDB provides pre-computed, categorical market data designed for LLMs and AI agents. Every response contains verifiable facts — no OHLCV, no raw indicator values, just derived categorical bands (e.g. `oversold`, not `RSI: 24`).

- **Asset classes:** US Stocks, Crypto (tickers require `USD` suffix, e.g. `BTCUSD`), ETFs
- **Timeframes:** `daily` (default), `weekly`
- **Update frequency:** End-of-day (~00:30 UTC). Responses expose `data_status` and `as_of_date`.
- **Response format:** JSON
- **Data is factual, not predictive** — no scores, no recommendations, no bias

## Authentication

All requests require a Bearer token in the Authorization header:

```
Authorization: Bearer $TICKERDB_KEY
```

Errors: `401` = missing/invalid token. `403` = endpoint requires higher tier (response includes `upgrade_url`).

## Base URL

```
https://api.tickerdb.com/v1
```

## Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticker` | string | Asset symbol, uppercase. Crypto needs `USD` suffix (e.g. `BTCUSD`). Required on per-asset endpoints. Passed as a path parameter (e.g. `/v1/summary/AAPL`). |
| `timeframe` | string | Supported on summary, search, and watchlist changes. `daily` or `weekly`. Default: `daily`. |

## Important: Asset Class Rules

- **Stocks** get all technical + fundamental data (valuation, growth, earnings, analyst consensus).
- **Crypto and ETFs** get technical data only. Fundamental fields are **omitted entirely** (keys absent, not null).
- Crypto tickers MUST include `USD` suffix: `BTCUSD`, `ETHUSD`, `SOLUSD`. Using just `BTC` returns an error.

---

## Categorical Bands Reference

TickerDB never returns raw indicator values. All data uses categorical bands:

- **RSI/Stochastic zones:** `deep_oversold`, `oversold`, `neutral_low`, `neutral`, `neutral_high`, `overbought`, `deep_overbought`
- **Trend direction:** `strong_uptrend`, `uptrend`, `neutral`, `downtrend`, `strong_downtrend`
- **MA alignment:** `aligned_bullish`, `mixed`, `aligned_bearish`
- **MA distance:** `far_above`, `moderately_above`, `slightly_above`, `slightly_below`, `moderately_below`, `far_below`
- **Volume ratio:** `extremely_low`, `low`, `normal`, `above_average`, `high`, `extremely_high`
- **Accumulation state:** `strong_accumulation`, `accumulation`, `neutral`, `distribution`, `strong_distribution`
- **Volatility regime:** `low`, `normal`, `above_normal`, `high`, `extreme`
- **Support/resistance distance:** `at_level`, `very_close`, `near`, `moderate`, `far`, `very_far`
- **Support/resistance status:** `intact`, `approaching`, `breached`
- **MACD state:** `expanding_positive`, `contracting_positive`, `expanding_negative`, `contracting_negative`
- **Momentum direction:** `accelerating`, `steady`, `decelerating`, `bullish_reversal`, `bearish_reversal`
- **Valuation zone (stocks only):** `deep_value`, `undervalued`, `fair_value`, `overvalued`, `deeply_overvalued`
- **Growth zone (stocks only):** `high_growth`, `moderate_growth`, `stable`, `slowing`, `shrinking`
- **Growth direction (stocks only):** `accelerating`, `steady`, `decelerating`, `deteriorating`
- **Earnings proximity (stocks only):** `within_days`, `this_week`, `this_month`, `next_month`, `not_soon`
- **Earnings surprise (stocks only):** `big_beat`, `beat`, `met`, `missed`, `big_miss`
- **Analyst consensus (stocks only):** `strong_buy`, `buy`, `hold`, `sell`, `strong_sell`
- **Analyst consensus direction (stocks only):** `upgrading`, `stable`, `downgrading`
- **Performance:** `sharp_decline`, `moderate_decline`, `slight_decline`, `flat`, `slight_gain`, `moderate_gain`, `sharp_gain` (per-ticker percentile-based)
- **Price direction on volume:** `up`, `down`, `flat`
- **Insider activity zone (stocks only):** `heavy_buying`, `moderate_buying`, `neutral`, `moderate_selling`, `heavy_selling`, `no_activity`
- **Insider net direction (stocks only):** `strong_buying`, `buying`, `neutral`, `selling`, `strong_selling`
- **Market cap tier:** `nano`, `micro`, `small`, `mid`, `large`, `mega`, `ultra_mega`
- **Condition rarity:** `extremely_rare`, `very_rare`, `rare`, `uncommon`, `occasional`, `common`
- **Stability (Plus/Pro only):** `fresh` (just changed), `holding` (changed recently, staying put), `established` (held for a long time), `volatile` (flipping back and forth frequently)

---

## Endpoints

### GET /v1/summary/:ticker

Unified endpoint for single-asset intelligence. Supports 4 modes depending on which parameters are provided:

1. **Snapshot** (default) — Current categorical state for a ticker.
2. **Historical snapshot** — Pass `date` for a point-in-time snapshot.
3. **Historical series** — Pass `start`/`end` for a date range of snapshots showing how bands evolved over time.
4. **Events** — Pass `field` (and optionally `band`) to get band transition history with aftermath performance data.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | string | — | Required. Path param (e.g. `/v1/summary/AAPL`) |
| `timeframe` | string | `daily` | `daily` or `weekly` |
| `date` | string | latest | Point-in-time snapshot (YYYY-MM-DD). Plus: 2 years. Pro: 5 years. |
| `start` | string | — | Range start date (YYYY-MM-DD). Use with `end` for historical series. Sequential ranges must fit within your plan cap: Free 3 rows, Plus 10 rows, Pro 50 rows. |
| `end` | string | latest | Range end date (YYYY-MM-DD). Use with `start`. |
| `fields` | string | full summary | Snapshot and history modes only. JSON array or comma-separated list of sections and dotted paths to return, such as `trend`, `momentum.rsi_zone`, `fundamentals.valuation_zone`, or `levels.support_levels`. |
| `meta` | boolean | `false` | Snapshot and history modes only. Add `meta=true` to include sibling `_meta` / `status_meta` stability objects in the response. Explicit `*_meta` field paths in `fields` still work without this flag. |
| `sample` | string | — | Date range mode only. Use `even` to evenly spread snapshots across the entire `start`/`end` range. |
| `field` | string | — | Band field name for events. Prefer full schema/search names like `momentum_rsi_zone`, `extremes_condition`, `trend_direction`, `trend_distance_ma50`, or `fundamentals_valuation_zone`. Legacy short aliases like `rsi_zone` still work. Switches to events mode. |
| `band` | string | all | Filter events to a specific band value (e.g. `deep_oversold`). For MA distance event fields such as `trend_distance_ma50`, grouped aliases `above` and `below` are also supported. Only with `field`. |
| `stats` | boolean | `false` | Event mode only. Add `stats=true` to return aggregate stats instead of raw event rows. |
| `limit` | int | plan max (`sample=even`) / 10 (events) | With `sample=even`, requested sampled rows up to your plan cap. With `field`, max event results (1-50), returned newest-first by default. |
| `before` | string | — | Return events before this date (YYYY-MM-DD). Only with `field`. |
| `after` | string | — | Return events after this date (YYYY-MM-DD). Only with `field`. |
| `context_ticker` | string | — | Cross-asset correlation: second ticker (e.g. `SPY`). Requires `context_field` + `context_band`. Plus/Pro only. 2 credits. |
| `context_field` | string | — | Band field to check on context ticker (e.g. `trend_direction` or `trend_distance_ma50`). |
| `context_band` | string | — | Required band on context ticker (e.g. `downtrend`). For MA distance context fields, grouped aliases `above` and `below` are also supported. |

**Tier access:** Free gets core technical (performance, trend, momentum, extremes, volatility, volume). Plus adds support/resistance, basic fundamentals, opt-in band stability metadata (`_meta` sibling objects / `status_meta`), aftermath data on events, and cross-asset correlation. Pro adds sector_context and advanced fundamentals. Date lookback limits: Free 30 days, Plus 2 years, Pro 5 years. Sequential date-range caps: Free 3 rows, Plus 10 rows, Pro 50 rows. Events lookback: Free 30 days, Plus 2 years, Pro 5 years.

**Band stability metadata (Plus/Pro only):** Summary keeps sibling `_meta` objects off by default so the primary band label stays front-and-center. Add `meta=true` to include them across the response, or explicitly request a `*_meta` field in `fields`. Each `_meta` object can include `stability` (`fresh`/`holding`/`established`/`volatile`), `periods_in_current_state` (int), `flips_recent` (int), and `flips_lookback` (e.g. `"30d"`). Not available on Free tier.

**Field selection:** Use `fields` when you want smaller, more LLM-friendly summary payloads. The API always keeps identity keys like `ticker` and `timeframe`, then returns only the requested sections or dotted paths. Summary omits `_meta` by default even when you request a whole section like `trend`; add `meta=true` for full-section stability metadata, or explicitly request just the few `*_meta` paths you need. In historical range mode, the duplicate top-level `levels` block is only returned when you explicitly request `levels` or a child path like `levels.support_levels`.

**Response sections (snapshot/historical modes):**

- Identity/freshness — `ticker`, `timeframe`, `asset_class`, `sector`, `data_status`, `as_of_date`, `performance`
- `trend` — `direction`, `duration_days`, `ma_alignment`, `distance_from_ma_band` (ma_8, ma_20, ma_50, ma_100, ma_200), `volume_confirmation` (`confirmed`/`diverging`/`neutral`)
- `momentum` — `rsi_zone`, `stochastic_zone`, `rsi_stochastic_agreement`, `macd_state`, `direction`, `divergence_detected`, `divergence_type` (`bullish_divergence`/`bearish_divergence`/null)
- `extremes` — `condition` (`deep_oversold` through `deep_overbought` or `normal`), `days_in_condition`, `historical_median_duration`, `historical_max_duration`, `occurrences_1yr`, `condition_percentile`, `condition_rarity`
- `volatility` — `regime`, `regime_trend` (`compressing`/`stable`/`expanding`), `squeeze_active`, `squeeze_days`, `historical_avg_squeeze_duration`
- `volume` — `ratio_band`, `percentile`, `accumulation_state`, `climax_detected`, `climax_type` (`buying_climax`/`selling_climax`/null), `price_direction_on_volume`, `consecutive_elevated_days`, `historical_avg_elevated_streak`
- `support_level` / `resistance_level` (Plus+) — `status` (`intact`/`approaching`/`breached`), optional `status_meta` when `meta=true` or explicitly requested, `distance_band`, `touch_count`, `held_count`, `broke_count`, `consecutive_closes_beyond`, `last_tested_days_ago`, `type` (`horizontal`/`ma_derived`), `ma_name`, `volume_at_tests_band`
- `range_position` — `lower_third`, `mid_range`, or `upper_third`
- `sector_context` (Pro) — `rsi_zone`, `trend`, `asset_vs_sector_rsi`, `asset_vs_sector_trend`, `agreement`, `oversold_count`, `overbought_count`, `breakout_count`, `total_count`, `valuation_zone`, `elevated_volume_count`
- `fundamentals` (stocks only, Plus+) — Plus: `valuation_zone`, `growth_zone`, optional `growth_zone_meta` when requested, `earnings_proximity`, `analyst_consensus`. Pro adds: `valuation_percentile`, `pe_vs_historical_zone`, `pe_vs_sector_zone`, `pb_vs_historical_zone`, `revenue_growth_direction`, optional `revenue_growth_direction_meta`, `eps_growth_direction`, optional `eps_growth_direction_meta`, `last_earnings_surprise`, `analyst_consensus_direction`, and nested `insider_activity` (`zone`, `net_direction`, `quarter`)

**Events mode response:** `ticker`, `field`, `timeframe`, `events` array, `total_occurrences`, `query_range`. Events are returned newest-first by default. Each event includes: `date`, `band`, `prev_band`, `duration_days` (or `duration_weeks`), `aftermath` object with lookahead performance bands (5d/10d/20d/50d/100d for daily, 2w/4w/8w/12w/16w for weekly). Plus/Pro also get `stability_at_entry`, `flips_recent_at_entry`, and `flips_lookback`. When cross-asset correlation is used, also includes `context` object. Add `stats=true` to swap the raw `events` list for aggregate `stats` with event-band counts and aftermath distributions.

**Examples:**

Snapshot (current state):
```
curl "https://api.tickerdb.com/v1/summary/NVDA" \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

Latest snapshot with stability metadata:
```
curl "https://api.tickerdb.com/v1/summary/AAPL?meta=true" \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

Historical series:
```
curl "https://api.tickerdb.com/v1/summary/AAPL?start=2026-01-05&end=2026-01-16" \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

Evenly sampled historical series:
```
curl "https://api.tickerdb.com/v1/summary/AAPL?start=2026-01-01&end=2026-12-31&sample=even&limit=10" \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

LLM-friendly sampled series with selected fields:
```
curl "https://api.tickerdb.com/v1/summary/AAPL?start=2026-01-01&end=2026-12-31&sample=even&limit=10&fields=[\"trend.direction\",\"momentum.rsi_zone\",\"fundamentals.valuation_zone\"]" \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

Single stability field without full meta:
```
curl "https://api.tickerdb.com/v1/summary/AAPL?fields=[\"trend.direction\",\"trend.direction_meta\"]" \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

Events (band transition history):
```
curl "https://api.tickerdb.com/v1/summary/AAPL?field=momentum_rsi_zone&band=deep_oversold&limit=5" \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

Events (extreme-state entries):
```
curl "https://api.tickerdb.com/v1/summary/AAPL?field=extremes_condition&band=deep_oversold&limit=5" \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

Events (MA distance lookback with grouped aliases):
```
curl "https://api.tickerdb.com/v1/summary/BTCUSD?field=trend_distance_ma50&band=above&context_ticker=SPY&context_field=trend_distance_ma50&context_band=below&limit=5" \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

Aggregate stats (cross-asset MA lookback):
```
curl "https://api.tickerdb.com/v1/summary/SOLUSD?field=trend_distance_ma20&band=above&context_ticker=QQQ&context_field=trend_distance_ma20&context_band=above&stats=true&before=2025-07-01" \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

Events with cross-asset correlation:
```
curl "https://api.tickerdb.com/v1/summary/AAPL?field=momentum_rsi_zone&band=deep_oversold&context_ticker=SPY&context_field=trend_direction&context_band=downtrend&limit=5" \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

---

### Watchlist — /v1/watchlist

The watchlist is a **persistent, server-side** list of tickers. Users save tickers once and then retrieve live data for them on demand. The saved watchlist is also what webhooks monitor — `watchlist.changes` events fire for tickers on the user's saved watchlist.

**Tier limits:** Free: 10 tickers. Plus: 50 tickers. Pro: 100 tickers.

#### GET /v1/watchlist — Retrieve saved watchlist with live data

Returns live snapshot data for all saved tickers.

**Response:**
```json
{
  "watchlist": [
    {
      "ticker": "AAPL",
      "asset_class": "stock",
      "as_of_date": "2026-04-11",
      "performance": "slight_gain",
      "trend_direction": "uptrend",
      "rsi_zone": "neutral_high",
      "volume_ratio_band": "normal",
      "extremes_condition": "normal",
      "days_in_extreme": 0,
      "condition_rarity": "common",
      "squeeze_active": false,
      "support_level_distance": "near",
      "resistance_level_distance": "very_close",
      "valuation_zone": "fair_value",
      "earnings_proximity": "this_month",
      "analyst_consensus": "buy",
      "notable_changes": ["earnings within_days"]
    }
  ],
  "tickers_saved": 1,
  "tickers_found": 1,
  "watchlist_limit": 50,
  "data_status": "eod",
  "as_of_date": "2026-04-11"
}
```

Tickers with no available data return `{"ticker": "XXX", "status": "not_found"}`. Empty watchlist returns `{"watchlist": [], "tickers_saved": 0, ...}`.

**Example:**
```
curl https://api.tickerdb.com/v1/watchlist \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

#### POST /v1/watchlist — Add tickers to saved watchlist

Add one or more tickers. Duplicates are skipped silently.

**Request body (JSON):**
```json
{
  "tickers": ["AAPL", "MSFT", "BTCUSD"]
}
```

**Response:**
```json
{
  "added": ["AAPL", "MSFT", "BTCUSD"],
  "already_saved": [],
  "watchlist_count": 3,
  "watchlist_limit": 50
}
```

Only supported tickers can be added — all tickers are validated against the assets database. Returns 400 `invalid_tickers` if any ticker is not a recognized asset (includes `invalid_tickers` array in the error). Returns 400 `watchlist_limit` if adding would exceed the tier limit (includes `upgrade_url`).

**Example:**
```
curl -X POST https://api.tickerdb.com/v1/watchlist \
  -H "Authorization: Bearer $TICKERDB_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tickers": ["AAPL", "TSLA", "BTCUSD"]}'
```

#### DELETE /v1/watchlist — Remove tickers from saved watchlist

Remove one or more tickers.

**Request body (JSON):**
```json
{
  "tickers": ["MSFT"]
}
```

**Response:**
```json
{
  "removed": ["MSFT"],
  "watchlist_count": 2
}
```

**Example:**
```
curl -X DELETE https://api.tickerdb.com/v1/watchlist \
  -H "Authorization: Bearer $TICKERDB_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tickers": ["MSFT"]}'
```

#### GET /v1/watchlist/changes — Field-level state changes

Returns structured, field-level diffs for your saved watchlist tickers since the last pipeline run. For `daily` timeframe, shows day-over-day changes. For `weekly`, week-over-week changes. Available on **all tiers** (including Free). This returns the same data format that webhooks deliver, but as a pull-based endpoint.

**Parameters:** `timeframe` (optional, default `daily`) — `daily` or `weekly`.

**Fields tracked:** `rsi_zone`, `trend_direction`, `trend_distance_ma8`, `trend_distance_ma20`, `trend_distance_ma50`, `trend_distance_ma100`, `trend_distance_ma200`, `volume_ratio_band`, `squeeze_active`, `extreme_condition`, `breakout_type`, and fundamental fields (`fundamentals.valuation_zone`, `fundamentals.analyst_consensus`, `fundamentals.earnings_proximity`, `fundamentals.last_earnings_surprise`, `fundamentals.growth_zone`).

**Response:**
```json
{
  "timeframe": "daily",
  "run_date": "2026-03-28",
  "changes": {
    "AAPL": [
      {"field": "rsi_zone", "from": "neutral", "to": "oversold", "stability": "fresh", "periods_in_current_state": 1, "flips_recent": 2, "flips_lookback": "30d"},
      {"field": "fundamentals.earnings_proximity", "from": "next_month", "to": "within_days"}
    ],
    "BTCUSD": [
      {"field": "squeeze_active", "from": false, "to": true, "stability": "volatile", "periods_in_current_state": 1, "flips_recent": 5, "flips_lookback": "30d"}
    ]
  },
  "tickers_checked": 5,
  "tickers_changed": 2
}
```

Only tickers with at least one field change are included in `changes`. If no tickers changed, `changes` is `{}`. If the watchlist is empty, `tickers_checked` is 0. Plus/Pro users also get stability metadata on each change object: `stability`, `periods_in_current_state`, `flips_recent`, `flips_lookback`. Free tier gets `field`, `from`, and `to` only.

**Example:**
```
curl https://api.tickerdb.com/v1/watchlist/changes?timeframe=daily \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

---

### GET /v1/search

Search for assets matching categorical filter criteria. Use this when you need to find tickers by their current band state (e.g. "which stocks are oversold?", "find tech stocks in strong uptrend").

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filters` | string | — | JSON-encoded array of `{field, op, value}` objects. Prefer canonical flat schema names from `/v1/schema/fields`, such as `momentum_rsi_zone` or `trend_direction`. |
| `timeframe` | string | `daily` | `daily` or `weekly` |
| `sort_by` | string | `ticker` | Column name to sort results by. Must be a valid field from the schema. |
| `sort_direction` | string | `desc` | `asc` or `desc` |
| `limit` | int | 20 | Max results (1-50) |
| `offset` | int | 0 | Pagination offset |
| `fields` | string | core subset | Columns to return. JSON array or comma-separated. Default if omitted: `ticker, asset_class, sector, performance, trend_direction, momentum_rsi_zone, extremes_condition, extremes_condition_rarity, volatility_regime, volume_ratio_band, fundamentals_valuation_zone, range_position`. Use `["*"]` for all 120+ fields. `ticker` is always included. Invalid fields return an error pointing to `/v1/schema/fields`. |

**Filter examples:**
```json
[{"field":"momentum_rsi_zone","op":"eq","value":"deep_oversold"}]
[{"field":"trend_direction","op":"in","value":["uptrend","strong_uptrend"]},{"field":"volume_ratio_band","op":"eq","value":"high"}]
[{"field":"sector","op":"eq","value":"Technology"},{"field":"momentum_rsi_zone","op":"eq","value":"oversold"}]
```

**Examples:**

Basic search:
```
curl -G "https://api.tickerdb.com/v1/search" \
  --data-urlencode 'filters=[{"field":"momentum_rsi_zone","op":"eq","value":"deep_oversold"}]' \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

Return only specific fields (reduces token usage):
```
curl -G "https://api.tickerdb.com/v1/search" \
  --data-urlencode 'filters=[{"field":"momentum_rsi_zone","op":"eq","value":"oversold"}]' \
  --data-urlencode 'fields=["ticker","sector","momentum_rsi_zone"]' \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

Sort by valuation percentile (cheapest first):
```
curl -G "https://api.tickerdb.com/v1/search" \
  --data-urlencode 'filters=[{"field":"fundamentals_valuation_zone","op":"in","value":["deep_value","undervalued"]}]' \
  --data-urlencode 'sort_by=fundamentals_valuation_percentile' \
  --data-urlencode 'sort_direction=asc' \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

**SDK Query Builder:** The official SDKs (JavaScript, Python, Go) provide a fluent query builder as an alternative to raw `/search` calls. Chain `.select()` -> `.eq()` -> `.sort()` -> `.limit()` -> `.execute()` for a Supabase-style interface. See each SDK's README for details.

---

### GET /v1/schema/fields

Get the schema of all available fields and their valid band values. Use this to discover what fields are available, what band values each field accepts, and what sectors exist. Does not count against request limits.

**Example:**
```
curl https://api.tickerdb.com/v1/schema/fields \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

---

## Webhooks

Webhooks let users receive push notifications when something changes on their watchlist. Instead of polling, TickerDB's engine POSTs structured, field-level diffs to registered URLs after each daily and weekly pipeline run.

**Tier access:** Plus and Pro only (free tier cannot use webhooks). Plus gets 1 webhook URL, Pro gets 3, Business Plus gets 3, and Business Pro gets 5.

Each webhook delivery counts as one API request against the user's daily allowance.

### Event Types

| Event | Description | Default |
|-------|-------------|---------|
| `watchlist.changes` | Structured field-level diffs for tickers on the user's watchlist. Only fires when at least one field has changed. | Enabled on creation |
| `data.ready` | Simple notification that fresh data has been computed and is available via the API. | Opt-in |

Fields tracked for `watchlist.changes`: `rsi_zone`, `trend_direction`, `trend_distance_ma8`, `trend_distance_ma20`, `trend_distance_ma50`, `trend_distance_ma100`, `trend_distance_ma200`, `volume_ratio_band`, `squeeze_active`, `extreme_condition`, `breakout_type`, and fundamental fields (`valuation_zone`, `analyst_consensus`, `earnings_proximity`, `last_earnings_surprise`, `growth_zone`).

### POST /v1/webhooks — Register a webhook

Register a new webhook URL. The `secret` is returned **only on creation** — save it immediately.

**Request body (JSON):**
```json
{
  "url": "https://example.com/webhook",
  "events": { "watchlist.changes": true, "data.ready": true }
}
```

- `url` (required) — Must be HTTPS.
- `events` (optional) — Defaults to `{"watchlist.changes": true}`.

**Response (201):**
```json
{
  "id": "d3f1a2b4-...",
  "url": "https://example.com/webhook",
  "secret": "a1b2c3d4e5f6...",
  "events": { "watchlist.changes": true, "data.ready": true },
  "active": true,
  "created_at": "2026-03-27T12:00:00.000Z"
}
```

### GET /v1/webhooks — List webhooks

Returns all registered webhooks for the user. The `secret` field is never included in GET responses.

**Response:**
```json
{
  "webhooks": [
    {
      "id": "d3f1a2b4-...",
      "url": "https://example.com/webhook",
      "events": { "watchlist.changes": true, "data.ready": true },
      "active": true,
      "created_at": "...",
      "updated_at": "..."
    }
  ],
  "webhook_count": 1,
  "webhook_limit": 1
}
```

### PUT /v1/webhooks — Update a webhook

Update the URL, event subscriptions, or active status.

**Request body (JSON):**
```json
{
  "id": "d3f1a2b4-...",
  "events": { "watchlist.changes": true },
  "active": false
}
```

### DELETE /v1/webhooks — Remove a webhook

**Request body (JSON):**
```json
{
  "id": "d3f1a2b4-..."
}
```

### Webhook Delivery

When the daily or weekly pipeline completes, TickerDB's engine POSTs payloads to all active webhooks. Each delivery includes:

| Header | Description |
|--------|-------------|
| `X-Webhook-Signature` | HMAC-SHA256 hex digest of the raw request body, signed with the webhook's `secret` |
| `X-Webhook-Event` | Event type: `watchlist.changes` or `data.ready` |
| `Content-Type` | `application/json` |
| `User-Agent` | `TickerDB-Webhook/1.0` |

**`watchlist.changes` payload:**
```json
{
  "event": "watchlist.changes",
  "timestamp": "2026-03-27T21:30:00Z",
  "data": {
    "timeframe": "daily",
    "run_date": "2026-03-27",
    "changes": {
      "AAPL": [{ "field": "rsi_zone", "from": "neutral", "to": "oversold", "stability": "fresh", "periods_in_current_state": 1, "flips_recent": 2, "flips_lookback": "30d" }],
      "TSLA": [
        { "field": "squeeze_active", "from": false, "to": true, "stability": "holding", "periods_in_current_state": 3, "flips_recent": 1, "flips_lookback": "30d" },
        { "field": "fundamentals.analyst_consensus", "from": "hold", "to": "buy", "stability": "established", "periods_in_current_state": 45, "flips_recent": 0, "flips_lookback": "30d" }
      ]
    },
    "tickers_checked": 15,
    "tickers_changed": 2
  }
}
```

**`data.ready` payload:**
```json
{
  "event": "data.ready",
  "timestamp": "2026-03-27T21:30:00Z",
  "data": {
    "timeframe": "daily",
    "run_date": "2026-03-27",
    "tickers_computed": 9847
  }
}
```

### Signature Verification

Always verify the `X-Webhook-Signature` before processing payloads. Compute HMAC-SHA256 of the raw request body using the webhook's `secret`, and compare it to the header value.

---

## Account

### GET /v1/account

Returns usage and plan information for the authenticated user. Does not count against request limits.

**Response:** `plan` (tier name), `usage` (current period request counts), `limits` (daily/hourly caps), `watchlist_limit`, `webhook_limit`.

**Example:**
```
curl https://api.tickerdb.com/v1/account \
  -H "Authorization: Bearer $TICKERDB_KEY"
```

---

## Errors

| Status | Type | Description |
|--------|------|-------------|
| 400 | `invalid_parameter` | Bad ticker, timeframe, or param |
| 401 | `unauthorized` | Missing/invalid token |
| 403 | `tier_restricted` | Needs higher tier (includes `upgrade_url`) |
| 404 | `not_found` | Ticker not supported |
| 429 | `rate_limit_exceeded` | Daily limit hit (includes `upgrade_url` + reset time) |
| 500 | `internal_error` | Server error |
| 503 | `data_unavailable` | Data feed temporarily down |

When you get a 403, tell the user which tier they need and share the upgrade URL from the response.

## Rate Limits

| Tier | Daily | Hourly |
|------|-------|--------|
| Free | 250 | 100 |
| Plus (Individual) | 50,000 | 5,000 |
| Pro (Individual) | 100,000 | 10,000 |
| Plus (Business) | 250,000 | 25,000 |
| Pro (Business) | 500,000 | 50,000 |

- `/v1/schema/fields` and `/v1/account` never count against limits
- HTTP 304 (conditional/cached) responses do not count
- Use `ETag` / `If-None-Match` headers for conditional requests
- Rate limit headers: `X-Requests-Remaining`, `X-Request-Reset`, etc.

## Plans & Tiers

TickerDB has three tiers: **Free**, **Plus**, and **Pro**. Each tier unlocks more data fields, higher limits, and historical access. If a user asks about upgrading, pricing, or wants to unlock more features, link them to **https://tickerdb.com/pricing**.

### What each tier unlocks

| Feature | Free | Plus | Pro |
|---------|------|------|-----|
| **Band stability metadata** | None | Summary opt-in via `meta=true` or explicit `*_meta` fields, plus full event/change stability | Summary opt-in via `meta=true` or explicit `*_meta` fields, plus full event/change stability |
| **Asset summary depth** | Technical only | + support/resistance, basic fundamentals | + sector context, advanced fundamentals |
| **Watchlist tickers** | 10 | 50 | 100 |
| **Historical snapshots** | 30 days lookback | 2 years lookback | 5 years lookback |
| **Cross-asset correlation** | No | Yes | Yes |
| **Webhooks** | None | 1 URL, all events | 3 URLs, all events |
| **Daily request limit** | 250 | 50,000 | 100,000 |
| **Support** | None | Email (48hr) | Email (48hr) |

### Key Plus-only features (not available on Free)
- Band stability metadata on summaries when requested (`_meta` sibling objects with `stability`, `periods_in_current_state`, `flips_recent`, `flips_lookback`), events (`stability_at_entry`, `flips_recent_at_entry`), and watchlist changes
- Support/resistance levels on summaries
- Fundamental data on summaries (valuation, growth, earnings, analyst consensus)
- Cross-asset event correlation (`context_ticker`, `context_field`, `context_band` on events endpoint)
- Historical date snapshots beyond 30 days (`date` parameter — Free gets 30 days, Plus gets 2 years)
- Hourly rate limit bucket (5,000/hr vs 50/hr on Free)

### Key Pro-only features (not available on Plus)
- Sector context on summaries (`rsi_zone`, `asset_vs_sector_rsi`, `agreement`, `oversold_count`, `overbought_count`, `breakout_count`, etc.)
- Advanced fundamental fields (`pe_vs_historical_zone`, `pe_vs_sector_zone`, `pb_vs_historical_zone`, `analyst_consensus_direction`, etc.)
- 5-year historical lookback (vs 2 years on Plus)
- 100-ticker watchlist (vs 50 on Plus). Business plans get 200/500 watchlist.

### Business plans
Plus and Pro each have a Business variant with higher request limits (250k–500k/day), larger watchlists (200–500 tickers), and team seats. Business plans are for internal organizational use only.

### When to mention upgrades
- When a user hits a **403 `tier_restricted`** error — tell them which tier they need and link to pricing.
- When a user hits a **429 `rate_limit_exceeded`** error — suggest upgrading for higher limits.
- When a user asks for a feature that requires a higher tier (historical data, more watchlist tickers, stability metadata, fundamentals).
- When a user explicitly asks about pricing, plans, or upgrading.
- **Always link to https://tickerdb.com/pricing** — never guess at prices, just send them to the page.

## Caching

All data is pre-computed after market close. Daily refreshes publish around 00:30 UTC, and responses include `as_of_date` so you can see which session date the snapshot represents. Weekly refreshes occur after Friday close. Responses are edge-cached with `Cache-Control` and `ETag` headers.

## Usage Guidelines

1. **Never try to get raw OHLCV from TickerDB** — it only serves derived categorical data.
2. **Always use uppercase tickers.** Crypto must include `USD` suffix.
3. **Use `/summary/TICKER` for current snapshots** — deep dive on any single ticker's categorical state.
4. **Use `/summary/TICKER?start=...&end=...` for historical snapshots** — see how categorical bands evolved over a date range.
5. **Use `/summary/TICKER?field=...` for band transition history** — use the same full field names returned by `/v1/schema/fields` (for example `momentum_rsi_zone`, `extremes_condition`, or `trend_distance_ma50`) to find when a ticker entered a specific band, how long it stayed, and what happened afterward. Add `&band=...` to filter. MA distance fields also support grouped `above` / `below` aliases. Supports cross-asset correlation with `context_*` params.
6. **Use `/search` to find assets by state** — pass a JSON array of `{field, op, value}` filters using canonical flat schema names from `/v1/schema/fields` (for example `momentum_rsi_zone`) to discover tickers matching categorical conditions.
7. **Use `/schema/fields` to discover fields and bands** — get the full list of available fields, valid band values, and sectors.
8. **Use `/watchlist` for portfolio monitoring** — save tickers once with POST, then GET for live snapshots with `notable_changes`. Use `/watchlist/changes` for structured field-level diffs (day-over-day or week-over-week). The saved watchlist is also what webhooks track.
9. **Fundamental fields only exist for stocks** — don't expect valuation/growth/earnings on crypto or ETFs.
10. **Historical snapshots** — Free tier gets 30 days of lookback. Plus gets 2 years. Pro gets 5 years.
11. **Data refreshes EOD** — don't poll for intraday changes.
12. **Link to https://tickerdb.com/pricing when users ask about upgrading, plans, or hit tier/rate limits.** Don't guess at prices — just send the link.
13. **Band stability metadata (Plus/Pro)** tells you how much to trust a band value: `fresh` = just changed, `holding` = recent change that's staying, `established` = held a long time, `volatile` = flipping frequently. Summary keeps `_meta` off by default, so ask for `meta=true` or explicit `*_meta` fields when that context matters.
14. **Use webhooks for event-driven workflows** — instead of polling `/watchlist` on a cron, register a webhook and get notified only when something actually changes. This is ideal for AI agents that need to react to market shifts.
15. **Match natural language to endpoints:**
    - "How's AAPL?" -> `/summary/AAPL`
    - "Show me AAPL's history this year" -> `/summary/AAPL?start=2026-01-01`
    - "Check my portfolio" -> GET `/watchlist` (if they have a saved watchlist)
    - "When was AAPL last oversold?" -> `/summary/AAPL?field=momentum_rsi_zone&band=oversold`
    - "When did AAPL enter deep oversold as an extreme condition?" -> `/summary/AAPL?field=extremes_condition&band=deep_oversold`
    - "How many times has TSLA been deep_oversold?" -> `/summary/TSLA?field=momentum_rsi_zone&band=deep_oversold`
    - "What happened after NVDA entered strong_uptrend?" -> `/summary/NVDA?field=trend_direction&band=strong_uptrend`
    - "When was AAPL oversold while SPY was in downtrend?" -> `/summary/AAPL?field=momentum_rsi_zone&band=oversold&context_ticker=SPY&context_field=trend_direction&context_band=downtrend`
    - "When was BTC above the 50d while SPY was below the 50d?" -> `/summary/BTCUSD?field=trend_distance_ma50&band=above&context_ticker=SPY&context_field=trend_distance_ma50&context_band=below`
    - "Which stocks are oversold?" -> `/search?filters=[{"field":"momentum_rsi_zone","op":"eq","value":"deep_oversold"}]`
    - "What fields are available?" -> `/schema/fields`
    - "Add AAPL to my watchlist" -> POST `/watchlist` with `{"tickers": ["AAPL"]}`
    - "Remove TSLA from my watchlist" -> DELETE `/watchlist` with `{"tickers": ["TSLA"]}`
    - "What changed on my watchlist?" -> GET `/watchlist/changes`
    - "Weekly changes on my watchlist" -> GET `/watchlist/changes?timeframe=weekly`
    - "Notify me when my watchlist changes" -> POST `/webhooks`
    - "List my webhooks" -> GET `/webhooks`
    - "Check my account usage" -> GET `/account`

---

## Slash Commands

Users can invoke this skill directly with `/tickerdb` followed by a command:

### Account Commands
- `/tickerdb login` (alias: `/tickerdb signup`) — sign in or create an account. Prompt for email and let the user know this will sign them into their existing account or create a new one. Call `POST https://api.tickerdb.com/auth` with `{ "email": "<email>" }`, then respond with:
  > "Check your inbox for a 6-digit verification code from TickerDB. Once you have it, type: `/tickerdb verify <code>`"
- `/tickerdb verify <code>` — verify the 6-digit code. Call `POST https://api.tickerdb.com/auth/verify` with `{ "email": "<email>", "code": "<code>" }`. If the response contains `apiKey`, respond with:
  > "Your account is ready! Here's your API key:
  >
  > `tdb_xxxxxxxxxxxx`
  >
  > Save it by running:
  > ```
  > openclaw config set skills.tickerdb.apiKey tdb_xxxxxxxxxxxx
  > ```
  > Then type `/tickerdb help` to see everything you can do, or `/tickerdb cron` to set up a daily morning watchlist check."
  If they already have an account (no `apiKey` in response), respond: "Looks like you already have an account. Grab your API key from https://tickerdb.com/dashboard, then run: `openclaw config set skills.tickerdb.apiKey <your key>`"
- `/tickerdb status` — show current account status: whether `TICKERDB_KEY` is set, and if so, make a test call to `/v1/account` to confirm it's valid and show plan/usage info.

### Help
- `/tickerdb help` — show all available commands. Respond with:
  > **TickerDB Commands**
  >
  > **Account**
  > `/tickerdb login` — sign in or create an account (alias: `/tickerdb signup`)
  > `/tickerdb verify <code>` — verify your 6-digit code
  > `/tickerdb status` — check if your API key is set and working
  >
  > **Lookup**
  > `/tickerdb AAPL` — full summary for any ticker
  > `/tickerdb summary AAPL 2026-01-01 2026-03-31` — historical categorical snapshots over a date range
  > `/tickerdb summary AAPL momentum_rsi_zone deep_oversold` — band transition history with aftermath data
  > `/tickerdb summary BTCUSD trend_distance_ma50 above --context SPY trend_distance_ma50 below` — MA distance lookback with cross-asset context
  > `/tickerdb search momentum_rsi_zone=deep_oversold` — find assets matching filter criteria
  > `/tickerdb schema` — list all available fields, bands, and sectors
  > `/tickerdb watchlist` — check your saved watchlist with live data
  > `/tickerdb watchlist add AAPL,TSLA,BTCUSD` — add tickers to your saved watchlist
  > `/tickerdb watchlist remove MSFT` — remove tickers from your watchlist
  > `/tickerdb account` — check usage and plan info
  >
  > **Webhooks**
  > `/tickerdb webhook add <url>` — register a webhook URL to receive push notifications
  > `/tickerdb webhook list` — list your registered webhooks
  > `/tickerdb webhook remove <id>` — remove a webhook
  >
  > **Automation**
  > `/tickerdb cron` — set up a daily morning watchlist check
  >
  > **Tips:** Crypto tickers need a `USD` suffix (e.g. `BTCUSD`). Data refreshes daily after market close. Save tickers to your watchlist, then use webhooks to get notified when something changes instead of polling.

### Automation
- `/tickerdb cron` — set up a daily scheduled watchlist check. Ask the user two questions: (1) what time they want the check (default: 9:35 AM ET, weekdays) and (2) which delivery channel they prefer (Slack, Telegram, WhatsApp, etc.). Then create the cron job with these defaults:
  - **Name:** `TickerDB morning watchlist`
  - **Schedule:** `35 9 * * 1-5` (or user's preferred time)
  - **Timezone:** `America/New_York`
  - **Session:** `isolated`
  - **Message:** `Run /tickerdb watchlist to check my saved watchlist. Flag any notable_changes and anything in an extreme condition. Then run /tickerdb watchlist changes to see what shifted overnight.`
  - **Delivery:** `announce` (or user's preferred channel)

### Watchlist Commands
- `/tickerdb watchlist` — show the user's saved watchlist with live data. Call `GET /v1/watchlist`. Display each ticker's key indicators (trend, RSI zone, extremes, notable changes). If the watchlist is empty, suggest adding tickers with `/tickerdb watchlist add`.
- `/tickerdb watchlist add <tickers>` — add tickers to the saved watchlist. Parse comma-separated tickers from the command, then call `POST /v1/watchlist` with `{"tickers": [...]}`. Report what was added vs already saved, and show the current count/limit (e.g. "3 / 50 tickers saved"). If the user hits the tier limit, tell them and link to https://tickerdb.com/pricing.
- `/tickerdb watchlist remove <tickers>` — remove tickers from the saved watchlist. Parse comma-separated tickers, then call `DELETE /v1/watchlist` with `{"tickers": [...]}`. Confirm what was removed and show the remaining count.
- `/tickerdb watchlist changes` — show what changed on the user's watchlist since the last pipeline run. Call `GET /v1/watchlist/changes`. Display each ticker that had changes with from→to values. If no changes, say "No state changes on your watchlist since the last run."
- `/tickerdb watchlist changes weekly` — same as above but with `?timeframe=weekly` for week-over-week changes.

### Webhook Commands
- `/tickerdb webhook add <url>` — register a webhook URL. Call `POST /v1/webhooks` with `{ "url": "<url>" }`. The response includes a `secret` — tell the user to save it immediately, as it won't be shown again. Respond with:
  > "Webhook registered! Here's your signing secret — save it now, it won't be shown again:
  >
  > `<secret>`
  >
  > TickerDB will POST to your URL after each daily/weekly pipeline run whenever something changes on your watchlist. Verify payloads using the `X-Webhook-Signature` header (HMAC-SHA256 of the request body, signed with this secret)."
  If the user is on the free tier and gets a 403, tell them webhooks require Plus or Pro and link to https://tickerdb.com/pricing.
- `/tickerdb webhook list` — list registered webhooks. Call `GET /v1/webhooks`. Show each webhook's URL, active status, and events. Include the count/limit (e.g. "1 / 1 webhook URLs used").
- `/tickerdb webhook remove <id>` — remove a webhook. Call `DELETE /v1/webhooks` with `{ "id": "<id>" }`. If the user doesn't know the ID, run `/tickerdb webhook list` first and let them pick.

### Market Data Commands
- `/tickerdb AAPL` — full summary for AAPL
- `/tickerdb summary AAPL 2026-01-01 2026-03-31` — historical snapshots over a date range
- `/tickerdb summary AAPL momentum_rsi_zone` — band transition history for a field
- `/tickerdb summary AAPL momentum_rsi_zone deep_oversold` — when was it last deep_oversold?
- `/tickerdb summary AAPL momentum_rsi_zone deep_oversold --context SPY trend_direction downtrend` — AAPL oversold while SPY was in downtrend
- `/tickerdb summary BTCUSD trend_distance_ma50 above --context SPY trend_distance_ma50 below` — BTC above the 50d while SPY was below the 50d
- `/tickerdb search momentum_rsi_zone=deep_oversold` — find assets matching filters
- `/tickerdb search trend_direction=strong_uptrend,sector=Technology` — combined filters
- `/tickerdb schema` — list all available fields, bands, and sectors
- `/tickerdb watchlist` — check saved watchlist with live data (GET)
- `/tickerdb watchlist add AAPL,TSLA,BTCUSD` — add tickers to saved watchlist (POST)
- `/tickerdb watchlist remove MSFT` — remove tickers from saved watchlist (DELETE)
- `/tickerdb watchlist changes` — field-level state changes since last run (GET)
- `/tickerdb watchlist changes weekly` — week-over-week state changes (GET)
- `/tickerdb account` — check usage and plan info

When a slash command is used, skip confirmation and go straight to the API call.

---

## Cron Job Examples

TickerDB's EOD data refresh (~00:30 UTC) makes it ideal for daily scheduled checks. Recommended cron patterns:

### Morning watchlist check (weekdays 9:35 AM ET — 5 min after market open)
```
openclaw cron add \
  --name "TickerDB morning watchlist" \
  --cron "35 9 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --message "Run /tickerdb watchlist to check my saved watchlist. Flag any notable_changes and anything in an extreme condition. Then run /tickerdb watchlist changes to see what shifted overnight." \
  --announce
```

### Weekly deep dive (Monday 9:45 AM ET)
```
openclaw cron add \
  --name "TickerDB weekly review" \
  --cron "45 9 * * 1" \
  --tz "America/New_York" \
  --session isolated \
  --message "Run /tickerdb watchlist changes weekly to check week-over-week state changes. For any ticker with significant changes, run /tickerdb summary <ticker> rsi_zone to check historical context." \
  --announce
```

### Tips for cron usage
- **Use isolated sessions** — TickerDB calls are self-contained and don't need conversation history.
- **Schedule after data refresh** — data updates ~00:30 UTC. Don't schedule before that or you get yesterday's data.
- **Weekdays only for stocks** — use `1-5` in the cron weekday field. Crypto updates daily including weekends.
- **Batch calls in one job** — combine multiple `/tickerdb` calls in a single cron message to save LLM tokens.
- **Use a cheaper model** — routine checks don't need Opus. Add `--model sonnet` to save costs.
- **TickerDB is pre-computed** — each call completes instantly (no request-time computation), so cron jobs finish fast.

