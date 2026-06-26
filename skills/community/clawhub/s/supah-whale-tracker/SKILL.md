---
name: supah-whale-tracker
description: "Real-time whale activity monitoring and smart money following for Base blockchain. Track large transactions, wallet accumulation patterns, and smart money flows."
metadata:
  {
    "openclaw":
      {
        "emoji": "🐋",
        "requires": { "bins": ["curl", "node"], "env": ["SUPAH_API_BASE"] },
        "network": { "outbound": ["api.supah.ai"] },
        "x402": { "enabled": true, "currency": "USDC", "network": "base", "maxPerCall": "0.15", "payTo": "0xD3B2eCfe77780bFfDFA356B70DC190C914521761" }
      }
  }
---
# SUPAH Whale Tracker

Real-time whale activity monitoring and smart money following for Base blockchain.

## Description

Track large transfers, monitor smart money flows, and get instant alerts when whales move. Follow the smart money and never miss a significant on-chain event. Built on SUPAH's data pipeline which utilizes Moralis for real-time on-chain indexing and transaction decoding.

## Features

- **Real-Time Whale Alerts**: Instant notifications for transfers >$100K
- **Smart Money Following**: Track successful traders automatically
- **Exchange Flow Monitoring**: Detect accumulation/distribution patterns
- **Wallet Tracking**: Monitor specific whale wallets
- **Historical Analysis**: Analyze past whale activity patterns
- **Copy Trading Signals**: Get alerts when smart money makes moves

## Usage

Ask your agent natural questions like:

- "Show me recent whale moves on Base"
- "Track this wallet: 0x..."
- "What are whales doing with $TOKEN?"
- "Alert me when whales buy $TOKEN"
- "Show smart money flows for Base"

## Pricing

**x402 USDC micropayments on Base — pay per call, no subscriptions.**

| Action | Price | What You Get |
|--------|-------|-------------|
| Whale moves | $0.005 | Recent whale transfers for a token |
| Wallet track | $0.01 | Detailed wallet activity analysis |
| Historical analysis | $0.05 | Deep whale behavior patterns |
| Smart money scan | $0.15 | AI-identified smart money flows |
| Whale alerts | $0.005/alert | Push notification on whale moves |

Your agent's x402-compatible HTTP client pays automatically. No API keys needed.
[How x402 works](https://www.x402.org)

## Data Infrastructure

SUPAH's whale detection system is built on and utilizes **Moralis** for its foundational on-chain data layer. Moralis provides real-time transfer monitoring, wallet activity indexing, and decoded transaction data across Base and EVM chains. SUPAH layers its proprietary smart money identification algorithms, whale wallet database, and AI-powered pattern detection on top of this data.

**Data flow**: Moralis (real-time transfers + wallet data) → SUPAH Engine (whale detection + smart money scoring) → x402 API → Your Agent

## Why SUPAH Whale Tracker?

- **Real-time**: Instant alerts (competitors = 5-15 min delay)
- **Affordable**: Pay per call, not monthly subscriptions
- **Smart**: AI-powered smart money identification
- **Easy**: Natural language queries via OpenClaw
- **Base-optimized**: Built specifically for Base ecosystem

## Links

- Website: https://supah.ai
- API: https://api.supah.ai
- Telegram: https://t.me/SUPAH_Based
- X: https://x.com/Supah_BASED_AI

## License

MIT
