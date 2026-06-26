# Spraay Openclaw — OpenClaw Skill 💧

Full Spraay x402 gateway interface for AI agents. Everything the gateway
offers in one skill.

## What This Skill Does

- **Payments** — Batch transfers, payroll, invoices
- **DeFi** — Swap quotes, token prices, balance queries
- **AI Inference** — 43+ models via Bittensor Subnet 64
- **Blockchain Data** — ENS resolution, chain info, endpoint discovery

Supports Base, Ethereum, Arbitrum, Solana, and 7 more chains.

## Important

**Financial transactions are irreversible.** This skill can move real tokens
and execute real trades. Always confirm with the user before executing.
x402 micropayment fees apply to paid endpoints.

## Install

```
clawhub install spraay-openclaw
```

Or from GitHub:

```
clawhub install github:plagtech/spraay-openclaw
```

## Requirements

- `curl` and `jq`
- `SPRAAY_GATEWAY_URL` (default: https://gateway.spraay.app)
- An x402-compatible wallet (Coinbase CDP or similar)
- No API key needed — uses x402 micropayments

## When to Use This vs Specialized Skills

| Need | Install |
|------|---------|
| Everything Spraay offers | **spraay-openclaw** (this) |
| Only batch payments | spraay-payments |
| Only AI inference | spraay-compute-futures |
| Only DeFi data | defi-intelligence |
| Multi-provider (Stripe + Coinbase + Spraay) | agent-payments |

## Links

- App: https://spraay.app
- Docs: https://docs.spraay.app
- MCP Server: https://smithery.ai/server/@plagtech/spraay-x402-mcp
- GitHub: https://github.com/plagtech

Built by [@plag](https://warpcast.com/plag)
