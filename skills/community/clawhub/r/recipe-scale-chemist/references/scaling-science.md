# Recipe Scale Chemist — The Science of Scaling

Why doubled recipes fail, in numbers.

## 1. The exponent model

Linear scaling assumes taste and chemistry are proportional to mass. They are
not. Empirical kitchen practice and sensory science converge on sub-linear
exponents for taste-active ingredients:

| Class | Exponent p | Rationale |
|---|---|---|
| Salt | 0.80 | Perceived saltiness grows sub-linearly (psychophysical power law); oversalting is unrecoverable |
| Chilies / capsaicin | 0.75 | Capsaicin heat stacks near-additively per bite but tolerance saturates; the #1 "doubled recipe disaster" |
| Dried spices | 0.80 | Aroma compounds overwhelm at concentration; volatile top notes scale up faster than perceived balance |
| Fresh herbs | 0.85 | Milder than dried but still sub-linear |
| Vanilla | 0.90 | Aromatic; slight over-adds are forgiving but noticeable |
| Leavening (baking powder/soda) | 0.90 | Excess leaves metallic/soapy taste (sodium residue) and over-rises thin batters |
| Alcohol / wine | 0.90 | Reduction is non-linear; extra volume over-extracts tannins |
| Fat | 0.95 | Nearly linear; greasiness appears at excess |
| Liquids, flour, sugar, meat, veg | 1.00 | Bulk physics — scale linearly |

`new_qty = old_qty × factor^p` — for both up- and downscaling. Downscaling
with p<1 keeps proportionally MORE of the taste-active ingredient, which
matches how professional kitchens halve recipes (never scrape the spice jar
math).

## 2. Eggs

1 large egg ≈ 50 g beaten ≈ 3 tbsp ≈ 45 ml (whites 30 g + yolk 20 g, approx).
For fractions: beat one egg, measure the fraction. Egg counts below 0.25 are
usually droppable in cookies, not in custards.

## 3. Pan geometry

- Round pan of diameter d holds like a square of side `0.886 × d`
  (equal areas: side = d·√(π/4)).
- Yield factor when moving recipe between pans = `A_new / A_old` at the SAME
  depth. Square/rect: A = w×d. Round: A = π(d/2)².
- Depth change at same area → longer bake, same temperature:
  `t2 = t1 × (depth2/depth1)^1.6` (empirical for cakes/bars; conduction +
  setting kinetics).
- Never fill a pan above 2/3–3/4: the factor tells you when to split batches.

## 4. Roasts and braises

Cooking time for solid meat pieces scales with the square-cube law:
`t ∝ M^(2/3)` (equivalently thickness²). Minutes-per-pound FALLS as roasts
get bigger. Internal temperature targets (63 °C medium beef rest-adjusted,
74 °C poultry, 71 °C ground meat) never scale — always verify by probe.

## 5. What never scales

- Thermometer / sugar-stage temperatures (physics of the material, not the mass).
- Oven temperature. Only time and pan area move.
- Pressure-cooker minutes (pressure sets temperature).
- Food-safety rules: cooling time limits for large batches get WORSE — split
  big pots into shallow containers (2-inch rule) before refrigerating.

## 6. Practice workflow

1. Run the scaler, print the adjusted list.
2. Add salt/spice at 80% of the scaled amount, taste, adjust — the exponent
   model is a strong prior, not a oracle for your specific palate.
3. For ×6 or larger, scale spices in two stages (×3 then ×2) with a taste
   check between.
4. Log the final amounts back into the recipe file — the second scaling is
   then exact for your kitchen.
