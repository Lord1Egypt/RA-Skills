---
name: sump-pump-outage-planner
description: Use when a sump pump fails or the power goes out in a wet-basement house — estimates hours-to-critical water level from pit geometry and inflow rate, ranks response options by cost per hour of protection (battery backup vs generator vs water-powered), sizes a backup pump to actual inflow, and gives the failure-mode diagnostic tree (float stuck vs check valve vs impeller) with an emergency bailing plan.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [sump-pump, basement, flooding, power-outage, backup-power, emergency, home-maintenance]
---

# Sump Pump Outage Planner

## Overview

A sump pump is the one appliance whose failure is measured in **hours to
flooded basement**. When the power cuts out or the pump dies at 2 AM,
you're not troubleshooting an appliance — you're racing water with a
bucket. The math is simple and almost nobody has done it: pit diameter
and depth give gallons-per-inch of rise; your soil's inflow rate
(rainy-season night = worst case) gives inches-per-hour; division gives
your countdown clock. That clock decides everything: whether a $150
battery backup is enough, whether you need a generator, whether you can
sleep through the outage or bail every 90 minutes.

`scripts/sump_outage.py` computes the clock from five numbers you can
measure with a tape and a bucket-timer, ranks backup options by honest
protection hours, sizes the backup pump to your actual inflow, and
walks the failure-mode tree (stuck float, frozen discharge, worn
impeller, tripped breaker, failed check valve) so a 2 AM no-pump event
gets the right first move instead of a panicky pump replacement that
was actually a 4-cent zip-tie float repair.

## When to Use

- Power outage with rain in the forecast and a sump in the basement.
- Pump running but water rising (mechanical failure diagnosis).
- Pre-purchase planning: battery backup vs generator vs water-powered
  backup for YOUR inflow rate.
- After a flood: figuring out why it happened before buying anything.
- Wet-season prep: testing the backup before you need it.

**Don't use for:** sewage ejector pumps (health hazard rules, different
pump class), new-construction drainage design (inflow from soil
engineering), or finished-basement active flooding >2 inches — that's
emergency extraction, call pros.

## How It Works

1. **Pit geometry.** Gallons per vertical inch = π × (diameter/2)² ×
   1 in / 231 in³. An 18-inch pit holds ~1.1 gal/inch; a 24-inch ~1.96.
   Usable rise = distance from resting water level to the floor lip or
   inlet that floods first (whichever is lower).
2. **Inflow measurement.** No instruments needed: during normal pump
   cycling, time how long the pump is OFF between cycles — water rose
   from "off" to "on" level during that time. Gallons/off-period ÷
   gal-per-inch → inflow rate. Rainy-night multiplier 2–4× applied as
   worst case.
3. **The clock.** Hours-to-critical = usable gallons ÷ worst-case
   inflow. Verdict bands: >12 h = plan calmly; 4–12 h = backup
   essential, generator or battery sized accordingly; <4 h = high-risk
   pit, dual pumps + alarm mandatory.
4. **Backup options ranked.** Battery backup (40–80 Ah deep-cycle +
   12 V backup pump): 6–15 h typical at moderate inflow. Generator:
   unlimited fuel-limited runtime, runs the main ⅓–½ HP pump (8–10 A
   surge ×3). Water-powered (municipal pressure): unlimited without
   power but uses ~1 gal city water per 2 gal pumped and needs 40+ PSI
   — worthless on a well. The script ranks by your clock.
5. **Sizing check.** Backup pump rated gph must exceed worst-case
   inflow × 1.5 or you're only slowing the flood. Table of typical
   12 V backup (1,000–2,500 gph at 10 ft head) vs main (3,000–4,500).
6. **Failure tree.** Pump silent → breaker/GFCI, float (lift by hand:
   runs = stuck float, ~$15 fix), then power. Pump runs but water
   rises → check valve (short-cycling siphon), impeller worn, discharge
   frozen/blocked, air lock. Pump runs constantly → stuck-on float or
   inflow beyond capacity (that's a drainage problem, not a pump
   problem).

## Using the Script

```bash
# 18in pit, 14in usable rise, pump off-period 8 min measured, rainy night
python3 scripts/sump_outage.py --pit-diameter 18 --usable-rise-in 14 \
  --off-minutes 8 --on-off-gap-in 6 --storm-mult 3

# size a battery backup for an 8h outage target
python3 scripts/sump_outage.py --pit-diameter 18 --usable-rise-in 14 \
  --off-minutes 5 --on-off-gap-in 6 --battery-ah 75 --target-hours 8

# failure triage quick card
python3 scripts/sump_outage.py --triage
```

Outputs: gallons per inch, measured and worst-case inflow (gph),
**hours to critical**, risk verdict band, backup option ranking with
protection hours for your battery size, pump sizing check, and the
2 AM triage card.

## Common Pitfalls

1. **Measuring inflow on a dry day.** A 40-minute off-period in August
   says nothing about April. Measure in wet season or apply the storm
   multiplier honestly.
2. **Sizing backup by the main pump's rating.** A backup needs to
   exceed INFLOW, not match the main pump. 2× your worst inflow is the
   target.
3. **Forgetting GFCI trips.** Most sump outlets are GFCI; a nuisance
   trip looks exactly like a dead pump. The triage tree checks it first
   because it's free.
4. **Battery backup never tested.** Deep-cycle batteries die in 2–4
   years; the backup that "worked when installed" fails silently.
   Quarterly: unplug main, confirm backup cycles, plug back.
5. **Check valve confusion.** A failed check valve short-cycles the
   pump (water falls back, refills pit) — looks like "pump runs
   constantly but level never drops." $20 part, not a pump.
6. **Discharge line freeze or blockage.** Pump runs, pipe's full of
   ice or a crushed end: water has nowhere to go. Winter: discharge
   must slope away and exit above grade with an air gap.
7. **Water-powered backup on a well.** It needs municipal pressure; on
   a well it's a paperweight *and* the well pump is out in the same
   outage.

## Verification Checklist

- [ ] Pit diameter + usable rise measured (tape, 5 minutes).
- [ ] Off-period timed during normal cycling; storm multiplier applied.
- [ ] Hours-to-critical computed and written on the pit lid.
- [ ] Backup pump gph ≥ 2× worst-case inflow.
- [ ] Backup tested by unplugging the main (quarterly, calendar it).
- [ ] Alarm (water sensor at critical-minus-2-inches) installed and loud
      enough to wake you.
- [ ] Generator/battery option chosen BEFORE the next outage, not during.
