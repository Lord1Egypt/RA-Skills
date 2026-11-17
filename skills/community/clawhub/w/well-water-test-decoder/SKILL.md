---
name: well-water-test-decoder
description: Use when a private well water test comes back with numbers and no explanation, before buying water treatment equipment, or diagnosing taste/stain/odor symptoms — parameter-by-parameter decode of hardness/iron/pH/nitrates/TDS/coliform against EPA secondary and MCL standards, symptom fingerprinting (blue-green stain = corrosive water, rotten-egg = SRB), treatment-selector logic that prices the right unit, and the oversell-guard against whole-house RO for normal problems.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [well-water, water-quality, water-treatment, home, health, testing]
---

# Well Water Test Decoder

## Overview
~43 million Americans drink private well water, and **EPA standards don't apply to private wells** — testing is the homeowner's job, and treatment is where a $30 lab report becomes a $3,000 sales call. The classic move: a free "water test" from a treatment company (strips that read everything bad), then a pitch for a whole-house system priced against fear. The information gap is the product being sold.

This skill decodes a lab report line by line: each parameter against its **EPA MCL** (health) and **secondary standard** (aesthetic), each with what-it-means and fix-if-over. It fingerprints **symptoms** (stains, odors, taste, appliance scale) to parameters before you test, generates the **right test panel** to order (county/state labs, $20–$150; skip the free pitches), and runs **treatment-selector logic** with honest price bands — including the oversell-guard: whole-house RO is almost never the answer, and a softener sold for iron removal clogs when iron > 5 ppm needs an oxidizing filter instead.

## When to Use
- Lab report back; numbers in mg/L or ppm; no idea what's actionable
- Symptoms: stains (blue-green, brown, black), rotten-egg smell, metallic taste, scale, recurring gastro illness
- Buying/building on a property with a well (test BEFORE closing — it's a negotiation item)
- A treatment salesman's proposal to sanity-check
- Annual/5-year retest scheduling (coliform annually; nitrate + arsenic every 3–5 yr; full panel at sale or after flood/work on the well)

**Don't use for:** municipal water reports (CCR — different standards, utility-owned), wastewater, or pools. Coliform-positive: this skill interprets and routes to shock-chlorination/pro-lab; it does not replace county health dept guidance.

## Quick Start
```bash
# Decode every parameter on a lab report
python3 scripts/wellwater.py decode --hardness 142 --iron 3.2 --manganese 0.4 \
    --ph 6.4 --nitrate 4.1 --tds 380 --coliform absent --arsenic 3

# Symptom-first: what should I test for?
python3 scripts/wellwater.py symptoms --stains blue-green --corrosion pipes

# Treatment sanity-check: sales quote for softener + RO under sink
python3 scripts/wellwater.py treat --hardness 142 --iron 3.2 --ph 6.4

# What test panel to order (new property)
python3 scripts/wellwater.py panel --context new-property
```

## The Standards (what decode checks against)
| Parameter | EPA MCL / action | Secondary (aesthetic) | Over-limit meaning |
|---|---|---|---|
| Total coliform | 0 present | — | surface intrusion / well defect — **fix the well, not just the water** |
| E. coli | 0 | — | fecal contamination — **health emergency, do not drink** |
| Nitrate (as N) | 10 mg/L | — | infant methemoglobinemia; septic/farm proximity |
| Arsenic | 10 µg/L | — | chronic (cancer); common in New England/Midwest aquifers |
| Lead | 15 µg/L (AL) | — | usually plumbing/corrosive water, not the well |
| Iron | — | 0.3 mg/L | red-brown stains, metallic taste |
| Manganese | 0.12 (health adv.) | 0.05 mg/L | black stains; neuro (children) at high levels |
| Hardness | — | >120 mg/L "hard" | scale, soap waste; no health harm |
| pH | — | 6.5–8.5 | <6.5 corrosive (leaches lead/copper); >8.5 scaling + chlorine taste |
| TDS | — | 500 mg/L | brackish taste; RO point-of-use if extreme |
| Sulfate | — | 250 mg/L | laxative effect at high dose |
| Chloride | — | 250 mg/L | road salt / sea proximity |

## Symptom Fingerprints
| Symptom | Prime suspects (in order) | First test |
|---|---|---|
| Blue-green stains, pinhole leaks | pH < 6.5 / low alkalinity corrosion | pH + alkalinity + lead/copper |
| Brown/red stains, rusty water | Iron > 0.3 (ferrous clears after standing) | iron + manganese + pH |
| Black stains on fixtures | Manganese (or Mn+Fe sulfur bacteria) | manganese + iron bacteria (slider) |
| Rotten-egg smell (hot only) | Sulfate-reducing bacteria in water heater (anode) | replace magnesium anode w/ aluminum-zinc; no test needed |
| Rotten-egg (cold too) | H₂S gas / SRB in well | H₂S test + shock chlorination |
| Musty/earthry | Iron bacteria or surface organic | check well cap, coliform |
| White scale, kettles | Hardness > 120 mg/L | hardness + TDS |
| Soap won't lather | Hardness | hardness |
| Recurring GI illness in household | Coliform / E. coli / nitrate | bacteria + nitrate — lab, not strips |
| Salty taste | Chloride/TDS (road salt, sea) | chloride + sodium + TDS |

## Treatment Selector (what `treat` computes)
Logic order matters — treat in sequence, price the *right* class:
1. **Bacteria positive → shock-chlorinate + fix well defect** (cap, casing, grading). $0–50 DIY; UV sterilizer $800–1,500 if recurring. Disinfection precedes everything.
2. **pH < 6.5 → calcite/soda-ash neutralizer** ($800–1,800) — before softener, or the softener resin suffers and pipes keep corroding.
3. **Iron ≤ 3 ppm → softener can remove it incidentally** (with rest); **3–10 ppm → oxidizing filter (air-injection/Manganese Greensand, $900–2,200)**; **>10 ppm or iron bacteria → chlorination + retention + filtration** ($1,500–3,500). The oversold case: softener-only for 5 ppm iron = resin clogs in months.
4. **Hardness > 120 → softener sized to grain load** (see water-softener-sizer doctrine; $600–1,500 DIY).
5. **Arsenic/nitrate/lead at level → point-of-use RO at drinking taps** ($200–600) or whole-house media if whole-house contact (arsenic > 50 µg/L). Nitrate > 8 mg/L with infants: bottled water until POE/POU confirmed.
6. **Whole-house RO ($4,000–15,000) — almost never.** Justified only at extreme TDS/sodium/sulfate whole-house needs. The oversell-guard fires when softener+neutralizer+iron handles the report for a fraction.

## Common Pitfalls
1. **Free water tests from treatment companies** — strips + sales script; order county/state-accredited lab panels instead.
2. **Testing right after a shock-chlorination** — false negatives; wait 2 weeks, run water 15 min before sampling.
3. **Interpreting hardness as a health problem** — it's an appliance/soap problem; don't buy a softener to "protect health."
4. **Softener sold as an iron solution at >3 ppm** — resin fouls; oxidizing filter is the right class.
5. **Whole-house RO as a default** — the biggest-ticket oversell; POU RO at the kitchen tap solves drinking-water parameters for 5% of the price.
6. **Coliform-positive → treating water only** — find and fix the entry (well cap, casing crack, graded ground, back-siphonage), then retest.
7. **Old reports treated as current** — wells change after floods, nearby drilling, and pump work; coliform is an annual test.

## Verification Checklist
- [ ] Report decoded line-by-line against MCL/secondary table; every health parameter under limit
- [ ] Symptoms cross-checked (stain color → parameter) BEFORE treatment decisions
- [ ] Bacteria: absent, or well defect fixed + shock-chlorinated + retested clean
- [ ] pH ≥ 6.5 before any softener/iron equipment decision
- [ ] Treatment classes sequenced (bacteria → pH → iron → hardness → POE/POU), not bundled by sales script
- [ ] Whole-house RO justified only by whole-house parameters (extreme TDS/sodium/sulfate)
- [ ] Annual coliform + nitrate scheduled; arsenic/lead every 3–5 yr or after well work
- [ ] Quotes cross-checked against the price bands in this skill

## Example Session
```
$ python3 scripts/wellwater.py decode --hardness 142 --iron 3.2 --manganese 0.4 \
    --ph 6.4 --nitrate 4.1 --tds 380 --coliform absent --arsenic 3
DECODING WELL WATER REPORT
  coliform ABSENT — good. Recheck annually.
  iron 3.2 mg/L — 11x SECONDARY LIMIT: red-brown stains, metallic taste.
    >3 ppm: oxidizing filter, NOT softener-only (resin fouls).
  manganese 0.4 mg/L — OVER HEALTH LIMIT (0.12): black stains AND
    children's neuro advisory — oxidizing filter (same unit as iron).
  hardness 142 mg/L — HARD (aesthetic): scale/soap waste. Not a health
    issue. Softener after iron/pH handling.
  pH 6.4 — BELOW RANGE: corrosive; blue-green stains, leaches
    lead/copper. Neutralizer FIRST in train.
  nitrate 4.1 / TDS 380 / arsenic 3 — fine.
TREATMENT SEQUENCE (order matters):
  1) calcite/soda-ash pH neutralizer $800-$1,800
  2) air-injection/greensand oxidizing filter (Fe+Mn) $900-$2,200
  3) ion-exchange softener sized to grain load $600-$1,500
  realistic installed total: $2,300-$5,500
OVERSELL GUARD: whole-house RO ($4,000-$15,000) is justified ONLY by
  whole-house TDS/sodium/sulfate extremes — not this report.
```
