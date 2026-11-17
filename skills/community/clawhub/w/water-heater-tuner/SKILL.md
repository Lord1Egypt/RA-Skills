---
name: water-heater-tuner
description: Use when setting, lowering, or troubleshooting a residential water heater temperature — scald-risk math by age, legionella pasteurization windows, energy savings per degree, single-parent vs cascade tank configs, vacation/away protocols, and recovery-time estimates for shower scheduling.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [water-heater, energy, scald-safety, legionella, home, plumbing, efficiency]
---

# Water Heater Tuner

## Overview

The water heater setpoint is a three-way trade almost nobody optimizes:
**scald safety** (kids and elders burn at 49°C in seconds), **legionella
risk** (the bacteria that causes Legionnaires' disease colonizes stagnant
warm water 20–45°C and dies slowly below 50°C, fast above 60°C), and
**energy cost** (every 10°F / ~5.6°C of setpoint costs roughly 3–5% of
water-heating energy via standby loss). This skill computes the trade for
YOUR household: who uses the hot water, how big the tank is, what climate
zone the tank sits in — and returns a setpoint verdict, a pasteurization
plan if you go low, exact vacation protocols, and recovery-time math for
"can three people shower back-to-back at 6 am".

## When to Use

- "What temperature should my water heater be set at?" — the classic
- New baby / elderly parent moves in → re-evaluate scald risk
- Cutting energy bills: savings estimate per degree + payback of a blanket/
  heat-pump upgrade
- Tank has been lukewarm / unused (vacation, vacancy, temp lowered) →
  legionella flush protocol
- Sizing questions: "will 150 L recover fast enough for our mornings?"
- Vacation/away mode decisions (off vs pilot vs vacation setting)

Don't use for: tankless/on-demand sizing (different physics — inlet temp
and flow rate dominate), boiler/radiator central heating, or solar thermal
controllers.

## The Physics & Standards (what the script computes)

1. **Scald times** (Moritz & Henriques burn data, the basis of UL/CPSC
   guidance): full-thickness burns at 49°C in ~10 min... no — at 52°C in
   ~90 s, 55°C in ~17 s, 60°C in ~3 s, 68°C in ~0.5 s. Children's skin
   burns faster (~1/4 the time). Verdict thresholds: with infants/elders,
   deliver ≤49°C at the tap (anti-scald valve or setpoint ≤49°C).
2. **Legionella** (WHO guidance): multiplies 20–45°C, dormant <20°C, dies
   at 50°C slowly (hours), 60°C in ~32 min, 70°C in ~seconds–minutes.
   A tank held ≥60°C keeps itself sanitized; below 50°C stored water needs
   periodic thermal disinfection.
3. **Energy**: standby loss scales with (tank_temp − ambient_temp). Tank in
   a cold basement loses proportionally more; lowering 60°C→50°C saves
   roughly 4–8% of water heating energy (bigger effect for older tanks,
  cold rooms, low hot-water-use households).
4. **Recovery**: gas recovers ~2× faster than electric per tank size
   (typical first-hour ratings: gas 40-gal ≈ 60-70 gal/hr; electric ≈ 45-55).
   Script converts tank size + fuel + setpoint into "showers until cold".
5. **Pasteurization protocol**: if operating low (<60°C storage), a weekly
  thermal purge — heat to 60°C+, hold ≥30 min (WHO: 60°C/32 min), then
  flush every tap/shower 5 min at high temp — keeps the system clean.

## Numbered Workflow

1. `profile` — household: ages of users (scald class), tank liters/gallons,
   fuel (gas/electric/heat-pump), location (basement/garage/conditioned),
   current setpoint if known.
2. `setpoint` — verdict: the recommended storage temperature + tap delivery
   strategy (anti-scald mixing valve at 49°C lets you STORE at 60°C — best
   of both worlds; note it in the output).
3. `energy --to 50` — estimated annual savings for a setpoint move, plus
   tank-blanket / pipe-insulation / heat-pump-upgrade deltas.
4. `recovery --showers 3` — first-hour and consecutive-shower math at your
   setpoint and inlet temperature (winter inlet matters).
5. `pasteurize` — dated protocol card for low-setpoint operation or after
   any stagnation (vacation >1 week, vacancy, temp was ever <50°C).
6. `vacation --days 14` — away plan: vacation mode vs off, what to do on
   return (flush protocol), what NOT to do (don't drain a gas tank's
   element... fuel-specific notes).

## Commands

```
python3 scripts/heater_tuner.py profile --tank-gal 40 --fuel gas \
  --users adult,adult,child2 --location basement --setpoint 130
python3 scripts/heater_tuner.py setpoint
python3 scripts/heater_tuner.py energy --to 120 --price 0.20
python3 scripts/heater_tuner.py recovery --showers 3 --inlet-c 9
python3 scripts/heater_tuner.py pasteurize
python3 scripts/heater_tuner.py vacation --days 14
```

Store: `heater_profile.json` next to the script (`--store` to override).

## Pitfalls

1. **Testing temperature at the tank, not the tap** — tank says 52°C, the
   upstairs shower delivers 47°C after pipe losses; legionella decisions
   are made at the FARTHEST tap, scald decisions at the NEAREST one. Measure
   both (run 30 s, thermometer in stream).
2. **Lowering setpoint without a flush plan** — going 60→49 saves energy
   and adds safety, but stored water at 46-49°C is prime legionella
   habitat: pair any low setpoint with the weekly pasteurization cycle or
   a mixing valve + 60°C storage.
3. **Trusting the dial** — heater dials are unlabeled/±10°F fantasy. Verify
   with a thermometer at the tap (30-second run), then mark the dial.
4. **Forgetting the vacation return** — stagnant tepid tank = bacterial
   culture. Run the pasteurize protocol after any week+ absence before
   letting immunocompromised users shower (healthy users: flush 5 min hot).
5. **Mixing valve ≠ setpoint license** — an anti-scald valve at 49°C does
   NOT sanitize the tank; keep storage ≥60°C for legionella control and let
   the valve do the safety. The valve is the strategy; the setpoint serves
   the tank.

## Example

Family with a 2-year-old, gas 40-gal tank in a cold basement set to 140°F:
verdict — store at 60°C/140°F with a 49°C anti-scald valve (legionella-safe
storage + child-safe delivery), savings vs "just lower to 120°F" are equal
but with better sanitation; without a valve: 49°C delivery cap → weekly
pasteurize protocol printed. Recovery math says 3 morning showers fit with
8 min spacing at 140°F (larger draw before mixed-cold), only 2 back-to-back
at 120°F — the morning schedule decides the strategy as much as safety does.
