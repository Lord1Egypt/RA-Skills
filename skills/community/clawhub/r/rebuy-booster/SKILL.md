---
name: Rebuy Booster
description: Design post-purchase sequences, loyalty incentives, and re-order triggers that turn one-time buyers into repeat customers for ecommerce brands.
---

# Rebuy Booster

The hardest sale is the first one. The most profitable sale is the second. Rebuy Booster designs the systems that convert one-time buyers into repeat customers — post-purchase sequences that build habits, loyalty programs that reward the right behaviors, and re-order triggers calibrated to actual product consumption cycles. Most ecommerce brands spend 80% of their marketing budget acquiring new customers while leaving second-purchase conversion — the single highest-ROI lever in their stack — completely unoptimized.

## Solves

1. **No second-purchase strategy** — brands with sophisticated acquisition funnels have zero post-purchase nurture beyond a shipping confirmation, leaving 60–70% of first-time buyers to never return despite high intent immediately after purchase

2. **Loyalty programs that reward passive behavior** — points systems that reward every purchase equally with no graduation logic, no VIP tiers, and no behavior shaping fail to increase purchase frequency or AOV

3. **Re-order timing that misses the consumption window** — re-order reminders sent too early (before product is consumed) or too late (after the customer has already found an alternative) have near-zero conversion

4. **Post-purchase sequences that only confirm orders** — transactional emails that fail to introduce the brand story, cross-sell adjacent products, or request reviews leave the post-purchase window completely monetized

5. **Win-back campaigns that treat all lapsed buyers the same** — sending the same "we miss you" message to a lapsed 90-day buyer and a lapsed 365-day buyer ignores purchase history depth and why each segment lapsed

6. **No VIP identification or,escalation logic** — brands without a formal VIP tier definition miss the opportunity to identify high-LTV customers early and accelerate their loyalty cycle before they have a chance to churn

7. **Referral programs with no activation trigger** — referral mechanics that activate before the customer has experienced the product (or too long after) miss the peak advocacy window and generate low-quality referrals

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| **Second-purchase email timing** | 3–5 days post-delivery — after product experience, before habit window closes | 7–10 days post-delivery | Same day as delivery or 30+ days later |
| **Re-order trigger timing** | Based on product consumption cycle — 80% of average repurchase interval | Fixed 30-day reminder regardless of product type | No re-order trigger; relies on customer initiating |
| **Loyalty program structure** | Tiered with behavioral escalation — purchase frequency + AOV + referrals unlock tiers | Points-per-purchase with redemption threshold | No formal program; ad-hoc discount codes for repeat buyers |
| **VIP definition** | Explicit threshold — 3+ orders OR $300+ LTV within 12 months; triggers separate flow | Top 10% of buyers by spend | Undefined — treated as general repeat buyers |
| **Cross-sell strategy** | Category-adjacent — product affinity data or purchase sequence logic | Bestseller recommendation | Random catalog or same category as first purchase |
| **Referral activation timing** | 7–14 days post-delivery — after first product experience | At purchase confirmation | Before delivery or 60+ days post-purchase |
| **Lapsed buyer segmentation** | 3+ tiers by recency × frequency × monetary (RFM) with distinct angles per tier | Segment by recency only (90d / 180d / 365d) | Single lapsed segment — one message for all non-buyers |
| **Win-back offer logic** | Escalate offer across 3 emails: no offer → soft offer → final offer; category-specific incentive | Offer in first win-back email only | Same discount to all lapsed buyers regardless of LTV |

## Workflow

### Step 1 — Map the customer lifecycle stages
Before building any sequence, map the stages: first purchase → second purchase → habitual buyer → VIP → advocate. Each stage needs a distinct strategy. Trying to move a first-time buyer to VIP status with one email sequence fails because the conversion steps are different at each stage boundary.

### Step 2 — Calculate product-specific repurchase windows
For consumable products, pull average repurchase interval from order history (or use category benchmarks if no data exists). Non-consumables need cross-sell mapping instead. This step determines re-order trigger timing and the urgency frame to use — "running low" only works if the timing matches actual consumption.

### Step 3 — Define the loyalty tier structure
Set explicit thresholds for tier entry and escalation (e.g., Tier 1: 2+ orders, Tier 2: 4+ orders or $250+ LTV, Tier 3 VIP: 8+ orders or $600+ LTV). Define what each tier unlocks: early access, exclusive products, free shipping, higher discount ceilings, or a personal account manager for enterprise. Tiers without distinct benefits are just labels.

### Step 4 — Build the second-purchase sequence
This is the highest-leverage sequence in the stack. It runs 3–5 days post-delivery, after the product experience has formed. Email 1: product onboarding + review request. Email 2 (no purchase): cross-sell with social proof. Email 3 (no purchase): soft incentive or bundle offer with urgency. Goal is a second purchase within 30 days of first delivery.

### Step 5 — Design win-back sequences by RFM segment
Segment lapsed buyers by recency, frequency, and monetary value. A lapsed high-frequency buyer (lapsed 90 days, 6 past orders) gets a different angle than a lapsed low-frequency buyer (lapsed 180 days, 1 past order). High-value lapsed buyers get personalized outreach and larger incentives; low-value lapsed buyers get a brand value reminder and small incentive or suppression.

### Step 6 — Configure referral activation logic
Referral asks should activate 7–14 days post-delivery — after the product experience forms but while advocacy intent is high. Pre-delivery referral asks generate low-quality referrals from people who haven't used the product. The referral mechanic should give the referrer a benefit tied to the referral's first purchase (not just a blanket coupon) to align incentives.

### Step 7 — Deliver complete output package
For every output: include the sequence overview table, individual email blocks, re-order timing logic, loyalty tier definitions, suppression rules, and platform setup notes. Flag any assumptions about product consumption cycle, repurchase interval, or loyalty tier thresholds that require verification from actual order data.

## Examples

### Example 1 — Second-purchase sequence for a supplement brand

**Inputs:**
- Product: Protein powder (avg. consumption: 30 days per unit)
- Platform: Klaviyo
- Brand voice: Science-backed, direct, non-hype
- Segment: First-time buyers only
- Repurchase window: 28 days average

**Sequence Overview:**

| Email | Timing | Angle | Offer |
|---|---|---|---|
| Email 1 | Day 5 post-delivery | Product education + review ask | None |
| Email 2 | Day 14 (no purchase) | Cross-sell: accessories + stacks | None |
| Email 3 | Day 21 (no purchase) | Re-order reminder — "you're halfway through" | 10% off first subscription |

**Exit condition:** Purchase at any step stops sequence.

---

**Email 1 of 3**

**Subject:** How's the protein treating you? (+ a quick favor)
**Preview text:** Most people notice a difference by day 7 — here's what to expect, and what to try next.

Hi [FIRST_NAME],

You've had [PRODUCT_NAME] for about five days now. Here's what's actually happening when you use it: [brief product education — 2-3 sentences on the science, outcome, best use case].

One quick ask: if you've tried it, we'd love a review. It takes 60 seconds and helps other customers make smarter choices.

[Leave a review →]

Questions? Reply here — our nutrition team reads every message.

— [BRAND_NAME]

**CTA:** Leave a review → product review page

---

**Email 3 of 3 (re-order trigger)**

**Subject:** You're probably about halfway through
**Preview text:** Day 21 — most customers re-order around now. Here's why, and a reason to do it today.

Hi [FIRST_NAME],

If you started using [PRODUCT_NAME] when it arrived, you're probably around the halfway point right now.

Most customers re-order at day 21 so their next supply arrives before they run out. We've added a reason to do it today:

**10% off your next order — or subscribe and save 15% with free shipping.**

Use [CODE] at checkout. Valid for 72 hours.

[Re-order now →]

---

### Example 2 — VIP escalation sequence for a skincare brand

**Inputs:**
- Trigger: Customer places 4th order (VIP threshold)
- Platform: Omnisend
- Brand voice: Warm, personal, aspirational

**Sequence Overview:**

| Email | Timing | Angle |
|---|---|---|
| Email 1 | Immediately on 4th order | Welcome to VIP — what it means |
| Email 2 | Day 7 | Exclusive early access to new product |
| Email 3 | Day 30 | Personal check-in + loyalty reward |

---

**Email 1 of 3**

**Subject:** You've officially made the list, [FIRST_NAME]
**Preview text:** Four orders in — here's what's unlocked for you from here.

Hi [FIRST_NAME],

We keep track of our best customers — not because we have to, but because they deserve something different.

You've just placed your fourth order with us. That puts you in our VIP tier, which means:
- Early access to new launches before anyone else
- Priority support with a 2-hour response guarantee
- A 20% birthday discount (we'll remind you)
- Exclusive bundles never listed publicly

This isn't a loyalty points game. It's just how we treat people who keep coming back.

Welcome to the list.

— [BRAND_NAME] Team

**CTA:** See your VIP benefits → account page

---

## Common Mistakes

1. **Re-order reminders at fixed intervals** — sending a "re-order now" email 30 days after purchase for a 60-day supply product means the customer isn't even close to running out. Calculate actual consumption cycles: check average repurchase interval from your order data, or use product size and usage instructions to estimate.

2. **Loyalty points that don't drive behavior change** — a points program that rewards $1 spend with 1 point and requires 500 points to redeem $5 is mathematically transparent and fails to motivate. Points programs work when earning feels fast and the reward feels meaningful. If customers can't redeem within 3–4 orders, the program won't change behavior.

3. **Second-purchase email too early** — sending a cross-sell the day of delivery assumes the customer has already formed a product opinion. Send after product experience (3–5 days post-delivery for consumables, 7 days for physical goods). The review request alone in this window doubles as a loyalty signal — customers who leave reviews have 3× higher repeat purchase rates.

4. **VIP perks that are just bigger discounts** — VIP tiers based purely on discount depth train high-value customers to expect discounts, reducing margin on your best segment. The best VIP perks are non-monetary: early access, exclusive products, faster support, behind-the-scenes content. These build emotional loyalty rather than transactional loyalty.

5. **Same referral offer for all customers** — offering a $10 referral credit to someone who just bought a $200 product feels token-level. Scale the referral incentive to match the product and customer LTV. High-AOV products warrant larger referral bonuses; consumables with high reorder cycles warrant subscription referrals.

6. **No suppression between win-back and regular broadcasts** — sending win-back sequences to lapsed buyers while also sending them regular promotional broadcasts doubles frequency, signals desperation, and defeats the win-back angle. Suppress lapsed buyers from broadcasts during the win-back window.

7. **Conflating recency with intent** — a buyer who ordered once 6 months ago and a buyer who ordered 5 times but last purchased 6 months ago have very different win-back potential. The multi-buyer is worth a significant retention investment; the single-buyer has a much lower probability of reactivation and should receive a lighter-touch sequence.

8. **Loyalty program launch without a clear value exchange** — launching points without telling customers the earn rate, redemption options, and tier benefits in the first email means most customers don't realize they're accumulating points. The onboarding sequence for a new loyalty program is as important as the program itself.

9. **Cross-sell timing that conflicts with product lifecycle** — suggesting a complementary product before the customer has experienced the first one creates confusion and erodes trust. Map cross-sell timing to product milestones, not calendar days.

10. **Not tracking second-purchase rate as a north star metric** — most ecommerce analytics track ROAS and CAC but not second-purchase conversion rate, which is the primary indicator of whether your retention stack is working. If you can't measure it, you can't optimize it.

## Resources

- `references/output-template.md` — Standard output format for all Rebuy Booster deliverables
- `references/retention-strategy-guide.md` — Lifecycle stage frameworks, RFM segmentation, repurchase timing benchmarks by category
- `references/loyalty-platform-guide.md` — Platform-specific setup for Klaviyo, LoyaltyLion, Yotpo, and Smile.io
- `assets/rebuy-quality-checklist.md` — 40-point quality checklist for retention sequences and loyalty program outputs
