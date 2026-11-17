# Pricing Curves — The Depreciation Model

## Model
For age `a` years, category with base retention `B`, yearly decay `d`, and
floor fraction `F`:

```
retain(a) = max( B · (1 − d)^(a−1),  F )
point     = original_price · retain(a) · condition_multiplier
list      = point · 1.15      (negotiation headroom)
floor     = point · 0.85      (below this: keep or donate)
```

The first year takes the base hit (unboxing), subsequent years decay
compounding. The floor prevents absurd near-zero outputs for old-but-still-
sellable gear.

## Condition multipliers
| Grade | Mult | Meaning |
|---|---|---|
| new-in-box | 1.15 | sealed; often ABOVE used market |
| excellent | 1.00 | like new, all accessories |
| good | 0.85 | visible wear, fully functional |
| fair | 0.65 | noticeable cosmetic damage |
| poor | 0.40 | functional but rough |

## Category table (base, decay, floor)
| Category | Base 1y | Decay/yr | Floor | Note |
|---|---|---|---|---|
| iphone | 0.65 | 0.12 | 0.10 | high demand, sells in days |
| android-phone | 0.55 | 0.14 | 0.08 | flagships only hold |
| laptop | 0.60 | 0.15 | 0.10 | MacBooks hold, Windows fades |
| tablet | 0.50 | 0.15 | 0.08 | weak market |
| tv | 0.45 | 0.18 | 0.05 | bulky, local pickup |
| camera | 0.65 | 0.10 | 0.15 | enthusiast market |
| game-console | 0.60 | 0.10 | 0.15 | strong resale |
| furniture | 0.35 | 0.10 | 0.05 | IKEA≈0, solid wood strong |
| bike | 0.50 | 0.08 | 0.15 | spring market; check serial |
| kids-gear | 0.40 | 0.15 | 0.05 | recall + expiry checks |
| appliance-small | 0.40 | 0.12 | 0.05 | works-or-scrap |
| appliance-large | 0.35 | 0.12 | 0.05 | pickup + working demo |
| tools-power | 0.55 | 0.08 | 0.20 | pro brands hold strong |
| clothing | 0.20 | 0.20 | 0.02 | brand names only |
| watch | 0.60 | 0.08 | 0.20 | luxury holds, fashion dies |
| other | 0.40 | 0.12 | 0.05 | generic curve |

## Worked examples
- iPhone bought $799, 2 years, good: 0.65·0.88 = 0.572 × 0.85 = 0.486 →
  $388 expect, list $447, floor $330.
- MacBook-class laptop $1,299, 3 years, excellent: 0.60·0.85² = 0.4335 →
  $563 expect, list $648, floor $479.
- IKEA-class couch $899, 4 years, good: 0.35·0.90³ = 0.255 × 0.85 = 0.217 →
  $195 expect. Solid-wood equivalent often doubles this — the category note
  matters more than the curve for furniture.

## Calibration to your local market
The curve anchors; sold listings decide.
1. Search the platform for the EXACT model + storage/color/config.
2. Filter to SOLD/completed listings (active = unsold = overpriced).
3. Take the lowest 3 sold prices; list 5-10% under the cheapest.
4. If zero sold comps exist: the curve band, then reduce 10%/week until
   messages arrive (a listing with no messages in 10 days is overpriced,
   full stop).
5. Seasonality: bikes peak in spring, furniture moves at month-end (lease
  turnover), consoles peak before holidays, kids gear peaks pre-summer.

## When NOT to use the curve
- Collectibles/vintage (cameras, watches, games): market is idiosyncratic —
  check eBay sold + enthusiast forums; curves lie.
- Broken 'for parts' units: price at 25-40% of working unit regardless of
  curve.
- Bundle pricing: sum parts, then discount the bundle 10% — bundles sell
  slower than singles.
