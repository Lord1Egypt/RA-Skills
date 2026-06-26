---
name: Referral Engine
description: Design a customer referral program with incentive structures, sharing mechanics, fraud prevention rules, and tracking setup that turns existing buyers into a scalable acquisition channel.
---

# Referral Engine

Design a customer referral program with incentive structures, sharing mechanics, fraud prevention rules, and tracking setup that turns existing buyers into a scalable acquisition channel. Referral is consistently the highest-converting acquisition source for ecommerce — referred customers convert at 3–5× the rate of cold traffic and have 16–25% higher LTV — but most referral programs fail because the incentive is wrong, the timing is off, or the mechanics are too complex for buyers to act on.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Incentive type | Double-sided reward (both referrer and referee get value) | One-sided reward for referrer only | Discount-only incentive with no novelty |
| Trigger timing | First positive experience moment (post-delivery Day 7–14) | Post-purchase confirmation page | Sent only to all customers at once via blast email |
| Reward value | 10–20% of AOV or product credit with real perceived value | Flat $5–$10 credit | $1–$2 credit that feels insulting |
| Sharing mechanics | 1-click share with pre-filled message to WhatsApp, SMS, email | Copy-paste link only | Manual "tell a friend" with no tracking |
| Fraud prevention | Email domain checks, IP/device deduplication, minimum order before payout | Basic duplicate email check | No fraud protection |
| Program measurement | Track referral CAC vs. other channels; CLV of referred cohort | Track total referrals sent | Count referral codes shared only |
| Program visibility | Persistent account page link + post-purchase flow + triggered email | Only in one email | Hidden in footer |

## Solves

- High customer acquisition cost from paid channels with no organic growth loop
- Strong product-market fit but weak word-of-mouth spread
- Loyal customers who would refer but have no easy mechanism to do so
- New store or brand with low ad budget needing cost-efficient first customers
- Existing customers who don't re-engage after their first purchase
- Discount dependency cycle — needing to offer promos to drive repeat business
- No measurable advocacy metric tied to customer satisfaction

## Workflow

### Step 1 — Define Program Economics

Before designing the referral experience, validate the economics work for your margins.

**Unit economics check:**

| Metric | Your number | Target range |
|---|---|---|
| Average Order Value (AOV) | | |
| Gross margin % | | |
| Current CAC (paid channels) | | |
| Target referral CAC | | <50% of paid CAC |
| Maximum reward budget | | <25% of gross margin on referred order |

**Reward type options by margin profile:**

| Margin | Best reward type | Why |
|---|---|---|
| >50% GM | Product credit or free item | High perceived value, low real cost |
| 30–50% GM | Discount code (15–20% off) | Sustainable; still feels meaningful |
| <30% GM | Cash reward on second order | Defer cost to proven repeat buyer |
| Any | Tiered rewards (more referrals = better reward) | Gamification without upfront cost |

**Double-sided reward benchmark:**
- Referrer gets: $15–20 credit or 15% off next order
- Referee gets: 10–15% off their first order
- Both rewards activate only when the referred order ships (not at sign-up)

### Step 2 — Choose Program Structure

**Standard referral (recommended for most stores):**
Every customer gets a unique referral link after purchase. Referrer rewards activate on friend's first order.

**Loyalty-gated referral:**
Referral program unlocked after Nth purchase or reaching a spend threshold. Keeps program exclusive and rewards your best customers.

**Influencer / ambassador tier:**
Separate track for customers with large networks. Higher reward rates (20–30%) in exchange for content creation or social posts. Requires manual vetting.

**Group referral / squad mechanic:**
Referrer gets progressive rewards for multiple friends referred (1 friend = $10, 3 friends = $40, 5 friends = $100). Drives high-effort sharing from motivated advocates.

### Step 3 — Design the Sharing Experience

The referral share moment must be frictionless. Each additional step cuts conversion by ~40%.

**Required elements:**
1. Unique shareable link (auto-generated per customer)
2. Pre-written share message (editable, but pre-filled — never blank)
3. One-click share buttons: WhatsApp (highest conversion), SMS, Email, Copy link
4. Visual referral card with the offer clearly stated

**Pre-written message template:**
> "Hey! I've been buying from [Brand] and genuinely love [product/brand]. Here's 15% off your first order: [link]. I get a credit too when you order — thought I'd share!"

Personal tone, names the brand benefit, explains the mechanic briefly.

**Where to surface the share moment:**
- Order confirmation page (highest intent moment)
- Day 7–14 post-delivery email ("How's your order?")
- My Account → Referrals page (persistent, always accessible)
- Reorder email for consumables

### Step 4 — Set Up Tracking and Attribution

**Minimum viable tracking setup:**

| Tool tier | Option | Tracks |
|---|---|---|
| Built-in (Shopify) | Shopify Referrals or ReferralCandy | Basic referral links, discount attribution |
| Mid-tier | Yotpo Loyalty, Smile.io, Friendbuy | Full referral + loyalty, email flows |
| Enterprise | Impact.com, PartnerStack | Multi-channel affiliate + referral |

**UTM parameters for custom implementations:**
`?utm_source=referral&utm_medium=friend&utm_campaign=referral-program&utm_content=[customer_id]`

**Metrics to track from Day 1:**
- Referral share rate: % of eligible customers who share a link
- Referral conversion rate: referred visits → first order
- Referral CAC: total reward cost ÷ referred new customers
- Referred customer CLV: compare to non-referred cohort at 6 months

### Step 5 — Build Fraud Prevention

Referral fraud is common. Implement at minimum:

**Basic controls (must-have):**
- Reward activates only on completed, shipped order (never on sign-up)
- Self-referral prevention: same email domain as referrer = flagged
- IP address deduplication: multiple orders from same IP in same session = flagged
- Minimum order threshold before reward activates ($25–$50)

**Intermediate controls:**
- Delay reward payout by return window (e.g., 30 days after delivery before credit issued)
- Device fingerprinting to catch same-device referral loops
- Email domain block list (temporary email services: mailinator, guerrilla mail, etc.)
- Manual review queue for orders that trigger 2+ fraud signals

**Signs of fraud to watch:**
- Same IP generating 5+ referrals in one day
- Referral codes used by email addresses sharing domain patterns
- Referred customers who never return after redeeming referral discount

### Step 6 — Launch and Promote

**Launch sequence:**
1. Soft launch to your top 200 customers (high LTV, repeat buyers) — test mechanics, confirm reward delivery
2. Full launch to entire customer base via email campaign
3. Add referral CTA to post-purchase email series (Day 7 trigger)
4. Add referral to My Account navigation permanently

**Announcement email subject lines (A/B test):**
- "Give $15, get $15 — share [Brand] with a friend"
- "You've been asking how to share [Brand]. Here's how."
- "[First name], your friends get 15% off. Here's why."

### Step 7 — Optimize and Scale

**Monthly review:**
- Share rate below 5%? The incentive is too small or the sharing UX has too much friction
- Conversion rate below 20%? The referee offer isn't compelling enough; test higher discount
- Fraud rate above 10%? Tighten controls in Step 5

**Growth levers:**
- Seasonal multipliers: 2× rewards during holiday or brand anniversary
- Category-specific programs: higher rewards for premium products with high social currency
- Ambassador upgrade path: top referrers (5+ conversions) get invited to ambassador program with better economics

## Examples

### Example 1 — Coffee Subscription Brand (Shopify + Klaviyo)

**Setup:**
- AOV: $38; GM: 62%; Current paid CAC: $41
- Target referral CAC: <$20
- Reward: Referrer gets $15 store credit; referee gets 20% off first order
- Trigger: Day 10 post-delivery email ("How's your first bag?") with Smile.io link embedded

**Share message:**
> "Honestly one of the best coffees I've tried. Use my link for 20% off your first bag: [link]"

**90-day results:**
- 847 shares sent
- 12.4% referral conversion rate → 105 new customers
- Referral CAC: $14.29 (vs. $41 paid CAC — 65% cheaper)
- Referred customer 6-month retention: 54% vs. 38% non-referred

---

### Example 2 — Skincare Brand (WooCommerce + ReferralHero)

**Setup:**
- AOV: $62; GM: 55%; no prior referral program
- Reward structure: Double-sided — referrer gets free travel-size product ($14 value); referee gets 15% off
- Fraud control: 30-day payout delay; self-referral email domain check; $40 minimum order

**Insight:** Product credit (free travel size) outperformed $10 cash credit in A/B test by 34% on share rate because recipients perceived it as a gift, not a transaction.

**Result:** 6.8% of customers shared within 30 days; 22% referee conversion rate; referral program accounted for 18% of new customer acquisition by Month 3.

## Common Mistakes

1. **One-sided incentive only** — If only the referrer benefits, the share feels selfish. Double-sided rewards outperform single-sided by 30–50% on conversion.

2. **Launching before product-market fit** — Referral amplifies your existing word-of-mouth signal. If customers aren't naturally recommending you, a referral program won't create that impulse.

3. **Too-small incentive** — A $2 credit isn't motivating. The referrer is doing you a favor; the reward should feel meaningful. Match 15–20% of AOV as a rule of thumb.

4. **No fraud prevention** — Without basic controls, self-referral loops and bulk fake account creation can drain your reward budget quickly.

5. **Burying the program** — If the only access point is a single email sent at sign-up, most customers will never remember or find the program again.

6. **Complicated reward mechanics** — If explaining how to earn rewards takes more than two sentences, customers won't participate. Simplicity converts.

7. **No post-share nurture** — Referred visitors who don't convert on first visit need a follow-up sequence. Capture email at minimum; retarget if budget allows.

8. **Treating all customers equally** — Your top 10% of customers by LTV are 5–10× more likely to refer effectively. Target them first with higher incentives.

## Resources

- [Output Template](references/output-template.md) — Referral program design brief
- [Incentive Calculator](references/incentive-calculator.md) — Unit economics worksheet
- [Fraud Prevention Rules](references/fraud-prevention-rules.md) — Controls checklist and detection patterns
- [Quality Checklist](assets/quality-checklist.md) — Pre-launch review checklist
