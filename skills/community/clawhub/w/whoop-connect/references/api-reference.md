# WHOOP API v2 Reference

Base URL: `https://api.prod.whoop.com/developer`

## Authentication

OAuth 2.0 Authorization Code flow.

- Auth URL: `https://api.prod.whoop.com/oauth/oauth2/auth`
- Token URL: `https://api.prod.whoop.com/oauth/oauth2/token`
- Scopes: `offline`, `read:profile`, `read:body_measurement`, `read:cycles`, `read:recovery`, `read:sleep`, `read:workout`

WHOOP rotates refresh tokens on each use. Always store the new refresh token from every token response.

## Endpoints

### Recovery

- `GET /v2/recovery` — paginated collection
- `GET /v2/cycle/{cycleId}/recovery` — single recovery by cycle

**RecoveryScore fields:**
- `recovery_score` (float) — 0-100%
- `hrv_rmssd_milli` (float) — HRV in milliseconds
- `resting_heart_rate` (float) — bpm
- `spo2_percentage` (float, optional) — blood oxygen, requires 4.0 hardware
- `skin_temp_celsius` (float, optional) — skin temperature, requires 4.0 hardware
- `user_calibrating` (bool) — true during initial calibration period

### Sleep

- `GET /v2/activity/sleep` — paginated collection
- `GET /v2/activity/sleep/{sleepId}` — single sleep by UUID
- `GET /v2/cycle/{cycleId}/sleep` — sleep for a cycle

**SleepStageSummary fields:**
- `total_in_bed_time_milli` (int) — total bed time
- `total_awake_time_milli` (int) — awake time
- `total_light_sleep_time_milli` (int) — Stage 1-2
- `total_slow_wave_sleep_time_milli` (int) — Stage 3 deep sleep
- `total_rem_sleep_time_milli` (int) — REM
- `total_no_data_time_milli` (int) — device disconnected
- `sleep_cycle_count` (int) — complete cycles
- `disturbance_count` (int) — disruptions

**SleepScore additional fields:**
- `respiratory_rate` (float, optional) — breaths/min
- `sleep_performance_percentage` (float, optional) — actual vs needed
- `sleep_efficiency_percentage` (float) — asleep vs in-bed
- `sleep_consistency_percentage` (float, optional) — night-to-night

**SleepNeeded fields:**
- `baseline_milli` (int) — historical baseline
- `need_from_sleep_debt_milli` (int) — debt component
- `need_from_recent_strain_milli` (int) — strain component
- `need_from_recent_nap_milli` (int) — nap reduction (zero or negative)

### Cycle

- `GET /v2/cycle` — paginated collection
- `GET /v2/cycle/{cycleId}` — single cycle

**CycleScore fields:**
- `strain` (float) — 0-21 scale
- `kilojoule` (float) — energy expenditure
- `average_heart_rate` (int) — mean HR
- `max_heart_rate` (int) — peak HR

### Workout

- `GET /v2/activity/workout` — paginated collection
- `GET /v2/activity/workout/{workoutId}` — single workout by UUID

**WorkoutScore fields:**
- `strain` (float) — 0-21
- `average_heart_rate` (int) — bpm
- `max_heart_rate` (int) — bpm
- `kilojoule` (float) — energy
- `percent_recorded` (float) — data completeness 0-100%
- `distance_meter` (float, optional) — distance
- `altitude_gain_meter` (float, optional) — elevation gain
- `altitude_change_meter` (float, optional) — net elevation change

**ZoneDurations fields** (all in milliseconds):
- `zone_zero_milli` — rest
- `zone_one_milli` — very light
- `zone_two_milli` — light
- `zone_three_milli` — moderate
- `zone_four_milli` — hard
- `zone_five_milli` — maximum

### Profile & Body

- `GET /v2/user/profile/basic` — name, email, user_id
- `GET /v2/user/measurement/body` — height, weight, max HR

### Pagination

All collection endpoints accept:
- `limit` (int, max 25, default 10)
- `start` (ISO 8601 datetime)
- `end` (ISO 8601 datetime)
- `nextToken` (string) — for next page

### Rate Limits

WHOOP enforces rate limits. On 429 response, respect the `Retry-After` header.
