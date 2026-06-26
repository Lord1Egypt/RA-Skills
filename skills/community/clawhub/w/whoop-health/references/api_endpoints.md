# WHOOP API v1 Endpoints Reference

Base URL: `https://api.prod.whoop.com/developer/v1`

All requests require: `Authorization: Bearer <access_token>`

---

## User

### GET /user/profile/basic
Returns name and email.

**Response:**
```json
{
  "user_id": 10129,
  "email": "user@example.com",
  "first_name": "Jane",
  "last_name": "Smith"
}
```

### GET /user/measurement/body
Returns height, weight, max heart rate.

**Response:**
```json
{
  "height_meter": 1.7,
  "weight_kilogram": 65.0,
  "max_heart_rate": 185
}
```

---

## Recovery

### GET /recovery

**Query params:**
| Param | Type | Description |
|-------|------|-------------|
| start | ISO8601 | Start of range (e.g. `2025-01-01T00:00:00Z`) |
| end | ISO8601 | End of range |
| nextToken | string | Pagination cursor |
| limit | int | Records per page (max 25) |

**Response record:**
```json
{
  "cycle_id": 93845,
  "sleep_id": 10235,
  "user_id": 10129,
  "created_at": "2022-04-24T11:25:44.774Z",
  "updated_at": "2022-04-24T14:25:44.774Z",
  "score_state": "SCORED",
  "score": {
    "user_calibrating": false,
    "recovery_score": 44,
    "resting_heart_rate": 64,
    "hrv_rmssd_milli": 31.813562,
    "spo2_percentage": 98.0,
    "skin_temp_celsius": 33.7
  }
}
```

**score_state values:** `SCORED`, `PENDING_SCORE`, `UNSCORABLE`

---

## Sleep

### GET /activity/sleep

Same pagination params as recovery.

**Response record:**
```json
{
  "id": 10235,
  "user_id": 10129,
  "created_at": "2022-04-24T02:25:44.774Z",
  "updated_at": "2022-04-24T10:25:44.774Z",
  "start": "2022-04-24T02:25:44.774Z",
  "end": "2022-04-24T10:25:44.774Z",
  "timezone_offset": "-05:00",
  "nap": false,
  "score_state": "SCORED",
  "score": {
    "stage_summary": {
      "total_in_bed_time_milli": 30051529,
      "total_awake_time_milli": 1530499,
      "total_no_data_time_milli": 0,
      "total_light_sleep_time_milli": 11863742,
      "total_slow_wave_sleep_time_milli": 5961067,
      "total_rem_sleep_time_milli": 7069415,
      "sleep_cycle_count": 2,
      "disturbance_count": 1
    },
    "sleep_needed": {
      "baseline_milli": 27395716,
      "need_from_sleep_debt_milli": 736282,
      "need_from_recent_strain_milli": 0,
      "need_from_recent_nap_milli": -8000000
    },
    "respiratory_rate": 16.11328,
    "sleep_performance_percentage": 98,
    "sleep_consistency_percentage": 65,
    "sleep_efficiency_percentage": 91
  }
}
```

---

## Workout

### GET /activity/workout

Same pagination params as recovery.

**Response record:**
```json
{
  "id": 1043,
  "user_id": 10129,
  "created_at": "2022-04-24T11:25:44.774Z",
  "updated_at": "2022-04-24T14:25:44.774Z",
  "start": "2022-04-24T11:25:44.774Z",
  "end": "2022-04-24T14:25:44.774Z",
  "timezone_offset": "-05:00",
  "sport_id": 1,
  "score_state": "SCORED",
  "score": {
    "strain": 8.2,
    "average_heart_rate": 123,
    "max_heart_rate": 155,
    "kilojoule": 1569.34,
    "percent_recorded": 100,
    "distance_meter": 1609.34,
    "altitude_gain_meter": 303.37,
    "altitude_change_meter": 2.1,
    "zone_duration": {
      "zone_zero_milli": 0,
      "zone_one_milli": 0,
      "zone_two_milli": 0,
      "zone_three_milli": 0,
      "zone_four_milli": 0,
      "zone_five_milli": 0
    }
  }
}
```

**Common sport_id values:** 1=Running, 0=Activity (general), 57=Cycling, 63=Weightlifting, 44=Swimming

---

## Cycle (Day Strain)

### GET /cycle

Same pagination params as recovery.

**Response record:**
```json
{
  "id": 93845,
  "user_id": 10129,
  "created_at": "2022-04-24T11:25:44.774Z",
  "updated_at": "2022-04-24T14:25:44.774Z",
  "start": "2022-04-24T02:25:44.774Z",
  "end": "2022-04-24T13:25:44.774Z",
  "timezone_offset": "-05:00",
  "score_state": "SCORED",
  "score": {
    "strain": 5.2,
    "kilojoule": 1569.34,
    "average_heart_rate": 68,
    "max_heart_rate": 141
  }
}
```

---

## Pagination

All list endpoints return:
```json
{
  "records": [...],
  "next_token": "optional_cursor_string"
}
```

When `next_token` is present, pass it as `?nextToken=<value>` to get the next page.

---

## Key Metrics Reference

| Metric | Range | Good | Concerning |
|--------|-------|------|-----------|
| Recovery Score | 0–100% | ≥67% (green) | ≤33% (red) |
| HRV (RMSSD) | varies | Above personal baseline | Trending down |
| Resting HR | varies | Below personal baseline | Elevated |
| Sleep Performance | 0–100% | ≥85% | <70% |
| Day Strain | 0–21 | Matches recovery capacity | Strain >> Recovery |
