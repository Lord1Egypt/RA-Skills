# WHOOP API Reference

Base URL: `https://api.prod.whoop.com/developer/v2`
Auth URL: `https://api.prod.whoop.com/oauth/oauth2/auth`
Token URL: `https://api.prod.whoop.com/oauth/oauth2/token`

## Scopes

| Scope | Data |
|---|---|
| `read:recovery` | Recovery score, HRV, RHR |
| `read:cycles` | Day strain, avg HR per cycle |
| `read:workout` | Workout strain, HR zones |
| `read:sleep` | Sleep performance, stages |
| `read:profile` | Name, email |
| `read:body_measurement` | Height, weight, max HR |
| `offline` | Enables refresh tokens |

Request all scopes (+ offline) when setting up the app.

## Endpoints

### Recovery

`GET /recovery` — paginated collection
`GET /cycle/{cycleId}/recovery` — recovery for a specific cycle

Response (score object):
```json
{
  "recovery_score": 44,        // 0-100
  "resting_heart_rate": 64,    // bpm
  "hrv_rmssd_milli": 31.8,     // HRV in ms
  "spo2_percentage": 95.7,
  "skin_temp_celsius": 33.7,
  "user_calibrating": false
}
```

### Sleep

`GET /activity/sleep` — paginated collection
`GET /activity/sleep/{sleepId}` — by ID

Response (score object):
```json
{
  "sleep_performance_percentage": 98,
  "sleep_consistency_percentage": 90,
  "sleep_efficiency_percentage": 91.7,
  "respiratory_rate": 16.1,
  "stage_summary": {
    "total_in_bed_time_milli": 30272735,
    "total_awake_time_milli": 1403507,
    "total_light_sleep_time_milli": 14905851,
    "total_slow_wave_sleep_time_milli": 6630370,
    "total_rem_sleep_time_milli": 5879573,
    "sleep_cycle_count": 3,
    "disturbance_count": 12
  },
  "sleep_needed": {
    "baseline_milli": 27395716,
    "need_from_sleep_debt_milli": 352230,
    "need_from_recent_strain_milli": 208595
  }
}
```

### Cycle (Day Strain)

`GET /cycle` — paginated collection
`GET /cycle/{cycleId}` — by ID

Response (score object):
```json
{
  "strain": 5.3,           // 0-21 scale
  "kilojoule": 8288.3,
  "average_heart_rate": 68,
  "max_heart_rate": 141
}
```

### Workout

`GET /activity/workout` — paginated collection
`GET /activity/workout/{workoutId}` — by ID

Response (score object):
```json
{
  "strain": 8.25,
  "average_heart_rate": 123,
  "max_heart_rate": 146,
  "kilojoule": 1569.3,
  "distance_meter": 1772.8,
  "percent_recorded": 100,
  "zone_durations": {
    "zone_zero_milli": 300000,
    "zone_one_milli": 600000,
    "zone_two_milli": 900000,
    "zone_three_milli": 900000,
    "zone_four_milli": 600000,
    "zone_five_milli": 300000
  }
}
```
Fields: `sport_name`, `sport_id`, `start`, `end`

### User

`GET /user/profile/basic` — name, email, user_id (scope: `read:profile`)
`GET /user/measurement/body` — height_meter, weight_kilogram, max_heart_rate (scope: `read:body_measurement`)

## Pagination

All collection endpoints return:
```json
{
  "records": [...],
  "next_token": "MTIz..."
}
```

Pass `?nextToken=<token>` for next page. Max limit: 25.
Default limit: 10.

## Interpreting Scores

**Recovery (0–100):**
- Green (67–100): Well-recovered, push hard
- Yellow (34–66): Moderate, listen to body
- Red (0–33): Under-recovered, prioritize rest

**Strain (0–21):**
- Light: 0–9
- Moderate: 10–13
- Strenuous: 14–17
- All Out: 18–21

**Sleep Performance:** % of sleep needed that was achieved.

**HRV (RMSSD):** Higher = better recovery; personal baseline varies widely.
