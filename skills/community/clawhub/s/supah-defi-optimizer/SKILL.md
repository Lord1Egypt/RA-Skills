---
name: supah-defi-optimizer
description: "DeFi yield optimization, impermanent loss tracking, and portfolio management for Base blockchain. Find the best yields, monitor LP positions, and optimize DeFi strategies."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔄",
        "requires": { "bins": ["curl", "node"], "env": ["SUPAH_API_BASE"] },
        "network": { "outbound": ["api.supah.ai"] },
        "x402": { "enabled": true, "currency": "USDC", "network": "base", "maxPerCall": "0.10", "payTo": "0xD3B2eCfe77780bFfDFA356B70DC190C914521761" }
      }
  }
---
# SUPAH DeFi Optimizer

DeFi yield optimization, impermanent loss tracking, and portfolio management for Base blockchain.

## Description

Auto-find best yields, get rebalancing suggestions, track impermanent loss, and optimize your DeFi positions with AI-powered recommendations. Built on SUPAH's data pipeline which utilizes Moralis for on-chain DeFi position indexing and protocol data.

## Features

- **Auto-Optimization**: Find best yields automatically
- **IL Calculator**: Track impermanent loss in real-time
- **Rebalancing**: Smart position adjustment suggestions
- **APY Comparison**: Compare yields across protocols
- **Yield Alerts**: Get notified of rate changes
- **Historical Tracking**: Monitor performance over time

## Usage

- "Show my DeFi positions: [wallet]"
- "Optimize my yield farming"
- "Compare APYs on Base"
- "Calculate IL for my position"
- "Suggest rebalancing for [wallet]"

## Pricing

**x402 USDC micropayments on Base — pay per call, no subscriptions.**

| Action | Price | What You Get |
|--------|-------|-------------|
| APY comparison | $0.02 | Top yields across Base protocols |
| IL calculation | $0.05 | Impermanent loss analysis for position |
| Position scan | $0.03 | All DeFi positions for a wallet |
| Optimization report | $0.10 | AI-powered rebalancing suggestions |
| Yield alert | $0.005/alert | Rate change notification |

Your agent's x402-compatible HTTP client pays automatically. No API keys needed.
[How x402 works](https://www.x402.org)

## Data Infrastructure

SUPAH's DeFi optimization engine is built on and utilizes **Moralis** for on-chain DeFi data — LP positions, protocol interactions, token approvals, and yield farming activity. SUPAH processes this through its proprietary optimization algorithms to generate actionable yield strategies and risk-adjusted recommendations.

**Data flow**: Moralis (DeFi positions + protocol data) → SUPAH Engine (yield optimization + IL calculation) → x402 API → Your Agent

## Links

- Website: https://supah.ai
- API: https://api.supah.ai
- Telegram: https://t.me/SUPAH_Based
- X: https://x.com/Supah_BASED_AI

## License

MIT
