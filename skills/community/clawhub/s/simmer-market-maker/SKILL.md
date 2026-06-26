---
name: simmer-market-maker
description: Places GTC limit orders on both sides (bid/ask) of liquid Polymarket markets. Finds active markets with >$10k 24h volume, mid-range prices, and ample time to resolve. Quotes spreads around the CLOB midpoint to capture bid/ask spread. Use when you want to passively earn spread as a market maker.
metadata:
  author: "PrYsM96"
  version: "1.2.0"
  displayName: "Simmer Market Maker"
  difficulty: "intermediate"
---

# Polymarket Market Maker

A market-making strategy that places GTC (Good-Till-Cancelled) limit orders on both sides of liquid Polymarket prediction markets, capturing the bid/ask spread.

## Strategy

1. **Market Selection:** Finds active markets with:
   - 24h volume > $10,000 (liquid enough to fill)
   - Price (YES probability) between 0.15 and 0.85 (avoids near-certain outcomes)
   - Resolves > 4 hours away (enough time to get fills)
   - No taker fees (`is_paid=False`) — 10% fee kills the edge

2. **Pricing:** Fetches the live CLOB midpoint for each market and quotes:
   - YES buy limit at `mid - 0.02` (2¢ below mid)
   - NO buy limit at `(1 - mid) - 0.02` (2¢ below NO mid)

3. **Order Management:** Cancels existing open orders before placing new ones each run.

4. **Limits:** Max $5 per order, max 3 markets per run.

## Requirements

**Environment variables (required):**

| Variable | Required | Description |
|----------|----------|-------------|
| `SIMMER_API_KEY` | ✅ Yes | Your Simmer API key — get it at simmer.markets/dashboard → SDK tab |
| `TRADING_VENUE` | Optional | `polymarket` (default) or `sim` for paper trading with virtual $SIM |

**Python dependency:** `simmer-sdk` — install with `pip install simmer-sdk`

## Setup

```bash
export SIMMER_API_KEY=sk_live_...         # required
export TRADING_VENUE=sim                   # optional: paper mode with $SIM
pip install simmer-sdk
```

## Usage

```bash
# Dry run (default)
python market_maker.py

# Live trading
python market_maker.py --live

# Show current positions
python market_maker.py --positions

# Show config
python market_maker.py --config

# Set config
python market_maker.py --set max_order_usd=10.0
```

## Config (env vars)

| Env Var | Default | Description |
|---------|---------|-------------|
| `SIMMER_MM_MAX_ORDER_USD` | 5.0 | Max USD per limit order |
| `SIMMER_MM_MAX_MARKETS` | 3 | Max markets per run |
| `SIMMER_MM_MIN_VOL_24H` | 10000 | Min 24h volume filter |
| `SIMMER_MM_SPREAD_OFFSET` | 0.02 | How far below mid to quote (2¢) |
| `SIMMER_MM_MIN_PRICE` | 0.15 | Min YES price to consider |
| `SIMMER_MM_MAX_PRICE` | 0.85 | Max YES price to consider |
| `SIMMER_MM_MIN_HOURS_TO_RESOLVE` | 4 | Min hours to resolution |
