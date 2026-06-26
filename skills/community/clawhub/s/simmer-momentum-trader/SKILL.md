---
name: simmer-momentum-trader
description: Momentum-based trading skill for Simmer prediction markets. Detects probability momentum and divergence to generate YES/NO trades on Polymarket. Remixable — swap in your own signal source or combine with other indicators.
author: "Joe"
version: "1.0.0"
displayName: "Simmer Momentum Trader"
difficulty: "intermediate"
---

# Simmer Momentum Trader

Trades prediction markets on Simmer using a **momentum + divergence** signal. When probability diverges from recent averages, it buys the underpriced side expecting mean reversion or continuation.

## What it does

1. Monitors markets from your Simmer watchlist
2. Calculates short-term momentum (recent probability vs. longer average)
3. Checks market context for flip-flop warnings and slippage
4. Executes trades when divergence exceeds threshold (default: 8%)

## Default signal

The default strategy uses a **price divergence** signal:
- If current probability is significantly above the recent average → momentum is pushing up → buy YES
- If current probability is significantly below → buy NO
- Threshold configurable via `DIVERGENCE_THRESHOLD` env var (default: 0.08)

> **This is a template.** The default signal is probability divergence — remix it with alternative signals like volume spikes, social sentiment, or your own model predictions. The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Setup

1. Set `SIMMER_API_KEY` in your environment
2. Optionally set `DIVERGENCE_THRESHOLD` (default: `0.08`)
3. Optionally set `TRADE_AMOUNT` (default: `5.0`)
4. Set `MARKET_IDS` to a comma-separated list of market IDs to monitor

## Remix guide

Swap in your own signal by replacing the `calculate_signal()` function in `simmer_momentum_trader.py`:

- **Volume-based**: Track trade volume spikes instead of price
- **Sentiment-based**: Feed in Twitter/Reddit sentiment scores
- **ML-based**: Use a trained model to predict outcomes
- **Combo**: Combine multiple signals with weighted scoring

The rest of the plumbing — market discovery, context checks, order execution, error handling — stays the same.

## Hard rules

- Always defaults to dry-run. Pass `--live` for real trades.
- Always tags trades with source and skill_slug for tracking.
- Always checks market context before trading (flip-flop detection, slippage).
- Reads API keys from env — never hardcodes credentials.
