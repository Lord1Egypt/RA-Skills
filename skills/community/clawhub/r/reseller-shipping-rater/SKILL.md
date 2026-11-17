---
name: reseller-shipping-rater
description: Use when selling online (eBay, Etsy, Mercari, Poshmark) and choosing how to ship — computes dimensional weight across carriers (the 139/166 divisor trap that turns a light box into an 8-lb bill), tests items against flat-rate and cubic tiers, prices total listing profitability after platform fees on item+shipping, and outputs the cheapest-service verdict with packaging guidance. Turns "why did I lose $6 on that sale?" into a pre-listing decision.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [shipping, reselling, ebay, ecommerce, dimensional-weight, flat-rate, profit-margin]
---

# Reseller Shipping Rater

## The number one small-seller mistake
New resellers price shipping by what the item weighs. Carriers price it by **dimensional weight**: `L×W×H / divisor` (UPS/FedEx daily divisor 139; USPS applies a 166 divisor over 1 cu ft for most services, with cubic-tier pricing under 0.5 cu ft for Ground Advantage). A 2-lb item in a 18×12×10 box bills as ~15 lbs dimensional at UPS rates. The second mistake is platform economics: eBay charges the final value fee on **item price AND shipping combined** — free shipping isn't free, it's fee-loaded. Third: flat-rate boxes beat scale weight exactly when density is high (books, tools, cast iron) and lose badly when items are light-but-large (pillows, plush, board games boxed).

This rater does the pre-listing math: dimensional weight per carrier, flat-rate fit test against real box interiors, cubic Ground Advantage tier check, a transparent cost model (label + packaging + fees), and the total-profit verdict across services so the listing's shipping choice is a computed decision.

## When to Use
- Listing an item and choosing "calculated / flat / free" shipping
- An item sold and every label option looks like a loss
- Deciding whether a big-light item (bedding, toys, lamp shades) is even worth shipping
- Comparing a buyer's "ship it yourself" quote vs platform labels
- Sourcing decisions: "can this 12-lb board game ship profitably at a $35 sale price?"

**Don't use for:** international/complex customs (declare honestly, but duty math is destination-specific), freight/LTL items (150+ lbs — different industry), or media mail eligibility questions beyond the quick check in references (it's books/media only — and the inspection right is real).

## Quick Start
```bash
# The core question: cheapest service for this box
python3 scripts/shipping_rater.py rate --dims 14,10,6 --weight 3 --value 45 --zone 4

# Does it fit a flat-rate box, and does flat-rate win?
python3 scripts/shipping_rater.py flatrate --dims 12,9,4 --weight 6 --zone 5

# Full listing profitability (eBay-style fees on item+shipping)
python3 scripts/shipping_rater.py profit --sold 60 --ship-charged 9 \
    --dims 14,10,6 --weight 3 --zone 4 --cost-goods 18 --packaging 1.2

# Worked demos: the light-big trap, the dense-book win, the margin autopsy
python3 scripts/shipping_rater.py --demo
```

## How the Model Works (honest about approximations)
```
dim_weight_ups = L×W×H (in) / 139      # billable = max(actual, dim)
dim_weight_usps= L×W×H / 166           # applied when volume > 1 cu ft
cubic GA       = volume < 0.5 cu ft → tier T1-T5 pricing (zone-based)
flat-rate      = fits interior dims AND weight < 70 lb → one price any zone
profit         = (sold + ship_charged)×(1−fee%) − label − packaging − goods
```
Retail rate bands are baked in as 2025-26-era approximations with a printed `ESTIMATE` warning — the **decision logic** (dim vs actual, flat-rate crossover, cubic eligibility, fee stacking) is carrier-stable and is the actual value; punch the winning 1-2 services into the real rate calculator or platform label flow before buying.

## Flat-Rate Interior Cheat Sheet (USPS)
| Box | Interior (in) | Fits |
|---|---|---|
| FR Envelope | 12.5×9.5 | documents, thin clothing |
| Small FR | 10×7×4.75 | phones, small electronics |
| Medium FR (top/side) | 11×8.5×5.5 / 14×12×3.5 | jeans, sneakers, books |
| Large FR | 12.25×12.25×6 | boots, small kitchen |
| APO/FPO | 12×12×5.5 | military addresses |

(The SKU game: any rigid box with "Flat Rate" branding works only for its own tier — Tyvek-envelopes-as-flat-rate is the classic rejected-at-counter mistake.)

## Numbered Workflow
1. Measure the BOX you'll actually use (add 2" padding per fragile side), weigh packed.
2. `rate` — see dim vs actual weight per carrier and the ranked service list.
3. `flatrate` — if dense (books/tools/cast iron) or zone 5+, check fit and price.
4. `profit` — with the REAL label estimate + fees on item+shipping + COGS.
5. Set listing shipping accordingly: calculated for big-light, flat/free priced from the winning service.
6. Before buying the label, confirm the winner's live price in the platform flow (platform-negotiated rates often beat retail by 20-40%).

## Common Pitfalls
1. **Pricing shipping by scale weight** — dim weight is the bill for anything bulky; a 16×16×16 box of plush is a 29-lb UPS bill at 2 lbs actual.
2. **"Free shipping" without repricing** — platform fees apply to shipping money too; free shipping costs you fee% on the embedded amount.
3. **Ignoring cubic Ground Advantage** — items under 0.5 cu ft and ~20 lb often ship cheapest by cubic tier; sellers boxing small items big leave the savings on the table.
4. **Padded vs rigid flat rate confusion** — padded FR is a different SKU from cardboard FR; wrong one = counter rejection.
5. **Forgetting packaging and handling in "profit"** — $0.90 box + $0.30 tape + fees on a $12 sale is a 20% haircut that feels like theft at tax time.
6. **Shipping from the wrong ZIP logic** — zone is origin→destination; a coast-to-coast zone 8 flips the flat-rate answer vs zone 3.

## Verification Checklist
- [ ] Packed-box dims and weight used (not the item's)
- [ ] Dim weight computed for the actual carrier/divisor
- [ ] Flat-rate fit tested against interior dims, correct SKU tier
- [ ] Fees applied to item+shipping in the profit line
- [ ] Winner service spot-checked against live platform label price
- [ ] Fragile items: +2" per side and packaging cost included before the verdict

## One-Shot Recipes
**"Vintage Levi's, 1.5 lb, zone 4"** → `rate --dims 13,10,2 --weight 1.5` → poly-bag or FR envelope class; medium FR is overkill; calculated beats free.
**"Cast iron skillet 9 lb cross-country zone 8"** → `flatrate --dims 14,10,4 --weight 9 --zone 8` → flat-rate wins outright.
**"Board game (18×12×3, 4 lb) sold $35, shipped free"** → `profit` shows the dim-weight + fee stack; verdict usually: box-down to 16×11.5×2.5 for cubic, or local pickup only.
