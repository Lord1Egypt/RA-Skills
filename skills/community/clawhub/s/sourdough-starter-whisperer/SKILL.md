---
name: sourdough-starter-whisperer
description: Use when maintaining a sourdough starter — feeding schedule math (counter vs fridge), hydration percentage calculator and conversion (100%↔stiff), readiness tests (float, rise tracking) with expected timelines by temperature, failure diagnosis (no rise, acetone smell, hooch, mold) with recovery protocols, and vacation/hibernation management. For baking-day starter levain builds there is a peak-timing planner.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [sourdough, starter, bread-baking, fermentation, feeding-schedule, baking]
---

# Sourdough Starter Whisperer

## Overview

A sourdough starter is a livestock of yeast + lactic-acid bacteria, and it
dies or underperforms for boring, predictable reasons: fed too cold, fed
too late, wrong ratios, or misread signals. Bakers lose weeks to "my
starter never doubles" when the fix is a 26°C spot and a 1:5:5 feed for
two days.

This skill is the starter's instrument panel:

1. **Feeding math** — ratios that scale (1:5:5, 1:2:2), retention math
   (keep X g, discard down), and schedules for counter (24°C, 26°C, 28°C)
   vs fridge life.
2. **Hydration calculator** — convert between 100% hydration and stiff
   (50–65%) or liquid (120–166%) levains; compute flour/water for any
   target from what you have.
3. **Readiness** — expected peak time by temperature and ratio; the float
   test's false positives; rise-tracking in a marked jar.
4. **Diagnosis engine** — 10 symptom clusters (no rise, acetone/nail-
   polish smell, gray hooch layer, mold vs kahm, sluggish after fridge,
   gummy collapse) each with a cause and a numbered recovery protocol.
5. **Vacation mode** — dry-chip and fridge-hibernation protocols with
   revival timelines.
6. **Levain build planner** — from starter to peak-aligned levain for a
  specific bake time, off a 1:1:5 build at your kitchen temperature.

## When to Use

- Keeping any sourdough starter (wheat or rye) alive and vigorous
- Starter looks dead / smells like nail polish / has liquid on top / rose
  and collapsed / never doubles
- Planning travel: how to park a starter for 1–8 weeks
- Building a levain timed to tomorrow's bake
- Converting starter hydration for a recipe (stiff vs 100% vs liquid)

**Don't use for:** commercial-yeast bread math (no starter involved),
gluten-free starter troubleshooting (different microbial stable — rye
adaptation advice only), or kneading/shaping technique.

## Quick Start

```bash
python3 scripts/starter.py feed --temp 24
python3 scripts/starter.py feed --temp 28 --style stiff
python3 scripts/starter.py hydration --have 100 --target 65 --mass 200
python3 scripts/starter.py readiness --temp 24 --ratio 5
python3 scripts/starter.py diagnose --symptom "smells like acetone"
python3 scripts/starter.py vacation --weeks 3
python3 scripts/starter.py levain --bake 07:30 --temp 22
```

Stdlib-only, no network.

## Core Numbers (what the math encodes)

| Parameter | Value | Meaning |
|---|---|---|
| Standard feed | **1 : 5 : 5** (starter:flour:water by weight) | peak in ~10-14 h at 24°C |
| Equal feed | 1 : 1 : 1 | fast peak (4-6 h at 24-26°C), acid accumulation — good for revival, bad as routine |
| 100% hydration | equal flour and water | the "default" liquid starter most recipes assume |
| Stiff levain | 50-65% hydration | slower, more acetic (tangier), easier timing |
| Peak at 24°C | ~2x rise, 10-12 h after 1:5:5 | jar marking makes this visible |
| Peak at 28°C | ~2x rise, 6-8 h | warm kitchens mature starters fast; feed 2x/day |
| Fridge storage | feed 1:2:2, wait 2 h, refrigerate | keeps ~2 weeks before a revival cycle |
| Hooch | dark liquid on top | underfed — pour off, feed; normal after fridge |
| Acetone smell | yeast stressed/starved | 2-3 days of 1:5:5 at 24-26°C fixes it |
| Float test | floats in water ≈ ready | FALSE PASS right after feeding; trust rise marks |

## Workflow

1. **Baseline your kitchen**: `feed --temp T` (T = where the jar actually
   lives, not the room's daytime high) → your feeding rhythm + ratios.
2. **Mark the jar** at feed time with a rubber band; target 2x by next
   feed. `readiness --temp --ratio` gives expected peak windows.
3. **Diagnose before adjusting**: any off-signal → `diagnose --symptom`
   first; most "dead" starters need 2-3 good days, not funeral rites.
4. **For tangier/stronger bread** use `hydration --target 60` to build a
   stiff levain; for milder and faster, stay at 100% or go 120%.
5. **Travel**: `vacation --weeks N` → fridge or dry-chip protocol with a
   revival timeline and a first-bake-ready date.
6. **Bake day**: `levain --bake HH:MM --temp T` → the 1:1:5 build start
   time so the levain peaks exactly when mixing starts.

## Common Pitfalls

1. **Feeding by volume (cups) instead of weight.** Hydration and ratios
   only exist by mass; a spoon of flour and a spoon of water are ~50%
   off from 100% hydration.
2. **Equal 1:1:1 feeds forever.** Peaks fast, acidifies fast, then the
   "my bread stopped rising" mystery. Routine feeding is 1:5:5 (or
   1:10:10 for a very warm spot).
3. **Cold kitchen, warm-kitchen expectations.** At 20°C a 1:5:5 peak can
   take 16-20 h; bakers read it as "dead". Move the jar (top of fridge,
   lamp-lit cupboard) before panicking.
4. **Reading hooch as disaster.** Dark liquid = underfed, not dead. Pour
   off, feed normally, 24 h later it's fine. Only pink/orange fuzz or
   fuzzy colored spots = mold = start over (or salvage from below).
5. **Trusting the float test blindly.** Freshly fed starters float from
   trapped air bubbles; a starter 3 h past peak can also float. The jar
   mark + expected peak window is the real instrument.
6. **Refrigerating right after feeding.** The culture drops dormant before
   consuming fresh flour → sour, weak revival. Feed 1:2:2, let it work 2
   hours at room temp, then refrigerate.
7. **Revival expectations.** A fridge-hibernated starter needs 2-3 feed
   cycles (1-2 days) before it doubles reliably; baking on day-1 revival
   gives dense loaves.
8. **Rye and wheat swaps without recalibration.** Rye ferments faster
   (more enzymes/minerals) — feed a rye starter on a shorter cycle or
   cut ratios to 1:7:7 equivalent timing.

## Verification Checklist

- [ ] Feeding by WEIGHT, ratios from the tool's plan for your temperature
- [ ] Jar marked at feed; 2x rise confirmed against expected peak window
- [ ] Any anomaly run through `diagnose` before changing routine
- [ ] Refrigeration follows the feed→2h→chill sequence
- [ ] Revivals given 2-3 cycles before judgment
- [ ] Levain build timed to bake time, confirmed by rise mark, not clock alone

## Safety Notes

- Mold (fuzzy, colored, on top) = discard; pulling starter from under a
  moldy layer sometimes works but is not worth it with flour this cheap.
- Everything else — hooch, acetone smell, gray tint — is recoverable.
- Pink/orange streaks = unwanted bacteria have won; start fresh.
