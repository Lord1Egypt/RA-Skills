---
name: oris
description: Give your OpenClaw agent the power to spend. Stablecoin payments, spending policies, and compliance — built-in.
version: 1.0.4
emoji: 💳
homepage: https://useoris.finance/docs/openclaw

metadata:
  openclaw:
    primaryEnv: ORIS_API_KEY
    requires:
      env:
        - ORIS_API_KEY
        - ORIS_API_SECRET
        - ORIS_AGENT_ID
      bins:
        - python
        - node
    mcpServers:
      oris:
        command: python
        args: ["-m", "oris_mcp.server"]
        cwd: ${SKILL_DIR}
        env:
          ORIS_API_KEY: ${ORIS_API_KEY}
          ORIS_API_SECRET: ${ORIS_API_SECRET}
          ORIS_AGENT_ID: ${ORIS_AGENT_ID}
          ORIS_BASE_URL: https://api.useoris.finance

install:
  - kind: uv
    path: .
    bins: []
---

# Oris Payments for OpenClaw

Oris is payment infrastructure for autonomous AI agents. Install this skill and your OpenClaw agent gains a verified identity (KYA — Know Your Agent), a non-custodial wallet, and programmable spending controls enforced on every transaction before execution.

## Setup

Get a free API key at [useoris.finance](https://useoris.finance), then run:

```bash
openclaw run oris setup
```

Setup takes about two minutes. It will:

1. Register your OpenClaw instance as a verified agent
2. Create a non-custodial ERC-4337 wallet on Base
3. Apply a default spending policy ($50 per transaction, $200 per day)

Your credentials are stored in your local OpenClaw config. They are used to sign authenticated requests to the Oris API (api.useoris.finance) when your agent performs payment operations.

## What your agent can do

**Send payments** — USDC, USDT, or EURC on Base, Ethereum, Polygon, Arbitrum, Solana, Avalanche, BSC, Optimism, and Celo. Supports x402, direct, ACP, MCP, UCP, Visa TAP, Mastercard Agentic Commerce, Solana Pay, and CCTP protocols.

**Check balance** — Query wallet balances across all chains before committing to a spending task.

**Review spending** — Get a daily, weekly, or monthly spending summary on request.

**Find and hire agents** — Search the Oris marketplace for AI agent services, place escrow-backed orders, and pay automatically on completion.

**Fund the wallet** — On-ramp from USD or EUR via bank transfer or card. Off-ramp back to a bank account.

**Get cross-chain quotes** — Route stablecoins across chains at the best available rate.

**Generate ZKP attestation** — Prove KYA status on-chain without revealing private details (Halo2 PLONK proof).

## Every payment goes through this pipeline

```
KYA check
→ Spending policy evaluation  (<10ms, Redis-cached)
→ Sanctions screening          (<100ms, OFAC + EU + UN lists)
→ On-chain execution
```

If any step fails, the payment is rejected — not delayed. The system is fail-closed. If the compliance engine is unreachable, the transaction does not go through.

## Spending policy

The default policy is conservative. You can adjust it from the [Oris dashboard](https://useoris.finance/dashboard) or in your OpenClaw config:

```json
{
  "oris": {
    "policy": {
      "max_per_transaction": 50,
      "max_daily": 200,
      "max_monthly": 2000,
      "allowed_chains": ["base", "polygon"]
    }
  }
}
```

## Available tools

| Tool | What it does |
|------|-------------|
| `oris_pay` | Send a stablecoin payment |
| `oris_check_balance` | Query wallet balances across chains |
| `oris_get_spending` | Spending summary (day / week / month) |
| `oris_find_service` | Search the Oris agent marketplace |
| `oris_place_order` | Buy a service from another agent |
| `oris_approve_pending` | Approve an escalated payment |
| `oris_fiat_onramp` | Fund wallet from fiat (USD/EUR) |
| `oris_fiat_offramp` | Withdraw to bank account |
| `oris_exchange_rate` | Fiat/stablecoin exchange rate |
| `oris_cross_chain_quote` | Cross-chain transfer quote and routing |
| `oris_get_tier_info` | KYA tier, limits, and current usage |
| `oris_generate_attestation` | ZKP proof of KYA status |
| `oris_promotion_status` | Tier upgrade eligibility and progress |

## Supported networks and assets

**Chains:** Base, Ethereum, Polygon, Arbitrum, Solana, Avalanche, BSC, Optimism, Celo
**Stablecoins:** USDC, USDT, EURC
**Protocols:** x402, direct, ACP, MCP, UCP, Visa TAP, Mastercard Agentic Commerce, Solana Pay, CCTP

## Enterprise and compliance

Every transaction generates an immutable audit trail accessible via the Oris dashboard or API. KYA levels scale from basic verification (L1) to behavioral baseline (L3, earned after 30 days of clean operation). Suitable for regulated deployments including financial services, healthcare, and legal.

## Support

- Docs: [useoris.finance/docs](https://useoris.finance/docs)
- Discord: [discord.gg/oris](https://discord.gg/oris) — `#openclaw` channel
- GitHub: [github.com/fluxaventures/oris](https://github.com/fluxaventures/oris)
- Enterprise: sales@fluxa.ventures

---

*Oris is a Fluxa Ventures product. Licensed MIT.*
