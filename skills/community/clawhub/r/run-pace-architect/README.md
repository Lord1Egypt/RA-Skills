# Run Pace Architect

**Stop guessing your training paces.** One honest race time → every pace you
should be running, goal-time feasibility, safe mileage ramps, and race-day
split tables.

## The problem

Ask ten recreational runners what their easy pace is and eight will name
something close to their 10K pace. The result is the "moderate rut": too fast
to recover, too slow to stimulate. Coaches fix this with a pace table derived
from a recent race — but most runners never build one, and generic online
calculators don't explain what the numbers mean or what to do with them.

## What it does

- `zones` — easy, long-run, marathon, threshold (true 60-minute pace, solved
  numerically), interval and repetition paces from ONE race result, per-km and
  per-mile.
- `predict` — Riegel equivalent performances across 1500 m to marathon.
- `plan` — is your goal time realistic in N weeks? Verdict + phase structure
  (base → build → peak → taper) with the key session per phase.
- `ramp` — 10 %-rule mileage ramp with automatic −20 % cutback weeks,
  simulated until your target volume.
- `splits` — even-split table for any goal time and distance.

## Quick start

```bash
python3 scripts/run_pace.py zones --race 5k=22:30
python3 scripts/run_pace.py predict --race 10k=48:00 --to hm,marathon
python3 scripts/run_pace.py plan --race 5k=22:30 --goal 5k=21:00 --weeks 8
python3 scripts/run_pace.py ramp --current 30 --target 50
python3 scripts/run_pace.py splits --race hm --goal 1:45
```

Stdlib-only Python 3, no dependencies, offline.

## The math

- Equivalent performances: `T2 = T1 × (D2/D1)^1.06` (Riegel).
- Threshold: binary-search the distance whose predicted time is exactly
  3600 s — the one-hour-race-pace definition of lactate threshold.
- Feasibility bands: 1–3 % improvement per 8–12-week block (trained),
  5–8 % (novice). Above that: aggressive/unrealistic.
- Ramp rule: ≤ +10 % weekly volume, −20 % every 4th week.

Full detail: `references/training-science.md`.

## Who needs this

~50 million people finish a road race each year worldwide and multiples of
that train informally. Pacing errors are the most common self-inflicted
training mistake and the cheapest to fix.

## Disclaimer

Educational tool, not medical advice. Build volume gradually; pain that
persists means rest and a professional.

## License

MIT © 2026 Denis Voronin
