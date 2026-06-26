---
name: trench
description: "Fast meme coin trading execution for AI agents. Snipe new token launches, execute rapid buys/sells on Solana DEXs (Jupiter, Raydium, Pump.fun), with MEV protection, auto-slippage, rug detection, and position management. Use when an agent needs to trade meme coins, snipe new pools, monitor token launches, or manage fast-paced degen positions on Solana."
---

# Trench 🪖

Fast meme coin trading execution skill for AI agents on Solana.

> ⚠️ This skill is under active development. Core modules coming soon.

## Capabilities (Planned)

### Execution
- Rapid buy/sell via Jupiter aggregator + Raydium direct
- Pump.fun token sniping and graduation tracking
- Jito bundle submission for MEV protection
- Priority fee optimization
- Auto-retry on failed transactions

### Intelligence
- New pool detection (Raydium, Pump.fun)
- Rug/honeypot detection (liquidity lock check, mint authority, top holders)
- Token safety scoring via Rugcheck API
- Real-time price feeds via DexScreener / Birdeye

### Position Management
- Auto take-profit / stop-loss
- Trailing stops
- Multi-wallet support
- PnL tracking per position

## Architecture

```
trench/
├── SKILL.md
├── scripts/
│   ├── buy.py           # Fast buy execution
│   ├── sell.py           # Fast sell execution
│   ├── snipe.py          # New pool sniper
│   ├── monitor.py        # Token monitor & alerts
│   ├── safety.py         # Rug detection & token analysis
│   └── portfolio.py      # Position & PnL tracking
└── references/
    ├── jupiter-api.md    # Jupiter V6 swap API reference
    ├── raydium.md        # Raydium pool interaction
    ├── jito-bundles.md   # Jito bundle submission
    └── pump-fun.md       # Pump.fun API & graduation mechanics
```

## Usage Examples

```
"Buy 0.5 SOL worth of POPCAT with 1% slippage"
"Snipe the next pump.fun graduation with 0.1 SOL"
"Set a 3x take-profit on my WIF position"
"Check if this token CA is safe: <address>"
"Show my open positions and PnL"
```
