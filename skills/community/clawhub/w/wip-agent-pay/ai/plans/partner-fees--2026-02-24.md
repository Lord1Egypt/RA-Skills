# Partner Fee Structure (Draft v2)

**Date:** 2026-02-24
**Status:** Draft. Refined after Parker's strategic review. Needs marketplace research before finalizing.

---

## Two-Sided Fee Model

AI CASH is a conversion layer. Double-sided fees are normal for conversion layers. But must be disclosed clearly.

### Buyer Side (AI CASH)
- **$0.25 convenience fee** per transaction + standard card processing (Stripe ~2.9% + $0.30)
- Only applies to AI CASH transactions (not AGENT WALLET)
- The $0.25 is really a micro-transaction tax ... intentional, not universal

### Seller Side (Partner Fee)
- Percentage-based, tiered by transaction size
- Free for first 90 days (introductory period)

---

## Proposed Fee Structure (v2)

### Option A: Transaction Size Tiers (Recommended)

Clean, three-lane model. Easy to explain. No cliffs.

| Transaction Size | Platform Fee |
|-----------------|-------------|
| Under $25 | 5% |
| $25 - $250 | 3.5% |
| $250+ | 2% |

No flat fee on the seller side. The $0.25 flat only lives on the buyer side.

### Examples

```
$5 article unlock:
  Buyer pays:    $5.00 + $0.25 + Stripe fees (~$0.45) = $5.70
  Seller receives: $5.00 - 5% ($0.25) = $4.75
  Platform take:  $0.25 (buyer) + $0.25 (seller) = $0.50

$50 product:
  Buyer pays:    $50.00 + $0.25 + Stripe fees (~$1.75) = $52.00
  Seller receives: $50.00 - 3.5% ($1.75) = $48.25
  Platform take:  $0.25 (buyer) + $1.75 (seller) = $2.00

$500 product:
  Buyer pays:    $500.00 + $0.25 + Stripe fees (~$14.80) = $515.05
  Seller receives: $500.00 - 2% ($10.00) = $490.00
  Platform take:  $0.25 (buyer) + $10.00 (seller) = $10.25
```

### Why This Structure

- **No cliffs.** The old model had a sharp jump at $99/$100. Three lanes are smoother.
- **$0.25 flat stays buyer-side only.** At $1,000 the flat fee is meaningless on the seller side. It's a micro-transaction tax, not a universal fee.
- **Max 2% at scale.** Extremely competitive vs app stores (15-30%), marketplaces (10-20%), affiliates (5-15%).
- **Three lanes map to the business:** Under $25 = AI unlock economy (articles, skills). $25-$250 = commerce. $250+ = enterprise/high-ticket.

---

## Alternative Models (Saved for Reference)

### Option B: Volume-Based (Cleaner for Merchants)

```
Base rate: 4%
After $X monthly volume: 3%
After $Y monthly volume: 2%
```

Rewards growth instead of price band. Merchants prefer this. But harder to implement (requires tracking monthly volume per partner in KV).

### Option C: Hybrid (Three Lanes by Category)

```
AI unlock economy (articles, APIs, skills): 5%
Commerce (products, subscriptions): 3%
Enterprise / high ticket: 2%
```

Very easy to explain. But requires categorization logic.

### Original v1 Model (Superseded)

```
Under $10:    $0.25 + 5%
$10-99:       $0.25 + 4%
$100-499:     $0.25 + 3%
$500+:        $0.25 + 2%
```

Problems: too many tiers, cliff at $99/$100, flat fee scales weirdly at high end.

---

## Strategic Considerations

### Double-Dipping Disclosure

Buyer pays $0.25 AND merchant pays 3-5%. This is double-sided.

- Normal for conversion layers (Stripe Connect, payment processors, marketplaces all do this)
- Must disclose clearly in partner agreements
- Merchants WILL ask
- Positioning matters: "high-value execution layer" not "commodity processor"

### What Are We Optimizing For?

Current model optimizes for: **perceived fairness + merchant adoption**

- 2% at scale signals we're not greedy
- 5% on micro-transactions is invisible ($0.25 on a $5 article)
- 90-day free intro removes adoption friction
- Clean three-lane structure feels intentional, not arbitrary

### Competitive Positioning

| Platform | Take Rate |
|----------|----------|
| Apple App Store | 15-30% |
| Amazon Marketplace | 8-15% |
| Etsy | 6.5% + listing |
| Uber Eats | 15-30% |
| **AI CASH** | **2-5%** |

We're the cheapest execution layer. That's the story.

---

## Research TODO

Before finalizing, study how these platforms structure seller fees:

- **Uber Eats** ... what % from restaurants? Flat fees? Tiered by volume?
- **DoorDash** ... same. How do they handle small vs large orders?
- **Etsy** ... transaction fee + listing fee + payment processing breakdown
- **Shopify** ... % on non-Shopify Payments transactions. Their tiers.
- **Amazon Marketplace** ... referral fee by category (8-15%). Any flat component?
- **Stripe Connect** ... what do platforms typically charge via application_fee? Industry norms?
- **Apple App Store / Google Play** ... 15-30% but different model. Ceiling reference.

### Open Questions

1. Should 402 partners have different fees than Stripe partners? (Different risk profile ... we're MoR on 402, merchant is MoR on Stripe)
2. Volume discounts? (e.g., partner processes $10K/month, fee drops) ... Option B above
3. Is 90-day intro long enough? What do competitors offer?
4. Minimum monthly fee after intro period? Or pure usage-based?
5. Stress test: what does our take look like on a $10K/month merchant?
6. Model: what does total platform revenue look like at scale (100 merchants, mixed transaction sizes)?

---

## Where This Gets Implemented

- **Stripe partners:** `application_fee_amount` on Stripe Connect checkout sessions in `worker/index.js`
- **402 partners:** Deducted from pool settlement. Needs design work.
- **Partner tiers:** Already defined in PARTNERS-STRIPE.md and PARTNERS-402.md (Tier 0/1/2). Fee tiers may or may not align with trust tiers.
- **Volume tracking (if Option B):** Would need KV-based monthly volume counter per partner domain.
