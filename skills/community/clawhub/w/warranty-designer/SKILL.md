---
name: warranty-designer
description: Design product warranty and guarantee programs that increase buyer confidence and conversion rates while managing liability exposure, including policy language, claim workflows, fulfillment costs, and disclosure requirements. Use when launching a new warranty, updating existing terms, calculating reserve costs, or writing customer-facing warranty copy.
---

# Warranty Designer

A warranty is a marketing instrument with a P&L. Design it so the buyer believes the brand stands behind the product, and the brand can actually afford the claims that result.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Length | Matched to expected product life (apparel: 1 yr, electronics: 2 yr, lifetime gear: lifetime-of-original-buyer) | Industry-default length | Vague "lifetime" with no terms |
| Coverage scope | Defects in materials and workmanship, clearly enumerated exclusions | Defects only, exclusions implied | "Covers everything" with no carve-outs |
| Remedy | Repair → replace → refund, in that order, brand picks | Replace only | Refund only (most expensive to brand) |
| Claim trigger | Photo + order number + ≤3 short questions | Photo + invoice + form | Phone-only, requires shipping in for inspection |
| Reserve | 1.5× projected claim rate, reviewed quarterly | 1× projected claim rate | No reserve, claims hit current-month margin |
| Disclosure placement | On PDP, in checkout, in shipping confirmation, on insert | On PDP only | Buried in T&C footer |
| Transferability | Original buyer only (cleaner reserves) | Transferable for first 6 months | Fully transferable forever (creates resale arbitrage) |

## Problems this skill solves

1. **Marketing promises a "lifetime warranty"** that operations cannot afford to honor at scale.
2. **Claim rates that nobody forecast** so they hit the P&L as a surprise variance.
3. **Warranty language that contradicts the consumer law** of the markets you sell into (UK Consumer Rights Act, EU directive 2019/771, US Magnuson-Moss).
4. **Claim friction designed to deter customers** rather than to filter abuse — produces 1-star reviews about "warranty is a scam."
5. **No reserve account**, so a single bad batch creates a quarterly hit.
6. **Transferable warranties** that create a secondary market the brand can't track or control.
7. **Coverage that overlaps insurance** — you're paying twice and customers don't know which to claim against.

## Workflow

### Step 1 — Define the product failure curve

Estimate the rate at which units fail in months 1, 6, 12, 24, 60. Use historical RMA data, vendor MTBF (mean time between failures), or a conservative analog from a similar SKU. The integral of this curve over the warranty length is your expected claim rate.

### Step 2 — Pick the warranty length

Length should be just longer than the failure-rate inflection point. If the product fails mostly in month 0–3 (defects) and then has a flat curve, a 1-year warranty is generous. If failures spike in months 12–24 (wear), you need 2+ years to be credible. Don't promise "lifetime" unless you've modeled lifetime claims.

### Step 3 — Choose the remedy hierarchy

In order of cost to the brand: repair < replace from B-stock < replace from new < refund. Pick the order, document it, and train support to follow it. Allow customer choice only for low-claim-rate products.

### Step 4 — Enumerate exclusions in plain language

Every excluded scenario should be named: "normal wear," "misuse," "damage from use outside intended purpose," "modifications," "consumables (batteries, filters)." If you can't name it, you can't exclude it. Use 6–10 exclusions, not 30.

### Step 5 — Design the claim flow

Three steps maximum: photo + order number + reason. Decision in ≤48 hours. No physical return required for items under a threshold (usually 1.5× shipping cost). For higher-value claims, prepaid return label with a window of 14 days.

### Step 6 — Reserve and book it

Multiply expected claim rate × average remedy cost × forward 12-month volume. Set this as a balance-sheet reserve and book a small monthly accrual. Review quarterly against actual claims. If you're under-reserving by >20%, the warranty terms are wrong.

### Step 7 — Disclose and surface

Warranty link on every PDP, in checkout, in order confirmation email, in shipping notification, and on the insert card. Customers who can't find the warranty assume there isn't one and either don't buy or claim against the wrong party.

## Example 1 — Outdoor brand, daypack

Daypack, $120 retail. Vendor MTBF data shows 1.5% defect rate in year 1, dropping to 0.3%/yr after. Materials and stitching can fail; zippers are the most common failure point. Customers expect "lifetime" from this category.

- **Length**: Lifetime of original purchaser, against defects in materials and workmanship.
- **Coverage**: Stitching, fabric integrity, zipper hardware.
- **Exclusions**: Normal wear (fading, abrasion, scuffs), damage from improper use (overloading, sharp tools), modifications, theft, lost packs.
- **Remedy hierarchy**: Repair (we mail you a kit or accept the pack at our repair partner) → replace from B-stock if irreparable → replace from new if no B-stock.
- **Claim flow**: Photo of damage + order number + 1 sentence on what happened. Decision in 48 hours. Pack mailed in only if repair team requests.
- **Reserve**: 2.5% of revenue (conservative), reviewed quarterly. Annual cost roughly $3 per unit on a $120 SKU.
- **Disclosure**: Linked on PDP, in checkout copy ("Backed by our lifetime guarantee"), included on insert card with QR to claim form.

## Example 2 — Consumer electronics, $80 wireless earbuds

Earbuds, $80 retail. Industry defect rate is ~3% in year 1, ~5% cumulative over 2 years. Customers expect ≥1-year warranty, will accept 2-year. Battery degrades after ~24 months.

- **Length**: 1 year on full unit; 6 months on battery (consumable).
- **Coverage**: Defects in materials and workmanship, audio quality issues, charging case failure.
- **Exclusions**: Water damage beyond IPX rating, physical damage from drops, ear-tip wear, lost earbuds (not theft cover), battery degradation after month 6.
- **Remedy hierarchy**: Replace from same-color B-stock → replace from new → refund.
- **Claim flow**: Photo + order number + brief description. No return needed for units under 18 months — we destroy-in-place to prevent resale of warrantied units.
- **Reserve**: 4% of revenue (year 1 + battery exposure). Adjust if claim rate shifts.
- **Disclosure**: PDP, checkout, post-purchase email with one-tap "Start a claim" link if device is registered to the account.

## Common mistakes

1. **Promising lifetime without defining "lifetime."** Lifetime of the product? Of the purchaser? Of the company? Each means a different cost.
2. **No exclusions list.** Without enumerated exclusions, every customer claim is potentially valid, and disputes go to whichever side has more patience.
3. **Forcing physical returns for low-value items.** Shipping is more than the unit cost; just send a replacement and tell the customer to keep or recycle the original.
4. **Hiding the warranty in fine print.** Customers read warranties before buying. Surface = sale; hidden = lost trust.
5. **Conflating warranty with statutory consumer rights.** In the EU, the 2-year statutory guarantee exists regardless of your warranty. Your warranty must be additive, not a replacement.
6. **No reserve, so claims hit margin in real time.** Then management cuts claim approval when revenue is down — the worst time for it.
7. **Transferable warranty on a high-resale-value item.** Resellers price the warranty into the second-hand price; you eat claims you didn't get the original margin on.
8. **Asking the customer to prove "intended use"** before approving a claim. This shifts burden to the buyer and produces brutal reviews.
9. **Different rules in different markets** with no internal documentation. Support agents wing it and create inconsistent precedents.
10. **Treating warranty as legal team work.** It's a marketing/ops/finance instrument. Legal reviews the wording but doesn't design it.

## Resources

- `references/output-template.md` — Warranty policy template ready for legal review and customer publication.
- `references/claim-rate-model.md` — How to model claim rate, reserves, and unit-economics impact.
- `references/legal-baselines.md` — Statutory consumer rights baselines for US, UK, EU, AU.
- `references/customer-copy-patterns.md` — Customer-facing warranty copy that builds trust without exposing risk.
- `assets/warranty-checklist.md` — Pre-launch quality checklist before publishing a new warranty.
