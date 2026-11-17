---
name: tire-pressure-coach
description: Use when checking or setting tire pressure on any vehicle — cold vs hot pressure physics, placard-vs-max myth-busting, load and speed corrections, temperature/altitude seasonal deltas, plus tread-depth safety math with legal limits and wet-grip cliff. Includes TPMS decode and monthly-check scheduler.
version: 1.0.2
author: Denis Voronin
license: MIT
tags: [tires, tire-pressure, car-maintenance, safety, vehicle, tread-depth]
---

# Tire Pressure Coach

## Overview

Tires are the only part of a car touching the road, yet pressure is set by
guesswork and gas-station air pumps at the wrong temperature. This skill runs
the real physics: ideal-gas pressure-vs-temperature deltas (≈1 psi per 10°F /
~0.06 bar per 5°C), cold-tire protocol (3h parked / 1 mi driven rule), placard
logic (the door sticker, NOT the sidewall max), load and speed corrections,
seasonal changeover math, and tread-depth safety (legal limits vs the wet-grip
performance cliff at ~4 mm, penny/quarter tests).

## When to Use

- "What pressure should my tires be?" — placard-first logic, corrected for
  your conditions
- Filling tires that aren't cold (the gas-station problem) — target-pressure
  math so you don't systematically underfill
- Seasonal swings / road trips to different climate or altitude
- "Are my tires worn out?" — tread depth → verdict + wet braking risk
- TPMS light on: what the threshold means and what to check
- Setting up a monthly check habit with exact psi targets per axle

Don't use for: tire *sizing/plus-sizing* questions, wheel offset, or tire
brand shopping (can advise safety-adjacent context only).

## The Physics (what the script computes)

1. **Cold target** = door-placard value (driver's door jamb, fuel flap, or
   manual — NEVER the sidewall max, which is a rim limit, not a setting).
2. **Temperature correction**: pressure scales with absolute temperature.
   ΔP ≈ P × ΔT/Τ (T in Kelvin). Rule of thumb at ~32 psi: **1 psi per 10°F**.
   Cold morning vs warm afternoon matters; so does an unheated garage.
3. **Hot-tire fill protocol**: if you must fill warm, fill to
   `placard + (current_tread_temp − ambient assumption)` — practically:
   measured hot pressure ≈ 2–4 psi above cold; the script computes your
   fill-to number from measured hot reading.
4. **Load correction**: full load / towing / high-speed (Germany-style)
   typically +2–4 psi on rear axle (per manufacturer high-load placard
   values where they exist).
5. **Altitude**: absolute vs gauge — driving 1500 m up changes gauge reading
   by ~2 psi; matters on mountain trips.
6. **Tread verdict**: depth mm → legal limit check (most jurisdictions
   1.6 mm; wet-performance cliff ≈ 4 mm; winter-tire practical minimum
   4–5 mm) + asymmetric wear flags.

## Numbered Workflow

1. Find the placard (driver's door jamb): front/rear psi + size + load
   rating. `placard` command records it per vehicle.
2. Check COLD (3+ hours parked or <1 mile driven): `check` with measured
   psi and ambient temperature.
3. The script prints per-tire verdict: OK / add / bleed, with the exact
   **fill-to number** (temperature-corrected, load-aware).
4. Filling warm at a station? `check --hot` — get the adjusted fill-to.
5. `tread` — record per-tire tread mm; get safety verdict and replace
   urgency (with wet-grip context, not just legal minimum).
6. `schedule` — monthly check reminder dates with next expected targets
   (accounts for season: expect −1..−2 psi entering winter).
7. Log every check: trends reveal slow leaks weeks before TPMS triggers.

## Commands

```
python3 scripts/tire_coach.py placard --vehicle "Mazda3" --front 33 --rear 33
python3 scripts/tire_coach.py check --vehicle "Mazda3" \
  --lf 30.5 --rf 30.7 --lr 32.0 --rr 32.2 --temp-c 8
python3 scripts/tire_coach.py check --vehicle "Mazda3" --hot \
  --lf 34 --rf 34 --lr 35 --rr 35
python3 scripts/tire_coach.py tread --vehicle "Mazda3" --lf 5 --rf 4.9 --lr 3.2 --rr 3.1
python3 scripts/tire_coach.py schedule --vehicle "Mazda3"
python3 scripts/tire_coach.py log --vehicle "Mazda3"
```

Store: `tire_coach.json` next to the script (`--store` to override).

## Pitfalls

1. **Using the sidewall max as target** — the #1 mistake. Max pressure is a
   tire capability limit; the car's placard is the engineered setting for
   contact patch, wear, and ABS/ESC calibration.
2. **Checking after driving** — even 1 mile of driving adds 1+ psi. Use the
   3-hour rule, or the `--hot` correction.
3. **Ignoring the spare** — spacesaver spares run 60 psi and are checked
   approximately never.
4. **Nitrogen folk-lore** — dry air behaves nearly identically; the real
   benefit of nitrogen shops is that they *set and check* pressure. Monthly
   checks with plain air beat annual nitrogen.
5. **Tread at legal minimum ≠ safe** — 1.6 mm passes inspection but wet
   braking distance from 80 km/h can be ~40% longer than at 4 mm. Treat
   4 mm as the practical replacement trigger, 3 mm as urgent for winters.
6. **Equalizing all four to one number** — many cars specify different F/R
   pressures; also a 2+ psi side-to-side gap on the SAME axle signals a
   leak or alignment issue, not a fill-everything job.

## Example

Cold morning 8°C, placard 33 psi, measured LF 30.5: verdict "add to 33" with
correction note — but afternoon fill-up at 22°C: fill-to becomes ~33.6 to
land back at 33 when cold. Tread LR 3.2 mm in October: legal (>1.6) but
flagged "wet-season risk — winter tires below 4 mm lose the compound
advantage; replace before the wet season." Monthly log shows LR losing
~1 psi/2 weeks vs others' ~1/month: slow leak caught before roadside.

## Safety Disclaimer

This skill is an **educational reference tool**, not a substitute for your
vehicle's documentation or a qualified technician:

- The **door placard / owner's manual is always authoritative** for your
  specific vehicle. If this tool's output ever disagrees with the placard,
  follow the placard.
- All pressure math here is ideal-gas approximation for *estimating*
  temperature effects; it cannot account for your tire's actual
  construction, load condition, or vehicle-specific systems (run-flats,
  self-sealing, TPMS recalibration requirements).
- Tread and TPMS outputs are screening guidance only. Any indication of
  abnormal wear, damage, vibration, repeated pressure loss, or a TPMS
  warning you can't resolve with a correct cold fill → **have the tire
  inspected by a professional before driving further**.
- Never exceed the **sidewall maximum** or the vehicle placard; when in
  doubt at a gas station, fill to placard cold spec and re-check cold
  at home.

When safety and this tool disagree, safety wins. When unsure, ask a
qualified tire professional.
