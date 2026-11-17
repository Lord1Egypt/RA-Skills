# Plan: Pool Mode (Mode A) + User Wallet (Mode C)

**Date:** 2026-02-24
**Status:** IMPLEMENTED

## Context

Path 4 was originally "Apple Pay pass-through to seller via Stripe Connect." That required sellers to have Stripe Connect accounts ... too much friction. Commit `c6efb49` tried to fix it by removing seller registration but accidentally turned Path 4 into a duplicate of Path 1 (direct x402 signing, no Apple Pay).

After research, the real architecture became clear:
- There's no "Apple Pay to x402" single-step product
- `@x402/fetch` SDK handles multi-chain x402 signing (Base, Solana, Monad)
- Facilitators are server-side only
- Coinbase Onramp exists (zero-fee USDC) but has unknowns

## What We Built

Two modes. Both use existing inline x402 signing (CDP + Privy) in the Worker.

### Mode A: Pool Mode (Parker's float)

Parker pre-funds a CDP wallet with USDC on **Base + Solana** (~$500 each). User pays fiat via Stripe Apple Pay. Worker signs x402 from the pool.

**Pricing:** x402 price + Stripe fees + $0.25 flat fee. Parker always nets $0.25.
**Limit:** Max $25 per x402 transaction. Over $25 requires Mode C.

```
Example: Morning Stew $0.10
  x402 cost:     $0.10
  Parker's fee:  $0.25
  Stripe (~5%):  ~$0.07
  User pays:     $0.42
  Parker nets:   $0.25

Example: Pawr.link create $19
  x402 cost:     $19.00
  Parker's fee:  $0.25
  Stripe (~3%):  ~$0.86
  User pays:     $20.11
  Parker nets:   $0.25
```

**Flow:**
```
1. Agent: wip-pay pay <url>
2. Worker: fetch(url) -> gets 402 (price, chain, payment info)
3. Worker: calculates total (x402 + Stripe fees + $0.25)
4. Worker: creates Stripe Checkout session (Apple Pay enabled)
5. CLI: opens checkout in browser
6. User: taps Apple Pay (Face ID)
7. CLI: polls /pool/confirm
8. Worker: checks Stripe session, signs x402 from pool wallet
9. Worker: replays request with payment proof
10. Content returned to agent
```

### Mode C: User's Own Privy Wallet

For transactions over $25, or users who want their own wallet.

**Flow:**
```
1. Agent hits URL -> gets 402 for > $25
2. CLI says: "Exceeds pool limit. Use --wallet=cdp or set up a user wallet."
3. /wallet/create creates Privy wallet by email (one-time)
4. User funds via Coinbase Onramp or manual USDC transfer
5. /wallet/pay signs x402 from user's Privy wallet
```

No fee from us on Mode C.

## Architecture

```
                     MODE A (Pool)                    MODE C (User Wallet)
                     ─────────────                    ────────────────────
User input:          Apple Pay (Stripe)               Fund own Privy wallet
x402 signing:        Pool CDP/Privy wallet            User's Privy wallet
Fee:                 x402 + Stripe + $0.25            None (user pays gas)
Max per tx:          $25                              Unlimited
Setup required:      None                             Create wallet + fund
```

## Worker Routes

| Route | Mode | What |
|-------|------|------|
| `POST /pool/pay` | A | Fetch 402, calculate pricing, create Stripe Checkout |
| `POST /pool/confirm` | A | Check Stripe, sign x402 from pool, return content |
| `POST /wallet/create` | C | Create Privy wallet by email |
| `POST /wallet/pay` | C | Sign x402 from user's Privy wallet |
| `POST /x402/pay` | 1 | Self-custody CDP signing (existing) |
| `POST /privy/pay` | 1 | Self-custody Privy signing (existing) |

## Provider Changes

| File | What changed |
|------|-------------|
| `providers/passthrough.js` | Renamed internally to pool. Calls /pool/pay + /pool/confirm. Handles over-pool-limit response. |
| `providers/index.js` | Default route goes to pool mode. Comments updated. |
| `cli.js` | Shows pool pricing breakdown. Handles over-pool-limit with guidance. |

## Pricing Formula

```
stripeFee = $0.30 + (x402Amount + $0.25) * 2.9%
totalCharge = x402Amount + $0.25 + stripeFee
```

Parker always nets $0.25 regardless of transaction size (up to $25).

## Technical Decision: Why Not @x402/fetch in Worker

The Worker is a single-file Cloudflare Worker (`main = "index.js"` in wrangler.toml). No bundler. No node_modules. The `@x402/fetch` SDK requires `@coinbase/cdp-sdk` and `viem` which are Node.js packages. The existing inline CDP signing (Ed25519 JWT + EIP-712 typed data) works correctly in the Worker's Web Crypto environment. No reason to add a bundler just for the SDK when the inline code does the same thing.

## What's Next

1. Parker: create CDP wallet at portal.cdp.coinbase.com (Base + Solana)
2. Parker: store creds in 1Password, set Worker env vars
3. Parker: create Stripe account, set up webhook to Worker
4. Deploy Worker to Cloudflare + create PAY_TOKENS + PAY_LEDGER KV namespaces
5. Test Pool Mode: Stripe test mode + small USDC on Base
6. Test $25 limit: confirm over-limit redirect works
7. Test Mode C: create Privy wallet by email, fund, sign x402

## Sources

- [Coinbase x402 SDK](https://github.com/coinbase/x402)
- [Coinbase x402 Buyer Quickstart](https://docs.cdp.coinbase.com/x402/quickstart-for-buyers)
- [Coinbase Onramp](https://docs.cdp.coinbase.com/onramp/docs/welcome)
- [Privy server wallets](https://docs.privy.io/guide/server-wallets/create)
