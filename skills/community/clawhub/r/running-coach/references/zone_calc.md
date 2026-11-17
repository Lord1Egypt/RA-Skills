# Heart Rate Zone Calculation

## Three Methods

| Method | Formula | Best for | Notes |
|--------|---------|----------|-------|
| **HRR (Heart Rate Reserve)** | (MaxHR - RestHR) × % + RestHR | Garmin default 5-zone | most individualised |
| **LT% (Lactate Threshold %)** | LT HR × % | highest training precision | needs measured LT (lab or field test) |
| **MaxHR% (Max Heart Rate %)** | MaxHR × % | simplest | least accurate, high individual variance |

## Standard 5-Zone HRR Distribution

| Zone | HRR% | Physiology | Purpose |
|------|------|------------|---------|
| Z1 | 50-60% | Recovery | warm-up, cool-down, active recovery |
| Z2 | 60-75% | Aerobic base | easy runs, long runs, fat metabolism |
| Z3 | 75-82% | Aerobic threshold | tempo edge, steady-state moderate |
| Z4 | 82-93% | Lactate threshold | tempo runs, cruise intervals |
| Z5 | 93-100% | VO2max | intervals, hill repeats, strides |

## Garmin Algorithm Caveats

Firstbeat LT estimation:
- Needs ≥ 10-15min of **stable-state** output (pace and HR plateau)
- Intervals (sawtooth HR) and progressive runs (continuously climbing HR) are **not sampled**
- Tends to regress toward conservative values during base phase (low-intensity dominance)
- Hot weather (>23°C) artificially inflates HR → underestimates LT

**Rule:** Trust power (watts) stability over Garmin LT HR/pace fluctuations. If threshold power is stable while LT pace/HR drift, it's algorithm noise, not fitness loss.
