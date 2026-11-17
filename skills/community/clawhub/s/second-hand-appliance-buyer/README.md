# Second-Hand Appliance Buyer

**A clean exterior is the cheapest thing to fake. Bearings and control boards are what cost you $500.**

The used-appliance market runs on asymmetric information: sellers know the failure history, buyers see shine and a friendly listing. Meanwhile risk is wildly uneven by category — a 6-year-old basic top-load washer is one of the best deals in home economics, while a 6-year-old premium fridge with an ice dispenser is a serial-repair subscription. Almost nobody carries the category table in their head; almost everyone judges by cleanliness.

## What this skill does

- **Category risk grading**: GOOD / FAIR / RISKY used-buy verdicts for 10 appliance classes, with the killer failure modes and what they cost.
- **Fair price bands**: age-based depreciation curve (steep years 1–2, flattening to a ~15% residual) × condition multipliers — including an honest untested discount.
- **Deal verdicts**: FAIR DEAL / OVERPRICED (counter with the band) / SKIP (buy scratch-dent instead) / SUSPICIOUSLY CHEAP (verify harder).
- **15-minute inspection protocols** per appliance type: the spin-listen test that catches washer bearings, the gasket-fold peel for front-loader mold, the paper test for fridge seals, the flashlight-on-panel trick for TV backlights.
- **The seven questions** that surface repair/transport/storage history before you drive anywhere.
- **Landed-cost pricing**: hoses, gas hookup, 240V circuits, anti-tip brackets — the $0–300 that flips a "deal".

## Quick start

```bash
# Demo: 5-yr-old front-load washer, $275 asking, $900 new
python3 scripts/appliance_deal_check.py --demo

# Your listing: 6-yr-old top-load washer, asking $150
python3 scripts/appliance_deal_check.py --category top-washer --age-years 6 --asking 150

# Untested estate-sale fridge
python3 scripts/appliance_deal_check.py --category fridge-simple --age-years 8 --asking 200 --condition untested
```

## Why it matters

- Washers/dryers/ranges bought smart used save $300–700 per machine versus new, with years of service left.
- The same purchase made blind lands a $400 bearing job on a $250 machine — the classic used-appliance trap.
- Landlords and rental furnishers run this math at scale; households run it once every few years and forget everything in between.

## What's inside

```
SKILL.md                                  category table, inspection protocols, pitfalls
references/category-risk-and-pricing.md   depreciation model, seven questions, transport costs
scripts/appliance_deal_check.py            pricing engine + inspection priorities (stdlib-only)
```

## Scope & honesty

Bands are class-level estimates; specific models vary (some front-loaders are tanks, some basic fridges are lemons — brand reliability tiers exist and shift). Prices are US-typical; the structure ports anywhere. Never buy gas appliances without a pro verifying connections before first use.
