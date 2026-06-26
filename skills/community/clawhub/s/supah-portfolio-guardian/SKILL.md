---
name: supah-portfolio-guardian
description: "Automated wallet monitoring with real-time alerts. Track portfolio value, detect suspicious transactions, monitor approvals, and get risk warnings across Base and EVM chains."
metadata:
  {
    "openclaw":
      {
        "emoji": "💼",
        "requires": { "bins": ["curl", "node"], "env": ["SUPAH_API_BASE"] },
        "network": { "outbound": ["api.supah.ai"] },
        "x402": { "enabled": true, "currency": "USDC", "network": "base", "maxPerCall": "0.10", "payTo": "0xD3B2eCfe77780bFfDFA356B70DC190C914521761" }
      }
  }
---
# SUPAH Portfolio Guardian Skill

**Category**: Crypto & DeFi  
**Tags**: base, portfolio-monitoring, risk-alerts, wallet-tracking, defi  
**Author**: SUPAH (@Supah_BASED_AI)  
**Version**: 1.0.0

## Description

Automated portfolio monitoring for Base blockchain. Watch wallets, get instant alerts on risky tokens, track position changes, and receive portfolio reports. Built on SUPAH's data pipeline which utilizes Moralis for real-time wallet activity indexing, token balance tracking, and transaction monitoring.

## Key Difference vs Base Intelligence

- **Base Intelligence**: Analyze individual tokens on-demand
- **Portfolio Guardian**: Monitor entire wallets continuously

## Usage

- "Watch my wallet 0x..."
- "Check my portfolio risks"
- "Show my watched wallets"
- "Get a portfolio health report"
- "Stop watching 0x..."

## Features

- **Continuous Monitoring**: Event-based tracking (new tokens, transfers, swaps)
- **Risk Alerts**: Instant notifications when portfolio risk increases
- **Portfolio Reports**: Comprehensive portfolio health summaries
- **Multi-Wallet**: Track multiple wallets
- **Smart Thresholds**: Auto-alert when risk scores drop below safe levels

## How It Works

1. **Add Wallet**: `watch wallet 0xYourAddress`
2. **Initial Scan**: SUPAH analyzes all tokens in wallet
3. **Continuous Monitor**: Watches for new tokens, risk changes, liquidity drains
4. **Smart Alerts**: Notified only when action needed (risky token, risk spike, large change)

## Pricing

**x402 USDC micropayments on Base — pay per call, no subscriptions.**

| Action | Price | What You Get |
|--------|-------|-------------|
| Portfolio scan | $0.05 | Full wallet risk analysis |
| Risk check | $0.02 | Current risk score + flagged tokens |
| Position history | $0.03 | Recent position changes |
| Health report | $0.10 | Comprehensive portfolio health |
| Risk alert | $0.005/alert | Push notification on risk change |

Your agent's x402-compatible HTTP client pays automatically. No API keys needed.
[How x402 works](https://www.x402.org)

## Data Infrastructure

SUPAH's portfolio monitoring is built on and utilizes **Moralis** for real-time wallet data — token balances, transaction history, approval events, and DeFi position tracking across Base and EVM chains. SUPAH processes this through its proprietary risk scoring engine to generate alerts and health assessments.

**Data flow**: Moralis (wallet activity + balances) → SUPAH Engine (risk scoring + alert logic) → x402 API → Your Agent

## Privacy

SUPAH never stores private keys. Monitoring is read-only via public blockchain data.

## Links

- Website: https://supah.ai
- API: https://api.supah.ai
- Telegram: https://t.me/SUPAH_Based
- X: https://x.com/Supah_BASED_AI

## License

MIT
