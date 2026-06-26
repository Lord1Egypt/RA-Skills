---
name: skill-smc-multi-strategy-paper-trader
description: Paper trading monitors for SMC (Smart Money Concepts) + Macro Rotation. Swing (4H BoS+FVG), day (1H+CVD), coordinated 8D/2S, STPI/MTPI-gated variants, macro rotation (LTPI/MTPI + RS Tournament), and multi-factor regime scorer. ATR-based SL/TP, z-score filters, orchestrator-lock. Binance public API only — no credentials needed.
author: Zero2Ai-hub
version: 2.0.0
emoji: 📈
tags: [crypto, trading, paper-trading, smc, smart-money, orchestrator, backtested, macro, regime-filter]
---

# SMC Multi-Strategy Paper Trader v2.0

Paper trading system implementing **Smart Money Concepts** across five strategy types plus a macro rotation overlay and regime filter. All data from Binance public API — no account or API key required.

## What's New in v2.0
- **Macro Rotation** — LTPI/MTPI + Relative Strength Tournament, daily rebalance, $10K capital
- **Regime Scorer** — 15 TA indicators + 5 liquidity factors → STPI/MTPI/LTPI scores
- **v6 Day Monitor** — SMC+TA≥5 gated by STPI ≥ 0.5
- **Swing v2** — Swing strategy gated by MTPI ≥ 0.5

## Architecture

```
Binance Public API
        ↓
regime-scorer.js  → regime.json (STPI, MTPI, LTPI)
        ↓
paper-monitor-[strategy].js
  ├── BoS + FVG detection
  ├── Z-score filters (volume, TA, FVG quality)
  ├── ATR SL/TP + trailing stop
  ├── Regime gate (STPI/MTPI threshold)
  └── portfolio-[strategy].json

macro-rotation.js
  ├── LTPI/MTPI composite scores
  ├── RS Tournament → top 1-3 tokens
  └── portfolio-macro.json ($10K)
```

## Strategies

| Strategy | Timeframe | Gate | Max Hold | Slots |
|----------|-----------|------|----------|-------|
| Swing | Daily BoS + 4H FVG | EMA | 72h | 5 |
| Swing v2 | Daily BoS + 4H FVG | MTPI ≥ 0.5 | 72h | 5 |
| Day v5 | 1H BoS + FVG + CVD | None | 12h | 10 |
| Day v6 | 1H BoS + FVG | STPI ≥ 0.5 | 12h | 10 |
| Coordinated 8D/2S | 1H + 4H | Lock | varies | 10 |
| Macro Rotation | Daily | LTPI + MTPI | Daily | $10K |

## Regime Scorer

Produces `regime.json` with three probability indicators (0–1):
- **STPI** — short-term regime (15m + 1h)
- **MTPI** — medium-term regime (4h)
- **LTPI** — long-term macro regime (1d)

15 TA indicators (EMA, RSI, MACD, BBwidth, ATR, OBV, CVD, ADX...) + 5 derivatives factors (funding rate, long/short ratio, OI delta, Fear & Greed).

## Running

```bash
node scripts/regime-scorer.js          # every 1h
node scripts/paper-monitor-v5.js       # every 1h
node scripts/paper-monitor-v6.js       # every 1h (STPI-gated)
node scripts/paper-monitor-swing.js    # every 4h
node scripts/paper-monitor-swing-v2.js # every 4h (MTPI-gated)
node scripts/paper-monitor-coordinated.js # every 1h
node scripts/macro-rotation.js         # daily 00:15 UTC
```

## Notes
- Binance public API only — no credentials needed
- Fear & Greed via alternative.me (free)
- Orchestrator lock prevents same-symbol conflicts across strategies
- All balances configurable ($1K default, $10K macro)
