# External Feedback: Stripe Connect Platform Plan

**Date:** 2026-02-25
**Reviewer:** Grok
**Verdict:** "This version is fundable, Stripe-partnerable, and actually makes the flywheel spin."

---

## What Grok Validated

- Architecture is correct. Stripe's deal team thinks exactly this way.
- We're their favorite playbook: vertical capability marketplace on Connect (like Shopify, DoorDash, OnlyFans)
- Pre-auth + partial capture fully supported via PaymentIntents (manual capture). Holds 7 days, partial capture releases remainder instantly.
- Express Connect is the right starting point

## Fresh Stripe Data (Feb 25, 2026)

- Standard cards: 2.9% + $0.30 domestic (no public micropayment tier at our scale)
- Connect Express: $2/month per active connected account + 0.25% + $0.25 per payout
- Can start with "platform pricing" where Stripe bills connected accounts directly, we just collect application_fee_amount

## The Fix: Wallet + Task-Level Batching Hybrid

**This is the missing piece that makes the model bankable.**

### Layer 1: AI CASH Wallet (Prepaid Balance) ... Default for Power Users

- User taps Apple Pay once to load $25 / $50 / $100
- Agent spends from balance instantly: "Deducting $0.82 from your AI CASH balance. Remaining: $42.18. Approve task?"
- No extra card fee until reload
- Turns 1,000 micro-connector calls into 2-4 top-ups per month
- **Effective Stripe cost drops to <1% in steady state**

### Layer 2: Task-Level Pre-Auth ... For One-Off Users

- Agent bundles everything: "Full research brief + 3 logos + PDF export = est $4.20 (budget cap $6). Approve?"
- One pre-auth, run all connectors internally, capture exact amount at end
- Partial failure = instant partial refund to wallet

## Year 2 Unit Economics (100K tasks/month)

| Metric | $1.50 avg | $4.50 avg (target) | $12 avg (mature) |
|---|---|---|---|
| Monthly GMV | $150K | $450K | $1.2M |
| Stripe processing | ~$19.5K | ~$43K | ~$95K |
| Our platform fee (4%) | $6K | $18K | $48K |
| Connect acct/payout fees | ~$4K | ~$4K | ~$6K |
| **Our net revenue** | **negative** | **+$11K** | **+$37K** |
| Devs receive | $126K | $389K | $1.05M |

**At $4.50+ average task size we're profitable on day one of scale.** Wallet model pushes effective fee way lower and makes $1.50 tasks viable too.

## Tightened Recommendations

1. **Minimum viable task size in registry: $1.50 est.** Agent must bundle micro-calls into outcomes ("Full deep-research report" not "single Tavily call")
2. **Lead with wallet** in consumer journey. Keep the "tap once" moment but make it a reload, not every task.
3. **De-emphasize $0.03/call** in all external decks. Replace with: "$4.20 for a complete research brief with sources and visuals."
4. **Delaware C-Corp.** Raising or talking Stripe seriously requires credibility.
5. **Start Express Connect.** Zero extra surface area.

## The Pitch Line

> "We are building the capability registry and orchestration layer that turns Stripe's existing Agentic Commerce infrastructure into a thriving two-sided marketplace of 10,000+ indie agent tools. Every developer becomes a Stripe connected account. Every consumer taps once."

No crypto-first language. Marketplace + long-tail onboarding + agent-native UX.

## Key Reframe: Bundle Outcomes, Not Calls

Don't sell "$0.03 per web search." Sell "$4.20 for a complete research brief with sources and visuals."

The registry should encourage developers to publish high-value bundled outcomes, not raw API wrappers. This pushes average task size into the $3-12 range where economics work.

## What Grok Suggests Next

1. Draft 1-page Stripe executive brief
2. Full unit economics model (wallet vs pure pre-auth scenarios)
3. Updated consumer + developer journeys with wallet/task-batch flows
4. Revised manifest spec that supports bundled high-value outcomes
