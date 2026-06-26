# Rebuy Booster Quality Checklist

Use this checklist before delivering any Rebuy Booster output. Items marked REQUIRED must pass before delivery. Items marked RECOMMENDED represent best practices that significantly improve performance.

---

## Category 1 — Sequence Architecture (REQUIRED)

- [ ] Campaign type is clearly identified (second-purchase / re-order / win-back / VIP escalation / referral / loyalty onboarding)
- [ ] Target segment is defined with explicit entry criteria (not "all customers")
- [ ] Behavioral trigger or schedule is defined for Email 1
- [ ] Exit condition (purchase, opt-out) is defined and applies to all emails in sequence
- [ ] Re-entry delay is specified after sequence completes without conversion
- [ ] Number of emails and send timing for each is specified

---

## Category 2 — Repurchase Timing Logic (REQUIRED)

- [ ] For consumable products: repurchase interval is stated (from data or estimated from product cycle)
- [ ] Re-order trigger timing is calibrated to 70–80% of consumption cycle — not a fixed calendar date
- [ ] Re-order trigger has a flow exit if customer purchases before trigger fires
- [ ] Non-consumable products: cross-sell logic is used instead of re-order logic
- [ ] Timing assumption is flagged if based on benchmark rather than actual order data

---

## Category 3 — Suppression Logic (REQUIRED)

- [ ] Purchase suppression is configured — sequence stops on conversion
- [ ] Opt-out suppression is configured — sequence stops and subscriber is added to permanent suppression list
- [ ] Win-back sequences: lapsed buyers are suppressed from regular broadcast emails during win-back window
- [ ] VIP escalation: customers entering VIP flow are exited from standard retention sequences
- [ ] Frequency cap with other active sequences is defined

---

## Category 4 — Subject Lines and Preview Text (REQUIRED)

- [ ] Every email has a subject line and preview text pair
- [ ] Subject lines are under 50 characters (mobile-optimized)
- [ ] Preview text is 85–100 characters and extends subject line with new information
- [ ] Preview text is not blank or a duplicate of the subject line
- [ ] No spam trigger words (FREE, YOU WON, CLICK HERE, GUARANTEED)
- [ ] No ALL CAPS subject lines or excessive punctuation (max 1 exclamation point)

---

## Category 5 — Body Copy (REQUIRED)

- [ ] Each email has a clear hook in the first sentence
- [ ] Offer (if present) is specific — dollar amount, percentage, free shipping, or product gift (not vague "savings")
- [ ] Single CTA per email — one action verb, one destination
- [ ] Merge tag placeholders are noted: [FIRST_NAME], [PRODUCT_NAME], [ORDER_NUMBER], [BRAND_NAME]
- [ ] Review request email does not contain promotional offers (transactional)
- [ ] Re-order reminder references specific product purchased — not generic catalog

---

## Category 6 — RFM Segmentation (RECOMMENDED)

- [ ] Win-back sequences segment by recency × frequency — high-value lapsed buyers receive different sequence than low-value
- [ ] Second-purchase sequence targets first-time buyers only (not repeat buyers)
- [ ] VIP escalation trigger is explicitly defined (order count threshold, spend threshold, or both)
- [ ] Lapsed threshold is defined and appropriate for the product category (90d / 180d / 365d)
- [ ] Lapsed single-order buyers are treated differently from lapsed multi-order buyers

---

## Category 7 — Loyalty Program Logic (RECOMMENDED)

- [ ] Points earn rate and redemption value are specified (not just "earn points")
- [ ] Tier entry thresholds are explicit (order count or spend amount)
- [ ] Each tier has distinct, non-monetary benefits (not just bigger discounts)
- [ ] Loyalty onboarding email explains how to earn, how to redeem, and current balance
- [ ] Points expiration policy is stated if applicable
- [ ] Loyalty economics have been validated: benefit cost < LTV uplift generated

---

## Category 8 — Referral Program Logic (RECOMMENDED)

- [ ] Referral activation timing is defined: 7–14 days post-delivery (not at purchase)
- [ ] Referrer reward and friend reward are both specified
- [ ] Referrer reward is tied to friend's purchase — not to link click
- [ ] Referral incentive is proportional to product AOV
- [ ] Referral link injection method is confirmed for the platform being used

---

## Category 9 — Platform Configuration (RECOMMENDED)

- [ ] ESP platform is identified
- [ ] Loyalty platform is identified (if applicable)
- [ ] Trigger event name matches ESP's actual metric name
- [ ] Loyalty property sync to ESP is confirmed (tier, points balance, referral URL)
- [ ] Flow exit event is specified using platform's terminology
- [ ] Subscription platform integration is noted if applicable (Recharge, Bold, Loop)

---

## Category 10 — Flags and Disclaimers (REQUIRED when applicable)

- [ ] Any assumed repurchase intervals are flagged — note if based on benchmark not actual data
- [ ] Any assumed brand voice or segment definitions are flagged as assumptions
- [ ] Platform-specific setup notes are accurate for current platform version
- [ ] Not legal advice disclaimer present for any compliance-adjacent guidance
- [ ] GDPR / CASL flags noted if sequences target EU or Canadian subscribers

---

**Checklist score guide:**
- All REQUIRED items pass + 80%+ RECOMMENDED items pass → Deliver output
- Any REQUIRED item fails → Fix before delivering
- Less than 60% of RECOMMENDED items pass → Note gaps explicitly in output
