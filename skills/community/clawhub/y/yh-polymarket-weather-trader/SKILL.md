---
name: polymarket-weather-trader
description: >-
  Weather temperature prediction market trading on Polymarket via Simmer SDK.
  Uses NOAA (US) and Open-Meteo ensemble (international) forecasts as signal,
  EV/Kelly framework for sizing, Bayesian probability updates for open positions,
  and dynamic Maker/Taker strategy switching.
  Use when the user wants to: scan weather markets, execute temperature arbitrage trades,
  configure locations/thresholds, or view weather trading performance.
  Trigger words: weather market, temperature trade, NOAA forecast, simmer weather.
---

# Polymarket Weather Trader

## When to Use

Use this skill when the user wants to:
- Scan active weather markets on Polymarket
- Execute temperature forecast arbitrage trades (US via NOAA, international via Open-Meteo)
- View or configure weather trading parameters
- Check open positions or trading performance
- Switch between Simmer virtual ($SIM) and Polymarket real (USDC) trading

## Architecture

```
weather-trader/
├── weather_trader.py       # Main entry point (2732 lines)
├── ev_calculator.py        # EV + Kelly Criterion + longtail bias
├── bayesian_update.py      # Position probability management
├── maker_taker_arbiter.py  # Dynamic Maker/Taker mode switching
├── trade_performance.py    # Logging, circuit breaker, health score
├── performance_report.py   # Performance reporting CLI
├── smart_money_signal.py   # Whale tracking signal
├── config.json             # Trading parameters
├── test_ev_calculator.py   # Unit tests
├── test_noaa_calibration.py
└── trades.jsonl            # Append-only trade log
```

## Quick Start

```bash
cd weather-trader

python weather_trader.py                    # Dry run
python weather_trader.py --live            # Real trades (venue from .env)
python weather_trader.py --positions       # Show open positions
python weather_trader.py --config          # Show current config
python weather_trader.py --set entry_threshold=0.20
python weather_trader.py --live --quiet     # Silent for cron
python weather_trader.py --smart-sizing     # Portfolio-based sizing
python weather_trader.py --no-safeguards   # Disable safeguards (not recommended)
python weather_trader.py --resume          # Clear circuit breaker
```

## Venue and Live Mode

| Mode | Flag | Effect |
|------|------|--------|
| Dry run | (default) | No API calls, just analysis |
| Live | `--live` | Real API calls to `TRADING_VENUE` |
| Simmer $SIM | `.env: TRADING_VENUE=sim` | Virtual trading, $10k starting balance |
| Polymarket USDC | `.env: TRADING_VENUE=polymarket` | Real USDC |

## Supported Locations

**US cities (NOAA + MADIS, 16 cities):**
NYC, Chicago, Seattle, Atlanta, Dallas, Miami, Houston, Phoenix, Philadelphia, Boston, Denver, Las Vegas, San Francisco, Los Angeles, San Diego, Washington DC, Nashville

**International cities (Open-Meteo ensemble, 20+ cities):**
Tel Aviv, Munich, London, Tokyo, Seoul, Ankara, Lucknow, Wellington, Taipei, Shanghai, Beijing, Hong Kong, Singapore, Sydney, Melbourne, Paris, Berlin, Madrid, Rome, Amsterdam, Toronto, Vancouver, Shenzhen, Guangzhou, Chengdu, Mumbai, Delhi, Wuhan

Use `config.json` or `--set locations=NYC,London,Tokyo` to configure.

## Strategy Logic

```
Signal = NOAA/Open-Meteo forecast probability vs Polymarket market price
EV     = p × (1-price)/price - (1-p) × 1
Trade  = take if EV > 0 and price < entry_threshold
Size   = Kelly Criterion (Quarter Kelly = kelly_multiplier × full Kelly)
```

1. Fetch active weather markets from Simmer/Polymarket API
2. Parse market name → location + temperature bucket
3. Fetch weather forecast (NOAA for US, Open-Meteo ensemble for international)
4. Compute forecast probability → derive YES price estimate
5. Check EV gate, safeguards, slippage, time decay
6. Execute with Kelly sizing; apply longtail EV penalty for <20¢ contracts
7. Track open positions; apply Bayesian update if market moves against position
8. Exit when price > exit_threshold or position P&L drops below threshold

## Core Modules

### `ev_calculator.py` — EV + Kelly Framework

```
EV = (p × (1-price)/price) - ((1-p) × 1)
Quarter Kelly = full_Kelly × kelly_multiplier
```

- `calculate_ev(price, win_prob)` → EV per dollar
- `should_take_trade(price, win_prob, min_ev=0.0)` → bool gate
- `kelly_fraction(price, win_prob)` → full Kelly (0–1)
- `quarter_kelly_position(price, win_prob, bankroll, max_pos)` → USD amount
- `is_longtail_contract(price, cutoff=0.20)` → flag for <20¢ contracts
- `longtail_ev_adjustment(price, raw_ev)` → applies 20% penalty to longtail EV

### `bayesian_update.py` — Position Probability Management

- `bayesian_update(prior_prob, likelihood_ratio)` → posterior probability
- `compute_likelihood_ratio(new_price, old_price)` → odds ratio
- `should_update_probability(position_pnl_pct, threshold=-0.10)` → triggers on -10% PnL
- `should_close_position(updated_prob, initial_prob, threshold=-0.15)` → close if prob dropped >15%
- `compute_new_kelly_size(initial_prob, updated_prob, initial_kelly_size)` → rescales position

### `maker_taker_arbiter.py` — Strategy Mode Switching

| Condition | Mode | Maker / Taker |
|-----------|------|---------------|
| spread < 50bps AND vol < 50% | MAKER_HEAVY | 65% / 35% |
| spread < 50bps XOR vol < 50% | BALANCED | 50% / 50% |
| spread ≥ 50bps AND vol ≥ 50% | TAKER_HEAVY | 30% / 70% |

## Configuration (`config.json`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `entry_threshold` | 0.15 | Buy when price below this |
| `exit_threshold` | 0.45 | Sell when price above this |
| `max_position_usd` | 2.00 | Max USD per trade |
| `sizing_pct` | 0.05 | Smart sizing: % of balance per trade |
| `max_trades_per_run` | 5 | Max trades per scan cycle |
| `locations` | NYC | Comma-separated cities |
| `binary_only` | false | Skip range-bucket events |
| `slippage_max` | 0.15 | Skip if slippage exceeds this |
| `min_liquidity` | 0.0 | Skip markets below this liquidity |
| `use_kelly_sizing` | true | Use Kelly Criterion vs fixed % |
| `kelly_multiplier` | 0.25 | Kelly fraction (0.25 = Quarter Kelly) |
| `ev_min_threshold` | 0.0 | Min EV to take trade |
| `longtail_ev_penalty` | 0.20 | EV penalty for <20¢ contracts |
| `noaa_win_probability` | 0.85 | Base NOAA forecast win rate |
| `circuit_breaker_threshold` | 3 | Losses before pause |
| `circuit_breaker_cooldown` | 6 | Hours before auto-resume |
| `use_smart_money` | true | Enable whale signal integration |
| `smart_money_min_score` | 7 | Min whale score (0-10) |

## Performance & Monitoring

```bash
python trade_performance.py --health-score   # 0-100 health score
python trade_performance.py --auto-tune     # Suggest param adjustments
python trade_performance.py --changelog      # View param change history
python trade_performance.py --resume         # Force clear circuit breaker
```

- **Structured logging:** Every trade → `trades.jsonl` (JSONL, append-only)
- **Circuit breaker:** 3 consecutive real losses → 6-hour pause
- **Health scoring:** 4-component weighted score (0-100) with half-life decay
- **Changelog:** Immutable audit trail of parameter changes

## Risk Controls

- `TRADING_VENUE=sim` (virtual $SIM) or `polymarket` (real USDC)
- `--live` flag required for real API calls
- Circuit breaker auto-pause
- Max position per trade
- Slippage checks (skip if >15%)
- Time decay guard (skip if <2h to resolution)
- Min liquidity filter

## Changelog

### v2.1 (2026-04-08) — MADIS Bias Correction + Trade Log
- **MADIS airport-observation bias correction**: Compare MADIS current observation (airport实测) vs forecast temperature. If forecast is systematically warm or cold, adjust probability accordingly (max ±6% shift). This addresses the core issue identified in @runes_leo's weather trading experience: forecasts can have city-level directional biases.
- **Trade log for city-level bias learning**: Every executed trade now writes to `~/.hermes/weather-trade-log.jsonl` with: city, target_date, forecast_temp, bucket, price, noaa_probability (pre-correction), bias_adjustment, MADIS bias message, and signal data. Over time this builds a per-city forecast bias statistics database.

## Known Constraints

### Polymarket MIN_SHARES_PER_ORDER = 5

At $0.10/bucket → $0.50 minimum (OK)
At $0.20/bucket → $1.00 minimum (OK)
At $0.30/bucket → $1.50 minimum (blocks $1 trades)
At $0.50/bucket → $2.50 minimum (blocks $1 trades)

For small budgets ($1/position): only buckets ≤ $0.20 are tradeable.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "No live tradeable markets" | Markets off-hours or seasonal; check Polymarket directly |
| "CLOB price unavailable" | Polymarket CLOB down; script uses Simmer API fallback |
| "Circuit breaker TRIPPED" | Wait 6h or run `--resume` |
| "Balance shows $0" | Polymarket uses USDC.e (bridged), not native USDC |
| "Position too small for 5 shares" | Bucket price too high; lower budget or wait for cheaper buckets |
| NOAA SSL timeout | Normal; retry logic falls back to Open-Meteo |
| Discovery 429 rate limit | Expected during scan; trading continues from cached markets |
