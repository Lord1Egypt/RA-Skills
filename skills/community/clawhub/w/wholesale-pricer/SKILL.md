---
name: wholesale-pricer
description: Calculate optimal wholesale and tiered pricing structures that protect retail margins while incentivizing volume orders, accounting for MOQs, shipping breaks, payment terms, and MAP policy. Use when onboarding a wholesale partner, building a tier schedule, setting a first-order promo, or reviewing retailer margin complaints.
---

# Wholesale Pricer

A wholesale price is a balance. Too high and retailers do not stock you or do not promote you. Too low and your direct channel looks worse every time a retailer discounts. Design the price tiers to make the retailer want volume without letting the cheapest channel race your own DTC margin to the bottom.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Starting discount off MSRP | 50% off MSRP (a standard keystone) | 45–50% | <40% (retailer under-margin, complains immediately) |
| Tier steps | 3 tiers with ≥20% unit-count gaps and 2–3 pt discount per step | 3 tiers with uneven steps | 7 tiers with 0.5 pt steps (nobody can remember) |
| MOQ | Aligned to case pack (12, 24, 48 units) | Open units but with a small-order surcharge | No MOQ, every order costs you to pick-and-pack |
| Payment terms | Prepay for new, Net-30 on approval, Net-60 only for top 10% accounts | Net-30 baseline | Net-90 across the board (working capital crisis) |
| MAP policy | 10% below MSRP floor, enforced with 2-warning removal | 15% MAP, loosely enforced | No MAP (price race ensues) |
| Freight | Free on $1k+ orders, otherwise pass through | Free on $2k+ | Free on all orders (eats 3–5 pts margin) |
| First-order promo | 5% first-order discount, one-time | Sample pack at cost | Free samples unlimited |

## Problems this skill solves

1. **Retailer margins too thin** so your product ends up on the "slow shelf" instead of the feature display.
2. **DTC undercut by retailer flash sales** because you never set or enforced MAP.
3. **Volume tiers nobody hits** because the break point was set too high, so everyone stays at the worst tier.
4. **Net-90 across the board** eating working capital — you're financing your retailers' business rather than growing yours.
5. **Hodgepodge pricing** where each account has a custom deal nobody can reproduce, and you can't tell if a new account is profitable.
6. **Free shipping on small orders** that makes every pick-pack a loss.
7. **No first-order incentive** for new accounts, so reps have nothing to close with.

## Workflow

### Step 1 — Start from MSRP and work down

Write down the target MSRP (what the consumer pays at retail full price). Keystone is the industry default: wholesale = MSRP × 0.5. So if MSRP is $40, baseline wholesale is $20. Validate that $20 is ≥2× your landed COGS.

### Step 2 — Set a 3-tier schedule

Three tiers is enough to reward scale without becoming a spreadsheet. Recommended structure:

- Tier 1 (opener): MOQ = 1 case, discount = 50% off MSRP.
- Tier 2 (growing): 5+ cases, discount = 52–53% off MSRP.
- Tier 3 (key account): 20+ cases or $10k+ order value, discount = 55% off MSRP.

Keep unit-count steps ≥20% apart so moving up a tier is a decision, not a rounding accident.

### Step 3 — Align MOQ to your case pack

Wholesale orders must be picked in whole cases. If your case is 12 units, MOQ = 12 (not 10, not 15). This lets the warehouse pull full pallets and avoids repacking. Anything else adds labor cost you are not charging for.

### Step 4 — Set payment terms by account maturity

- New account, unrated: prepay or credit card only.
- Account with 2+ paid invoices and clean credit: Net-30.
- Top 10% of revenue or a major chain: Net-60 maximum; use trade credit insurance if offered.
- Never Net-90 unless the retailer pays 2% early-pay discount for Net-10.

### Step 5 — Publish and enforce MAP

MAP (Minimum Advertised Price) policy sets the lowest price retailers may publish. A typical floor is 10% below MSRP. Publish the policy in plain English, list the enforcement mechanism (two warnings then account suspension), and actually enforce it. Use a MAP monitoring service once you have >20 accounts.

### Step 6 — Design the freight split

Free freight above a threshold that makes the order profitable after shipping. Rule of thumb: threshold = the point where freight is ≤1.5% of order value. For small SKUs that is usually $1,000. Below the threshold, pass through carrier rates at cost + 10% handling.

### Step 7 — Give new accounts a credible first order

A 5% first-order discount (on top of Tier 1) gets the rep through the "I'll think about it" with minimal margin damage. Offer a sample pack at cost, not free, so the retailer's buyer has skin in the game. Put an expiry on the first-order promo (30 days) so the rep can reclose.

## Example 1 — Candle brand onboarding indie retailers

MSRP $28 candle, landed COGS $6.50, case pack 6.

- MSRP: $28. Wholesale keystone: $14.
- Tier 1: 1 case (6 units), $14/unit. Retailer margin = 50%, which is standard.
- Tier 2: 6 cases (36 units), $13.30/unit (52.5% off MSRP). Retailer margin = 52%.
- Tier 3: 24 cases (144 units), $12.60/unit (55% off MSRP). Retailer margin = 55%. Offer this only to accounts that commit to 4 annual orders.
- MAP: $25.20 (10% off MSRP). Two warnings, then a 30-day suspension, then termination.
- Freight: Free above $1,200. Below, UPS Ground rate + 10%.
- First-order promo: 5% off Tier 1 on first case, expires in 30 days.
- Payment: Prepay first order; Net-30 from order 2 on clean credit.

Unit economics: Gross margin at Tier 1 = ($14 − $6.50) / $14 = 54%. At Tier 3 = ($12.60 − $6.50) / $12.60 = 48%. Still healthy; volume makes up for the margin compression.

## Example 2 — Kitchen tool, national chain request

MSRP $32 kitchen tool, landed COGS $9, case pack 12. National chain asks for a $12 cost with 90-day terms.

- Keystone baseline is $16. $12 is a 62.5% discount, far below the published Tier 3 (55%).
- Run the math: at $12 with 90-day terms, 10,000 units/yr, working capital cost 12%:
  - Gross margin: ($12 − $9) / $12 = 25%. This is not healthy at the line-item level.
  - Working capital drag on Net-90: $12 × 10,000 × (90/365) × 12% = $3,550/yr.
- Counter: $13.50 (58% off MSRP) with Net-60, or $12 with prepay. Offer a $5k MDF (marketing development fund) per calendar year in lieu of further discount.
- If the chain insists on $12 Net-90, walk away or negotiate a separate endcap / promotional commitment that lifts the volume to justify the terms.

The discipline: know your floor, walk from the deal when the numbers don't work, and offer non-price concessions (MDF, co-op advertising, exclusive SKU) when you can't meet on price.

## Common mistakes

1. **Starting from COGS instead of MSRP.** Retailers buy discount-off-MSRP, not cost-plus. Quote in their frame.
2. **Too many tiers.** Seven-tier schedules confuse reps and retailers and get ignored; 3 tiers is plenty.
3. **No MAP policy or unenforced MAP.** Every race-to-the-bottom starts here.
4. **Letting a big retailer dictate terms** without running the working-capital math on Net-90.
5. **Freight on every order** — it is not a gift when it makes the pick-pack unprofitable.
6. **Customizing pricing per account** until no two reps quote the same price and you cannot reconcile retailer chargebacks.
7. **Ignoring freight class.** Heavy or bulky products have very different real shipping costs than your small gift-boxed SKUs.
8. **First-order discount bundled with free shipping** — stacked incentives compound margin loss. Pick one.
9. **No case-pack alignment.** Ordering 13 units of a 12-pack forces a split case and destroys margin on that order.
10. **Paying returns freight without a reason code.** Retailers expect to return slow movers; pay freight only on defective-unit returns.

## Resources

- `references/output-template.md` — Wholesale price sheet template to hand to new accounts.
- `references/tier-math.md` — Worked pricing math for a 3-tier schedule with different case packs.
- `references/map-policy-template.md` — Minimum Advertised Price policy template and enforcement workflow.
- `references/payment-terms-guide.md` — Payment terms, credit checks, and working-capital math.
- `assets/wholesale-checklist.md` — Pre-onboarding checklist before accepting a new wholesale account.
