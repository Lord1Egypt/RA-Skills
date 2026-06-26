---
name: yh-polymarket-smart-money
description: >
  Trade Polymarket markets where PolyClawster whale signals are active.
  Fetches smart money signals (score 0-10) and buys YES/NO on Polymarket when whales
  are positioned. Use when user wants to: follow whale traders, get smart money alerts,
  trade alongside institutional signals, or scan for high-conviction positions.
  Trigger words: whale trade, smart money, polyclawster, copy trade, follow whales.
metadata:
  author: "YHlorra"
  version: "1.0.0"
  displayName: "Polymarket Smart Money"
  difficulty: "intermediate"
---

# Polymarket Smart Money Trader

Follow whale and high-conviction trader signals on Polymarket via PolyClawster API.

## What It Does

1. **Fetches** active whale/trader signals from PolyClawster API (`polyclawster.com/api/signals`)
2. **Matches** signals to live Polymarket markets via Simmer SDK
3. **Trades** YES/NO based on signal direction and conviction score

## Quick Start

```bash
# Dry run (show opportunities, no trades)
python smartmoney_trader.py

# Live trading on Polymarket
python smartmoney_trader.py --live

# Only high-confidence signals (score 8+)
python smartmoney_trader.py --min-score 8

# Show current positions
python smartmoney_trader.py --status
```

## Signal Score

| Score | Conviction | Position Size Multiplier |
|-------|-----------|-------------------------|
| 7-8   | Medium    | 70-80% of max position  |
| 8-9   | High      | 80-90% of max position  |
| 9-10  | Very High | 90-100% of max position  |

Max position per trade: `$SIMMER_SMARTMONEY_MAX_POSITION` (default: $10)

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SIMMER_API_KEY` | required | From https://simmer.markets/dashboard |
| `TRADING_VENUE` | `polymarket` | `polymarket` for real USDC, `sim` for $SIM |
| `SIMMER_SMARTMONEY_MIN_SCORE` | `7` | Minimum signal score to trade |
| `SIMMER_SMARTMONEY_MAX_POSITION` | `10.0` | Max position size in USD |

## Architecture

```
smart-money-trader/
├── smartmoney_trader.py   # Main entrypoint (scan → match → trade)
├── smart_money_signal.py  # PolyClawster API client + signal normalization
└── clawhub.json           # ClawHub + Automaton config
```

## Risk Controls

- **Signal threshold**: Only trades scores ≥ `min_score` (default 7)
- **Position sizing**: Scales with conviction score (1.0x - 1.0x of max)
- **Venue guardrails**: `TRADING_VENUE=sim` for virtual, omit `--live` for paper
- **Circuit breaker**: 3 consecutive losses → pause (via Simmer SDK)
