# Rebuy Booster — Output Template

Use this template for every Rebuy Booster deliverable. Fill in all sections. Write "N/A — [reason]" for non-applicable sections.

---

## Campaign Summary

| Field | Value |
|---|---|
| Campaign type | [second-purchase / re-order / win-back / VIP escalation / referral / loyalty onboarding] |
| Platform | [Klaviyo / Omnisend / ActiveCampaign / Shopify Email / other] |
| Trigger | [behavioral trigger or segment criteria] |
| Target segment | [first-time buyers / repeat buyers / VIPs / lapsed 90d+ / loyalty members] |
| Product category | [consumable / physical goods / subscription / digital] |
| Repurchase interval | [X days — from data or estimated from product cycle] |
| Offer (if any) | [discount code, amount, expiry] |
| Brand voice | [tone notes] |
| Emails in sequence | [N] |

---

## Sequence Overview Table

| Email | Timing | Angle | Offer |
|---|---|---|---|
| Email 1 | [Xd after trigger] | [angle description] | [none / offer description] |
| Email 2 | [Xd after trigger] | [angle description] | [none / offer description] |
| Email 3 | [Xd after trigger] | [angle description] | [none / offer description] |

**Exit conditions:** [e.g., "Purchase exits all emails. Opt-out exits all emails."]

---

## Email 1 of N

**Trigger / send time:** [behavioral trigger or delay]

**Subject line:** [subject line text — note character count]
**Preview text:** [preview text — aim for 85–100 characters]

**Body copy:**

---
[Full email body. Use [FIRST_NAME], [PRODUCT_NAME], [ORDER_NUMBER], [BRAND_NAME] as merge tag placeholders.]
---

**CTA button text:** [single action verb phrase]
**CTA destination:** [page type — product, cart, account, review, referral]

**A/B Subject Line Variant:**
- Variant A: [primary subject]
- Variant B: [alternative subject with different hook angle]
- Variable being tested: [urgency / curiosity / personalization / benefit-first]

---

## [Repeat Email block for each message in sequence]

---

## Loyalty Program Definition (if applicable)

| Tier | Entry Threshold | Benefits |
|---|---|---|
| Tier 1 | [e.g., 2+ orders or $100+ LTV] | [e.g., free shipping on all orders] |
| Tier 2 | [e.g., 4+ orders or $250+ LTV] | [e.g., early access + 10% standing discount] |
| Tier 3 VIP | [e.g., 8+ orders or $600+ LTV] | [e.g., dedicated support + exclusive products] |

**Points structure (if points-based):**
- Earn rate: [X points per $1 spent]
- Redemption rate: [X points = $Y]
- Bonus multiplier events: [e.g., birthday month = 2× points]

---

## Re-Order Trigger Logic (if applicable)

| Product | Avg. consumption cycle | Trigger timing | Message angle |
|---|---|---|---|
| [PRODUCT_NAME] | [X days] | [X% of cycle, e.g., day 21 of 28-day cycle] | [running low / refill now / subscription nudge] |

---

## Suppression and Exit Logic

| Event | Action |
|---|---|
| Purchase | Exit sequence immediately — suppress all remaining emails |
| Opt-out | Exit sequence — add to suppression list permanently |
| VIP tier entry | Exit standard sequence — enter VIP-specific flow |
| Sequence completion without purchase | Re-entry delay: [X days] minimum |
| Frequency cap | [Do not send if subscriber received any flow/campaign in past X hours] |

---

## Platform Setup Notes

**[Platform name]:**
- Trigger configuration: [specific event or segment criteria]
- Flow exit event: [metric name in platform]
- Suppression list: [name or tag]
- Loyalty integration: [loyalty platform and sync method]
- A/B test setup: [split percentage recommendation]

---

## Notes and Flags

[List any compliance issues, segmentation assumptions, repurchase interval estimates, or recommendations not covered above. Flag any assumed product consumption data.]
