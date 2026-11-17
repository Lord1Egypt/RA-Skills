# Implementation Roadmap: AI CASH + AGENT WALLET

**Date:** 2026-02-24
**Status:** Planning. Code for Rail 1 written. Not deployed. Rail 2 not started.

---

## What This Document Is

This is not the plan. This is the map to make the plan.

It captures where everything lives, what's been decided, what's been built, what hasn't, and what needs to happen before writing a detailed implementation plan for each phase.

---

## Where The Decisions Live

| Document | What it contains | Path |
|----------|-----------------|------|
| Thesis (full) | Two-rail architecture, chargeback philosophy, unified abstraction | `ai/plans/thesis--full.md` |
| Thesis (summary) | Shorter version, same structure | `ai/plans/thesis--agent-cash-wallet.md` |
| Risk control | Tiers, refund policy, dispute metrics, seller vetting, $25 cap rationale | `ai/plans/risk-control--agent-cash.md` |
| One codebase, two READMEs | Why one repo, two consumer doors | `ai/plans/one-codebase-two-readmes.md` |
| Pool mode architecture | Technical plan for Pool Mode A + Mode C, reverted c6efb49 | `ai/plans/pool-mode-user-wallet--2026-02-24.md` |
| Partner fees (draft) | Tiered fee structure ($0.25 + 2-5%), 90-day intro, marketplace research TODO | `ai/plans/partner-fees--2026-02-24.md` |
| Universal installer alignment | TODO for machine-readable specs, manifest | `ai/todo/universal-installer-alignment.md` |
| Next drops | Loom demo, inter-agent payment example | `ai/todo/next-drops.md` |

## Where The Product Docs Live

| Document | Audience | Path |
|----------|----------|------|
| CASH.md | Consumers, normies | `CASH.md` |
| WALLET.md | Developers, protocol users | `WALLET.md` |
| README.md | Combined (reference, will be replaced) | `README.md` |
| PARTNERS-STRIPE.md | Shopify/SaaS merchants wanting to join | `PARTNERS-STRIPE.md` |
| PARTNERS-402.md | x402 gate operators wanting to join | `PARTNERS-402.md` |
| SPEC.md | Technical spec for agents and developers | `SPEC.md` |
| SETUP.md | Setup commands, wallet config, security | `SETUP.md` |

## Where The Code Lives

| File | What it does | Status |
|------|-------------|--------|
| `worker/index.js` | Cloudflare Worker. All payment routes. | Written. Not deployed. |
| `providers/passthrough.js` | Pool Mode client (calls /pool/pay, /pool/confirm) | Written. |
| `providers/index.js` | Route selector (pool vs wallet) | Written. |
| `cli.js` | CLI interface, Apple Pay flow, pricing display | Written. |
| `SKILL.md` | Skill definition for agent install | Exists but may need update for AI CASH branding. |

---

## The Two Rails

### Rail 1: 402 → Apple Pay (AI CASH for paywalled content)

**What it does:** Agent hits a 402 gate. Worker fetches the price. Creates Stripe Checkout. User taps Apple Pay. Worker signs x402 from pool wallet. Content unlocks.

**What's built:** All code written. Worker routes, CLI, providers.

**What's NOT done:**
- CDP wallet not created (need Base + Solana wallets with USDC)
- Stripe account not created (need keys, webhook URL)
- Worker not deployed to Cloudflare (need KV namespaces)
- No end-to-end test yet
- SKILL.md not updated for AI CASH branding

**To plan this phase, you need to answer:**
1. Which Stripe account? New or existing?
2. How much USDC to seed the pool wallets? ($50? $500?)
3. Test mode first or go straight to live?
4. Which 402 endpoint to test first? (Morning Stew is cheapest at $0.10)

### Rail 2: Stripe Checkout → Apple Pay (AI CASH for Shopify/SaaS)

**What it does:** Agent finds a product on a partner Stripe store. Creates a Stripe Connect checkout session. User taps Apple Pay. Purchase completes. Agent resumes.

**What's NOT built:** Everything. No code exists for this rail.

**To plan this phase, you need to answer:**
1. How does the agent discover products on a Shopify store? (Shopify Storefront API? Scraping? Manual product feed?)
2. How does Stripe Connect onboarding work for partners? (Standard? Express?)
3. Who is merchant-of-record? (Partner via Connect ... confirmed in risk doc)
4. How does the agent create a checkout session for a specific product?
5. What's the partner application flow? (Manual review? Email? Form?)
6. Modern Weaving ... have they agreed? What's the timeline?

### AGENT WALLET (Sovereign mode)

**What it does:** User creates wallet (CDP or Privy), funds it, agent signs x402 directly.

**What's built:** Worker routes `/wallet/create`, `/wallet/pay`, `/x402/pay`, `/privy/pay`. CLI flags `--wallet=cdp`, `--wallet=privy`.

**What's NOT done:**
- Not tested end-to-end
- Privy account not set up
- No onboarding flow for wallet creation

**To plan this phase, you need to answer:**
1. Is Privy wallet creation free? What are the limits?
2. Coinbase Onramp ... is the 15-transaction cap per user or per app?
3. Priority vs Rail 1? (Rail 1 first, confirmed)

---

## Operational Systems Not Built

### Seller Tiering
- KV-based whitelist in Worker
- Tier 0/1/2 limits enforced per domain
- Needs: schema design, admin API or manual KV management

### Refund/Dispute Automation
- Stripe webhook for disputes
- Auto-refund before dispute if possible
- Dispute rate monitoring
- Needs: Stripe dispute webhook handler, refund logic, alerting

### Partner Onboarding
- Application flow (form? email? AI-guided?)
- Domain whitelisting
- Stripe Connect account linking
- Needs: decision on flow, then build

### Monitoring
- Transaction volume tracking
- Dispute rate dashboard
- Pool wallet balance monitoring (auto-alert when low)
- Needs: KV ledger queries, alerting

---

## Deployment Checklist (Rail 1)

This is the critical path to a live test:

1. Parker: Create CDP wallet at portal.cdp.coinbase.com (Base + Solana)
2. Parker: Fund with USDC ($50-100 to start)
3. Parker: Create Stripe account, enable Apple Pay + Google Pay
4. Parker: Configure Stripe webhook → Worker URL
5. Parker: Store all creds in 1Password
6. Deploy: `wrangler deploy` + create KV namespaces
7. Deploy: Set env vars from 1Password
8. Test: Stripe test mode, small transaction on Morning Stew
9. Test: Verify pool pricing math matches CASH.md
10. Test: Verify $25 cap redirect to AGENT WALLET
11. Go live: Switch Stripe to live mode
12. Go live: Real $0.10 Morning Stew purchase
13. Go live: Real Pawr transaction on Base

---

## What The Robust Plan Needs To Cover

When writing the full implementation plan for each rail:

- **Exact API calls** (Stripe Checkout create, CDP sign, x402 replay)
- **Error handling** (what if Stripe fails? what if x402 signing fails? what if pool is empty?)
- **State machine** (quote → checkout → webhook → sign → unlock → destroy)
- **Security** (Worker auth, webhook verification, token lifecycle)
- **Testing strategy** (test mode → staging → live)
- **Rollback plan** (what if chargebacks spike? kill switch?)
- **Monitoring** (pool balance, dispute rate, transaction volume)

---

## Priority Order

1. **Rail 1: 402 → Apple Pay** ... code is written, just needs deploy + test
2. **Seller tiering** ... whitelist Morning Stew + Pawr as Tier 1
3. **AGENT WALLET testing** ... end-to-end with CDP
4. **Rail 2: Stripe merchants** ... new code, Stripe Connect, partner onboarding
5. **Operational systems** ... refund automation, monitoring, partner application flow
6. **Universal installer alignment** ... machine-readable spec, manifest

---

## How To Use This Document

When starting a new session to work on any of this:

1. Read this file first.
2. Read the specific plan/doc for the phase you're working on.
3. Read the code files listed above.
4. Write a detailed implementation plan for that specific phase.
5. Get Parker's approval.
6. Build it.
