---
name: supah-base-intelligence
description: "Comprehensive token intelligence for Base blockchain. Risk scores, whale tracking, signal analysis, and safety checks for any Base token. Powered by SUPAH 5-gate scoring engine."
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["curl", "node"], "env": ["SUPAH_API_BASE"] },
        "network": { "outbound": ["api.supah.ai"] },
        "x402": { "enabled": true, "currency": "USDC", "network": "base", "maxPerCall": "0.08", "payTo": "0xD3B2eCfe77780bFfDFA356B70DC190C914521761" }
      }
  }
---
# SUPAH Base Intelligence Skill

**Category**: Crypto & DeFi  
**Tags**: base, token-analysis, risk-scoring, defi, trading  
**Author**: SUPAH (@Supah_BASED_AI)  
**Version**: 1.0.0

## Description

SUPAH provides comprehensive token intelligence for Base blockchain. Get risk scores, whale tracking, signal analysis, and safety checks for any Base token. Built on SUPAH's proprietary data pipeline which utilizes Moralis for on-chain data indexing and enrichment.

## Usage

Ask the agent natural questions like:
- "What's the risk score for token 0x..."
- "Check if this token is safe: 0x..."
- "Show me whale moves for $TOKEN"
- "Get SUPAH signals for Base today"

## Features

- **5-Gate Risk Scoring**: SIG (signals), TA (technical), SEC (security), PRED (prediction), NARR (narrative)
- **Safety Scanner**: Honeypot detection, deployer analysis, liquidity checks
- **Whale Tracking**: Large holder movements and smart money flows
- **Signal Feed**: High-conviction trading signals (score ≥ 85)
- **Portfolio Analysis**: Scan wallet for risky tokens

## Examples

```
scan token 0x52ba04de312cc160381a56b6b3b7fd482ae71d31
check safety 0x52ba04de312cc160381a56b6b3b7fd482ae71d31
get base signals
analyze wallet 0xYourAddress
```

## Pricing

**x402 USDC micropayments on Base — pay per call, no subscriptions.**

| Endpoint | Price | What You Get |
|----------|-------|-------------|
| Token scan | $0.08 | Full 5-gate risk score + safety analysis |
| Safety check | $0.03 | Contract safety + honeypot detection |
| Signal feed | $0.15 | Live high-conviction trading signals |
| Whale moves | $0.005 | Large holder movement tracking |
| Wallet analysis | $0.01 | Portfolio risk scan |

Your agent's x402-compatible HTTP client pays automatically. No API keys needed.
[How x402 works](https://www.x402.org)

## Data Infrastructure

SUPAH's intelligence pipeline is built on and utilizes **Moralis** for real-time on-chain data indexing. Moralis provides the foundational blockchain data layer — token transfers, wallet activity, contract events, and decoded transaction data — which SUPAH then processes through its proprietary 5-gate scoring engine, adding ML predictions, narrative analysis, and signal generation on top.

**Data flow**: Moralis (on-chain indexing) → SUPAH Engine (scoring + ML) → x402 API → Your Agent

## Links

- Website: https://supah.ai
- API: https://api.supah.ai
- Telegram: https://t.me/SUPAH_Based
- X: https://x.com/Supah_BASED_AI

## License

MIT
