---
name: pumpclaw-agent
description: Generate customer-ready Telegram polling bots + an Express-style web server that integrate Pump.fun Tokenized Agent payments using @pump-fun/agent-payments-sdk (build invoices, accept payments, and verify invoices on Solana). Use when asked for pump.fun / pumpfun agent integrations, tokenized agent payment flows, invoice verification, or a Telegram+web bot scaffold for Pump Tokenized Agents.
---

# PumpClaw Agent — Pump.fun Tokenized Agents + Telegram + Web Server

This skill stamps a reusable template project and customizes it for a customer.

Template:
- `assets/template/`

Reference:
- `references/PUMP_TOKENIZED_AGENTS.md`

## Before you start — required info

Ask for these before writing code:

1. **Agent token mint address** (pump.fun Tokenized Agent mint)
2. **Payment currency** (USDC or wSOL) → determines `CURRENCY_MINT`
3. **Price** (smallest units: USDC=6 decimals, SOL=9 decimals)
4. **What to deliver after payment** (what the bot/server unlocks)
5. **Solana RPC URL** (must support `sendTransaction`)
6. **Telegram commands** the bot should expose (and where alerts/messages go)

## Safety rules (must follow)

- Never log or output private keys / secret key material.
- Never sign transactions on behalf of the user.
- Always verify payments server-side via `validateInvoicePayment` before delivering service.
- Validate `amount > 0`, and ensure `endTime > startTime`.

## Workflow

### Step 1 — Stamp the template

Copy `assets/template/` into a new customer folder (project slug).

### Step 2 — Configure env vars

Ensure `.env.example` includes:

- `SOLANA_RPC_URL`
- `AGENT_TOKEN_MINT_ADDRESS`
- `CURRENCY_MINT`
- `TELEGRAM_BOT_TOKEN`
- `PORT`

Do not create/commit real `.env`.

### Step 3 — Implement Pump Tokenized Agent payment flow

Use `@pump-fun/agent-payments-sdk`:

- Build payment instructions with `buildAcceptPaymentInstructions`.
- Verify with `validateInvoicePayment` on the server.

If a frontend wallet flow is requested, follow the Pump reference skill (see `references/PUMP_TOKENIZED_AGENTS.md`).

### Step 4 — Telegram bot (polling)

Implement requested commands. Always include `/help`.

### Step 5 — Web server endpoints

Always include:

- `GET /health` → `{ ok: true }`

Add payment-related endpoints only as requested (e.g. create invoice, verify invoice).

### Step 6 — Deliverables

Provide:
- the full project folder
- run instructions
- smoke test checklist
