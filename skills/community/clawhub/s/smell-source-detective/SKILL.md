---
name: smell-source-detective
description: "Use when your home has a mystery smell you can't locate (sewage in the bathroom morning-only, fish smell with no fish, musty bedroom, gas whiff near the stove, sweet chemical in the hallway) — a diagnosis engine that ranks probable sources from smell type + location + timing triggers, separates the four DANGER smells (gas, smoke, sewage backup, dead animal in walls) that need immediate action from the annoying-but-safe ones, gives a no-tools localization protocol (sniff-mapping, dry-trap tests, fixture-by-fixture elimination), and surface-specific kill protocols (dry P-traps, enzymatic vs bleach, mold remediation decision line)."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [home, smell, odor, diagnosis, mold, plumbing, safety, household]
---

# Smell Source Detective

**Every house eventually produces a smell nobody can find.** The
internet's advice is a list of 30 possible causes; this skill is a
triage engine: it ranks causes by YOUR data (what it smells like,
where it's strongest, when it appears), tells you which of the four
danger patterns you're in (or not), and walks the localization
protocol in fixture order — cheapest test first.

## Overview

1. **diagnose** — smell type + location + timing → ranked hypotheses,
   each with the confirming check and the fix. 12 smell families,
   30+ sources.
2. **danger** — the four act-now patterns (gas, smoke/electrical,
   sewage backup, cadaverine) with the exact first 10 minutes.
3. **localize** — the no-tools protocol: sniff-mapping gradient,
   dry-trap pour test, appliance isolation, wall/void sniffing.
4. **kill** — source-specific elimination: dry P-traps, enzymatic
   cleaner rules, mold decision line (DIY ≤ 1 m² vs professional),
   dead-animal-in-wall lifecycle and what actually helps.
5. **log** — record episodes (date, intensity 1-5, trigger) so
   patterns emerge: "every time it rains" = trap seal evaporation or
   roof vent; "mornings only" = dry traps; "when dishwasher runs" =
   drain air gap.

Pure stdlib Python, offline, no network calls.

## When to Use

- Any persistent or recurring household smell with no obvious source
- Before paying an "odor inspection" service ($150-400) — run the
  engine first; most causes are dry traps, garbage disposal funk,
  or a dead rodent with a known 2-week clock
- After vacation (dry traps), heavy rain (sewer gas), or when a
  smell appears in ONE room only
- Tenant-landlord situations: the episode log builds the evidence
  trail for a written complaint

**Don't use for:** known active gas leak you can hear/see — leave
and call the gas line, don't stop to run scripts. Known active fire —
same. Carbon-monoxide suspicion (can't smell it anyway) → CO alarm,
not this tool.

## How It Works — Numbered Steps

1. Classify the smell (12 families — pick closest):
   ```
   python3 scripts/smell_detective.py diagnose --smell sewage --location bathroom --timing mornings
   python3 scripts/smell_detective.py diagnose --smell fish --location kitchen
   python3 scripts/smell_detective.py diagnose --smell musty --location bedroom --timing "after rain"
   ```
   Output: ranked hypotheses (probability-ordered), the confirming
   check for each, and the fix.
2. Check the danger list first if anything matches:
   ```
   python3 scripts/smell_detective.py danger --smell gas
   ```
3. Run the localization protocol for the top hypothesis:
   ```
   python3 scripts/smell_detective.py localize --hypothesis "dry p-trap"
   ```
4. Kill it with the source protocol:
   ```
   python3 scripts/smell_detective.py kill --source "dry p-trap"
   python3 scripts/smell_detective.py kill --source "dead animal in wall"
   python3 scripts/smell_detective.py kill --source mold
   ```
5. Log every episode; review the pattern after 5+ entries:
   ```
   python3 scripts/smell_detective.py log --note "3/5 intensity, guest bath, after 10 days away"
   python3 scripts/smell_detective.py log --stats
   ```

## The 12 Smell Families (excerpts)

| Smell | Top sources | Key discriminator |
|---|---|---|
| Sewage / rotten eggs | Dry P-trap; venting problem; backup | Pours away after running water 30 s = trap |
| Fishy (no fish) | Overheating plastic/electrical, CFL ballast | Stronger near a fixture/lamp = URGENT electrical |
| Musty / earthy | Mold cavities, damp carpet, dirty AC coil | Grows after rain / in one wall = moisture path |
| Gas (rotten eggs additive) | Stove fitting, flex line, pilot | Do NOT flip switches/test with flame — leave, call |
| Sweet / chemical | Antifreeze leak, new furniture off-gassing | Near HVAC or radiator vs new-product box |
| Urine / ammonia | Pet soak in carpet pad, dirty litter | Blacklight at night fluoresces the map |
| Rotten meat | Dead rodent in wall/void, forgotten garbage | Sudden onset, peaks day 3-5, gone by ~2 weeks |
| Burnt / smoke | HVAC motor, trapped plastic, duct debris | When blower runs = furnace; else hunt appliance |
| Vinegar / sour | Fermenting food drop, dirty disposal, beer spill | Disposal: ice + citrus + bake-soda flush |
| Paint / solvent | Fresh paint, stored cans, adjac. unit work | Check garage/basement shelves for lid failure |
| Skunk-ish | Actual skunk under deck; gas mercaptan overlap | Outside-strong at dusk = skunk, not gas |
| Wet dog / dusty | Dirty HVAC filter, duct dust after renovation | Changes with blower cycles; check filter date |

## Common Pitfalls

1. **Masking before finding.** Candles/plug-ins add VOCs and hide
   the gradient you need for localization. Find first, then deodorize.
2. **Chlorine bleach on sewage smells.** Bleach doesn't digest waste
   films; enzymatic cleaner does. Bleach on mold porous surfaces
   deadens odor but leaves roots — the smell returns in weeks.
3. **Assuming "sewage = city problem."** 80% of bathroom sewage
   smells are a dry or cracked P-trap or a missing cleanout cap —
   $0-15 fixes you can verify in one minute (pour a glass of water,
   wait, sniff).
4. **Ignoring the fish smell.** Overheating PVC wiring insulation
   smells exactly like fish. It precedes failures that start fires.
   If it strengthens near any fixture, outlet, or lamp — treat as
   electrical (danger mode), unplug, get it checked.
5. **Cutting open the wall on day 1 of a dead-rodent smell.** The
   animal desiccates in 1-2 weeks and the smell dies with it. Opening
   walls is the last resort; odor-absorbing gels + vent sealing
   handles the window.
6. **One data point = diagnosis.** Mornings-only, rain-triggered,
   and appliance-linked smells have completely different causes.
   Use the log — timing is half the diagnosis.

## Example

```
$ smell_detective.py diagnose --smell sewage --location basement --timing mornings
SMELL: sewage | basement | mornings
DANGER? no immediate pattern — sewage ODOR only (backup = water
appearing; if water: danger mode)

RANKED HYPOTHESES:
1. DRY FLOOR-DRAIN TRAP (65%) — check: pour 2 L water into the
   floor drain, wait 10 min, re-sniff. fix: refill + 1 tbsp mineral
   oil to slow evaporation.
2. FAILED/LOOSE TOILET WAX RING (20%) — check: rock the toilet
   gently; sniff at base while flushing. fix: reset toilet, new wax
   ring (~$5 + 1 h).
3. SEWER VENT BLOCKAGE (10%) — check: smell at roof vent; gurgle
   when other fixtures drain. fix: clear vent (leaves/bird nest).
4. CLEANOUT CAP MISSING/CRACKED (5%) — check: look for open pipe
   stub near main. fix: cap it ($3).

$ smell_detective.py log --note "basement 3/5, 9am, after weekend away"
logged episode #4 — pattern so far: ALL episodes follow >3 days of
low water use → dry-trap hypothesis strengthened.
```

## Verification Checklist

- [ ] Danger screen done for gas/electrical/sewage-backup patterns
- [ ] Smell family classified + timing trigger identified
- [ ] Localization protocol run in fixture order (cheapest first)
- [ ] Top hypothesis CONFIRMED by its check before any demolition
- [ ] Kill protocol matched to surface (enzymatic for organics)
- [ ] Episode logged; pattern reviewed at 5+ entries
