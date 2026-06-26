# RiskState API v1 Documentation

Pre-trade risk permissions for BTC/USD and ETH/USD. Spot, perpetual futures (perps), and DeFi borrowing aware.

> **USD-denominated:** All scoring is based on BTC/USD and ETH/USD price action, derivatives, and macro conditions. If you trade non-USD pairs (e.g., BTC/EUR, ETH/BTC), additional cross-rate risk is not covered by this API.

## Endpoint

```
POST /v1/risk-state
```

## Authentication

All requests require a Bearer token in the `Authorization` header.

```
Authorization: Bearer <your_api_key>
```

### Key types

| Type | Format | Rate limit | Access |
|------|--------|------------|--------|
| **Owner** | `RISKSTATE_API_KEY` env var | Unlimited | All endpoints |
| **External** | `rs_live_` + 64 hex chars | 60 req/min | `/v1/risk-state` + read-only endpoints |

### Getting an API key

Request API access at [https://riskstate.ai](https://riskstate.ai) — only an email is required. You'll receive an `rs_live_` key via email within minutes.

Keys are managed through the `/api/api-keys` admin endpoint (owner-only).

The endpoint **fails closed**: if the server secret is not configured, all requests are denied (401). Rate-limited requests return 429 with `retry_after_seconds: 60`.

## Request

### Headers

| Header | Required | Value |
|--------|----------|-------|
| `Authorization` | Yes | `Bearer <token>` |
| `Content-Type` | Yes | `application/json` |

### Body (JSON)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `asset` | string | `"BTC"` | Asset to evaluate. `"BTC"` or `"ETH"`. |
| `wallet` | string | `null` | Ethereum wallet address (0x...) for DeFi position data. Optional. |
| `protocol` | string | `"spark"` | DeFi lending protocol. `"spark"` or `"aave"`. Only used when `wallet` is provided. |
| `include_details` | boolean | `false` | Include expanded scoring details in response. |
| `reference_time` | number | `now` | Unix seconds. Pins `daysSinceHalving` and the policy hash to a single timestamp, enabling bit-exact reproducibility. Must be in `[halving, now+1d]`. |
| `allow_degraded` | boolean | `false` | If `false` (default), the endpoint returns **503 Core data unavailable** when any of `price`, `rsi`, `funding` are missing upstream. Set to `true` to receive a degraded policy (with `data_integrity` capped). |

### Example requests

**Minimal (BTC):**

```bash
curl -X POST https://api.riskstate.ai/v1/risk-state \
  -H "Authorization: Bearer $RISKSTATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asset": "BTC"}'
```

**Detailed (with scoring breakdown):**

```bash
curl -X POST https://api.riskstate.ai/v1/risk-state \
  -H "Authorization: Bearer $RISKSTATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asset": "BTC", "include_details": true}'
```

**DeFi monitoring (with wallet + Aave):**

```bash
curl -X POST https://api.riskstate.ai/v1/risk-state \
  -H "Authorization: Bearer $RISKSTATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asset": "ETH", "wallet": "0xYOUR_WALLET_ADDRESS", "protocol": "aave", "include_details": true}'
```

> **Note:** All parameters go inside the `-d` JSON string. The `\` at the end of each line is a shell line continuation — the entire command is one curl call.

### Validation

- `asset` must be `"BTC"` or `"ETH"` (case-insensitive) → 400 otherwise
- `wallet` must match `^0x[a-fA-F0-9]{40}$` if provided → 400 otherwise
- `protocol` must be `"spark"` or `"aave"` (case-insensitive) → 400 otherwise
- `reference_time` must be a finite number in `[new Date('2024-04-20').getTime()/1000, now+86400]` if provided → 400 otherwise
- Invalid JSON body → 400
- Core data missing (and `allow_degraded` not set) → **503** with `Retry-After: 30` and body `{ error, missing, sources, retry_after_seconds, hint }`

### Determinism contract (v1.2.0)

The policy hash now includes `api_version`, `scoring_version`, `ts` (from `reference_time`), prices, indicators, **positioning** (funding percentile, OI z-score, squeeze direction), **macro** (regime, coupling, DXY), **volatility** (regime + score), **cycle** (phase, MVRV percentile, boost flag), composite, and policy binding. Given identical inputs and the same `reference_time`, the hash is bit-for-bit identical across requests.

## Response — Minimal (default)

Three blocks: **Permissioning**, **Classification**, **Auditability**.

### Permissioning

| Field | Type | Description |
|-------|------|-------------|
| `exposure_policy.max_size_fraction` | float (0–1) | Maximum position size as fraction of portfolio |
| `exposure_policy.leverage_allowed` | boolean | Whether leverage is permitted |
| `exposure_policy.max_leverage` | string | Maximum leverage for DeFi borrowing (`"0x"`, `"1x"`, `"1.5x"`, `"2x"`). For perps, use `max_size_fraction` as notional cap instead. |
| `exposure_policy.direction_bias` | string | `"LONG_PREFERRED"`, `"SHORT_PREFERRED"`, or `"NEUTRAL"` |
| `exposure_policy.reduce_recommended` | boolean | Agent should reduce exposure |
| `exposure_policy.allowed_actions` | string[] | Actions the agent MAY take (enum tokens, see reference below) |
| `exposure_policy.blocked_actions` | string[] | Actions the agent MUST NOT take (enum tokens, see reference below) |

### Classification

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `tactical_state` | string | BULLISH, LEAN BULL, NEUTRAL, LEAN BEAR, BEARISH | 24-72h directional tilt from composite |
| `structural_state` | string | Cycle phase | BTC: BOTTOM/EARLY/MID/LATE/EUPHORIA/CORRECTION/POST-PEAK. ETH: DEPRESSED/VALUE_ZONE/RECOVERY/EXTENDED/DISTRIBUTION |
| `macro_state` | string | RISK-ON, NEUTRAL, RISK-OFF | Macro regime from FRED data |
| `market_regime` | string | PANIC, EUPHORIA, SQUEEZE, TREND, RANGE | 5-state unified market regime |
| `volatility_regime` | string | LOW, NORMAL, HIGH, EXTREME | Volatility classification |
| `policy_level` | int | 1–5 | Informational classification. The `exposure_policy` fields are the binding constraints. 1=BLOCK Survival, 2=BLOCK Defensive, 3=CAUTIOUS, 4=GREEN Selective, 5=GREEN Expansion |
| `confidence_score` | float (0–1) | Signal agreement × data quality | Measures subscore agreement and data integrity. NOT a probability of market prediction accuracy. Higher = signals agree more and data is fresher. |
| `data_quality_score` | int (0–100) | % of data sources live | Percentage of data sources reporting live data. Different scale from `confidence_score` (0–1 factor). <70 = degraded, <50 = unreliable |

### Constraints & Flags

| Field | Type | Description |
|-------|------|-------------|
| `binding_constraint.source` | string | Which cap is limiting: `"RULES"`, `"DEFI"`, `"MACRO"`, `"CYCLE"` |
| `binding_constraint.reason` | string | Human-readable explanation (e.g., `"RISK-OFF × NORMAL"`) |
| `binding_constraint.reason_codes` | string[] | Machine-parseable reason tokens (e.g., `["MACRO_RISK_OFF", "COUPLING_NORMAL"]`) |
| `binding_constraint.cap_value` | float | The binding cap's value (0–1) |
| `risk_flags.structural_blockers` | string[] | Hard blockers — agent MUST pause new entries |
| `risk_flags.context_risks` | string[] | Soft risks — agent should reduce conviction |
| `defi` | object\|null | DeFi position data if wallet provided, else `null`. See fields below. |
| `defi.health_factor` | float | Current health factor (>1 = safe, <1.1 = danger) |
| `defi.ltv` | float | Current loan-to-value ratio % (debt / collateral × 100). E.g., 35.4 means 35.4% utilized. |
| `defi.max_ltv` | float | Protocol's maximum LTV threshold % (e.g., 82.99). Borrowing above this is blocked. |
| `defi.liquidation_threshold` | float | Liquidation threshold % (e.g., 82.5). Position liquidatable above this. |
| `defi.protocol` | string | `"spark"` or `"aave"` |

### Auditability

| Field | Type | Description |
|-------|------|-------------|
| `policy_hash` | string | SHA-256 hash of policy inputs for non-repudiation |
| `scoring_version` | string | `"score_v2"` — scoring algorithm version |
| `version` | string | `"1.2.2"` — API version |
| `timestamp` | string | ISO 8601 timestamp |
| `asset` | string | Asset evaluated |
| `cached` | boolean | Whether response was served from cache |
| `ttl_seconds` | int | Cache TTL in seconds (60). Agent should re-request after this interval for fresh data. |
| `key_type` | string | `"owner"` or `"external"` — identifies which auth tier was used |
| `stale_fields` | string[] | Core signals that are missing or stale |

## Response — Detailed (`include_details=true`)

All minimal fields plus:

| Field | Type | Description |
|-------|------|-------------|
| `caps.rules` | float | Rules cap (0–1) |
| `caps.defi` | float | DeFi health cap (0–1) |
| `caps.macro` | float | Macro regime cap (0–1) |
| `caps.cycle` | float | Cycle phase cap (0–1) |
| `caps.quality` | float | Quality factor (conflict × integrity) |
| `caps.data_integrity` | float | Data freshness score |
| `positioning.squeeze_direction` | string | UPSIDE, DOWNSIDE, TWO-SIDED, NONE |
| `positioning.squeeze_confidence` | int | 0–100 |
| `positioning.ls_crowding` | string | LONG_CROWDED, SHORT_CROWDED, BALANCED, etc. |
| `positioning.ls_crowding_score` | int | 0–100 |
| `positioning.funding_percentile` | int | Funding rate percentile vs 30d (0–100) |
| `positioning.oi_zscore` | float | OI z-score vs 30d |
| `positioning.basis_pct` | float | Perp-spot basis % |
| `volatility.regime` | string | LOW, NORMAL, HIGH, EXTREME |
| `volatility.score` | int | 0–100 |
| `whale_pressure.score` | int | 0–100 (9 proxy signals) |
| `whale_pressure.direction` | string | STRONG_BUY, BUY, NEUTRAL, SELL, STRONG_SELL |
| `trend_strength.score` | int | 0–100 |
| `trend_strength.direction` | string | STRONG_TREND, TREND, NEUTRAL, COUNTER_TREND, STRONG_COUNTER |
| `trend_strength.components` | object | `{ ma_cluster, expansion, flow_alignment }` (each 0–100) |
| `composite.overall` | int | 0–100 weighted composite score |
| `composite.subscores` | array | `[{ name, score, weight }]` — 7-8 subscores |
| `extreme_scores.panic` | int | 0–100 panic percentile |
| `extreme_scores.euphoria` | int | 0–100 euphoria percentile |
| `eth_structural` | object\|null | ETH structural score (ETH only): `{ overall, label, dataQuality, subfamilies: { network, supply, relative, demand } }` |
| `eth_downgrade` | object\|null | ETH structural downgrade (ETH only): `{ active, count, hardCount, softCount, severity, signals, capReduction }` |
| `macro_detail` | object | Full macro data for diagnostics: `{ regime, coupling, realRate10y, liquidityRegime, yield10y, yield10yChg, spxChangePct, fedBsDelta3m, spread10y2y, riskOffSignals, riskOnSignals, dxy }` |
| `data_sources` | object | Per-field source status (LIVE/MOCK/CG_FALLBACK/CC_FALLBACK/DEFAULT) |
| `core_missing` | string[] | Missing core signals |

## Error Responses

| Status | Body | Cause |
|--------|------|-------|
| 400 | `{ "error": "Invalid JSON body" }` | Malformed JSON |
| 400 | `{ "error": "Invalid asset. Must be BTC or ETH." }` | Unknown asset |
| 400 | `{ "error": "Invalid wallet address format." }` | Bad wallet format |
| 401 | `{ "error": "Unauthorized" }` | Missing or invalid Bearer token |
| 429 | `{ "error": "Rate limit exceeded", "retry_after_seconds": 60 }` | External key exceeded 60 req/min |
| 500 | `{ "error": "Internal server error" }` | Server-side failure |

## Data Sources & Fallback Chain

The endpoint fetches from 15+ external APIs in parallel waves. Binance returns HTTP 451 from Netlify servers, so all Binance data has fallbacks:

| Data | Primary | Fallback | Last Resort |
|------|---------|----------|-------------|
| RSI (4h) | Binance klines | CryptoCompare `histohour` | Default 50 |
| Funding rate | Binance `fundingRate` | OKX V5 → Bybit V5 → CoinGlass | Default 0 |
| Daily klines (200d) | Binance klines | CryptoCompare `histoday` | `null` (trend strength unavailable) |
| MVRV | blockchain.info | CoinGlass `/indicator/market/mvrv` | Default 1.8 |
| Real Rate | FRED T10YIE (breakeven) | — | `null` |
| Liquidity Regime | FRED WALCL (13-week delta) | — | `NEUTRAL` |
| Gold | Yahoo Finance | — | `null` |
| Macro regime + coupling | `/api/macro` (single source of truth) | — | `NEUTRAL` / `NORMAL` |
| ETH Structural | Lido + Ultrasound + DefiLlama (6 APIs) | — | Score defaults to 50 |
| SPX | Yahoo Finance (^GSPC) via macro.js | FRED SP500 (T-1 lag) | `null` |
| Staking APR | Lido `/apr/last` | Lido `/apr/sma` | Default 2.8% |

The `data_sources` field (in detailed response) shows per-field source: `LIVE`, `CC_FALLBACK` (CryptoCompare), `CG_FALLBACK` (CoinGlass), `ESTIMATED` (price-based), `DEFAULT_ZERO`, `DEFAULT`, or `MOCK`.

### Known Data Limitations (v1.2.0)

Binance returns HTTP 451 from Netlify servers. Current CoinGlass tier lacks certain endpoints. These cause permanent fallback states for some fields:

| Field | Server Status | Impact | Dashboard Comparison |
|-------|--------------|--------|---------------------|
| Funding | OKX or BYBIT fallback | Live data via cascading fallback chain. Neutral default (0) only if all fallbacks fail | Dashboard gets real data from browser-side Binance |
| Open Interest | OKX or BYBIT fallback | Live data via cascading fallback chain. Affects squeeze detection and OI z-score | Dashboard gets real data from browser-side Binance |
| MVRV | ESTIMATED (~price/$36K) | Accurate to ±5%. Affects cycle phase near thresholds | Dashboard gets real MVRV from blockchain.info |
| DXY | LIVE (Frankfurter EUR/USD proxy) | Same formula as dashboard. Affects detectRegime + macro scoring | Dashboard uses same Frankfurter proxy via market-data.js |

### API vs Dashboard Classification Alignment (v1.2.0, Mar 19 2026)

All classification fields now match between API and dashboard for the same market conditions:

| Field | Status | Notes |
|-------|--------|-------|
| cycle_phase | Aligned | Full 9-branch BTC classification (was simplified 6-branch) |
| market_regime | Aligned | DXY fix resolved false BEAR → TREND (was missing Frankfurter call) |
| macro_state | Aligned | Same macro.js as single source of truth |
| composite | Aligned | Same scoring-core.js functions |
| policy_level | Aligned | Same cap computation; DeFi cap differs when API called without wallet |

**Expected deltas** (not bugs — different data availability):
- **DeFi cap**: API=100% (no wallet) vs dashboard=84% (wallet connected) — pass `wallet` param to API for parity
- **Whale score**: ~9pt gap — browser computes 9 signals with real-time data; server has fewer
- **Trend strength**: ~3pt gap — minor data timing/source differences
- **Quality factor**: ~8pt gap — DeFi cap + subscore spread differences affect conflict_penalty

All other fields (RSI, daily klines, L/S ratio, CVD, ETF, exchange flow, macro, correlations, ETH structural) have working fallback chains.

## Caching Behavior

- **60-second TTL** via Netlify Blobs
- First call: 5–12 seconds (fetches from 15+ external APIs in 5 parallel waves)
- Subsequent calls within 60s: <1 second
- `cached: true` in response indicates cache hit
- **Wallet parameter bypasses cache** (DeFi data is personalized)

## Action Enums Reference

### `allowed_actions` values

| Token | Meaning | Policy Levels |
|-------|---------|---------------|
| `REDUCE` | Reduce existing exposure | 1 |
| `ADD_COLLATERAL` | Add collateral to DeFi position | 1 |
| `HEDGE` | Hedge existing positions | 1, 2 |
| `WAIT` | Wait for better conditions | 2, 3 |
| `REDUCE_LEVERAGE` | Reduce leverage on existing positions | 2 |
| `SCALP_SMALL` | Small scalp trades only | 2 |
| `RR_GT_2` | Trades with R:R > 2:1 only | 2, 3 |
| `DCA` | Dollar-cost averaging | 3, 4 |
| `LIGHT_ACCUMULATION` | Light spot accumulation | 3 |
| `LONG_SHORT_CONFIRMED` | Long or short with confirmation signals | 4 |
| `LEVERAGE_MODERATE` | Moderate leverage (up to 1.5x) | 4 |
| `TREND_FOLLOW` | Trend following strategies | 5 |
| `ADD_ON_PULLBACK` | Add to winners on pullbacks | 5 |
| `LEVERAGE_2X` | Leverage up to 2x | 5 |
| `AGGRESSIVE_ACCUMULATION` | Aggressive spot accumulation | 5 |

### `blocked_actions` values

| Token | Meaning | Policy Levels |
|-------|---------|---------------|
| `NEW_TRADES` | All new position entries blocked | 1 |
| `LEVERAGE` | Any leverage blocked | 1, 3 |
| `INCREASE_POSITION` | Increasing existing positions blocked | 1 |
| `LEVERAGE_GT_1X` | Leverage above 1x blocked | 2 |
| `AGGRESSIVE_LONG` | Aggressive long entries blocked | 2, 3 |
| `FOMO_ENTRY` | FOMO-driven entries blocked | 2 |
| `ALL_IN` | Full portfolio allocation blocked | 3, 4 |
| `LEVERAGE_GT_2X` | Leverage above 2x blocked | 4 |
| `COUNTER_TREND_SHORT` | Shorting against confirmed trend blocked | 5 |

### `binding_constraint.reason_codes` values

| Source | Possible codes | Example |
|--------|---------------|---------|
| RULES | `RULES_CRITICAL_{n}`, `RULES_WARNING_{n}` | `["RULES_CRITICAL_2", "RULES_WARNING_5"]` |
| DEFI | `DEFI_HF_LOW` | `["DEFI_HF_LOW"]` |
| MACRO | `MACRO_{regime}`, `COUPLING_{level}` | `["MACRO_RISK_OFF", "COUPLING_HIGH_COUPLING"]` |
| CYCLE | `CYCLE_{phase}` | `["CYCLE_MID"]`, `["CYCLE_EUPHORIA"]` |

## Risk Flags Reference

### Structural Blockers (agent MUST pause)

| Flag | Meaning |
|------|---------|
| `DEFI_LIQUIDATION_RISK` | Health Factor critically low |
| `SQUEEZE_RISK` | High-confidence directional squeeze |
| `MACRO_CONTAGION` | SPX/QQQ selloff >1.5% with normal or high coupling |
| `MACRO_RISK_OFF` | Macro regime risk-off with multiple signals |
| `ONCHAIN_EUPHORIA` | MVRV + NUPL at historical extremes |
| `EXTREME_FEAR` | F&G ≤ 10 (panic conditions) |
| `FUNDING_EXTREME` | Funding + RSI both extreme |
| `LIQUIDATION_CASCADE` | >$100M liquidations with asymmetry |

### Context Risks (agent should reduce conviction)

| Flag | Meaning |
|------|---------|
| `HIGH_FUNDING` | Funding rate elevated |
| `RSI_OVERBOUGHT` | RSI > 70 |
| `RSI_OVERSOLD` | RSI < 25 |
| `DXY_HEADWIND` | DXY > 104 |
| `YIELD_PRESSURE` | 10Y yield elevated or spiking |
| `HIGH_OI` | OI z-score > 2.0 (30d) |
| `BASIS_EXTREME` | Perp-spot basis > 0.15% |
| `WHALE_ACTIVITY` | Whale score ≥ 50 |
| `ETH_STRUCTURAL_WEAK` | ETH structural downgrade active |
| `ETH_SUPPLY_INFLATIONARY` | ETH supply strongly inflationary |
| `TREND_NOT_CONFIRMED` | Trend strength ≤ 45 with directional tilt |
| `NO_TREND` | Trend strength ≤ 20 |
| `HIGH_COUPLING` | High macro correlation |
| `SIGNAL_CONFLICT` | Subscore dispersion high |
| `LS_CROWDED` | L/S ratio extreme |
| `YIELD_SPIKE` | 10Y yield change > 0.08% in session |
| `CURVE_INVERTED` | 10Y-2Y spread < -0.2% |
| `REAL_RATE_HEADWIND` | Real rate > 1.5% |
| `LIQUIDITY_TIGHTENING` | Fed balance sheet shrinking (3m delta < -1%) |
| `STAKING_HEADWIND` | Real rate > ETH staking APR (ETH only) |
| `LIQUIDATION_ASYMMETRY` | >75% of liquidations on one side |

## How to Use by Context

The API returns the same response regardless of how you trade. The **market conditions assessment** (composite score, regime, policy level) is identical. What changes is how you **interpret the risk permissions** for your specific context.

### Spot Trading (BTC/USD or ETH/USD)

You are buying or selling the asset on a spot exchange (Coinbase, Binance Spot, Kraken, Uniswap, CoW Swap).

**Key fields:**
- `max_size_fraction` → **% of portfolio to deploy.** If 0.33, allocate up to 33% of your portfolio to this position.
- `direction_bias` → `LONG_PREFERRED` means "buy signal." `SHORT_PREFERRED` means "don't buy / consider selling." `NEUTRAL` means "no directional edge."
- `structural_blockers` → If non-empty, do not buy.
- `allowed_actions` / `blocked_actions` → Filter for relevant actions (DCA, WAIT, LIGHT_ACCUMULATION).

**Ignore for spot:** `max_leverage`, `leverage_allowed`, and leverage-related blocked actions (`LEVERAGE_GT_1X`, `LEVERAGE_GT_2X`). These apply to leveraged markets and DeFi borrowing.

**Pre-trade workflow:**
1. Call the API with `{"asset": "BTC"}`
2. Check `structural_blockers` — if non-empty, do not enter
3. Read `max_size_fraction` — this is your max allocation
4. Check `direction_bias` — respect the directional guidance
5. Proceed to your exchange and place the spot order

### Perpetual Futures (Perps)

You are trading BTC/USDT or ETH/USDT perpetuals on Binance Futures, Hyperliquid, dYdX, Bybit, or similar venues.

**Key fields:**
- `max_size_fraction` → **Max notional exposure as % of portfolio.** If 0.33 and your portfolio is $100K, your max notional is $33K. At 10x leverage, that means max $3.3K margin.
- `direction_bias` → Directly actionable: `LONG_PREFERRED` favors longs, `SHORT_PREFERRED` favors shorts.
- `structural_blockers` → If `SQUEEZE_RISK` is present, **do not open leveraged positions** — liquidation risk is elevated.

**Especially relevant for perps (in detailed response):**
- `positioning.funding_percentile` → How extreme the current funding rate is vs. 30 days. P>85 = paying heavy carry on longs. P<15 = shorts are crowded.
- `positioning.basis_pct` → Perp-spot premium. Positive = longs dominant, negative = discount.
- `positioning.squeeze_direction` → UPSIDE (short squeeze probable) or DOWNSIDE (long squeeze probable).
- `positioning.oi_zscore` → OI z-score vs. 30 days. >2.0 = excessive leverage in the market.

**Margin guide (from `max_size_fraction`):**

| Your leverage | Max margin (% of portfolio) | Example ($100K portfolio, max_size=0.33) |
|---------------|----------------------------|------------------------------------------|
| 3x | max_size / 3 = 11.0% | $11,000 margin |
| 5x | max_size / 5 = 6.6% | $6,600 margin |
| 10x | max_size / 10 = 3.3% | $3,300 margin |
| 25x | max_size / 25 = 1.3% | $1,300 margin |

> **Note:** RiskState does not impose a leverage cap for perpetual futures. The `max_leverage` field reflects DeFi borrowing constraints (see below). For perps, the binding constraint is `max_size_fraction` as max notional exposure — you choose your own leverage within that cap.

**Pre-trade workflow (e.g., Hyperliquid):**
1. Call the API with `{"asset": "BTC", "include_details": true}`
2. Check `structural_blockers` — if `SQUEEZE_RISK` present, do not open leveraged positions
3. Read `max_size_fraction` — this is your max notional as % of portfolio
4. Divide by your intended leverage to get max margin
5. Check `positioning.funding_percentile` — if P>85, longs are paying heavy carry
6. Check `positioning.squeeze_direction` — if DOWNSIDE, longs are at risk
7. Respect `direction_bias` for trade direction
8. Place your order on the venue

### DeFi Borrowing (Aave, Spark, Morpho)

You borrow stablecoins against BTC or ETH collateral on-chain.

**Key fields:**
- `max_size_fraction` → **% of collateral to deploy.** Accounts for your current health factor.
- `max_leverage` → Borrowing ratio cap: `"0x"` (don't borrow), `"1x"`, `"1.5x"`, `"2x"`.
- `defi.health_factor` → Current health factor (>1 safe, <1.1 danger).
- `defi.ltv` → Current loan-to-value ratio.
- `binding_constraint.source` → If `"DEFI"`, your on-chain position is the limiting factor.

**Pre-trade workflow:**
1. Call the API with `{"asset": "ETH", "wallet": "0xYOUR_WALLET", "protocol": "aave"}`
2. Check `defi.health_factor` — if <1.5, prioritize adding collateral
3. If `binding_constraint.source === "DEFI"`, do not increase debt
4. Respect `max_leverage` for borrowing ratio
5. If `structural_blockers` contains `DEFI_LIQUIDATION_RISK`, reduce position immediately

### AI Trading Agent Integration

You are building an autonomous trading agent (Hermes, ElizaOS, OpenClaw, AgentKit, custom) that calls the API programmatically.

**See [SKILL.md](SKILL.md) for the complete agent integration guide**, including:
- Binding precedence (evaluation order for response fields)
- Decision rules by policy level
- Failure modes and conservative fallback behavior
- Example requests

**Key principle:** Call the API **between decision and execution**. Your agent decides what to trade (intelligence layer). RiskState tells it **how much** it can risk (governance layer). Then the agent executes within those bounds.

## Interpretation Guide

### Position Sizing

**Spot:**
```
position_size = portfolio_value × max_size_fraction × conviction
```

**Perps:**
```
max_notional = portfolio_value × max_size_fraction × conviction
margin = max_notional / leverage
```

Where `conviction` is your own confidence factor (0–1), whether human or algorithmic.

### Re-consultation Frequency

| Use case | Recommended interval |
|----------|---------------------|
| Active trading (scalps, day trades) | Every 5 minutes |
| Swing trading (24h–72h holds) | Every 15 minutes |
| Holding / DCA | Every 4 hours |
| After significant move (>3% 1h) | Immediate |

### When to Force-Check

- Before any new position entry
- When `policy_level` was previously ≤ 2 (check if conditions improved)
- After external events (ETF announcements, Fed meetings, major hacks)

## Examples

### Pre-trade check (agent workflow)

```
1. curl -X POST https://api.riskstate.ai/v1/risk-state \
     -H "Authorization: Bearer $RISKSTATE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"asset": "BTC"}'
2. If structural_blockers non-empty → ABORT new entries
3. If blocked_actions contains NEW_TRADES → ABORT new entries
4. If reduce_recommended → reduce exposure (not necessarily close all)
5. Size position: max_size_fraction × agent_conviction
6. Respect max_leverage limit
7. Respect direction_bias for trade direction
8. Check allowed_actions before executing
9. If stale_fields non-empty or data_quality_score < 70 → halve size or abstain
10. policy_level is summary only — do not use for enforcement
```

### DeFi monitoring

```bash
curl -X POST https://api.riskstate.ai/v1/risk-state \
  -H "Authorization: Bearer $RISKSTATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asset": "ETH", "wallet": "0xYOUR_WALLET_ADDRESS_HERE", "include_details": true}'
```

The `defi` field will contain `health_factor` and `ltv` from Spark Protocol or Aave V3.
If `binding_constraint.source === "DEFI"`, the DeFi position is the limiting factor.
