# Training Science Behind Run Pace Architect

## 1. The Riegel model

Peter Riegel (1981, *Athletic Records and Human Endurance*, American
Scientist) showed that running times across distances follow a power law:

```
T2 = T1 × (D2 / D1)^e     with e ≈ 1.06 for road running
```

- `e = 1.0` would mean constant speed regardless of distance — false.
- Larger exponents = faster fatigue accumulation. Elite marathoners sit near
  1.03–1.05; recreational runners near 1.06–1.08; ultra distances climb above
  1.1 (which is why this tool refuses to extrapolate beyond the marathon).
- The model assumes **even pace, road-like terrain, and training appropriate
  to the target distance**. A 5K time "predicts" a marathon only *with
  marathon training* — the number is a potential, not a promise.

Common named distances used by the tool:

| Key | Distance (km) | Label |
|---|---|---|
| 1500m | 1.5 | 1500 m |
| 1mile | 1.609344 | Mile |
| 5k | 5 | 5K |
| 10k | 10 | 10K |
| 10mi | 16.09344 | 10 miles |
| hm | 21.0975 | Half marathon |
| marathon | 42.195 | Marathon |

## 2. Training zones and where they come from

The polarized-training literature (Seiler) and classic coaching frameworks
(Daniels) converge on the same shape: **most volume easy, a little hard,
little in between.** This tool encodes:

| Zone | Physiological target | Definition used here |
|---|---|---|
| Easy | Aerobic base, mitochondrial density, capillarization | Marathon pace + 45–75 s/km |
| Long run | Fat metabolism, durability, gut practice | Upper half of easy range |
| Marathon | Race-specific endurance | Riegel @ 42.195 km |
| Threshold | Lactate steady-state | **Pace holdable for exactly 60 min** |
| Interval (VO₂max) | Maximal aerobic uptake | Riegel @ 3 km |
| Repetition | Speed, economy, mechanics | Riegel @ 1.5 km |

### Why threshold is *solved*, not guessed

Lactate threshold is conventionally "the pace you could race for about one
hour." Rather than applying a fixed percentage of anything, the script finds
the distance `D*` for which the runner's own Riegel curve predicts exactly
3600 seconds, and reports `D*` pace. This adapts automatically to the
runner's fatigue profile: for a 3:30 marathoner, threshold is close to
15K-race pace; for a 60-minute 10K runner, almost exactly 10K pace.

### The 80/20 shape

Weeks should be roughly 80 % easy volume, 20 % hard. Two quality sessions per
week is plenty for recreational runners; three is the elite/young-athlete
case. The most common self-coaching error is making easy days moderately
hard, which subtracts from hard-day quality — the "moderate rut."

## 3. Goal feasibility bands

Improvement potential per focused training block:

| Runner profile | Realistic gain / 8–12 wk block |
|---|---|
| Trained (consistent 1+ yr) | 1–3 % |
| Recreational (6–12 mo) | 3–5 % |
| Novice / returning | 5–8 % (sometimes more) |

Verdicts:
- `LIKELY` — inside the band for the stated profile.
- `AGGRESSIVE` — above the band; extend the block or stage it.
- `UNREALISTIC` — > 2× the band; needs multiple blocks with an intermediate
  race.

Required improvement is `(current_seconds − goal_seconds) / current_seconds`.

## 4. Block structure (periodization)

For a block of N weeks the tool emits phases:

- **Base** — first ~50 % of weeks. Volume growth, mostly easy, strides 2×/wk,
  long run extends. Purpose: raise the aerobic floor.
- **Build** — next ~30 %. Key sessions become specific: VO₂max intervals,
  threshold work, race-pace segments inside long runs.
- **Peak** — remaining weeks minus the final one. Sharpening: race-pace
  practice at goal effort, volume starts to drop.
- **Taper** — final week. Volume −30–40 %, **intensity preserved** (short
  race-pace touches), everything easy otherwise. Tapering intensity is the
  classic mistake — cutting it leaves the legs flat.

## 5. Mileage ramping rules

- ≤ **+10 %** week-over-week volume increase (classic guideline; evidence is
  observational but it bounds risk in practice).
- **Cutback week −20 %** every 4th week: adaptation happens during recovery.
  The tool schedules these automatically and prints total ramp duration.
- Do not stack volume growth **and** new intensity in the same week. The ramp
  output assumes intensity is held constant while volume climbs.
- If the ramp requires more weeks than your goal race allows, the honest
  answer is to lower the target volume — the tool says so explicitly.

## 6. Race-day pacing

Even pacing is optimal on flat courses (world records are overwhelmingly
negative-to-even split). The split table gives per-km and per-mile targets
summing exactly to the goal. Practical use:

- Write the per-km numbers on your wrist or set a watch alert.
- Banked time is a myth: going out 10 s/km fast costs disproportionately
  more late in the race (glycogen + neuromuscular cost of early speed).
- Warm day (+10 °C over ideal) adds ~1–3 % to time — adjust the goal, not
  the effort.

## 7. Limitations

- Power law assumes even terrain; trail/ultra invalid.
- No accounting for heat, altitude acclimatization state, or hills — apply
  judgment.
- Not medical advice; persistent pain → rest and a professional.
