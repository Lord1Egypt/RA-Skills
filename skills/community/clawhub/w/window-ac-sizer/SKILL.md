---
name: window-ac-sizer
description: Use when buying or troubleshooting a room air conditioner — Manual-J-style BTU sizing from room geometry, sun exposure, insulation and occupancy, with the oversizing trap (short-cycling => no dehumidification), 110V vs 230V circuit checks, and noise/heat-pump guidance.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [air-conditioner, btu-sizing, cooling-load, short-cycling, hvac]
---

# Window AC Sizer

## Overview
The most common window air conditioner mistake is not undersizing — it's **oversizing**. A too-big unit hits setpoint in minutes, shuts off, and never runs long enough to pull water off the coil: the room ends up cold, **clammy, and mold-prone**, with the compressor thrashing itself to death. Yet store shelves and "just buy 10,000 BTU" folklore push people exactly there. Correct sizing is a 5-minute load estimate: area, ceiling height, sun exposure, insulation quality, occupants, heat-producing appliances, and kitchen load — plus honest adjustment factors instead of fear-driven padding.

This skill computes a **Manual-J-flavored room load** (with every assumption printed), converts it to a recommended BTU band with the classic +600 BTU/person-over-two and +4,000 kitchen corrections, checks the **oversize ceiling** (never more than ~15% over calculated load), flags the **short-cycle signature** for existing units, and covers the practical purchase gates: 110V/15A vs 230V circuits, window type compatibility, CEER efficiency math ($/season between two models), noise placement, and the heat-pump-vs-AC question for shoulder seasons.

## When to Use
- Buying a window/portable AC for a bedroom, living room, office, or rental
- Existing unit "cools but the room feels damp" — short-cycling diagnosis
- Comparing two models' CEER and runtime cost at your electricity price
- Deciding between a second small unit vs one big one (spoiler: zone them)
- Landlord/rental constraints: no permanent install, window types, noise rules

**Don't use for:** whole-house central AC replacement (needs real Manual J from a contractor), multi-split design, or garage/server-room cooling with continuous high internal loads — those need different load assumptions, not a bigger fudge factor.

## Quick Start
```bash
# Bedroom: 12x14 ft, 8 ft ceiling, shaded, average insulation, 2 people
python3 scripts/window_ac_sizer.py size --length 12 --width 14 --ceiling 8 \
    --sun shaded --insulation average --occupants 2

# West-facing living room with big windows, poor insulation, kitchen adjacent
python3 scripts/window_ac_sizer.py size --length 18 --width 14 --ceiling 9 \
    --sun west --insulation poor --occupants 3 --kitchen yes

# Is my existing 12,000 BTU unit the reason the room is clammy?
python3 scripts/window_ac_sizer.py check --length 12 --width 14 --ceiling 8 \
    --sun shaded --insulation average --occupants 2 --unit-btu 12000

# Season cost compare: 8,000 BTU CEER 12 vs 10,000 BTU CEER 15
python3 scripts/window_ac_sizer.py cost --btu 8000 --ceer 12 --price 0.17 \
    --hours 8 --days 120
```

## The Load Model (transparent, not magic)
```
base = area_sqft × 20 BTU/h            (the classic starting point)
ceiling_adj = base × (ceiling_ft − 8) × 0.05      per extra foot (5%/ft)
sun: heavily shaded ×0.90 | average ×1.00 | sunny ×1.10 | west-facing ×1.15
insulation: good ×0.90 | average ×1.00 | poor ×1.15 | very poor (drafty old) ×1.25
occupants: +600 BTU/h per person beyond the first two
kitchen: +4,000 BTU/h if used for cooking
recommended band = load × 1.00 … × 1.15        (NEVER round "up for safety" beyond this)
```
Every factor exists because heat gain is real: west glass loads in the afternoon, a drafty 1900s wall assembly leaks both ways, a kitchen exhausts a meal's worth of heat into the adjacent room. The model prints the full stack so you can argue with any single line.

## The Oversizing Trap (the core teaching)
An AC does two jobs: drop temperature, **and** condense humidity. The second needs sustained coil time. Size a 6,000 BTU/h room at 12,000 and you get: 5-minute blasts, cold-but-wet air, compressor short-cycling (wear, efficiency collapse), and 60%+ RH that feels warmer than the thermostat claims — so you lower the setpoint and make it worse. The `check` subcommand quantifies oversizing and names the clamminess mechanism.

**The one legitimate oversize case:** if the room's load estimate sits within 10% below a standard size (5k/6k/8k/10k/12k/15k...), buy the size up — but not two sizes up.

## Purchase Gates (before you click buy)
1. **Circuit**: ≤8,000 BTU @110/120V on a standard 15A outlet (dedicated preferred); 10–15k often 230V (check for the right receptacle — a 230V unit on an adapter is a fire meme, not a plan); 12k+ @110V pulls ~11–12A — don't share the circuit with a gaming rig.
2. **Window**: double-hung fits most bracket-mounted units; casement/sliding windows need specifically designed units or a plexi panel kit. Measure width AND the free sash opening height.
3. **Weight & install**: 55–90 lb; sleeve vs bracket; landlord rules for ground-floor street-facing units.
4. **Efficiency**: CEER (combined, includes standby) — compare $/season with the `cost` command at YOUR price and hours, not the Energy Guide national average.
5. **Noise**: bedroom target ≤ 55 dB max / low-50s dB on low fan; inverter-driven units (variable speed) run quieter and dehumidify better *because they modulate instead of cycling*.
6. **Heat pump variant**: if you'd also use it for spring/fall heating, a window heat pump handles the shoulder seasons and dodges resistive-heat cost — but check its heating rating at your design low.

## Common Pitfalls
1. **"Bigger is safer"** — the #1 error; cold + clammy + dead compressor in 4 seasons.
2. **Sizing by room type folklore** ("bedrooms need 8k") instead of the actual envelope.
3. **Ignoring west glass** — a 12×14 west room can need 40% more than the same room facing north.
4. **Two rooms, one big unit** — an open doorway halves delivered cooling to the far room; two right-sized units beat one oversized.
5. **Portable "14,000 BTU" single-hose units** — the hose dumps conditioned air outside, pulling hot air IN; effective capacity is often 40–50% of the label. Dual-hose only, if portable at all.
6. **Skipping the tilt/sleeve drainage check** — modern units often route condensate to the condenser fan slinger; mounting dead-level when the manual wants a slight tilt floods the room side.

## Verification Checklist
- [ ] Load stack printed with every factor (argue line by line, not the total)
- [ ] Recommended band vs nearest standard sizes: within +15%, never 2 sizes up
- [ ] Circuit voltage/amperage confirmed for the chosen model
- [ ] Window type + sash opening measured
- [ ] CEER season-cost comparison run at local kWh price
- [ ] Bedroom units: dB on low fan checked against sleep needs

## Example Session
```
$ python3 scripts/window_ac_sizer.py size --length 12 --width 14 --ceiling 8 \
    --sun shaded --insulation average --occupants 2
Base load: 168 sqft x 20 = 3,360 BTU/h
Sun (shaded): x0.90 -> 3,024 | Insulation (average): x1.00 -> 3,024
Occupants: 2 (no add) | Kitchen: no
CALCULATED LOAD: ~3,024 BTU/h
Recommended band: 3,024 - 3,478 BTU/h -> buy 6,000 BTU (nearest sane size,
within +15% doctrine NOT met: explain 5k/6k gap; 6k = oversize +98% -> prefer
inverter unit that modulates down, or accept slightly clammy corners on design days)
```
Note: the script names the honest gap between tiny room loads and the smallest market sizes — inverter modulation is the modern fix, and the output says so instead of pretending.
