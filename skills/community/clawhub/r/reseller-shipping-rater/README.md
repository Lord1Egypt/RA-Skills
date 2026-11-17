# Reseller Shipping Rater

**Pre-listing shipping math for online sellers — dimensional weight per carrier, flat-rate fit tests, cubic-tier eligibility, and full margin autopsy after platform fees.**

## The problem
New resellers lose money on shipping in three predictable ways: (1) pricing by scale weight while carriers bill dimensional weight (a 2-lb plush box bills at 15+ lbs dim), (2) offering "free shipping" without realizing platform fees (eBay ~13.25%) apply to shipping money too, and (3) missing the flat-rate/cubic crossovers that flip by density and zone. The result is the classic "sold it and lost $6" post, and sourcing decisions made blind to landed cost. This tool computes the whole stack before listing: billable weight per carrier, flat-rate fit and price, cubic eligibility, label estimate, fee load, packaging, and net margin with a verdict.

## What this skill does
- `rate` — dim weight (139/166 divisors), billable pounds, ranked service estimates, cubic-tier check
- `flatrate` — fit test against real USPS flat-rate interior dimensions with zone-based win/compare verdict
- `profit` — listing autopsy: fees on item+shipping, label, packaging, COGS → net margin + verdict (LOSS / THIN / HEALTHY)
- `--demo` — the light-big plush trap, dense books to zone 8, and a $60-sale margin autopsy

## Quick example
```bash
python3 scripts/shipping_rater.py --demo
```
Demo 1: a 2.5-lb plush in an 18×14×12 box = 27 lb dim weight at UPS rates — the box choice costs more than the item's shipping budget. Demo 3: a $60 + $9-shipping eBay sale nets out with fees, label, packaging and $18 COGS to a real margin number with a verdict.

## Who needs this
- eBay/Etsy/Mercari/Poshmark sellers (millions of US side-hustlers; shipping is the top margin leak)
- Flippers making sourcing decisions (can this ship profitably at all?)
- Anyone confused why a sale felt like a loss

## Install
Python 3.9+, stdlib only:

```bash
python3 scripts/shipping_rater.py --demo
```

Note: rate bands are 2025-26-era retail estimates for decision support — the dim/flat-rate/cubic/fee logic is carrier-stable; confirm the winning service's live price before buying a label.

## License
MIT © Denis Voronin
