---
name: rozo-intents
description: >
  Cross-chain crypto payments and bridging via Rozo. Send USDC/USDT across
  Ethereum, Arbitrum, Base, BNB Chain (BSC), Polygon, Solana, and Stellar
  (Base and Stellar are USDC-only; Solana receives USDC only but can pay in
  USDT). On Stellar the trustline checker can also verify EURC trustlines;
  EURC is trustline-verification only, never a payment token here.
  Use when the user asks to pay, send, transfer, or bridge crypto/USDC/USDT,
  check a wallet or USDC/USDT balance, check a crypto payment's status, or
  shares a crypto payment QR code screenshot, a wallet address (0x, base58,
  G/C stellar), or a transaction hash. Auto-detects wallet type and
  auto-selects token (USDC preferred).
  Every payment shows full details and waits for an explicit yes/no by
  default. Small-amount auto-execute is opt-in: it runs only if the user
  raises the confirmation thresholds in version.json (shipped 0 = off).
  Do NOT use for general blockchain questions, non-payment tasks, or
  ordinary fiat payments, bank transfers, or bank-account balance questions.
metadata:
  author: rozo
  version: 1.0.9
  runtime: node
  permissions:
    network_endpoints:
      - intentapiv4.rozo.ai (Rozo payment API — create/get/check payments)
      - api-balance.rozo-deeplink.workers.dev (Rozo balance API)
    environment_variables: none read by the scripts (CLAUDE_PLUGIN_ROOT is
      referenced in docs only, to locate the plugin root)
    filesystem: none — scripts read/write no files; the agent reads
      version.json for confirmation thresholds
    spending: creates Rozo payment intents; every payment prompts for an
      explicit yes/no by default. Auto-execute below user-raised thresholds
      is opt-in via version.json and ships disabled (0/0).
    subprocess: none — scripts run via node with no child processes
---

# Rozo Cross-Chain Payments / Bridging

Send cross-chain crypto payments and bridging via Rozo. Send USDC/USDT across
Ethereum, Arbitrum, Base, BNB Chain (BSC), Polygon, Solana, and Stellar
(Base and Stellar are USDC-only; Solana receives USDC only but can pay in USDT).

**Confirmation:** every payment, any amount, shows full details and waits
for an explicit yes/no. Small-amount auto-execute exists but ships OFF
(thresholds `0` in `version.json`); it runs only if the user raises them.

## Before any payment

**Crypto transfers are irreversible.** Before funding anything, restate and
have the user verify the destination address, chain, token, memo (Stellar)
and amount against a source they trust. A payment to a wrong address, wrong
chain, or without a required memo is not recoverable by Rozo or anyone else. (If the
user has deliberately raised the auto-execute thresholds, their standing
opt-in covers amounts below them — correctness checks still run, but the
per-payment restatement is not required there.)

## Routing

Determine the user's intent and load the matching sub-skill:

| Intent | Sub-skill | Triggers |
|--------|-----------|----------|
| Send a payment | `skills/send-payment/SKILL.md` | "pay", "send", "transfer", "payout", shares a QR code, provides an amount + address |
| Check wallet balance | `skills/check-balance/SKILL.md` | "check balance", "how much do I have", "show my balance", "wallet balance" |
| Parse a QR code | `skills/parse-qr/SKILL.md` | "scan QR", "parse QR", "read this QR", shares a QR image without mentioning payment |
| Check payment status | `skills/payment-status/SKILL.md` | "check payment", "payment status", "where is my payment", "track payment", provides a payment UUID or tx hash |

**Rules:**
1. If the user mentions sending/paying → route to `send-payment` (it handles QR parsing internally)
2. If the user shares a QR code WITHOUT mentioning payment → route to `parse-qr` first, then offer to send
3. If the user asks about balance before sending → route to `check-balance`, then continue to `send-payment` if they want to pay
4. If ambiguous, ask the user what they'd like to do

## Supported Chains

### Pay-Out (sending to)

| Chain | USDC | USDT |
|-------|------|------|
| Ethereum | Yes | Yes |
| Arbitrum | Yes | Yes |
| Base | Yes | No |
| BSC | Yes | Yes |
| Polygon | Yes | Yes |
| Solana | Yes | No |
| Stellar | Yes | No |

### Pay-In (paying from)

| Chain | USDC | USDT |
|-------|------|------|
| Ethereum | Yes | Yes |
| Arbitrum | Yes | Yes |
| Base | Yes | No |
| BSC | Yes | Yes |
| Polygon | Yes | Yes |
| Solana | Yes | Yes |
| Stellar | Yes | No |

**Trust the live API over these tables.** Do NOT refuse a user's request
based purely on the tables above. Tables can be stale or misread — always
call `create-payment.js --dryrun` first and let the API be the source of
truth. If dryrun returns `success: true`, the route is supported; if it
returns an error, report that error to the user. Never tell a user "this
route isn't supported" without running the dryrun first.

## Runtime

Requires **Node.js** (ES modules). All scripts in `scripts/dist/` are run with `node`.

## Authentication & Rate Limiting

The Rozo APIs are **public and rate-limited** — no API keys or authentication tokens are required.

| Endpoint | Host | Auth | Notes |
|----------|------|------|-------|
| Payment API (create, get, check) | `intentapiv4.rozo.ai` | None (rate-limited) | Main Rozo payment API |
| Balance API (check balance) | `api-balance.rozo-deeplink.workers.dev` | None (rate-limited) | Rozo balance service (Cloudflare Workers) |

Both hosts are operated by Rozo. The balance endpoint uses a separate Cloudflare Workers deployment for performance.

**Data sent to Rozo:** as part of normal operation, wallet addresses,
chain/token choices, amounts, memos, and payment IDs are transmitted to
Rozo's public rate-limited APIs (`intentapiv4.rozo.ai`,
`api-balance.rozo-deeplink.workers.dev`). No API key is involved. Anyone
who can observe a payment ID can query that payment's status.

## Quick Reference

- **Amount limits:** $0.01 minimum, $10,000 maximum per transaction
- **Token selection:** Auto — fetch balance, prefer USDC, fall back to USDT
- **Payment type:** `exactOut` by default — recipient gets exact amount, fee added on top

## Scripts

Shared Node.js scripts in `scripts/dist/` (run with plain `node`):

| Script | Purpose |
|--------|---------|
| `check-balance.js` | Fetch wallet balances via Rozo balance API |
| `check-stellar-trustline.js` | Verify asset trustline (USDC/EURC) on Stellar G-wallets |
| `create-payment.js` | Create a payment (or dryrun for fee estimate) via Rozo API |
| `get-payment.js` | Get payment status by ID, tx hash, or address+memo |
| `parse-qr.js` | Parse payment QR code URIs (EIP-681, Solana Pay, Stellar URI) |
| `chains.js` | Shared chain/token config (imported by other scripts) |

## Shared Resources

- `references/supported-chains.md` — chain IDs, token addresses, decimals
- `references/api-reference.md` — Rozo API endpoints and schemas
- `references/wallet-detection.md` — address format detection rules
