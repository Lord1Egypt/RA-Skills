# Wellness normalized schema (v1)

Goal: provide a stable, source-agnostic shape so the hub can generate summaries without caring about vendor-specific fields.

Principles:
- Prefer daily granularity for digests (today / yesterday).
- Keep fields nullable.
- Preserve provenance per field (which source).

## Top-level

```json
{
  "date": "YYYY-MM-DD",
  "timezone": "IANA/Zone",
  "generated_at": "ISO-8601",

  "sleep": {
    "duration_minutes": 0,
    "efficiency": 0.0,
    "score": 0,
    "bedtime": "ISO-8601|null",
    "waketime": "ISO-8601|null",
    "stages_minutes": {
      "deep": 0,
      "rem": 0,
      "light": 0,
      "awake": 0
    },
    "source": "whoop|oura|apple_health|health_connect|..."
  },

  "recovery": {
    "score": 0,
    "hrv_ms": 0,
    "resting_hr_bpm": 0,
    "resp_rate": 0.0,
    "temp_deviation": 0.0,
    "source": "whoop|oura|..."
  },

  "activity": {
    "steps": 0,
    "active_calories_kcal": 0,
    "total_calories_kcal": 0,
    "distance_km": 0.0,
    "source": "apple_health|health_connect|fitbit|..."
  },

  "training": {
    "strain": 0.0,
    "workouts": [
      {
        "start": "ISO-8601",
        "end": "ISO-8601|null",
        "type": "run|ride|strength|yoga|...",
        "duration_minutes": 0,
        "distance_km": 0.0,
        "calories_kcal": 0,
        "avg_hr_bpm": 0,
        "max_hr_bpm": 0,
        "source": "strava|garmin|whoop|..."
      }
    ]
  },

  "nutrition": {
    "calories_kcal": 0,
    "protein_g": 0,
    "carbs_g": 0,
    "fat_g": 0,
    "water_ml": 0,
    "source": "cronometer|myfitnesspal|..."
  },

  "body": {
    "weight_kg": 0.0,
    "body_fat_percent": 0.0,
    "source": "withings|fitbit|apple_health|..."
  },

  "vitals": {
    "bp_systolic": 0,
    "bp_diastolic": 0,
    "blood_oxygen_percent": 0.0,
    "glucose_mg_dl": 0.0,
    "source": "withings|apple_health|health_connect|..."
  },

  "notes": {
    "tags": ["string"],
    "freeform": "string"
  },

  "sources_present": ["string"],
  "raw": {
    "files": ["string"]
  }
}
```

## Scope of v1

- Prioritize: sleep + recovery + training + body weight.
- Nutrition and vitals may be sparse depending on user sources.
