# Agent Cash & Agent Wallet

## A Payment Execution Layer for AI Systems

**Date:** 2026-02-24

---

## 1. The Core Thesis

AI systems can now:
- Discover products
- Identify paid APIs
- Detect paywalls
- Recommend purchases
- Navigate commerce flows

But they cannot natively complete payment in a way that:
- Works for normal humans
- Integrates with existing commerce rails
- Manages chargeback risk
- Preserves trust
- Supports both card and crypto ecosystems

There is a gap between:

> AI intent

and

> Economic execution

This project fills that gap.

We are building a payment execution layer that allows AI systems to complete real-world transactions through two models:

1. Human-approved execution (Agent Cash)
2. Sovereign wallet-based execution (Agent Wallet)

---

## 2. The Two Primary Economic Surfaces of the Web

There are two major monetized environments today:

### A) The Programmable Web (402)

- HTTP 402 Payment Required
- Metered APIs
- Microtransactions
- Pay-per-request systems
- Protocol-native settlement (USDC, Solana, Base, etc.)

These systems are machine-friendly but not human-friendly.

### B) The Commercial Web (Stripe / Shopify / SaaS)

- Stripe Checkout
- Shopify stores
- SaaS subscriptions
- Digital goods
- Direct-to-consumer brands

These systems are human-friendly but not AI-native.

AI agents operate across both environments.
There is no unified payment layer that works in both.

That is the opportunity.

---

## 3. Product 1: Agent Cash (Human-Approved Execution)

Agent Cash allows a user to approve AI-initiated transactions using standard card rails (Apple Pay / Google Pay via Stripe).

It operates in two equally important scenarios:

### 3.1 Unlocking 402 Gates

If an agent encounters a 402 payment requirement:
- The cost is presented.
- The user approves with Apple Pay.
- Settlement occurs (crypto behind the scenes if required).
- The resource unlocks.
- The authorization is destroyed.

The user does not:
- Hold a wallet.
- Understand USDC.
- Fund crypto.
- Store balances.

The underlying settlement mechanism is abstracted.

From the user's perspective:

> "This costs $0.10. Tap to unlock."

This makes 402 usable for normal humans.

### 3.2 Buying from Stripe Merchants (Including Shopify)

If an agent finds something purchasable from a Stripe-powered merchant:
- A Stripe Checkout session is generated.
- The user approves with Apple Pay.
- The purchase completes.
- The agent resumes workflow.

This includes:
- Shopify stores
- SaaS subscriptions
- Digital downloads
- Physical goods

Stripe Checkout effectively represents a large portion of modern internet commerce.

Agent Cash makes those merchants buyable from inside AI conversations.

---

## 4. Product 2: Agent Wallet (Sovereign Mode)

Agent Wallet is the bring-your-own-wallet model.

It allows:
- Funding via Coinbase or other on-ramps
- Holding USDC
- Direct 402 settlement
- Programmatic autonomy
- Fully agent-native execution

This model:
- Does not require Stripe
- Does not require Apple Pay
- Does not involve human approval per transaction
- Is open source (MIT)

**Agent Wallet is sovereignty. Agent Cash is consent.**

Both share core logic. They differ in trust and risk models.

---

## 5. The Chargeback Problem

The primary systemic risk in card-backed AI execution is chargebacks.

There are two failure modes:
1. Legitimate refund requests
2. Refund + chargeback abuse (filing dispute after receiving refund)
3. Direct chargebacks without contacting the platform

If AI agents are allowed to trigger payments at scale, unmanaged chargebacks can destroy the business.

Therefore, the system adopts a clear philosophy:

**Minimize friction. Do not fight users. Manage risk structurally.**

---

## 6. Chargeback Philosophy

The strategy is not aggressive dispute defense.
The strategy is controlled exposure.

### 6.1 Micro-Transaction Limits

- Unlisted sites may be capped at very low transaction amounts (e.g., $0.10-$0.25).
- Higher amounts require merchant onboarding or whitelist status.

This limits financial exposure per event.

### 6.2 Whitelisted Merchants

Merchants can:
- Opt into the ecosystem.
- Agree to platform terms.
- Integrate via Stripe Connect.
- Accept merchant-of-record status when possible.

Whitelisted merchants receive:
- Higher transaction limits.
- Reduced gating.
- AI-native discoverability.

The platform receives:
- Lower chargeback exposure.
- Defined refund flows.
- Clear settlement rules.

### 6.3 Conservative Refund Policy

For end users:
- If someone requests a refund, it is issued.
- The platform does not fight consumers aggressively.
- Refund experience is clean and immediate.

Risk is absorbed through:
- Reserves
- Transaction caps
- Merchant gating
- Monitoring chargeback ratios

### 6.4 Merchant-of-Record Structure

When possible:
- Stripe Connect is used.
- The merchant remains merchant of record.
- Chargeback liability sits with the merchant.

When not possible (e.g., 402 bridge mode):
- The platform may act as merchant of record.
- Exposure is capped via micro-transaction limits and reserves.

---

## 7. Controlled Rollout Model

This system is not launched open to the entire internet on day one.

Initial model:
- Limited beta access
- Merchant vetting
- Chargeback monitoring
- Transaction caps
- Controlled merchant onboarding

This allows experimentation with:
- AI-native purchasing behavior
- Refund rates
- Fraud patterns
- User approval UX

The goal is to determine whether AI-executed commerce can function safely at scale.

---

## 8. Risk Model

Risk is managed through:
- Per-transaction caps
- Whitelisting tiers
- Reserve buffers
- Refund-first philosophy
- Stripe fraud tooling
- Merchant onboarding controls

The system is intentionally conservative at launch.

It is designed to explore viability without catastrophic exposure.

---

## 9. The Unified Abstraction

Internally, both Agent Cash and Agent Wallet share:
- 402 detection
- Payment intent creation
- Settlement abstraction
- Unlock execution
- Token lifecycle management

The system routes based on context:
- Human-approved rail (Stripe / Apple Pay)
- Wallet-based rail (USDC / 402 native)

From the outside, it appears as:

> "Do you want me to buy this?"

From the inside, it is a controlled payment execution engine.

---

## 10. What This Is

This is:
- A payment abstraction layer for AI
- A consent-based execution system
- A bridge between programmable web and commercial web
- A controlled experiment in AI-initiated commerce

It is not:
- A bank
- A wallet app for consumers
- A crypto exchange
- A marketplace

It is infrastructure for AI-driven economic activity.

---

## 11. The Foundational Bet

AI will increasingly:
- Discover paid APIs
- Recommend purchases
- Trigger economic decisions

Humans will require:
- A clear approval surface
- Low-friction execution
- Refund confidence
- Chargeback-aware architecture

Agent Cash provides consent-based execution.
Agent Wallet provides sovereign execution.

Together, they form the first coherent payment layer designed specifically for AI agents operating across both protocol-native and commerce-native environments.
