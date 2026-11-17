# Slow Cooker Converter — Reference

The physics and the rule tables behind `scripts/slow_converter.py`.

## 1. Time-mapping model

### 1.1 Why the mappings aren't linear
- **Slow cooker LOW ≈ 90-95 °C**, HIGH ≈ 100 °C barely-simmer.
  Both are far below oven braise temps (160 °C air) but the FOOD
  internal temperature converges near the liquid's temp — braising
  is a liquid-temperature process everywhere, so times map via
  collagen kinetics, not air temp.
- **Collagen → gelatin** runs meaningfully from ~60 °C and doubles
  in speed roughly every +10 °C. That's why 2.5 h oven braise ≈
  8 h LOW: the oven's hotter liquid phase front-loads the
  conversion, the slow cooker gets there on time-on-temp.
- **Pressure @ 0.7 bar gauge ≈ 115-118 °C**: ~2.5-3× the rate of a
  bare simmer. Rule encoded: 1 min HP ≈ 15-20 min simmering for
  liquid dishes, then natural release continues cooking as temp
  glides down — that's why NR10 + "0 min" recipes still cook food.

### 1.2 Master table (liquid/braise dishes)

| Original | Slow LOW | Slow HIGH | Pressure (HP + NR10) |
|---|---|---|---|
| Simmer 15-30 min (soup w/ cooked proteins) | 3-4 h | 1.5-2 h | 3-5 min |
| Simmer 30-45 min | 4-6 h | 2-3 h | 5-8 min |
| Braise 1-1.5 h | 5-7 h | 2.5-3.5 h | 12-18 min |
| Braise 1.5-2.5 h | 6-8 h | 3-4 h | 15-25 min |
| Oven 2.5-3.5 h @ 325 | 8-10 h | 4-5 h | 25-35 min |
| Oven 3.5 h+ @ 300 (pot roast class) | 9-11 h | 5-6 h | 35-45 min |
| Soaked dried beans | 8-10 h | 4-5 h | 8-12 min |
| Unsoaked beans | n/a (uneven) | n/a | 25-35 min |
| Whole chicken | 6-7 h | 3.5-4 h | 20-25 min + 5 NR |
| Rice, white (1:1.25 liquid in HP) | 2-3 h | 1-1.5 h | 3-4 min + NR10 |
| Rice, brown | 3-4 h | 2 h | 20-22 min |
| Root vegetables, chunks | 6-8 h | 3-4 h | 8-10 min |
| Lentils, red (puree) | 5-6 h | 2.5-3 h | 5-7 min |

The 1h-HIGH ≈ 2h-LOW equivalence holds across braises; use it for
recipes that land between rows.

### 1.3 Reverse direction (slow → stovetop/oven)
- LOW hours ÷ 4 ≈ stovetop simmer time; ÷ 2.5 ≈ oven 325 °F.
- Keep all liquid: slow-cooked liquid quantity is the correct
  final sauce volume (no evaporation happened).
- Flavor note: slow pots develop less Maillard — add a sear step
  and a finish acid to compensate when going back.

## 2. Liquid adjustment classes

| Target | Evaporation | Liquid change | Why |
|---|---|---|---|
| Stovetop/oven | high (20-40%) | as written / +0 | open system |
| Slow cooker | ~none | **−25%** | sealed-ish, condense cycle |
| Pressure | zero | **−50%** | fully sealed |

Water-line rule for pressure: if it looks too little, it's probably
right. Pressure cooking needs only what the food absorbs plus
steam-headroom safety minimum (~1/2 cup for most pots).

## 3. Ingredient behavior tables

### 3.1 Dairy under long/slow/pressure heat
| Ingredient | At hour 0 of 8h LOW | Under pressure | Fix |
|---|---|---|---|
| Milk | curdles, gray | splits, scorches | last 30-60 min; or evaporated milk (stabilized) |
| Cream (heavy 36%+) | survives longer, still thins | splits | last 30 min; reduce after |
| Sour cream/yogurt | breaks, grainy | breaks hard | temper in at end, off heat residual |
| Coconut milk | stable but separates (restir ok) | stable-ish | anytime; restir |
| Cream cheese | fine long-cook (dips!) | splits | OK in slow pot early |

### 3.2 Starches
- Pasta: 20-30 min LOW-equivalent at the END, or cook apart.
  Under pressure: 4-6 min but foams — half-fill max.
- White rice in slow cooker: 2-3 h LOW with +25% liquid vs
  absorption; better: pressure 3-4 min.
- Potatoes: waxy hold shape 6 h LOW; russets fall apart (good for
  mash-style, bad for stew chunks) — pick by dish intent.
- Flour dusting on meat: lumps pale in slow pot — make a proper
  slurry at the end instead, or sauté the flour taste out first.

### 3.3 Alcohol
Raw wine in a dump-and-go: sharp, boozy edge at dinner because
alcohol needs boil-off the slow pot barely does and the pressure pot
never does. Reduce by half in the microwave (5 min, high, wide
bowl) or sauté mode before it goes in. Under pressure cut quantity
by ~1/3 additionally.

### 3.4 Vegetables by cook-speed class
| Class | Examples | Slow pot | Pressure |
|---|---|---|---|
| Hard (all-day) | carrot, parsnip, celery root, onion | hour 0 | with pot |
| Medium | bell pepper, broccoli stems | hour 0-2 | last half |
| Fast | zucchini, peas, spinach, corn | last 30 min | 0 min (add at release) |
| Mushroom | any | hour 0 (they melt = umami) | with pot |

### 3.5 Herbs & spices
- Woody (bay, thyme, rosemary, oregano): hour 0.
- Fresh tender (basil, cilantro, parsley, dill, chive): at serve.
- Ground spices: bloom 30 s in the sear fat or they stay raw-ish.
- Whole spices under pressure: flavor extraction is higher — cut
  cloves/star anise type quantities slightly or they dominate.

## 4. Capacity & scaling

- Slow cooker: min 1/2, max 2/3 fill. Below half = scorch cycling;
  above two-thirds = boil-over risk at the rim.
- Pressure: max 2/3 (1/2 for foaming: beans, grains, pasta).
- Recipe volume estimate: soup/chili ≈ 0.6 L per serving; stew ≈
  0.5 L; side dishes ≈ 0.3 L. The capacity command uses these.
- Doubling in a slow cooker: +25-50% time LOW, NOT double (thermal
  mass argument). Pressure: +~20% time, same liquid ratio logic.

## 5. Food-safety notes encoded in outputs

- Frozen meat into slow cooker: NO — keeps food 20-60 °C too long
  (danger zone). Thaw first; or pressure from frozen (+50% time,
  block-shaped frozen roasts don't count — cut them).
- Chicken to 74 °C, ground meats 71 °C, braises are there by
  construction; reheating leftovers: sauté to a full simmer, not
  the warm setting (warm ≈ 65 °C holds, doesn't reheat safely).
- "Warm" setting is a hold, never a cook.
- Beans: kidney/varieties with phytohaemagglutinin — slow LOW may
  NOT reach a high enough temperature fast enough to denature the
  toxin: boil hard 10 min first (or pressure, which fixes it).

## 6. No-mapping zone

Baked goods, custards set by dry heat, candy stages, deep fry, and
anything crisped (wings, skin) have no honest conversion — a slow
cooker is a braising machine. Crisp finish = oven 5 min at the end,
not a conversion.
