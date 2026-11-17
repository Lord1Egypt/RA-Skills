---
name: recipe-scale-chemist
description: Use when scaling a recipe up or down, converting a recipe to a different pan size, or diagnosing why a doubled recipe tastes wrong. Computes non-linear ingredient scaling (salt, chilies, dried spices, leavening, fat, alcohol scale with exponents, not multiplication), pan-area yield factors, and bake/roast-time corrections with the food-science reason for every adjustment.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [cooking, baking, recipes, scaling, kitchen-math, pans]
---

# Recipe Scale Chemist

## Overview

Doubling a recipe by doubling every ingredient is the most reliable way to ruin
it. Salt, chilies, dried spices, vanilla, leavening and alcohol do not scale
linearly with volume — perception and chemistry are sub-linear — while pan
geometry changes both yield and bake time. `scripts/recipe_scaler.py` applies
an exponent model (`new = old × factor^p`) to each ingredient class, handles
whole-egg rounding, converts pan shapes (round → square → rectangle), and
adjusts bake time for depth and roast time by the mass^(2/3) law.

## When to Use

- Scaling any recipe by ×0.25 … ×6 (dinner party, meal prep, halving a bake).
- Moving a recipe to a different pan (9" round → 9×13, squares → rounds).
- Someone asks "why does the doubled version taste saltier / soapy / boozy?"
- Converting a 4-serving recipe for a 12-person pot.

**Don't use for:** candy/sugar-work stages (temperature targets never scale),
pressure-cooker times (pressure dominates), or bread hydration re-balancing
(bakers percentages) — those need their own workflow, not exponents.

## How It Works

1. **Classify** each ingredient name against ~12 regex rule classes
   (salt p=0.80, chilies p=0.75, dried spices p=0.80, fresh herbs p=0.85,
   vanilla p=0.90, leavening p=0.90, alcohol p=0.90, fat p=0.95, liquids and
   bulk solids p=1.00).
2. **Scale** each quantity: `new = old × factor^p`. Sub-linear classes
   deliberately scale less aggressively in BOTH directions (a halved recipe
   keeps proportionally more salt than arithmetic would give).
3. **Eggs** round to the nearest half with a beat-and-measure note
   (1 large egg ≈ 50 g ≈ 3 tbsp).
4. **Pan conversion** computes area ratios (round d → square side = 0.886×d)
   and derives the scale factor from pan area, not from serving counts.
5. **Time corrections**: cakes/bars by depth ratio `t2 = t1 × (d2/d1)^1.6`;
   roasts by mass `t2 = t1 × (m2/m1)^(2/3)`; oven temperature stays THE SAME.
6. Emit a **warnings block**: thermometer targets unchanged, "taste at 80%",
   bloom-reheat notes for spice-heavy dishes.

## Using the Script

```bash
# Built-in demo: chili ×3, cookies ×0.5, 9x13 cake -> two 9" rounds
python3 scripts/recipe_scaler.py --demo

# Scale a JSON recipe by factor or to a target serving count
python3 scripts/recipe_scaler.py --recipe myrecipe.json --factor 3
python3 scripts/recipe_scaler.py --recipe myrecipe.json --servings 4:12

# Pan math: yield factor and bake-time correction
python3 scripts/recipe_scaler.py --pan-from 9x13x2 --pan-to 9rx9rx1.5 --time 32
```

Recipe JSON shape: `{"title", "servings", "bake_minutes"?, "ingredients":
[{"name", "qty", "unit"}...]}`.

## Worked Example

Beef chili for 4 scaled ×3. Kosher salt 1.5 tsp → 3.3 tsp (not 4.5 — salt
perception is sub-linear); cayenne 0.25 tsp → 0.44 tsp (not 0.75 — capsaicin
stacks fast); kidney beans 800 g → 2400 g (bulk scales linearly). Roast
geometry: a 2 kg brisket to 5 kg → time ×(5/2)^(2/3) ≈ ×1.84, same oven temp,
same internal pull temp.

## Common Pitfalls

1. **Multiplying everything.** Salt and heat are perceived sub-linearly;
   oversalting is unrecoverable, so the model under-scales them on purpose.
2. **Scaling leavening linearly for big jumps.** Excess soda tastes metallic
   and soapy; p=0.90 tames it — verify with the p-value note in output.
3. **Changing oven temperature when scaling.** Temperature sets the chemistry
   (Maillard, setting of proteins); only TIME moves.
4. **Egg fractions.** Half eggs are fine when beaten and measured; the script
   tells you the millilitre equivalent.
5. **Pan depth ≠ pan area.** Same area at double depth needs longer bake
   (`(d2/d1)^1.6`), not more flour.
6. **Scaling thermometer targets.** 74 °C poultry does not become 148 °C for
   a double batch — doneness temperatures never scale.

## Verification Checklist

- [ ] Every output quantity carries its class and exponent (transparency).
- [ ] Eggs rounded to halves, never decimals like 1.33 eggs.
- [ ] Pan conversion reports area ratio AND the derived yield factor.
- [ ] Warnings block present for |factor| ≥ 2.
- [ ] Time corrections cite the law used (depth^1.6 / mass^2/3).
