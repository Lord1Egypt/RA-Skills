---
name: run-pace-architect
description: Use when training for anything from a 5K to a marathon — converts one recent race time into every training pace (easy, threshold, interval, rep) using Riegel-equivalent performances, predicts equivalent race times across distances, checks whether a goal-time is realistic, plans 10%-rule mileage ramps with cutback weeks, and prints even-split tables for race day.
version: 1.0.1
author: Denis Voronin
license: MIT
tags: [running, training, pace-calculator, race-predictor, riegel, fitness, marathon]
---

# Run Pace Architect

## Overview

Most runners train in the wrong zone: their "easy" runs are too fast (so their
hard days can't be hard enough) and their hard days are too slow (because they
are always tired). The fix is a pace table generated from **one honest recent
race performance** — not from a wish, not from a single good interval session.

This skill is that table generator plus the planning math around it:

1. **Equivalent performances** — Riegel's power-law model (`T2 = T1 × (D2/D1)^1.06`)
   converts one race result into predicted times for every common distance.
2. **Training zones** — easy, long-run, marathon, threshold (defined precisely
   as *the pace you could hold for 60 minutes*, solved numerically), interval
   (VO₂max) and repetition (speed) paces, each derived from the same model.
3. **Goal feasibility** — is a 22:30 → 21:00 5K in 8 weeks realistic? The tool
   compares the required improvement against typical per-block gains for trained
   vs novice runners and says LIKELY / AGGRESSIVE / UNREALISTIC.
4. **Mileage ramping** — 10%-per-week cap with an automatic down week every 4th
   week, simulated week by week until the target mileage is reached.
5. **Race-day splits** — even-split tables (per-km and per-mile) for a goal time.

## When to Use

- "I ran a 5K in X — what should my training paces be?"
- "What marathon time does my 10K predict?"
- "Is my goal of sub-1:45 half realistic in N weeks?"
- "I run 25 km/week, I want to get to 50 — how fast can I ramp?"
- "What pace per km do I need for a sub-X race?" → split tables
- Pacing a training plan: which phase (base / build / peak / taper) to run

**Don't use for:** injury diagnosis, shoe selection, trail/ultra pacing over
wildly varying terrain (Riegel assumes even, road-like conditions), or
heart-rate zone calculation without field data.

## Quick Start

```bash
# All training paces from a recent 5K
python3 scripts/run_pace.py zones --race 5k=22:30

# Equivalent race predictions from one performance
python3 scripts/run_pace.py predict --race 10k=48:00 --to hm,marathon

# Feasibility of a goal + phase structure for the block
python3 scripts/run_pace.py plan --race 5k=22:30 --goal 5k=21:00 --weeks 8

# Safe mileage ramp with cutback weeks
python3 scripts/run_pace.py ramp --current 30 --target 50

# Race-day split table
python3 scripts/run_pace.py splits --race hm --goal 1:45

# Everything in miles
python3 scripts/run_pace.py zones --race 5k=22:30 --unit mi
```

## How the Math Works

### Riegel equivalent performances

Riegel (1981) modeled distance-running time as a power law:

```
T2 = T1 × (D2 / D1)^1.06
```

A 22:30 5K therefore predicts a ~47:00 10K, a ~1:44 half and a ~3:38
marathon. The exponent 1.06 is the classic road-running value; it assumes
even pace, comparable terrain and adequate training for the target distance.
Predictions degrade when you jump more than ~4× in distance (a 5K predicts a
marathon poorly for an untrained runner).

### Training paces (all derived from the same model)

| Zone | Definition used | How it's computed |
|---|---|---|
| Easy / aerobic | Comfortable conversational | Marathon pace + 45–75 s/km |
| Long run | Easy effort, extended | Easy pace (upper half of range) |
| Marathon | Race pace for 42.2 km | Riegel prediction at 42.195 km |
| Threshold | Pace holdable for **60 min** | Distance solved numerically so Riegel time = 3600 s |
| Interval (VO₂max) | ~3K–5K race effort | Riegel prediction at 3 km |
| Repetition (speed) | ~1500 m race effort | Riegel prediction at 1.5 km |

The threshold pace is **solved, not guessed**: the script binary-searches the
distance `D` where your predicted time equals exactly 60 minutes, then reports
that pace. That is the textbook definition of threshold (one-hour race pace).

### Feasibility of a goal block

Required improvement = `(current − goal) / current`. Rules of thumb encoded:

- Trained runners: **1–3 %** per 8–12 week focused block is realistic.
- Novice/returning runners: up to **5–8 %** is possible (bigger fitness headroom).
- More than that in one block → verdict `AGGRESSIVE` (extend weeks) or
  `UNREALISTIC` (split into two blocks with a race in between).

Block structure output for N weeks: **base** (~50% of weeks, volume + easy
strength), **build** (~30%, key sessions get race-specific), **peak** (~20%
minus taper, sharpening), **taper** (final week: −30–40% volume, intensity
kept). Every phase lists its purpose and the key session shape.

### Mileage ramp safety

- Never increase weekly volume more than **10 %** week-over-week.
- Insert a **cutback week (−20 %)** every 4th week — adaptation happens during
  recovery, not during accumulation.
- The tool simulates this rule week by week and prints the schedule, including
  how many weeks the ramp actually needs (usually more than people expect).

## Common Pitfalls

1. **Feeding it a training-run time.** Garbage in, garbage out. Use a real
   race or an all-out time trial on a measured course, in race conditions.
2. **Easy pace creep.** If easy pace feels "too slow", that's correct —
   elite runners do the majority of volume slower than marathon pace.
3. **Trusting a 5K → marathon prediction without marathon training.** The
   model assumes you can actually cover the distance; the prediction is
   "with appropriate training", not "tomorrow".
4. **Ramping volume and intensity simultaneously.** The 10 % rule applies to
   volume; add quality only after volume has been stable for 2–3 weeks.
5. **Even splits ≠ negative splits.** The split table assumes even pacing;
   going out 10 s/km faster than plan is the classic marathon blow-up recipe.

## Verification Checklist

- [ ] Input race time parses (`5k=22:30`, `10k=48:00`, `marathon=3:15:00`)
- [ ] Zones table prints all five zones in per-km AND per-mile
- [ ] Threshold pace sits between marathon pace and interval pace
- [ ] Feasibility verdict matches required-% vs the 1–3 % / 5–8 % bands
- [ ] Ramp table includes a −20 % cutback every 4th week and never exceeds +10 %
- [ ] Splits table sums exactly to the goal time

## Examples

```
$ python3 scripts/run_pace.py zones --race 5k=22:30
Reference performance: 5K in 22:30 (4:30/km)
  Easy          5:26–5:56 /km   (8:45–9:33 /mi)
  Long run      5:41–5:56 /km
  Marathon      4:50 /km        (predicts 3:24:30)
  Threshold     4:40 /km        (your 60-minute pace)
  Interval      4:22 /km        (3K–5K effort)
  Repetition    4:04 /km        (1500 m effort)

$ python3 scripts/run_pace.py plan --race 5k=22:30 --goal 5k=21:00 --weeks 8
Required improvement: 5.6% in 8 weeks → AGGRESSIVE for a trained runner
(likely OK for a novice; consider 10-12 weeks)
  W1-4  BASE    volume +, strides 2×/wk
  W5-6  BUILD   VO₂max intervals + threshold
  W7    PEAK    race-pace specific
  W8    TAPER   −35% volume, keep strides
```

Data and formulas: Riegel fatigue model; threshold-as-one-hour-pace
convention; widely used 10 %-rule and 4th-week-cutback practice. Individual
response varies — the numbers are starting points, not prescriptions.
