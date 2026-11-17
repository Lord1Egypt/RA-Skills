# External Feedback: Stripe Connect Platform Plan

**Date:** 2026-02-25
**Reviewer:** Grok
**Verdict:** "Structurally sound. First version that feels institutional."

---

## What Grok Validated

- Architecture is correct: Stripe is regulated layer, we're orchestration layer
- Not a money transmitter under Connect model
- Partner Stores is Stripe's favorite (low risk, high volume, clean)
- Connectors is what Stripe will care about most (high-volume micro-marketplace)
- "You're effectively onboarding the long tail of AI tool builders onto Stripe"
- Platform company framing is the correct move

## Critical Issues

### 1. The $0.30 Fixed Fee Problem (Existential)

At $0.60 transactions: 2.9% + $0.30 = ~51% fee. Impossible.

**Solutions:**
- Batch (pre-authorize budget, capture once per task)
- Minimum task spend floor ($0.50 or $1)
- Wallet top-ups (load $5, spend in micro-increments)
- Negotiate micropayment pricing (5% + $0.05) ... but won't get this pre-scale

**Economics require average task size >= $3-$5.** Or heavy batching.

### 2. Pre-Authorization Timing

Stripe will ask: how long are holds? What if task fails?

**Policy needed:**
- Auth expires in X minutes
- Task fails: cancel intent
- No long-running holds
- Keep under 24 hours max

### 3. Crypto Component

Stripe will scrutinize the 402 USDC piece. Don't lead with it.

**Framing:** "Stripe funds go to our treasury. We independently fund USDC pool." Keep crypto operationally separated from Stripe flow.

## Strategic Advice

### How to Pitch Stripe

> "We are building a vertical marketplace on Connect optimized for agent-mediated transactions."

**Lead with:** Marketplaces, SaaS platforms, creator platforms, API monetization (things Stripe understands)

**Don't lead with:** Crypto, AI hype, USDC paywalls

**The wedge:** Stripe does NOT yet have agent-native commerce infrastructure. That's the gap.

### Before Talking to Stripe

1. Clarify minimum task spend assumption
2. Remove "$0.03 per call" examples from Stripe conversation
3. Show batching math
4. Emphasize $5-$50 task size vision
5. De-emphasize crypto complexity initially

## Decisions

### LLC vs Corp
**Delaware C-Corp.** Not Wyoming LLC. Investors care about this. Stripe doesn't.

### Express vs Custom Connect
**Start Express.** Stripe handles KYC, tax, payouts. Less surface area.

### International
**Not in v1.** US only. USD only. Expand after chargeback rates proven and fraud model tuned.

### Legal
**2-hour fintech counsel consult.** Required because: orchestrating split payments, enabling third-party sellers, touching crypto rails. Probably fine but cheap insurance.

## Year 2 Unit Economics Check

$10M GMV, average task size $5:

```
Stripe processing (~3%): $300K (Stripe keeps this)
Our application_fee (3-5%): $300K-$500K (we keep this)
```

Viable at $5 average. Collapses at $0.60 average.

## The Moat

Every connector dev builds on our manifest format, settlement flow, and registry. Switching away means rebuilding billing, onboarding, and losing discovery. That's lock-in.
