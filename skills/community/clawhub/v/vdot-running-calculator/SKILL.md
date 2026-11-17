---
name: vdot-running-calculator
description: Calculates VDOT (Jack Daniels' running fitness score) and all five Daniels training paces — Easy, Marathon, Threshold, Interval, Repetition — from one recent race time, using the exact 1979 Daniels-Gilbert VO2/velocity and %VO2max equations that are still the unchanged, industry-standard method used by coaches and elite distance programs today. Use when a user asks for their VDOT score, Jack Daniels training paces, a running pace calculator, race time equivalents/predictions across distances, or "what pace should I run my easy/tempo/threshold/interval/repetition runs at".
license: MIT
metadata:
  category: health-fitness
  author: Arbaz Asif
  version: "1.0.0"
---

# VDOT Running Calculator

Computes a runner's VDOT score and personalized training paces from a single recent race result, using Jack Daniels and Jimmy Gilbert's published running-economy equations (_Oxygen Power: Performance Tables for Distance Runners_, 1979; refined across four editions of _Daniels' Running Formula_, Human Kinetics). These equations are the physiological model most competitive coaches and training apps still use unchanged decades later — the coefficients below never need updating. Fully self-contained arithmetic — no external API or lookup table required.

## Rule zero — collect a valid input before calculating

Never state a VDOT or a pace before you have a real race result. Ask for it conversationally.

## Phase 1 — Ask for the race result

- "What's a recent race distance and finish time you'd like to base this on?" (e.g. "5K in 22:30", "half marathon in 1:45:00").
- Prefer the runner's **best recent, honestly-raced** result under normal conditions (flat course, no major heat, no significant hills, not a training run). If the person offers multiple results, ask which was their best effort, or use the fastest one — VDOT is fitness-neutral to distance, so an inconsistent set of results just means picking the one that best reflects current fitness.
- If they only have a goal time rather than a past result, that's fine too — note explicitly that the output describes the fitness level needed to run that time, not their current fitness.

## Phase 2 — Convert to velocity and duration

- `distance_m` = race distance in meters (1 mile = 1609.34 m; 1K = 1000 m).
- `time_min` = finish time in minutes (e.g. 22:30 → 22.5).
- `v` = `distance_m ÷ time_min` (velocity in meters per minute).

## Phase 3 — Calculate oxygen cost of the race pace

```
VO2 = -4.60 + 0.182258 × v + 0.000104 × v²
```

(`v` in m/min; result in mL·kg⁻¹·min⁻¹.) This is the rate of oxygen consumption required to sustain that velocity.

## Phase 4 — Calculate the sustainable fraction of VO2max for that duration

```
%VO2max = 0.8 + 0.1894393 × e^(-0.012778 × t) + 0.2989558 × e^(-0.1932605 × t)
```

where `t` = `time_min` from Phase 2. This models the well-established fact that a runner can sustain a higher percentage of their VO2max in a short race than a long one.

## Phase 5 — Calculate VDOT

```
VDOT = VO2 ÷ %VO2max
```

VDOT is a "pseudo-VO2max" — the VO2max value that would be needed to produce that exact race performance, given typical running economy. It ranges roughly 30 (recreational beginner) to 85+ (elite).

## Phase 6 — Calculate the five training paces

Each Daniels training zone targets a fixed percentage of VDOT (i.e. of the runner's effective VO2max). For each zone, compute the target VO2, then invert the Phase 3 equation to solve for velocity:

```
target_VO2 = VDOT × zone_percent
v = (-0.182258 + √(0.182258² + 4 × 0.000104 × (4.60 + target_VO2))) ÷ (2 × 0.000104)
pace_per_km = 1000 ÷ v      (minutes per km)
pace_per_mile = 1609.34 ÷ v (minutes per mile)
```

Zone percentages (published Daniels intensity bands — give the pace as a range using the low and high end of each band, except Interval and Repetition which are typically given as a single target pace at the top of the band):

| Zone               | % of VDOT                                                                      | Physiological purpose                                                |
| ------------------ | ------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| **E — Easy**       | 59–74%                                                                         | Aerobic base building, recovery, conversational effort               |
| **M — Marathon**   | 75–84%                                                                         | Marathon race-specific pace, long-run practice                       |
| **T — Threshold**  | 83–88%                                                                         | "Comfortably hard" — improves lactate clearance, sustainable ~1 hour |
| **I — Interval**   | 95–100% (use 98%)                                                              | Stresses aerobic power near VO2max, 3–5 min work bouts               |
| **R — Repetition** | ~105–120% of VDOT-implied pace at the mile-race-equivalent velocity (use 108%) | Speed and running economy, short fast reps with full recovery        |

Note: R pace is intentionally faster than what the VO2 equation would predict as "sustainable" — it's a neuromuscular/economy zone, not a VO2max zone, and the source material treats it as approximate for this reason. Present the R-pace figure with that caveat rather than as precisely as the other four.

## Phase 7 — Report results

Present, clearly labeled and rounded sensibly (nearest second per km/mile, VDOT to one decimal):

1. **VDOT score**
2. **Easy pace** (range)
3. **Marathon pace** (range)
4. **Threshold pace** (range)
5. **Interval pace** (single target)
6. **Repetition pace** (single target, flagged as approximate)

Always include, briefly:

- This estimate assumes the input race was run honestly, under normal conditions (flat course, mild weather, not fatigued from other training). A poor race day, extreme heat, altitude, or major hills will distort the result.
- VDOT reflects current fitness — it should be recalculated every training block (roughly every 4–8 weeks) or after any new honest race result, since fitness naturally changes over time even though the underlying formula never does.
- This is a training-planning tool, not medical advice. Anyone new to structured running training, returning from injury, or with a cardiovascular concern should check with a doctor before following intensity-based training paces.

## Example (show working like this)

5K in 22:30 (22.5 minutes):

```
v = 5000 ÷ 22.5 = 222.22 m/min
VO2 = -4.60 + 0.182258(222.22) + 0.000104(222.22)² = 40.09 + 5.14 - 4.60 ≈ 40.6 mL/kg/min
%VO2max = 0.8 + 0.1894393·e^(-0.012778·22.5) + 0.2989558·e^(-0.1932605·22.5) ≈ 0.943
VDOT = 40.6 ÷ 0.943 ≈ 43.1
```

Then invert the velocity equation at each zone percentage of 43.1 to get E/M/T/I/R paces.

## Sources

- Daniels, J. & Gilbert, J. (1979). _Oxygen Power: Performance Tables for Distance Runners._ Self-published, Tempe, AZ. (Original VO2–velocity and %VO2max–duration regressions.)
- Daniels, J. (2021). _Daniels' Running Formula_, 4th ed. Human Kinetics, Champaign, IL. ISBN 978-1-4925-7443-2. (Training zone percentages and application.)

These are the original, still-current published equations — nothing here needs revisiting as sports science evolves, because the model is the same one Daniels' own current editions still use.
