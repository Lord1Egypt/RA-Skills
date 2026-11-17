---
name: spraay-bankr
description: >
  Earn with Bankr, distribute with Spraay 💧. Composition skill that pairs a
  Bankr agent wallet (trading, token launches, creator fees, treasury) with
  Spraay's batch payment gateway (pay up to 200 recipients in one atomic
  transaction, ~80% gas savings). Use when the user wants to: airdrop a token
  they launched via Bankr, split creator/trading fees across a team, run
  USDC payroll from a Bankr-managed treasury, or batch-distribute any ERC-20
  from a Bankr wallet on Base. Triggers on: "airdrop my token", "split fees",
  "pay my team from my Bankr wallet", "batch send", "distribute to holders",
  "spraay from bankr", "mass payout".
---

# Spraay × Bankr — Earn, Then Distribute

**What this skill does:** Bankr gives your agent a wallet that trades, launches
tokens, and earns fees. Spraay turns that wallet into a distribution engine —
**pay up to 200 recipients in a single atomic transaction** instead of N
separate transfers. This skill composes the two: every recipe ends in a Spraay
batch call funded by a Bankr wallet.

**Why batch:** N individual transfers cost N× gas and can partially fail.
One Spraay batch is atomic (all succeed or all revert) and saves ~80% gas.
Primary chains: **Base**, Ethereum, Solana (15 mainnet chains total).

## Prerequisites

1. **Bankr skill installed** — https://github.com/BankrBot/skills (or the
   Bankr CLI / Agent API with an API key from bankr.bot/api-keys).
2. **Spraay gateway access** — `https://gateway.spraay.app`. Free endpoints
   need no payment. Paid endpoints use **x402**: Bankr wallets handle x402
   USDC payments on Base automatically, so no separate signup or API key is
   needed — the agent pays per call from its own wallet.

## Core Spraay endpoints used by this skill

Free (plan & validate before spending anything):

- `GET  /free/prices` — endpoint pricing
- `GET  /free/chain-status` — supported chains + health
- `POST /free/validate-batch` — validate recipients/amounts before execution
- `POST /free/estimate-batch` — gas + cost estimate for a batch

Paid (x402, USDC on Base — Bankr pays automatically):

- `POST /api/v1/batch/execute` — execute a batch payment (up to 200 recipients)
- `POST /api/v1/escrow/create` — escrowed/conditional payouts
- `GET  /api/v1/tokens` — supported token registry
- `GET  /api/v1/balances` — balance checks

**Always call `/free/validate-batch` and `/free/estimate-batch` before
`/api/v1/batch/execute`.** Show the user the estimate and get confirmation
before any funds move.

## Recipe 1 — Launch → Airdrop

User launched (or is launching) a token via Bankr and wants it in holders'
or community members' hands.

1. Launch or locate the token via Bankr (Clanker deploys to Base by default).
   Get the token contract address from the Bankr response.
2. Collect the recipient list (addresses + amounts). Sources: a CSV the user
   provides, a holder snapshot, or an allowlist. Never invent addresses.
3. `POST /free/validate-batch` with `{ token, recipients: [{address, amount}] }`.
   Fix any rejects before proceeding.
4. `POST /free/estimate-batch` — present total cost + gas to the user.
5. On explicit confirmation: `POST /api/v1/batch/execute`. Bankr's wallet
   pays the x402 fee and funds the batch. One tx, all recipients.
6. Return the tx hash and a per-recipient summary.

## Recipe 2 — Creator Fee Split

Bankr routes trading fees to the token creator. Teams want those fees split
automatically across contributors.

1. Via Bankr: check claimable creator fees, claim them to the agent wallet.
2. Compute the split from the user's configured shares (e.g. 50/30/20).
   Confirm the math with the user — show each recipient's amount.
3. Validate → estimate → execute the batch (same free-then-paid flow as
   Recipe 1). USDC or the fee token itself both work.
4. For recurring splits, re-run on a schedule the user controls; never
   auto-execute without a standing, explicit instruction.

## Recipe 3 — Treasury → Payroll

The agent manages a treasury in its Bankr wallet and pays a roster in USDC.

1. Via Bankr: confirm treasury balance covers the pay run (plus fees).
   If holdings are in another asset, Bankr can swap to USDC first —
   confirm the swap with the user before executing it.
2. Load the roster (addresses, amounts, optional memo per recipient).
3. Validate → estimate → **pause for user confirmation** (payroll is
   high-stakes; always show the full run before executing).
4. `POST /api/v1/batch/execute` — the whole roster in one atomic tx.
5. Log the tx hash + per-recipient record for bookkeeping.

For scheduled runs and compliance screening, see the `crypto-payroll` skill —
this recipe is the manual/on-demand path.

## Safety rails

- **Atomic or nothing:** a Spraay batch reverts entirely on failure — no
  partial payouts. Surface this to users as a feature.
- **Validate first, always.** The free endpoints exist so that no paid call
  is ever made on malformed input.
- **Explicit confirmation before funds move.** Show token, total, recipient
  count, and estimated cost. Get a clear yes.
- **Never fabricate addresses or amounts.** Recipient lists come from the
  user or a verifiable source only.
- **Key hygiene:** the Bankr API key controls real funds. Never echo it,
  log it, or send it anywhere except `api.bankr.bot`.

## Reference

- Spraay gateway: https://gateway.spraay.app · docs: https://docs.spraay.app
- Live dashboard: https://live.spraay.app
- Bankr docs: https://docs.bankr.bot
- Spraay batch contract (Base): `0x1646452F98E36A3c9Cfc3eDD8868221E207B5eEC`
