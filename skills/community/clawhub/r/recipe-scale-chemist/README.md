# Recipe Scale Chemist

**Non-linear recipe scaling that actually tastes right.**

## The problem

You found a great 4-serving recipe. You need 12 servings. You multiply every
ingredient by 3 — and the result is saltier, painfully spicy, faintly soapy,
and slightly boozy. Every home cook has done this; it fails because **taste
perception and baking chemistry don't scale linearly with quantity**:

- Salt and capsaicin perception are sub-linear (psychophysical power laws) —
  tripling the salt triples the sodium but *more-than*-triples the harshness.
- Baking soda/powder leave a metallic, soapy residue when over-scaled.
- Pan geometry changes: a double batch in a deeper pan needs a different bake
  *time*, not a different temperature.
- Roasts follow the square-cube law: minutes-per-pound *falls* as the roast
  grows.

## What it does

`scripts/recipe_scaler.py` scales recipes with an exponent model
(`new = old × factor^p`) using per-class exponents grounded in food science:

| Class | p | Effect at 3× on 1 tsp salt |
|---|---|---|
| Salt | 0.80 | 2.4 tsp (not 3) |
| Chilies | 0.75 | 2.3× |
| Dried spices | 0.80 | 2.4× |
| Leavening | 0.90 | 2.7× |
| Fat | 0.95 | 2.9× |
| Flour, liquids, meat | 1.00 | 3× exactly |

Plus:
- **Egg rounding** to halves with gram/tablespoon equivalents
- **Pan conversion** (round ↔ square ↔ rectangle): area ratios, yield factor,
  round→square equivalents, depth-based bake-time correction `t×(d2/d1)^1.6`
- **Roast time law** `t × (m2/m1)^(2/3)`
- Warnings for big jumps (add spice at 80% and taste; shallow-container
  cooling for food safety)

## Example

```bash
python3 scripts/recipe_scaler.py --demo
python3 scripts/recipe_scaler.py --recipe chili.json --servings 4:12
python3 scripts/recipe_scaler.py --pan-from 9x13x2 --pan-to 9rx1.5 --time 32
```

Scaling the demo chili ×3 outputs kosher salt 1.5 tsp → **3.3 tsp** (with the
note "linear would be 4.5 tsp"), cayenne 0.25 → **0.44 tsp**, beans
800 g → 2400 g, and a warnings block for the 3× jump.

## Who needs this

Anyone who cooks for crowds (holidays, potlucks, meal prep), scales baking
recipes between pans, or halves recipes for a smaller household — i.e. almost
everyone who cooks. Wasted ingredients from a ruined double batch cost more
than this skill ever will.

## Limitations

Exponents are strong priors, not oracles — final seasoning is always
taste-to-adjust. Candy stages, pressure-cooker times, and bread hydration
re-engineering are out of scope by design. See `references/scaling-science.md`
for the reasoning and sources of each exponent.

## License

MIT © 2026 Denis Voronin
