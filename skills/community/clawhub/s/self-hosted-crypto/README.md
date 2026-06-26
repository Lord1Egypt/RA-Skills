# Self-Hosted Crypto Payments

> Accept Bitcoin, Ethereum, Solana, USDC, USDT and 25+ coins in your Next.js app. No payment processor. No fees. Full self-custody.

## What's included

| File | Purpose |
|---|---|
| `resources/crypto-wallets.ts` | HD wallet derivation (EVM, BTC, SOL) |
| `resources/crypto-checkout-route.ts` | `POST /api/billing/crypto-checkout` |
| `resources/crypto-checkout-status-route.ts` | `GET /api/billing/crypto-checkout/[id]/status` |
| `resources/check-crypto-payments-route.ts` | Cron: polls blockchain + confirms payments |
| `resources/crypto-payment-modal.tsx` | React modal with coin picker, QR, countdown |
| `resources/005_crypto_payments.sql` | Supabase migration — payments table |
| `resources/006_crypto_direct.sql` | Supabase migration — HD wallet index columns |
| `examples/integration-example.tsx` | How to wire the modal into a billing page |

## Quick start

```bash
# 1. Install via Claude Code skills
npx skills add Flacko2048/self-hosted-crypto-payments

# 2. Install npm dependencies
npm install ethers @scure/bip32 @scure/bip39 @scure/base @noble/hashes @solana/web3.js

# 3. Run migrations in Supabase SQL editor
#    supabase/migrations/005_crypto_payments.sql
#    supabase/migrations/006_crypto_direct.sql

# 4. Add env vars
CRYPTO_MASTER_MNEMONIC="your 12-word mnemonic"
CRON_SECRET="your-32-char-hex-string"
```

Then ask Claude (with this skill loaded):

> "Add the self-hosted crypto payment checkout to my billing page"

Claude will copy the files, wire up the modal, and configure the cron job for your specific setup.

## Supported networks

| Chain | Native | Stablecoins |
|---|---|---|
| Polygon | MATIC | USDC, USDT |
| Base | ETH | USDC |
| Arbitrum | ETH | USDC, USDT |
| Optimism | ETH | USDC |
| Solana | SOL | USDC, USDT |
| BNB Chain | BNB | USDC, USDT |
| Ethereum | ETH | USDC, USDT, DAI |
| Avalanche | AVAX | USDC |
| Bitcoin | BTC | — |

## How it works

1. User selects a coin in the modal
2. Server derives a **unique deposit address** from your BIP39 mnemonic (HD wallet path)
3. Server fetches the live exchange rate (CoinGecko) and stores the expected amount
4. User sends crypto to the displayed address — a QR code and 1-hour countdown are shown
5. A cron job polls the actual blockchain every minute and verifies the on-chain balance
6. Once confirmed, your `applyPayment()` function runs (add credits, upgrade plan, unlock features)

## Security

- **Mnemonic never leaves the server** — sourced only from `process.env.CRYPTO_MASTER_MNEMONIC`
- Users cannot modify the destination address or payment amount
- Cron endpoint protected with `timingSafeEqual(CRON_SECRET)`
- Payments confirmed against real blockchain data — not forgeable webhooks
- Supabase RLS: users can only read their own payment records
- **QR codes generated client-side** using `qrcode` — payment addresses are never transmitted to any external service

## Security Advisory

### Master mnemonic is a single point of control

`CRYPTO_MASTER_MNEMONIC` controls all derived deposit wallets across every chain. Treat it with the same care as a private key.

**Recommended mitigations:**
- Store it in your hosting provider's secrets manager (Vercel Environment Variables, AWS Secrets Manager, etc.) — not in `.env` files committed to git
- Keep an offline backup (written on paper, stored securely)
- To sweep received funds: import the mnemonic into MetaMask (EVM chains), Phantom (Solana), or any BIP84 wallet (Bitcoin) — accounts correspond to derivation indices

### External network calls

This skill makes the following outbound calls. All receive **only public blockchain data** — no user identity, no secrets, no mnemonic-derived material is ever transmitted:

| Service | Purpose | Data sent |
|---|---|---|
| `api.coingecko.com` | Native token exchange rates | Coin ID (e.g. "ethereum") |
| `mempool.space/api` | Bitcoin balance check | Bitcoin address (public) |
| Public EVM RPCs (Cloudflare, Base, etc.) | EVM/token balance check | Wallet address (public) |
| `api.mainnet-beta.solana.com` | Solana balance check | Wallet address (public) |

No third-party QR service is used — QR codes are generated locally in the browser.

## Requirements

- Next.js 14+ (App Router)
- Supabase (PostgreSQL + Auth)
- Node.js 18+

## License

MIT — built by [cr8claw](https://cr8claw.com)
