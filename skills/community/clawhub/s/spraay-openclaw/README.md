# Spraay Openclaw — OpenClaw Skill 💧

Full Spraay x402 gateway interface for AI agents: payments, DeFi data, AI
inference, and blockchain data in one skill.

## What This Skill Does

- **Payments** — Batch transfers, payroll, and invoices on Base. The gateway
  returns unsigned transactions; the user's own wallet signs them.
- **DeFi data** — Swap quotes, token prices, wallet balances
- **AI Inference** — Open-weight models via Bittensor Subnet 64
- **Blockchain Data** — Basename and ENS resolution, gas and chain status for
  9 EVM chains, endpoint discovery

## Important

**Financial transactions are irreversible.** This skill prepares transactions
that move real tokens. It never signs on its own: every transaction is
decoded and checked locally, then confirmed by the user before signing.
x402 micropayment fees ($0.001–$0.10 in USDC on Base) apply to paid
endpoints.

## Install

```
clawhub install spraay-openclaw
```

## Requirements

- `curl` and `jq`
- `SPRAAY_GATEWAY_URL` set to `https://gateway.spraay.app`
- An x402 v2 compatible wallet client for micropayments
- No API key needed

## When to Use This vs the Specialized Skill

| Need | Install |
|------|---------|
| Payments, DeFi data, AI, and chain data together | **spraay-openclaw** (this) |
| Only batch payments and payroll | spraay-payments |

## Links

- App: https://spraay.app
- Gateway: https://gateway.spraay.app
- Docs: https://docs.spraay.app
- MCP Server: https://smithery.ai/server/@plagtech/spraay-x402-mcp
- GitHub: https://github.com/plagtech

Built by [@plag](https://warpcast.com/plag)
