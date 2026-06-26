---
name: vantage
description: "Vantage — Autonomous trading agent for Hyperliquid perpetual futures. Signal-to-execution in one loop. Runs on your machine. No cloud infra. No ongoing cost after purchase. Includes: live signal engine (funding rates, momentum, THORChain volume), Kelly criterion position sizing, EIP-712 signed order execution, paper trading mode, pre-flight setup validator, and profit sweep alerts."
metadata:
  {
    "openclaw": {
      "emoji": "📈",
      "requires": { "bins": ["node"] }
    }
  }
---

# Vantage — HL Autonomous Trading Agent

**Version:** 1.0.0  
**Author:** MoreBetter Studios (@morebetterclaw)  
**Product page:** https://morebetterstudios.com/products

---

## What It Does

Vantage runs a continuous signal → decision → execution loop on Hyperliquid perpetual futures.

```
Every N minutes (configurable)
  Signal Engine  →  funding rates + momentum + THORChain volume
    Decision Layer  →  Qwen (local) | OpenAI | rule-based fallback
      Kelly Sizing  →  live account balance × confidence × fraction
        Hyperliquid  →  signed market order (your private key)
          Profit Alert  →  log when balance exceeds threshold
```

All market data uses **public APIs only** — no external API keys required.

---

## Setup

```bash
npm install
cp .env.example .env
# Fill in your Hyperliquid private key + wallet address + trading limits
node src/setup-check.js   # validate before going live
```

---

## Usage

```bash
# Paper mode (no real orders)
node src/index.js start --paper

# Live trading
node src/index.js start

# Market data
node src/index.js hl-data RUNE
node src/index.js hl-arb BTC ETH RUNE

# Positions
node src/index.js hl-positions --paper
node src/index.js hl-positions 0xYourWallet

# Setup validator
node src/setup-check.js
```

---

## Configuration (`.env`)

| Variable | Required | Default | Description |
|---|---|---|---|
| `HYPERLIQUID_PRIVATE_KEY` | Yes | — | Your HL account private key |
| `HYPERLIQUID_WALLET_ADDRESS` | Yes | — | Your wallet address |
| `MAX_POSITION_SIZE_USD` | Yes | 500 | Hard cap per position |
| `MAX_OPEN_POSITIONS` | Yes | 3 | Max concurrent positions |
| `MAX_ACCOUNT_RISK_PCT` | Yes | 2 | Max % of balance per trade |
| `KELLY_FRACTION` | Yes | 0.25 | Kelly multiplier (0.25 = conservative) |
| `CRON_INTERVAL_MINUTES` | Yes | 60 | Scan frequency |
| `OLLAMA_URL` | No | — | Local Ollama (recommended) |
| `OLLAMA_MODEL` | No | qwen3.5:35b | Ollama model |
| `OPENAI_API_KEY` | No | — | OpenAI fallback |
| `PROFIT_SWEEP_ENABLED` | No | false | Enable profit sweep alerts |
| `PROFIT_SWEEP_THRESHOLD_USD` | No | 100 | Sweep trigger (USD) |

---

## Moving Funds Cross-Chain

- **Crypto Swap Agent** — [LINK TO BE UPDATED]
- **THORChain Swap Website** — [LINK TO BE UPDATED]

_(MoreBetter Studios products — morebetterstudios.com/products)_
