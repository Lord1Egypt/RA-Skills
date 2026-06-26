---
name: skill-smc-multi-strategy-paper-trader
description: Paper trading monitors for SMC (Smart Money Concepts) + Macro Rotation strategies. Includes swing (4H BoS+FVG), day (1H BoS+FVG+CVD), coordinated 8D/2S orchestration, STPI/MTPI-gated monitors, macro rotation (LTPI/MTPI + RS Tournament), and multi-factor regime scorer. ATR-based SL/TP, z-score filters, orchestrator-lock. Binance public API only — no credentials needed.
author: Zero2Ai-hub
version: 2.0.0
emoji: 📈
tags: [crypto, trading, paper-trading, smc, smart-money, orchestrator, backtested, macro, regime-filter]
---

# SMC Multi-Strategy Paper Trader v2.0

Paper trading system implementing **Smart Money Concepts** across five strategy types plus a macro rotation overlay and regime filter. All data from Binance public API — no account or API key required.

## What's New in v2.0
- **Macro Rotation** (`macro-rotation.js`) — LTPI/MTPI + Relative Strength Tournament, daily rebalance, $10K capital
- **Regime Scorer** (`regime-scorer.js`) — 15 TA indicators + 5 FRED liquidity factors → STPI/MTPI/LTPI scores
- **v6 Day Monitor** (`paper-monitor-v6.js`) — SMC+TA≥5 gated by STPI ≥ 0.5
- **Swing v2** (`paper-monitor-swing-v2.js`) — Swing strategy gated by MTPI ≥ 0.5

## Architecture

```
Binance Public API (Kline, Ticker, Funding, OI)
        ↓
regime-scorer.js  → regime.json (STPI, MTPI, LTPI)
        ↓
paper-monitor-[strategy].js
  ├── Fetch candles (1H/4H/1D)
  ├── Detect Break of Structure (BoS)
  ├── Find Fair Value Gaps (FVG)
  ├── Z-score: Volume, TA, FVG quality
  ├── ATR-based SL / TP / Trailing stop
  ├── Regime gate: STPI/MTPI threshold check
  ├── Orchestrator lock read/write
  └── portfolio-[strategy].json (P&L tracking)

macro-rotation.js
  ├── Daily candles + 7d close for all tokens
  ├── LTPI: M2/liquidity proxy via BTC dominance + funding
  ├── MTPI: momentum + derivatives composite
  ├── RS Tournament: z-scored returns → top 1-3 tokens
  └── portfolio-macro.json ($10K, daily rebalance)

paper-dashboard/index.html (5-curve equity chart)
```

## Strategies

| Strategy | File | Timeframe | Gate | Max Hold | Slots |
|----------|------|-----------|------|----------|-------|
| Swing | `paper-monitor-swing.js` | Daily BoS + 4H FVG | EMA | 72h | 5 |
| Swing v2 | `paper-monitor-swing-v2.js` | Daily BoS + 4H FVG | MTPI ≥ 0.5 | 72h | 5 |
| Day v5 | `paper-monitor-v5.js` | 1H BoS + FVG + CVD | None | 12h | 10 |
| Day v6 | `paper-monitor-v6.js` | 1H BoS + FVG | STPI ≥ 0.5 | 12h | 10 |
| Coordinated | `paper-monitor-coordinated.js` | 1H + 4H mixed | Lock | varies | 10 |
| Macro Rotation | `macro-rotation.js` | Daily candles | LTPI + MTPI | Daily | $10K |

## Regime Scorer

`regime-scorer.js` produces `regime.json` with three probability indicators:

- **STPI** (Short Term): 15m + 1h composite → fast regime
- **MTPI** (Medium Term): 4h composite → swing regime
- **LTPI** (Long Term): Daily composite → macro regime

Indicators per timeframe: EMA cross, ADX, MA200, RSI, MACD, BBwidth, ATR pct, OBV, CVD z-score, funding rate, long/short ratio, OI delta, Fear & Greed (macro only).

## Macro Rotation

LTPI/MTPI guide overall allocation:
- Both bearish → 100% CASH
- Mixed → reduced position count
- Both bullish → full RS Tournament deployment

RS Tournament: z-scored 7d returns across 30+ tokens → rotates into top 1-3 by strength.

## Orchestrator Lock

All SMC monitors share `orchestrator-lock.json` — prevents same-symbol entries across strategies:

```json
{
  "BTCUSDT": { "strategy": "swing", "entryTime": 1742400000000 },
  "ETHUSDT": { "strategy": "day",   "entryTime": 1742405000000 }
}
```

## Portfolio JSON Structure

```json
{
  "balance": 1000,
  "positions": [],
  "history": [],
  "metrics": { "totalTrades": 0, "wins": 0, "losses": 0, "winRate": 0 }
}
```

Macro: starts at $10,000.

## Running

```bash
# Regime (every 15m)
node scripts/regime-scorer.js

# Day v5: every 1h (XX:02)
node scripts/paper-monitor-v5.js

# Day v6 (STPI-gated): every 1h (XX:03)
node scripts/paper-monitor-v6.js

# Swing (EMA-gated): every 4h (XX:30)
node scripts/paper-monitor-swing.js

# Swing v2 (MTPI-gated): every 4h (XX:35)
node scripts/paper-monitor-swing-v2.js

# Coordinated 8D/2S: every 1h (XX:05)
node scripts/paper-monitor-coordinated.js

# Macro Rotation: daily (00:15 UTC)
node scripts/macro-rotation.js
```

## Cron Setup (OpenClaw)

```
Regime:           50 * * * *    (XX:50 UTC every 1h)
Day v5:           2 * * * *     (XX:02 UTC every 1h)
Day v6:           3 * * * *     (XX:03 UTC every 1h)
Swing:            30 */4 * * *  (XX:30 UTC every 4h)
Swing v2:         35 */4 * * *  (XX:35 UTC every 4h)
Coordinated:      5 * * * *     (XX:05 UTC every 1h)
Macro Rotation:   15 0 * * *    (00:15 UTC daily)
```

## Files

```
scripts/
  paper-monitor-swing.js         — swing (EMA-gated)
  paper-monitor-swing-v2.js      — swing (MTPI-gated, NEW v2.0)
  paper-monitor-v5.js            — day + CVD
  paper-monitor-v6.js            — day + STPI gate (NEW v2.0)
  paper-monitor-coordinated.js   — 8D/2S coordinated
  macro-rotation.js              — LTPI/MTPI + RS Tournament (NEW v2.0)
  regime-scorer.js               — Multi-factor regime scoring (NEW v2.0)
paper-dashboard/index.html       — 5-curve equity chart
```

## Notes
- Uses Binance **public** API only — no credentials required
- All start balances configurable (default: $1,000 day/swing, $10,000 macro)
- Fear & Greed Index via alternative.me API (free, no key)
- Orchestrator lock: internal coordination only, files stored locally
