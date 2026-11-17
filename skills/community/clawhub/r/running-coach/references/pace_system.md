# Pace System & Fitness Estimation

## Core idea
Use one recent race result (or a calibration test) to estimate current fitness (VDOT, Jack Daniels system), then derive training pace zones. With no race, use a time trial.

## 1. Fitness estimation
- **Has a recent race:** take the best "normal-condition" result among 5k / 10k / half / marathon, map to VDOT via a VDOT table.
- **No race:** do a calibration test — recommended 5k all-out, or 30-min best effort (the average pace of the last stretch ≈ 10k race pace). Need 2 weeks of consistent training and good form beforehand.
- **Has lab/field LT test:** use LT pace directly as the T-zone baseline (most accurate).

## 2. VDOT → training paces (generic example)
Example runner: recent 10k = 46:00 → VDOT ≈ 42 → training paces:

| Type | Meaning | Pace (this example) | % of VDOT pace |
|------|---------|---------|---------|
| E (Easy) | aerobic base / recovery | 5:35–6:05 /km | ~70-80% |
| M (Marathon) | marathon goal pace | 4:58 /km | 100% of MP |
| T (Threshold) | threshold | 4:35 /km | ~88% |
| I (Interval) | VO2max | 4:10 /km | ~80% |
| R (Rep) | neural speed | 3:50 /km | ~70% |

> Use a real VDOT table/calculator with your own result. The table above only illustrates the format, not any personal data.

## 3. Pace rules
- Easy runs: slower is safer; exceeding the Z2 ceiling loses aerobic benefit.
- T/I/R: calibrate by both feel + HR; ease 5-10s on hot/fatigued days.
- Marathon goal pace (M) should be based on an achievable, slightly conservative VDOT — don't force it from a PB.

## 4. Output template (Route G)
```
## Pace system — [based on X result / test]
VDOT estimate: ≈ [value]
| Type | Pace range | Purpose |
| E | ... | aerobic / recovery |
| M | ... | marathon pace |
| T | ... | threshold |
| I | ... | interval |
| R | ... | speed |
Next calibration: suggest [date] do [test] to update VDOT
```
