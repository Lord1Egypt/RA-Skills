---
name: rozo-intents
description: >
  Cross-chain crypto payments and bridging via Rozo. Send USDC/USDT across
  Ethereum, Base, BNB Chain, Solana, and Stellar.
  Use when user says "pay", "send", "transfer", "payout", "check balance",
  "payment status", or shares a QR code screenshot. Also
  triggers on wallet addresses (0x, base58, G/C stellar), transaction
  hashes. Auto-detects wallet type, auto-selects token
  (USDC preferred), checks balances, gets fees, and confirms before sending.
  Do NOT use for general blockchain questions or non-payment tasks.
metadata:
  author: rozo
  version: 1.0.2
  runtime: node
---

# Rozo Cross-Chain Payments / Bridging

Send cross-chain crypto payments and bridging via Rozo. Send USDC/USDT across
  Ethereum, Base, BNB Chain, Solana, and Stellar.

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
| Base | Yes | Yes |
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

## Runtime

Requires **Node.js** (ES modules). All scripts in `scripts/dist/` are run with `node`.

## Authentication & Rate Limiting

The Rozo APIs are **public and rate-limited** — no API keys or authentication tokens are required.

| Endpoint | Host | Auth | Notes |
|----------|------|------|-------|
| Payment API (create, get, check) | `intentapiv4.rozo.ai` | None (rate-limited) | Main Rozo payment API |
| Balance API (check balance) | `api-balance.rozo-deeplink.workers.dev` | None (rate-limited) | Rozo balance service (Cloudflare Workers) |

Both hosts are operated by Rozo. The balance endpoint uses a separate Cloudflare Workers deployment for performance.

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
