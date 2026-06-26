---
name: supah-nft-intelligence
description: "NFT collection tracking, whale monitoring, and portfolio valuation for Base blockchain. Track floor prices, whale moves, and discover undervalued collections."
metadata:
  {
    "openclaw":
      {
        "emoji": "🖼️",
        "requires": { "bins": ["curl", "node"], "env": ["SUPAH_API_BASE"] },
        "network": { "outbound": ["api.supah.ai"] },
        "x402": { "enabled": true, "currency": "USDC", "network": "base", "maxPerCall": "0.05", "payTo": "0xD3B2eCfe77780bFfDFA356B70DC190C914521761" }
      }
  }
---
# SUPAH NFT Intelligence

NFT collection tracking, whale monitoring, and portfolio valuation for Base blockchain.

## Description

Track NFT floor prices, monitor whale NFT moves, analyze rarity, and value your NFT portfolio with real-time analytics. Built on SUPAH's data pipeline which utilizes Moralis for NFT metadata indexing, ownership tracking, and transfer monitoring.

## Features

- **Floor Price Tracking**: Monitor collection floors
- **Whale NFT Moves**: Alerts when whales buy/sell
- **Rarity Analysis**: Instant rarity scoring for any NFT
- **Portfolio Valuation**: Real-time NFT portfolio worth
- **Sale Alerts**: Notifications for collection sales
- **Collection Analytics**: Volume, holders, trends

## Usage

- "What's the floor price of [collection]?"
- "Track this NFT collection: [address]"
- "Value my NFT portfolio: [wallet]"
- "Show whale NFT moves on Base"

## Pricing

**x402 USDC micropayments on Base — pay per call, no subscriptions.**

| Action | Price | What You Get |
|--------|-------|-------------|
| Floor price | $0.01 | Current floor + 24h change |
| Rarity lookup | $0.02 | Rarity score + rank for any NFT |
| Portfolio valuation | $0.05 | Full NFT portfolio value |
| Collection analytics | $0.03 | Volume, holders, trends |
| Whale NFT alerts | $0.005/alert | Whale buy/sell notifications |

Your agent's x402-compatible HTTP client pays automatically. No API keys needed.
[How x402 works](https://www.x402.org)

## Data Infrastructure

SUPAH's NFT intelligence is built on and utilizes **Moralis** for NFT data indexing — metadata, ownership history, transfer events, and collection-level analytics. SUPAH adds proprietary rarity scoring, whale detection, and valuation algorithms on top.

**Data flow**: Moralis (NFT metadata + transfers) → SUPAH Engine (rarity scoring + valuation) → x402 API → Your Agent

## Links

- Website: https://supah.ai
- API: https://api.supah.ai
- Telegram: https://t.me/SUPAH_Based
- X: https://x.com/Supah_BASED_AI

## License

MIT
