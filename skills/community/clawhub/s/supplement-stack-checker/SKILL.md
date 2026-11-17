---
name: supplement-stack-checker
description: Use when someone is taking multiple supplements/vitamins together, planning a new stack, or worried about interactions — checks 60+ ingredients for pair interactions (calcium-iron blocking, zinc-copper depletion, St. John's Wort drug clearing, vitamin K-warfarin), harmful dose flags vs ULs, redundant overlap (5 forms of the same thing), and builds a timed daily schedule that separates conflicting minerals by 2+ hours.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [supplements, vitamins, health, interactions, scheduling]
---

# Supplement Stack Checker

## Overview

People assemble supplement stacks from blog posts: magnesium here, zinc
there, a multivitamin, iron "for energy", fish oil, and a friend's St. John's
Wort. Nobody checks that calcium blocks iron absorption by up to 50%, that
long-term zinc above 40 mg depletes copper, or that three of their products
contain the same vitamin B6. `scripts/stack_check.py` ingests a stack,
checks it against an interaction matrix and Tolerable Upper Intake Levels
(ULs), finds duplicate ingredients across products, and builds a timed
schedule that separates antagonists by 2+ hours.

**Educational instrument, not medical advice.** It flags; a pharmacist or
doctor decides.

## When to Use

- Reviewing an existing multi-product supplement routine.
- Planning a new stack before buying.
- Someone reports odd symptoms (nausea, insomnia) on a supplement routine.
- Consolidating a cabinet of products after "stack crepe".

**Don't use for:** prescription drug interaction checking (only the
supplement-drug highlights below), pediatric/pregnancy dosing (different
ULs), or treating diagnosed disease.

## How It Works

1. **Parse** each product: `name|ingredient:mg|ingredient:mg` on the command
   line or a stack file (one product per line).
2. **Interaction matrix** (~25 pair rules): blockers (calcium↔iron, zinc↔
   iron, coffee/caffeine↔minerals), depleters (zinc→copper over time),
   enhancers (vit C + iron, fat + vitamin D/A/K/E absorption), danger pairs
   (SJW + SSRIs: serotonin syndrome risk; vitamin K + warfarin: INR
   destabilization; ginkgo/garlic/fish-oil anticoagulant stacking).
3. **UL check**: each ingredient's daily total vs its adult UL (e.g.
   vitamin A retinol 3000 µg, B6 100 mg, zinc 40 mg, selenium 400 µg, iron
   45 mg, niacin 35 mg flush form, vitamin D 100 µg / 4000 IU). Combined
   totals across products count.
4. **Overlap detection**: same ingredient via multiple products (three B6
   sources is common) with summed dose.
5. **Scheduler**: assigns ingredients to meal slots respecting rules — iron
   in the morning with vitamin C, NOT with coffee/tea/calcium; zinc away
   from iron and calcium by 2+ h; fat-solubles with the largest meal;
   magnesium/glycine at night; stimulating compounds (B-complex, ginseng)
   before 14:00.

## Using the Script

```bash
# Demo: a realistic 'blog-assembled' stack with 6 problems
python3 scripts/stack_check.py --demo

# Check your stack (ingredients in mg; µg values written as u)
python3 scripts/stack_check.py \
  "Multivitamin|vitamin A:800u|vitamin B6:2|zinc:15|calcium:100" \
  "Calcium+D|calcium:500|vitamin D:25u" \
  "Iron+VitC|iron:18|vitamin C:100" \
  "Zinc lozenge|zinc:23" \
  "Fish oil|omega-3:1000"

# From a file
python3 scripts/stack_check.py --stack mystack.txt --schedule
```

## Worked Example

The demo stack flags: calcium (600 mg total) taken with iron blocks up to
~50% of iron absorption → separate by 2+ h; zinc totals 38 mg from two
products — near the 40 mg UL and chronically depletes copper → drop the
lozenge to occasional use; vitamin D 25 µg is fine but take WITH the calcium
meal (fat-soluble); scheduled output puts iron+vitC at breakfast, calcium+D
at lunch, zinc at dinner — zero blocking pairs left.

## Common Pitfalls

1. **Everything at breakfast.** The default behavior guarantees the
   calcium-iron-zinc fight. Timing is the cheapest fix in supplement land.
2. **mg ≠ µg confusion.** A "10,000 IU" vitamin A label is 3000 µg retinol
   = AT the UL. The script works in mg with µg written as `u` units to keep
   this visible.
3. **Assuming "natural" means safe.** St. John's Wort is a potent CYP3A4
   inducer that clears ~half of prescription drugs faster (contraceptives,
   cyclosporine, many statins).
4. **Ignoring multivitamin baselines.** The multi already has zinc/B6/A;
   adding dedicated products stacks duplicates past ULs silently.
5. **Chronic high zinc.** 50+ mg/day for months → copper deficiency,
   anemia, neuropathy. The interaction is not acute; it's cumulative.
6. **Anticoagulant stacking.** Fish oil + ginkgo + garlic + vitamin E
   together thins blood additively — relevant before surgery (typically stop
   1–2 weeks; surgeon decides).

## Verification Checklist

- [ ] Every pair flag cites its rule (block/deplete/enhance/danger).
- [ ] Daily totals per ingredient sum ACROSS products before UL comparison.
- [ ] Schedule separates all flagged antagonists by ≥2 h or states a
      conflict that timing cannot fix.
- [ ] µg/IU conversions shown, never silent.
- [ ] Output ends with the not-medical-advice boundary statement.
