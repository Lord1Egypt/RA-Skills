---
name: self-hosted-crypto-payments
description: >
  Add self-custodied crypto payment checkout to a Next.js + Supabase app.
  Accepts ETH, BTC, SOL, USDC, USDT and 25+ coins across 9 chains.
  No payment processor fees — HD wallet derivation, on-chain polling, zero third-party dependency.
  Use when: user asks to add crypto payments, accept Bitcoin/Ethereum/Solana, Web3 checkout,
  self-hosted crypto, no-middleman payments, blockchain payments, accept USDC/USDT.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
env:
  required:
    - name: CRYPTO_MASTER_MNEMONIC
      description: "BIP39 mnemonic (12-24 words). Master key for HD wallet derivation. Server-only — never expose to client."
      sensitive: true
    - name: CRON_SECRET
      description: "32-char hex string. Protects /api/cron/check-crypto-payments from unauthorized calls."
      sensitive: true
---

# Self-Hosted Crypto Payments

## What This Skill Does

Adds a complete, production-ready crypto payment system to any **Next.js 14+ App Router** app backed by **Supabase**. No Stripe, no CryptAPI, no payment processor — you keep 100% of every payment.

**Supported chains & coins:** ETH, Base, Polygon, Arbitrum, Optimism, BNB Chain, Avalanche, Solana, Bitcoin — including USDC/USDT/DAI stablecoins on each chain.

**Architecture:**
1. User picks coin → server derives a unique HD wallet address (BIP44/84/SLIP-0010)
2. Server stores address + expected amount in DB with a 1-hour expiry
3. A cron job polls the actual blockchain every minute, verifies balance, confirms payment
4. On confirmation, credits/plan/addon is applied atomically to the user's profile

**Security model:** Mnemonic never touches client or source code. User cannot influence destination address or amount. Payment confirmation is blockchain-verified, not webhook-forgeable.

---

## Files to Copy

All template files are in `resources/`. Copy them into your project at these paths:

| Resource file | Destination in your project |
|---|---|
| `crypto-wallets.ts` | `src/lib/crypto-wallets.ts` |
| `crypto-checkout-route.ts` | `src/app/api/billing/crypto-checkout/route.ts` |
| `crypto-checkout-status-route.ts` | `src/app/api/billing/crypto-checkout/[id]/status/route.ts` |
| `check-crypto-payments-route.ts` | `src/app/api/cron/check-crypto-payments/route.ts` |
| `crypto-payment-modal.tsx` | `src/components/dashboard/crypto-payment-modal.tsx` |
| `005_crypto_payments.sql` | `supabase/migrations/005_crypto_payments.sql` |
| `006_crypto_direct.sql` | `supabase/migrations/006_crypto_direct.sql` |

---

## Installation Steps

### 1. Install dependencies

```bash
npm install ethers @scure/bip32 @scure/bip39 @scure/base @noble/hashes @solana/web3.js qrcode
npm install -D @types/qrcode
```

### 2. Run database migrations

In Supabase SQL editor (or via `supabase db push`), run both migration files in order:
- `005_crypto_payments.sql`
- `006_crypto_direct.sql`

### 3. Add environment variables

```env
# Generate mnemonic: https://iancoleman.io/bip39/ (12 or 24 words — NEVER commit this)
CRYPTO_MASTER_MNEMONIC=word1 word2 word3 ... word12

# Protects the cron endpoint — generate with:
# node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
CRON_SECRET=your-32-char-hex-string
```

### 4. Set up a cron job

The cron endpoint `POST /api/cron/check-crypto-payments` must be called every 60 seconds.

**Vercel Cron** (`vercel.json`):
```json
{
  "crons": [
    {
      "path": "/api/cron/check-crypto-payments",
      "schedule": "* * * * *"
    }
  ]
}
```

Add the Authorization header in your cron config or Vercel dashboard:
```
Authorization: Bearer <your CRON_SECRET>
```

**Fly.io machines / self-hosted:** Use a scheduled task or external cron (e.g. cron-job.org) hitting the endpoint with `Authorization: Bearer <CRON_SECRET>`.

### 5. Customise payment types

The checkout route handles three payment `type` values — edit to match your app's data model:

| Type | What it does | Required body fields |
|---|---|---|
| `credits` | Adds credits to user profile | `packId` |
| `plan` | Upgrades user plan | `plan`, `months` (optional for lifetime) |
| `addon` | Applies a one-time resource addon | `addonId`, `botId` (optional) |

**To customise:** In `crypto-checkout-route.ts`, replace the `CREDIT_PACKS`, `PLANS`, and `validAddons` references with your own constants. The amount must always come from **server-side constants** — never from user input.

In `check-crypto-payments-route.ts`, update `applyPayment()` to perform whatever action your app takes when a payment is confirmed (add credits, unlock features, update subscription, etc.).

### 6. Wire up the modal

```tsx
import { CryptoPaymentModal } from '@/components/dashboard/crypto-payment-modal'

// Example: pay for a credit pack
<CryptoPaymentModal
  target={{
    type: 'credits',
    packId: '1000',
    label: '1,000 Credits',
    amountUsd: 10,
  }}
  onClose={() => setModalOpen(false)}
/>
```

The modal handles coin selection, QR display, countdown timer, and polls for confirmation automatically.

---

## How Address Derivation Works

Each payment gets a **unique deposit address** derived from your master mnemonic:

- **EVM** (ETH, Base, Polygon, etc.): `m/44'/60'/0'/0/{index}` — checksummed Ethereum address, valid on all EVM chains
- **Bitcoin**: `m/84'/0'/0'/0/{index}` — native SegWit P2WPKH (`bc1q...`)
- **Solana**: `m/44'/501'/{index}'/0'` — SLIP-0010 ed25519 (matches Phantom/Solflare)

The `derivation_index` increments per payment and is stored in the DB. A `UNIQUE` constraint prevents two active payments from sharing an address.

**Implication:** One mnemonic controls all your payment wallets. Back it up securely. If you ever need to sweep funds, import the mnemonic into MetaMask (for EVM), Phantom (for SOL), or a BIP84 wallet (for BTC) and derive the child accounts.

---

## What to Customise

| Thing | Where |
|---|---|
| Supported coins list | `SUPPORTED_COINS` in `crypto-checkout-route.ts` |
| Quick-pick coins shown first | `QUICK_PICKS` in `crypto-payment-modal.tsx` |
| Payment window (default 1hr) | `expiresAt` in `crypto-checkout-route.ts` |
| Balance tolerance (default 0.5%) | `minRequired` in `check-crypto-payments-route.ts` |
| Payment types + fulfilment logic | `applyPayment()` in `check-crypto-payments-route.ts` |
| Rate limit (default 3 req/5min) | `checkRateLimit` call in `crypto-checkout-route.ts` |

---

## Security Notes

- `crypto-wallets.ts` is **server-only** — never import it in client components or pages
- `CRYPTO_MASTER_MNEMONIC` must never appear in source code, git history, or logs
- The cron endpoint uses `timingSafeEqual` to prevent timing attacks on `CRON_SECRET`
- Payment amounts are sourced from server-side constants — users cannot manipulate them
- Address uniqueness is enforced at the DB level (unique index on `wallet_type + derivation_index`)

---

## Troubleshooting

**"CRYPTO_MASTER_MNEMONIC is not set"** — The env var is missing. Add it to `.env.local` (development) or your hosting provider's environment settings (production).

**Payments not confirming** — Check that your cron job is running and the `Authorization: Bearer <CRON_SECRET>` header matches exactly. Check Vercel/server logs for `[check-crypto]` lines.

**"Failed to allocate payment address"** — Extremely rare concurrent collision (3 retries exhausted). Safe to retry.

**EVM token not detected** — Ensure the contract address for that token+chain exists in `ERC20_CONTRACTS` in `crypto-wallets.ts`. Check [etherscan.io](https://etherscan.io) for the canonical USDC/USDT address on your chain.
