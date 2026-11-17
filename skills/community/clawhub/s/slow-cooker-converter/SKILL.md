---
name: slow-cooker-converter
description: "Use when you want to cook a regular stovetop/oven recipe in a slow cooker or Instant Pot (or vice versa) — converts cooking times across 7 appliance modes with the physics of WHY (collagen→gelatin at 60-70°C, milk curdles at 2h+, rice liquid ratios change in sealed pots), checks capacity fill (half-full min, two-thirds max), detects ingredients that must be added late or omitted entirely (dairy, pasta, fresh herbs, thickening), and produces a step-rewritten recipe with an insert-at-mark timeline."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [cooking, slow-cooker, instant-pot, recipes, conversion, kitchen]
---

# Slow Cooker Converter

**"Can I just throw this in the Crock-Pot?"** Sometimes yes,
sometimes you get curdled milk soup and chalk pasta. This converter
rewrites a normal recipe for the slow cooker or pressure cooker with
real rules: time mappings across 7 modes, capacity checks, and — the
part that actually saves dinner — an ingredient triage that moves
dairy, pasta, herbs and thickeners to late-add windows.

## Overview

1. **convert** — recipe text in → same recipe rewritten for the
   target appliance, with per-step time conversions and an
   INSERT-AT timeline for late additions.
2. **time** — standalone time table: stovetop braise 2 h → LOW 8 h
   / HIGH 4 h / pressure 25 min; plus the 1h-HIGH ≈ 2h-LOW rule.
3. **capacity** — recipe servings × typical volume vs your cooker
   size: verdicts half-to-two-thirds fill rule, scaling advice.
4. **ingredients** — triage of problem ingredients per direction of
   conversion: what to add late, omit, or swap (dairy → evap/cream
   at end; pasta → cook separately or last 30 min; wine → reduce
   first, never raw in a sealed pot).

Stdlib Python, offline. The knowledge base covers the 7 modes:
stovetop, oven, slow-cook-LOW, slow-cook-HIGH, pressure, rice
program, sauté.

## When to Use

- Converting a favorite stovetop soup/braise/chili recipe for the
  morning-before-work dump-and-go
- Oven recipe → Instant Pot on a hot day (or the oven's broken)
- Scaling a recipe up for a bigger cooker / party batch
- "Why did my slow-cooker Alfredo break?" — the ingredients triage
  answers retroactively what went wrong

**Don't use for:** baking (bread/cakes are a different physics —
no direct mapping; pressure-baking is its own genre), candy-making,
or deep-frying conversions. Those have no safe mapping.

## How It Works — Numbered Steps

1. Convert the whole recipe (paste or reference the text):
   ```
   python3 scripts/slow_converter.py convert --from oven --to slow-low \
       --recipe "Beef stew: brown beef 10 min; oven 325F 2.5h; add potatoes carrots; 1 cup red wine, 2 tbsp flour"
   ```
   → rewritten steps + INSERT-AT timeline + warnings.
2. Just need the time mapping?
   ```
   python3 scripts/slow_converter.py time --from stovetop --minutes 45 --to slow-low
   python3 scripts/slow_converter.py time --from oven --minutes 150 --to pressure
   ```
3. Check capacity before you scale:
   ```
   python3 scripts/slow_converter.py capacity --servings 6 --cooker 6
   ```
4. Triage problem ingredients for your direction:
   ```
   python3 scripts/slow_converter.py ingredients --to slow-low
   python3 scripts/slow_converter.py ingredients --to pressure
   ```

## Core Conversion Table (excerpt)

| Original | Slow LOW | Slow HIGH | Pressure |
|---|---|---|---|
| Stovetop simmer 30-45 min | 4-6 h | 2-3 h | 5-8 min HP |
| Stovetop braise 1.5-2 h | 6-8 h | 3-4 h | 15-20 min HP |
| Oven braise 2.5-3 h @325 | 8-10 h | 4-5 h | 25-30 min HP |
| Whole chicken (roast 1.5 h) | 6-7 h | 3-4 h | 20-25 min (not roast-like) |
| Dried beans (soaked) | 8-10 h | 4-5 h | 8-12 min HP |
| Soup (any) | 6-8 h | 3-4 h | 5-10 min + veg later |
| Rice (absorption 15 min) | 2-3 h (rarely worth it) | 1-1.5 h | 3-4 min HP |

Rules of thumb encoded: 1 h HIGH ≈ 2 h LOW; pressure ~1 min ≈
15-20 min simmer for most liquids; always natural-release 10+ min
for braises (fast release toughens muscle fibers).

## The Ingredient Triage (the part that saves dinner)

**Into slow cooker (either setting):**
- Dairy (milk, cream, sour cream, yogurt): curdles 2 h+ at simmer →
  add LAST 30-60 min; swap to evaporated milk or coconut cream for
  longer windows.
- Pasta: blooms to mush → cook separately, or add last 20-30 min LOW
  equivalent; never the full cook.
- Fresh herbs (basil, parsley, cilantro, dill): stir in at serve;
  woody herbs (rosemary, thyme, bay) go in early.
- Flour/cornstarch thickeners: dump-and-go dust sinks and lumps →
  mix with cold water first, or thicken at the end on sauté, or use
  a roux base.
- Wine/liquor: never raw into a sealed/slow pot (stays sharp) →
  reduce by half in a pan (or sauté mode) first.
- Rice: long-cycle grains turn to paste; if the dish needs rice,
  convert to pressure rice program or cook apart.
- Quick-cook veg (zucchini, peas, spinach, bell pepper): last 30
  min, or they vanish.
- Frozen veg: last 1 h — earlier turns them army-green and soft.

**Into pressure cooker:**
- Anything milk-based: pressure curdles guaranteed → finish on
  sauté after release, never under pressure.
- Alcohol > 2 tbsp in a sealed pot: flavor trap + foaming → reduce
  first, and reduce the amount by ~1/3.
- Thickeners: flour grits under pressure → thicken AFTER release.
- Delicate fish/shellfish: 0 min HP (add at release, sauté 2-3 min).

**From slow cooker BACK to stovetop/oven:** divide LOW hours by ~4
for stovetop simmer, keep liquid as-is (slow cookers lose almost
no liquid — cut added stock by ~25% going the other way).

## Common Pitfalls

1. **Lifting the lid "to check."** Each peek = 20-30 min added on
   LOW (thermal recovery). The recipe timeline assumes a closed pot.
2. **No reduction possible in a slow cooker.** Water doesn't
   evaporate — sauces stay thin. Plan a sauté-mode or stovetop
   reduce/thicken at the end, or start with less liquid (see
   pitfall 4's inverse).
3. **Same liquid volume across appliances.** Oven/stovetop lose
   20-40% to evaporation; slow cookers lose ~none; pressure cookers
   lose zero. The converter adjusts: → slow: −25% stock; →
   pressure: −50%.
4. **Dairy dumped at 8 AM for a 6 PM dinner.** 10 h at simmer
   temperature = grainy broken sauce. Late-add window, always.
5. **Overfilling the pressure pot.** Max 2/3 fill (1/2 for
   foaming foods — beans, pasta, oatmeal). Capacity check exists
   for this.
6. **Underfilling the slow cooker.** Below half full, a slow cooker
   cycles hot and scorches. Scale the recipe or use a smaller pot.
7. **Quick-releasing a braise.** The fibers seize. Natural release
   10-15 min for anything with big muscle chunks.

## Example

```
$ slow_converter.py convert --from oven --to slow-low --recipe "chicken thighs 325F 90min, 1 cup rice, 2 cups broth, 1 cup milk, mushrooms"
CONVERTED (oven -> slow LOW):
  1. Sear chicken (skillet, 3-4 min/side) — flavor base, don't skip.
  2. Combine chicken, mushrooms, broth (CUT to 1.5 cups — slow pot
     loses ~nothing), seasoning. Cook LOW 5-6 h.
  INSERT-AT TIMELINE:
    T-60 min (5 h mark): rice IN only if converted to par-cooked or
      using converted-rice trick — otherwise cook rice separately.
    T-30 min: milk STIRRED IN now (never at start).
  SERVE: adjust thickness (sauté reduce or cornstarch slurry).
WARN: milk at hour 0 = broken sauce by dinner.
```

## Verification Checklist

- [ ] Target appliance + mode chosen; time mapped via table
- [ ] Liquid adjusted for evaporation class of the target
- [ ] Problem ingredients triaged: dairy/pasta/herbs/thickeners
      moved to late-add or swapped
- [ ] Fill level between half and two-thirds (capacity check)
- [ ] Pressure: NR 10+ min for braises; ≤2/3 fill; no milk under
      pressure
- [ ] Lid discipline: no peeks (or +25 min each on LOW)
