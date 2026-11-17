# Profile Schema (field reference & example)

This skill reads physiological parameters from `~/.workbuddy/running-coach/profile.json`. On first use (or if missing) it guides the user to create it. The values below are **generic placeholders, not real data** — only to show the format.

> **Sensitive data note:** Physiological and health-related fields (heart rate, lactate threshold, injury history) are sensitive personal data. Providing them is **optional** — they only personalize pacing and risk screening, the skill works without them. All data stays in the local file on your machine; the skill never transmits it anywhere. Skip any question you prefer not to answer.

```json
{
  "weight_kg": 65,
  "rest_hr": 50,
  "max_hr": 190,
  "lactate_threshold": { "hr": 175, "pace": "4:15", "power": 320 },
  "zones": {
    "method": "HRR",
    "z1": { "hr": [95, 114] },
    "z2": { "hr": [114, 143] },
    "z3": { "hr": [143, 157] },
    "z4": { "hr": [157, 177] },
    "z5": { "hr": [177, 190] }
  },
  "pbs": {
    "5k": "22:00",
    "10k": "46:00",
    "half_marathon": "1:45:00",
    "full_marathon": null
  },
  "goal": {
    "type": "full_marathon",
    "target_time": "3:30:00",
    "target_pace": "4:58",
    "race_date": "YYYY-MM-DD",
    "season": "2026-FALL"
  },
  "history": {
    "injuries": [],
    "training_years": 3,
    "weekly_mileage_base": 50
  },
  "current_phase": {
    "name": "base",
    "weekly_mileage": "50-60",
    "quality_sessions_per_week": 1
  }
}
```

## Field notes
- **zones.method**: `HRR` (heart-rate reserve) / `LT%` (threshold %) / `MaxHR%` (max HR %). Default HRR; table in `zone_calc.md`.
- **zones.zN.hr**: HR low/high bounds `[low, high]`, bpm.
- **pbs**: personal bests; use `null` if none.
- **goal.type**: `5k` / `10k` / `half_marathon` / `full_marathon`.
- **goal.race_date**: goal race day (YYYY-MM-DD), used for season back-calculation (Route F).
- **goal.season**: prep season tag, e.g. `2026-FALL`.
- **current_phase.name**: `base` / `build` / `peak` / `taper`.
- **history.injuries**: past injury list, used for Route E risk context.

## Setup questions (when profile.json missing)

All questions are optional — answer only what you are comfortable sharing; sensitive items (HR thresholds, injury history) can be skipped or filled later.

1. Age, resting HR, measured/estimated max HR
2. Lactate threshold (HR / pace / power, if known)
3. PBs per distance (5k / 10k / half / full)
4. Current goal (race type + target + race day)
5. Training years, current weekly base, past injuries
6. Current period phase
