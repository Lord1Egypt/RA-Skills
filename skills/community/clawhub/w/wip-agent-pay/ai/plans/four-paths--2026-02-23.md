# Plan: Four Paths ... Build 1 & 4, Spec 2 & 3

**Date:** 2026-02-23
**Author:** Claude Code (Opus 4.6)
**Status:** SUPERSEDED by `pool-mode-user-wallet--2026-02-24.md`

> **Note:** Path 4 was redesigned on 2026-02-24. The "Apple Pay pass-through to seller via Stripe Connect" model was replaced with Pool Mode (Parker's float) + User Wallet (Mode C). See the new plan for details.

## The Four Paths

| Path | Model | Build or Spec | User setup | We custody? | Requires |
|------|-------|---------------|-----------|-------------|----------|
| **1** | **Self-custody** | **BUILD** | User sets up CDP or Privy | No | Nothing |
| 2 | We-hosted wallet | SPEC ONLY | None | Yes (crypto) | Inc + % fee |
| 3 | Stripe + our float | SPEC ONLY | None | Stripe fiat + we front crypto | Inc + % fee |
| **4** | **Pass-through** | **BUILD** | None | No. Never. | Seller has Stripe Connect |

**Path 1** ... power users. They own their wallet. They own their keys. We provide the agent interface.
**Path 4** ... normies. Apple Pay per transaction. Money goes directly to seller via Stripe. We never touch it.
**Paths 2 & 3** ... post-incorporation. Need legal entity, fee structure (%), terms of service.

## Path 1: Self-Custody (BUILD)

User creates their own CDP or Privy wallet. Stores creds in 1Password. Agent signs x402 payments from their wallet.

**Already built:**
- `providers/x402.js` ... CDP x402 provider
- `providers/privy.js` ... Privy x402 provider
- `worker/index.js` ... /x402/pay and /privy/pay routes
- `lib/cdp-auth.js` ... Ed25519 JWT generation
- CLI `pay` command
- MCP `agent_pay_x402` tool
- OpenClaw `agent_pay_x402` tool

**Still needed:**
- Parker: create CDP wallet at portal.cdp.coinbase.com
- Parker: store creds in 1Password (`wip-agent-pay-coinbase-cdp`)
- Parker: set Worker env vars for CDP
- Test against Morning Stew
- (Optional) Parker: create Privy app + wallet
- (Optional) Parker: store Privy creds

**Flow:**
```
User sets up CDP/Privy wallet (one-time)
User funds wallet manually (transfer USDC)
Agent hits paywalled URL → 402
Worker signs payment from user's wallet (CDP or Privy)
Content returned
```

## Path 4: Pass-Through (BUILD)

No wallet. No balance. No custody. Agent hits a paywalled URL, gets 402, opens Apple Pay for that exact amount, Stripe sends money directly to seller. Pure pass-through.

**How it works:**
```
1. Agent: wip-pay pay https://morning-stew.../v1/issues/MS-3
2. Worker: fetch(url) → gets 402 (amount: $0.10, seller: morning-stew)
3. Worker: create Stripe Checkout ($0.10, destination: seller's Stripe Connect account)
4. Worker: return { checkoutUrl, paymentId }
5. Agent: opens checkout in user's browser
6. User: taps Face ID (Apple Pay)
7. Stripe: sends $0.10 to seller (minus Stripe fee)
8. Stripe: webhook → Worker confirms payment
9. Worker: retries URL with payment proof
10. Content returned to agent
```

**Requirements for seller:**
- Seller must have a Stripe Connect account linked to Agent Pay platform
- OR seller provides a Stripe payment link in the 402 response
- OR seller accepts x402 on-chain (then use Path 1 instead)

**Requirements for user:**
- Apple Pay (or card)
- That's it

**New Worker route:**
```
POST /passthrough/pay
  Input: { url }
  1. Fetch URL, get 402
  2. Look up seller's Stripe Connect account (or parse from 402)
  3. Create Stripe Checkout session (destination: seller)
  4. Return { checkoutUrl, paymentId }

POST /passthrough/confirm
  Input: { paymentId }
  1. Check if Stripe payment completed
  2. If yes, retry original URL with payment receipt
  3. Return content
```

**New provider:**
```
providers/passthrough.js
  - Calls Worker /passthrough/pay
  - Opens checkout URL in browser
  - Polls /passthrough/confirm until payment clears
  - Returns content
```

**CLI:**
```bash
wip-pay pay <url>                    # Auto-detect: Path 4 if no wallet configured
wip-pay pay <url> --wallet=cdp       # Force Path 1 (CDP)
wip-pay pay <url> --wallet=privy     # Force Path 1 (Privy)
wip-pay pay <url> --passthrough      # Force Path 4 (Apple Pay per-tx)
```

**Auto-detection:**
- If user has CDP/Privy creds configured → Path 1
- If not → Path 4 (Apple Pay per transaction)
- User can always override with flags

**Stripe fee transparency:**
```
Agent: "This article costs $0.10. With payment processing, total is $0.40. Grab it?"
```
The $0.30 Stripe fee is shown to the user. No surprises.

**Seller registration:**
Sellers register their Stripe Connect account with Agent Pay. We maintain a registry:
```
KV: seller-registry
  "morning-stew.railway.app" → { stripeAccountId: "acct_xxx", name: "Morning Stew" }
```
When the Worker gets a 402 from a known seller domain, it routes payment to their Stripe Connect account.

For unknown sellers, the 402 response itself can include a Stripe payment link. The Worker just redirects.

### New Files for Path 4

| File | What |
|------|------|
| `providers/passthrough.js` | Local provider: call Worker, open checkout, poll confirm |
| Worker route: `/passthrough/pay` | Parse 402, create Stripe Checkout for seller |
| Worker route: `/passthrough/confirm` | Check payment status, retry URL, return content |
| Worker KV: seller registry | Map seller domains to Stripe Connect account IDs |

---

## Path 2: We-Hosted Wallet (SPEC ONLY)

**Requires:** Incorporation (LLC or C-Corp), money transmitter analysis, terms of service, fee structure.

We create wallets under our Privy/CDP account. Each user gets a wallet. We hold the keys. Users fund via Apple Pay or transfer.

**Fee structure (TBD):**
- % per transaction (e.g. 2-3%)
- Monthly subscription?
- Free tier with limits?

**Why it needs incorporation:**
- We custody crypto on behalf of users
- Money transmitter laws (state by state in US)
- Need legal entity to hold Stripe account for this model
- Need terms of service, privacy policy
- Need compliance (KYC/AML above certain thresholds?)

**Architecture (already built, just needs activation):**
- Same providers (x402.js, privy.js)
- Worker creates wallets per-user via CDP/Privy API
- Worker manages wallet mapping: user → wallet address
- Stripe funding goes to our account, we deposit to user's wallet

**Spec saved. Build after incorporation.**

---

## Path 3: Stripe + Our Float (SPEC ONLY)

**Requires:** Same as Path 2 (incorporation, legal, fees).

User funds via Apple Pay. Stripe holds fiat. We hold a small crypto float ($50-100). When agent pays, we sign from our wallet and debit user's fiat balance.

**Fee structure (TBD):**
- % per transaction
- Spread on fiat-to-crypto conversion
- Or flat fee per transaction

**Why it needs incorporation:**
- We hold user fiat balances (via Stripe)
- We front crypto payments
- Need reconciliation system
- Need legal entity, insurance, compliance

**Architecture:**
- Stripe holds all user fiat
- One CDP/Privy wallet (our float, $50-100)
- Worker tracks user balances in KV
- Agent pays → we sign from our wallet → debit user balance
- Daily reconciliation: fiat collected vs crypto spent
- Auto-replenish float from Stripe → crypto conversion

**Risk:**
- If our wallet is compromised: lose $50-100 float (register model)
- Conversion risk: fiat/USDC rate fluctuation (minimal for stablecoin)
- Reconciliation errors

**Spec saved. Build after incorporation.**

---

## Execution Order

### Now: Build Path 1 + Path 4

1. ~~Create CDP auth, x402 provider, Privy provider~~ DONE
2. ~~Create Worker routes for x402/pay, privy/pay~~ DONE
3. ~~Update CLI with pay command~~ DONE
4. Create `providers/passthrough.js` (Path 4)
5. Add Worker routes: `/passthrough/pay`, `/passthrough/confirm`
6. Add seller registry in KV
7. Update CLI auto-detection (no wallet = passthrough)
8. Parker: create Stripe Connect platform account
9. Parker: create CDP wallet, store creds, set Worker env vars
10. Test Path 1 against Morning Stew (x402)
11. Test Path 4 against Morning Stew (Apple Pay pass-through)
12. Update docs
13. PR + merge

### Later: Build Paths 2 + 3

14. Incorporate (LLC or C-Corp)
15. Define fee structure (% per tx)
16. Legal review (money transmitter, ToS, privacy)
17. Build user wallet management
18. Build reconciliation system
19. Launch

---

## Updated CLI

```bash
# Path 4: Pass-through (default if no wallet configured)
wip-pay pay <url>                    # Apple Pay per transaction
wip-pay pay <url> --passthrough      # Force pass-through

# Path 1: Self-custody
wip-pay pay <url> --wallet=cdp       # Sign with your CDP wallet
wip-pay pay <url> --wallet=privy     # Sign with your Privy wallet

# Wallet management (Path 1 only)
wip-pay balance
wip-pay history
wip-pay budget
wip-pay budget set 5.00 1.00

# Funding (Path 1 only ... fund your own wallet)
wip-pay fund 10

# One-time URL (works with any path)
wip-pay 0.10 morning-stew "MS-#8"
```
