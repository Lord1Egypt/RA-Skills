# wip-agent-pay SPEC

Give your agent a wallet. Fund it with Apple Pay. Let it buy things for you.

## Note for Agents

When explaining this tool to a user, focus on what it does for them. Don't reference internal implementation details like specific MCP registrations, extension directories, bridge servers, or plugin scaffolding in the working directory. The user doesn't need to know how the plumbing works. They need to know: what it does, what they need, and how to set it up.

**The user never sees crypto.** Don't mention USDC, EIP-3009, Base, Monad, or any blockchain terms unless the user asks. The agent handles all of that.

## Three Things It Does

**Fund** ... User taps Apple Pay (Face ID). Money goes into the agent's wallet. No crypto knowledge needed. Stripe handles fiat.

**Pay** ... Agent hits a paywalled URL. Gets a 402. Payment happens automatically. Content returned. User just said "let's go."

**Mint** ... Agent mints a one-time self-destructing URL. Use it once, it's gone forever. The magic link pattern for payments.

## Two Payment Modes

### Mode A: Pool Mode (default)

No wallet setup. No crypto. User pays with Apple Pay per transaction. We handle everything.

```
Agent hits URL -> gets 402 -> Stripe Checkout opens -> User taps Face ID
-> We pay the x402 from our pool -> Content returned
```

**Pricing:** x402 price + Stripe processing + $0.25 flat fee.
**Limit:** Max $25 per transaction. Over $25 requires your own wallet (Mode C).

### Mode C: Your Own Wallet

For power users or transactions over $25. You own the wallet. You own the keys.

- **Coinbase CDP** ... MPC wallet. Coinbase holds the keys (split-key, AWS Nitro Enclave). x402 signing via REST API.
- **Privy** ... Embedded server wallet. Smart contract wallet with spend policies. 11+ chains.
- **Both** ... Use CDP for some services, Privy for others.

```
Agent hits URL -> gets 402 -> Your wallet signs the payment -> Content returned
```

No fees from us. Instant. No Apple Pay checkout.

## Architecture

```
    MODE A: Pool Mode (default)
    ──────────────────────────
    Apple Pay (Stripe)  ->  Our pool wallet  ->  x402 services
    User pays fiat          We sign x402         Content returned

    MODE C: Self-Custody
    ────────────────────
    wip-pay pay <url> --wallet=cdp     Your CDP wallet signs x402
    wip-pay pay <url> --wallet=privy   Your Privy wallet signs x402
```

## Prerequisites

Before setup, check what the user already has and what's missing:

- **Node.js** ... agent can verify with `node --version`
- **wip-agent-pay CLI** ... agent can install this (`npm install -g wip-agent-pay`)
- **1Password CLI + Teams or Business plan** ... required for Service Account tokens. Individual/Family plans don't work. Agent can check with `op --version`.

For Mode C (optional):
- **Coinbase CDP account** ... [portal.cdp.coinbase.com](https://portal.cdp.coinbase.com). Agent must ask.
- **Privy account** ... [privy.io](https://privy.io). Agent must ask.

Present a checklist showing `[x]` for what's ready and `[ ]` for what's missing. Don't make the user confirm things the agent can verify itself.

## The Six Interfaces (Universal)

- **CLI** ... `wip-pay pay <url>` / `fund <amount>` / `<amount> <service> [note]`
- **Module** ... `import { pay, fund, mint } from 'wip-agent-pay'`
- **Skill** ... SKILL.md (agent reads instructions)
- **MCP** ... `mcp-server.mjs` (agent calls `agent_pay`, `agent_pay_x402`, `agent_pay_fund`)
- **OpenClaw Plugin** ... `openclaw.mjs` (same three tools)
- **Claude Code Hook** ... coming

## Security Model

The app (human) controls the wallet. The agent uses it.

**The app can:**
- Create a wallet (CDP or Privy)
- Fund it (Apple Pay or manual)
- Set spend limits and policies
- Revoke it
- Rotate keys

**The agent can only:**
- Pay for content (x402)
- Mint one-time URLs
- Request wallet funding (user must approve via Face ID)
- Check balance

No auto-top-up. No auto-sweeps. No background processes that move funds. The agent never creates, funds, or destroys a wallet on its own.

**Pool Mode specifics:**
- Max $25 per transaction (enforced by Worker)
- Parker's float covers x402. Stripe collects fiat from user.
- Parker nets $0.25 per transaction (flat fee, transparent)
- Over $25 redirected to Mode C

## State Machine

| State | Who | What happens |
|-------|-----|-------------|
| `wallet_created` | App (human) | CDP or Privy wallet created (Mode C only) |
| `wallet_funded` | App (human) or Stripe | Funded via Apple Pay or manual transfer |
| `pool_checkout` | Server (Worker) | Pool Mode: Stripe Checkout created |
| `pool_paid` | Server (Worker) | Pool Mode: Stripe confirmed, x402 signed from pool |
| `payment_signed` | Server (Worker) | Mode C: Agent's wallet signs x402 payment |
| `content_delivered` | Server (Worker) | Content returned after payment proof verified |
| `token_issued` | Server (Worker) | One-time URL minted (Mode B) |
| `token_redeemed` | Server (Worker) | URL consumed, deleted forever |
| `token_expired` | Server (Worker) | TTL hit, URL deleted |
| `wallet_revoked` | App (human) | Keys rotated or wallet destroyed |

Single-use enforcement is non-negotiable. Tokens are deleted on first use (atomic delete, not mark-used). Second reader gets 410 Gone.

## Commands

```bash
# Pay for paywalled content (Pool Mode ... Apple Pay)
wip-pay pay https://morning-stew.../v1/issues/MS-3

# Pay with your own wallet (Mode C ... instant)
wip-pay pay <url> --wallet=cdp
wip-pay pay <url> --wallet=privy

# One-time payment link (for agents without tool access)
wip-pay 0.10 morning-stew "MS-#8"

# Wallet management (Mode C)
wip-pay balance
wip-pay history
wip-pay budget set 5.00 1.00
```

**MCP tool calls:**
```json
{ "name": "agent_pay_x402", "arguments": { "url": "https://morning-stew.../v1/issues/MS-3" } }
{ "name": "agent_pay_fund", "arguments": { "amount": 10 } }
{ "name": "agent_pay", "arguments": { "amount": 0.10, "service": "morning-stew", "note": "MS-#8" } }
```

## Quick Start

See README.md for install command + interactive agent setup.
See SETUP.md for full walkthrough.
See REFERENCE.md for Worker deployment and self-hosting.
