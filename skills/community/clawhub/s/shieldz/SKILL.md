---
name: shieldz
title: Shieldz Payments
description: Accept crypto payments with zero setup. Turn a wallet address into a shareable payment link or a reusable tip jar. Non-custodial, no account, no API key.
version: 0.1.0
homepage: https://shieldz.cash/agents
license: MIT
keywords: [payments, crypto, usdc, usdt, non-custodial, invoice, tip-jar]
---

# Shieldz Payments

Let the agent accept crypto with **nothing but a destination wallet address**. No
account, no dashboard, no API key. Funds settle directly to the address you give;
Shieldz never holds them. Every link is OFAC sanctions-screened and rate-limited.

Two ways for the agent to use this skill:

1. **Direct HTTP (recommended for OpenClaw)** — call the keyless REST API below
   with `curl`. Works out of the box; nothing to install.
2. **MCP** — Shieldz also runs a remote MCP server at `https://shieldz.cash/mcp`
   (tools `create_payment_link`, `create_tip_jar`, `get_account_status`). Use it
   if your runtime prefers MCP tools.

## When to use

- The user says "take payments to <address>", "set up a checkout", "charge $X",
  "make a tip jar", "let people pay me", or asks how much has come in.

## Create a one-time payment link

```bash
curl -s -X POST https://shieldz.cash/api/v1/links \
  -H "content-type: application/json" \
  -d '{
    "settlement": { "chain": "BASE", "asset": "USDC", "address": "0xUSER_WALLET" },
    "amount_usd_cents": 4900,
    "memo": "Pro plan",
    "email": "owner@example.com"
  }'
```

`chain` may be `BASE`, `ARB`, `OP`, `POLY`, or `ETH`. `asset` is `USDC` or `USDT`.
`amount_usd_cents` is USD cents (4900 = $49.00). `email` is optional (lets the
owner claim a dashboard later). The response includes:

- `pay_url` — send this to the payer.
- `embed` — a `<script>` button snippet.
- `manage_url` / `manage_token` — keep this; it is how you read status later.

## Create a reusable tip jar (payer chooses the amount)

```bash
curl -s -X POST https://shieldz.cash/api/v1/tip-jars \
  -H "content-type: application/json" \
  -d '{
    "settlement": { "chain": "BASE", "asset": "USDC", "address": "0xUSER_WALLET" },
    "title": "Buy me a coffee",
    "suggested_amounts_usd_cents": [300, 500, 1000],
    "email": "owner@example.com"
  }'
```

Returns a reusable `url` (e.g. `https://shieldz.cash/tip/...`). Idempotent per
wallet address: calling again updates the same jar.

## Report what came in (e.g. on a heartbeat)

```bash
curl -s https://shieldz.cash/a/<manage_token>.json
```

Returns settlement details, tip jars, and `totals` (paid/pending counts and
amounts) so you can tell the user "you've received $X across N payments".

## Rules for the agent

- Always confirm the destination address with the user before creating a link.
- Never invent an address. If you don't have one, ask.
- A `403 sanctioned_address` means the address is on the OFAC list; do not retry.
- A `429` means slow down; wait and retry once.
- Funds are non-custodial: they go straight to the user's wallet, not to Shieldz.

## Optional: connect via MCP instead of curl

If your runtime supports MCP servers, add the remote server and call its tools:

```json
{ "mcpServers": { "shieldz": { "url": "https://shieldz.cash/mcp" } } }
```

Tools: `create_payment_link`, `create_tip_jar`, `get_account_status`.
