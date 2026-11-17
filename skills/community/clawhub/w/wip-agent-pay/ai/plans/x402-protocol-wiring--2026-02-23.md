# Plan: Wire x402 Protocol Into Agent Pay

**Date:** 2026-02-23
**Author:** Claude Code (Opus 4.6)
**Status:** Planning

## Context

Agent Pay mints one-time self-destructing URLs via a Cloudflare Worker. That works. But the x402 protocol (Coinbase's standard) is how real services charge agents natively. Morning Stew already speaks x402.

Agent Pay needs to speak x402. The Coinbase isolated portfolio IS the wallet. No hot wallets. No local private keys. Coinbase holds the keys. The agent just tells Coinbase "send X to Y" via API.

## Architecture

### The Flow (x402)

```
Agent: "This article costs $0.10. Want me to grab it?"
Human: "let's go"

  1. Agent hits paywalled URL
  2. Gets 402 back with payment requirements (amount, payTo address, network)
  3. Agent calls agent_pay with URL
  4. Agent Pay pulls Coinbase API creds from 1Password
  5. Agent Pay sends USDC from isolated portfolio to payTo via Coinbase API v2
  6. Agent retries URL with proof of payment (tx hash or x402 header)
  7. Content returned. URL/payment is done.
```

No hot wallet. No local private keys. No Solana keypair. The Coinbase portfolio is the cold wallet. Coinbase holds the keys. The API creds in 1Password just authorize "send X to Y."

### Coinbase API v2 Send

```
POST /v2/accounts/{account_id}/transactions

Headers:
  CB-ACCESS-KEY: (from 1Password)
  CB-ACCESS-SIGN: HMAC SHA-256 signature
  CB-ACCESS-TIMESTAMP: unix timestamp

Body:
  {
    "type": "send",
    "to": "{payTo address from 402 response}",
    "amount": "0.10",
    "currency": "USDC",
    "description": "Agent Pay: morning-stew MS-#3"
  }
```

The API key is locked to the `wip-agent-pay` portfolio only (Transfer + View permissions). Can't touch the main balance.

### Two Payment Modes

**Mode A: x402 (service tells you what to pay)**
```bash
wip-agent-pay pay https://morning-stew.../v1/issues/MS-#3
```
- Hit URL, get 402, extract payment requirements
- Send USDC from Coinbase portfolio to payTo address
- Retry with payment proof
- Return content

**Mode B: One-time URL (existing flow)**
```bash
wip-agent-pay 0.10 morning-stew "MS-#8"
```
- Mint one-time URL on Worker
- Return URL to agent
- Agent or consumer uses URL once

Both modes stay. x402 is for services that speak the protocol. One-time URLs are for everything else.

### Security Model (unchanged)

- Human creates portfolio, funds it, sets limits
- Agent can only send from that portfolio via API
- Coinbase holds the keys (not the agent, not the machine)
- API creds in 1Password, pulled at runtime via SA token
- No private keys on disk. Ever.

## 1Password Entries

| Entry | Vault | Fields | Status |
|-------|-------|--------|--------|
| `wip-agent-pay-worker-secret` | Agent Secrets | `credential` | EXISTS |
| `wip-agent-pay-coinbase` | Agent Secrets | `api-key`, `api-secret`, `account-id` | NEEDS CREATION |

## New Files

| File | What |
|------|------|
| `providers/x402.js` | x402 payment flow (hit URL, parse 402, send via Coinbase, retry) |
| Updated `cli.js` | Add `pay <url>` subcommand |
| Updated `mcp-server.mjs` | Add `url` param to `agent_pay` tool |
| Updated `openclaw.mjs` | Add `url` param to `agent_pay` tool |

## Updated CLI

```bash
# Mode B (existing)
wip-agent-pay 0.10 service-name "note"

# Mode A (new)
wip-agent-pay pay <url>
```

## Execution Order

1. Create `providers/x402.js` (parse 402, Coinbase send, retry)
2. Wire Coinbase API v2 send in `providers/coinbase.js` (HMAC auth, POST transactions)
3. Update `cli.js` with `pay` subcommand
4. Update `mcp-server.mjs` and `openclaw.mjs`
5. Update SPEC.md, SETUP.md, SKILL.md
6. Test against Morning Stew free endpoint
7. Test against paid endpoint
8. PR, merge

## Open Questions

1. **Coinbase API v2 vs CDP SDK:** v2 uses HMAC auth. CDP SDK uses JWT. Which does Parker's API key support? Need to check when creating the key.
2. **x402 payment proof format:** Morning Stew uses PAYMENT-SIGNATURE header with a base64 payload. Does Coinbase on-chain USDC send produce a compatible proof? Or does the service just verify the on-chain tx?
3. **Network:** Morning Stew accepts Solana and Monad USDC. Coinbase sends on which network? Need to confirm Coinbase supports USDC withdrawal to Solana addresses.

## Verification

```bash
# Free (no payment)
wip-agent-pay pay https://morning-stew-production.up.railway.app/v1/issues/free

# Paid ($0.10 USDC)
wip-agent-pay pay https://morning-stew-production.up.railway.app/v1/issues/MS-#3
```
