---
name: smoke-alarm-auditor
description: Use when a smoke or CO alarm chirps, or for a home safety audit — decodes beep patterns (low battery vs CO vs fault vs end-of-life) by brand behavior, dates the whole house (10-year smoke / 7-year CO / battery schedules), sizes the install plan to NFPA 72 (every bedroom, outside sleeping areas, per floor, interconnected), and prints a placement anti-pattern list (dead air zones, kitchen false alarms).
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [smoke-alarm, carbon-monoxide, home-safety, nfpa, fire-safety, chirping, detector-placement]
---

# Smoke Alarm Auditor

## Overview

The smoke alarm chirps at 3AM. Nobody remembers what the pattern means,
whether it's the battery or the unit dying, or how old the units even
are. Meanwhile the actual safety facts stay unknown in most homes: smoke
alarms have a **10-year life**, CO alarms **7**, every bedroom needs its
own alarm plus one outside each sleeping area and one per floor
(interconnected), and a chirp pattern is a *language* — one beep/minute is
low battery, but 3-4 quick beeps repeating is SMOKE, 4-5 with a pause on
CO units is CARBON MONOXIDE.

This skill:

1. **Decodes chirp patterns** — low battery / smoke / CO / fault / end-of-
   life, with the caveat list (patterns vary by brand; the tool lists
   First Alert / Kidde conventions).
2. **House audit** — inventory with install dates, computes age vs the
   10-year (smoke) and 7-year (CO) end-of-life math, flags the oldest
   first, generates a replacement plan.
3. **Battery schedule** — 9V/AA replace yearly vs 10-year sealed units;
   lithium vs alkaline chirp behavior.
4. **Coverage plan to NFPA 72** — room-by-room requirements from a
   bedroom/floor count, interconnected-vs-standalone, hearing-impaired
   (strobe/shaker) options.
5. **Placement anti-patterns** — the dead-air corners, kitchen 10-ft
   rule, garage never, CO height truth (floor vs ceiling barely matters —
   placement relative to sources does).

## When to Use

- An alarm is chirping and you need to know what it's saying *now*
- Moving into / auditing a home: are units expired? Is coverage legal-
   -ish and adequate?
- After replacing batteries and the chirp continues (end-of-life unit)
- Deciding units for a renovation or a new baby's room
- A CO alarm went off and you need the immediate-action script

**Don't use for:** commercial fire systems (NFPA 72 commercial code +
licensed inspectors), heat-detector-only specs for attics (simple rule in
references), or investigating a *current fire* — leave and call emergency
services.

## Quick Start

```bash
python3 scripts/alarms.py chirp --pattern "1 beep every minute"
python3 scripts/alarms.py chirp --pattern "3 quick beeps repeating"
python3 scripts/alarms.py audit --units unit.json
python3 scripts/alarms.py coverage --bedrooms 3 --floors 2
python3 scripts/alarms.py placement --room kitchen
python3 scripts/alarms.py co --event "alarm sounded 30 min ago"
```

`unit.json` format: `[{"id":"hall-1","kind":"smoke|co|combo",
"installed":"2019-04","battery":"9v|aa|sealed10"}]`

Stdlib-only, no network.

## The Beep Language (what patterns mean)

| Pattern | Meaning | Action |
|---|---|---|
| ~1 chirp / 30-60 s, steady for hours/days | LOW BATTERY | replace battery (or unit if sealed) |
| 3-4 loud fast beeps, pause, repeat | SMOKE ALARM | treat as fire: evacuate, verify |
| 4 fast beeps + voice/"CO" or 5 beeps on Kidde | CARBON MONOXIDE | evacuate, ventilate, call for CO eval |
| 3 chirps (unit not 1/minute) or 5 every minute on some models | UNIT FAULT / EOL | replace the unit |
| Chirp continues after NEW battery | END-OF-LIFE (sensor) | replace unit — it's 10 years old |
| Brief chirp at exact same time nightly | temperature dip + weak battery | replace battery; it's marginal |

**Brand variance is real**: First Alert CO = 4 beeps + "Warning carbon
monoxide"; Kidde CO often 4 beeps repeating, EOL = 5 chirps/minute. The
decoder prints both conventions and tells you to confirm against the
label on the back of the unit (which also carries the manufacture date).

## The Age Rules

| Unit type | Service life | Why it expires |
|---|---|---|
| Ionization/smoke (any brand power) | **10 years** from manufacture | sensing chamber drifts; dust + age |
| Photoelectric smoke | **10 years** | same |
| CO alarm (standalone or combo) | **7-10 years** (electrochemical cell dies) | label date governs |
| Sealed 10-year lithium units | battery lasts the unit's life; still expires at 10y | chirps = replace whole unit |
| 9V/AA replaceable | battery yearly (or at chirp) | alkaline fades with cold |

Manufacture date is printed on the BACK of the unit (MMYYYY or similar).
If your home's alarms have no dates you can find, they're older than 10
years — replace them all.

## Workflow

1. **Chirp now?** `chirp --pattern "..."` → what it means + immediate
   action. If smoke/CO pattern: stop, follow the evacuation script.
2. **Inventory**: walk the house, photograph the back of each unit (date
   label), note kind and battery type → `unit.json`.
3. `audit --units unit.json` → ages, EOL flags, ordered replacement
   plan (oldest + bedrooms first).
4. `coverage --bedrooms N --floors F` → NFPA-72-based unit count and
   placement plan; check gaps.
5. `placement --room <room>` for each planned spot → anti-pattern check
   (dead-air corners, kitchen proximity, garage).
6. **Buy list**: sealed 10-year combo units unless you prefer replaceable
   batteries; interconnect (wireless or hardwired) for any multi-floor.

## Common Pitfalls

1. **Battery-swap as a reflex.** A chirping unit that keeps chirping
   after a new battery is telling you it's 10 years dead. Read the back
   date.
2. **One alarm per home.** The minimum-legal-legacy setup. Bedrooms,
   outside sleeping areas, every floor including basement; heat detector
   in the garage/attic (never smoke there — dust/exhaust false alarms).
3. **Kitchen placement errors.** Within 10 ft of cooking appliances =
   constant false alarms → people disable units → the fatal classic.
   Photoelectric near (not in) kitchens false-alarm less.
4. **Dead-air mounting.** Within 4 in of a corner or peak ceiling apex =
   smoke may not reach the sensor early. Wall mounts: top of alarm 4-12
   in below ceiling.
5. **CO units at the wrong ceiling height debate.** CO mixes nearly
   evenly — height matters far less than proximity to sources (fuel
   appliances, attached garage) and sleeping areas (to wake you).
6. **Removing the battery to silence nuisance alarms.** The single most
   common fatal error. Move the unit, replace with photoelectric, never
   leave it dead.
7. **Forgetting interconnected units exist.** Hardwired/wireless-linked
   units all sound together — one kitchen trigger wakes the whole house;
   also means "which unit is chirping?" requires per-unit silence button
   hunting (listen close: chirps localize poorly).
8. **Renter assumptions.** Landlord duties vary by jurisdiction, but the
   10-year rule doesn't. Ask for the install date; test on move-in.

## Verification Checklist

- [ ] Chirp pattern decoded against back-of-unit label (brand variance)
- [ ] Every unit's manufacture/install date recorded
- [ ] No unit older than 10y (smoke) / per-label (CO); oldest flagged
- [ ] Coverage: every bedroom + outside sleeping areas + per floor
- [ ] Placement: no dead-air corners, 10 ft from cooking, none in garage
- [ ] Test button monthly; date of last test recorded
- [ ] Replacement plan dated and (if renting) sent to landlord in writing

## Safety Disclaimer

This skill encodes widely published NFPA consumer guidance; codes vary by
jurisdiction and change. It cannot hear your alarm — when the decoder
says smoke or CO, act first (evacuate/ventilate/call) and verify after.
CO symptoms (headache, nausea, confusion) with an active alarm = fresh
air immediately and emergency evaluation.
