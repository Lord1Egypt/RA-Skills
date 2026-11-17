# Data schema and deterministic rules

## Local files

Default directory:

- `SLEEP_ROUTINE_DATA_DIR` when set.
- Otherwise `$XDG_DATA_HOME/sleep-routine-coach`.
- Otherwise `~/.local/share/sleep-routine-coach`.

Files are created with best-effort directory mode `0700` and file mode `0600`:

- `profile.json`: consent and preferences.
- `sleep-records.json`: final effective records with provenance and audit history.
- `reminders.json`: reminder state; never an OpenClaw Cron database.
- `sleep-shift-plan.json`: the consented gradual adjustment plan, current stage, review date, and audit history.

Do not save these files under the Skill or repository. Do not sync them externally unless the user explicitly exports and moves them.

## Record fields

Every record includes at least:

| Field | Type | Meaning |
| --- | --- | --- |
| `date` | `YYYY-MM-DD` | Local session date anchored to the reported preparation-for-sleep event. |
| `timezone` | IANA string | Timezone used for this session. |
| `goodnight_at` | ISO 8601 or null | User reported preparing for sleep; not actual sleep onset. |
| `sleep_latency_minutes` | integer or null | User-reported/clarified latency, or deterministically derived from two reported timestamps. |
| `sleep_latency_category` | string or null | Raw short answer such as `quick`, `about_30`, `over_60`, or `unknown`. |
| `reported_sleep_at` | ISO 8601 or null | Direct user report of sleep onset; self-reported, not measured. |
| `estimated_sleep_at` | ISO 8601 or null | Derived from `goodnight_at + sleep_latency_minutes`. |
| `morning_at` | ISO 8601 or null | User-reported awake time; not necessarily out-of-bed time. |
| `out_of_bed_at` | ISO 8601 or null | User-reported out-of-bed time. |
| `night_awakenings` | integer or null | Reported awakenings for any reason. |
| `night_awakenings_category` | string or null | Non-exact raw choice such as `3_plus`. |
| `nocturia_count` | integer or null | Reported awakenings involving urination. |
| `nocturia_category` | string or null | Non-exact raw choice such as `3_plus`. |
| `night_awake_minutes` | integer or null | Reported total awake time after sleep onset. |
| `rested_score` | integer 0–5 or null | Optional self-rating. |
| `notes` | string or null | User-intended note only. |
| `source` | string | Record origin, normally `user_report`. |
| `created_at` | ISO 8601 | Record creation time. |
| `updated_at` | ISO 8601 | Last modification time. |

Additional derived fields:

- `reported_window_minutes`: elapsed time from goodnight to morning. Never call this sleep duration.
- `estimated_sleep_at`: derived estimate from goodnight plus latency; a direct onset report remains separately visible in `reported_sleep_at`.
- `estimated_sleep_duration_minutes`: set only when estimated sleep onset, morning time, and night-awake duration are known. `night_awakenings == 0` establishes zero night-awake duration.
- `provenance`: marks values as reported, estimated, or derived.
- `audit_history`: append-only changes within the surviving record.

Deleting a day removes that record, including its audit history. Deleting all removes every local file. Do not retain a hidden tombstone.

## Gradual sleep-shift plan

`sleep-shift-plan.json` includes:

| Field | Meaning |
| --- | --- |
| `status` | `active`, `paused`, `completed`, or `cancelled`. |
| `current_sleep_time` / `target_sleep_time` | Baseline and target reminder anchors for sleep time. |
| `current_wake_time` / `target_wake_time` | Optional user-supplied reminder references; never derived from sleep time. |
| `wake_policy` | `independent_optional`; wake reminders do not define sleep duration. |
| `sleep_duration_target_minutes` | Null by default; the Skill does not require a fixed duration target. |
| `direction` / `phase_shift_minutes` | Earlier/later direction and total wall-clock shift. |
| `step_minutes` / `hold_days` | Stage size (15 or 30 minutes) and minimum nights at each stage. |
| `current_stage_index` | Explicitly confirmed active stage; never inferred from missing reports. |
| `stage_started_on` / `review_on_or_after` | Local dates controlling when the next review may occur. |
| `stages` | Deterministically generated sleep-time, wind-down, and review values. |
| `audit_history` | Plan start, hold, advance, back, pause, resume, complete, or cancel events. |

Starting or changing a stage updates only the profile's sleep-time reminder anchor with an audit entry. It does not silently change a wake reminder, infer sleep duration, or create/edit external jobs itself.

## Time rules

- Require offset-aware ISO 8601 timestamps.
- Store the IANA timezone separately because an offset alone does not encode future/past DST rules.
- Convert to UTC for elapsed-time arithmetic, then convert back through `zoneinfo`.
- Never add wall-clock hours directly across DST changes.
- Accept timezone changes by storing the zone on each session; do not rewrite old records automatically.
- Anchor a normal session to the local date of `goodnight_at`. If morning arrives without a matching open record, default to the previous local date and let the user correct it.
- Require explicit date/offset clarification for ambiguous fall-back times or nonexistent spring-forward wall times.

## Missing data and estimates

- Keep unknown values as JSON `null`.
- Never infer actual sleep onset from a goodnight message.
- Never infer out-of-bed time from a morning message.
- Never invent awake duration, awakening count, rested score, or notes.
- Calculate `estimated_sleep_at` only with a reported latency.
- Calculate estimated sleep duration only when both boundaries and intervening awake time are sufficiently known.
- Report all trends as descriptive associations, not causes.

## Commands

All commands accept `--data-dir`.

```bash
python3 {baseDir}/scripts/manage_profile.py init --consent \
  --timezone America/Toronto --sleep-window-start 23:00

python3 {baseDir}/scripts/build_reminder_schedule.py plan \
  --reminder wind_down --reminder sleep_time

python3 {baseDir}/scripts/record_sleep_event.py goodnight \
  --at 2026-07-29T23:06:00-04:00

python3 {baseDir}/scripts/record_sleep_event.py morning \
  --at 2026-07-30T07:32:00-04:00

python3 {baseDir}/scripts/record_sleep_event.py sleep-onset \
  --date 2026-07-29 --at 2026-07-30T01:00:00-04:00 \
  --reason "User said: I actually fell asleep at one"

python3 {baseDir}/scripts/record_sleep_event.py correct \
  --date 2026-07-29 --field sleep_latency_minutes --value 30 \
  --reason "User said about half an hour"
```

Substitute the actual Skill directory for `{baseDir}` when running outside OpenClaw.
