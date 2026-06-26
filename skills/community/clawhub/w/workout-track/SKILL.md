---
name: workout-track
description: Log a strength training session and insert it into the life_db database. Use when the user shares their gym session, exercises, sets, reps, weights, RPE, rest times, session duration, feelings, or asks to record a workout.
metadata: {"openclaw":{"requires":{"bins":["uv"]}}}
---

# Workout Log

Parses strength training sessions from natural or structured input and inserts them into the `sport` schema of `life_db`.

## Connection

Credentials are in `~/.openclaw/services/life-db/.env`.

## Workflow

### 1. Parse the user's message

Extract from free text or structured input:

| Field | Type | Notes |
|-------|------|-------|
| `session_date` | YYYY-MM-DD | Default: today |
| `duration_min` | int | Total session duration |
| `feeling` | 1–10 integer | Overall session feeling |
| `notes` | string | Optional — program name, injuries, etc. |
| `exercises[]` | array | One object per exercise |

Each exercise:

| Field | Type | Notes |
|-------|------|-------|
| `exercise_name` | string | Normalize consistently (e.g. "Bench Press", "Squat", "Romanian Deadlift") |
| `sets` | int | Number of working sets |
| `reps` | int | Reps per set (use average if varied) |
| `weight_kg` | float | Working weight — `null` for bodyweight exercises |
| `rpe` | float | Rate of perceived exertion (1–10), optional |
| `rest_sec` | int | Rest between sets in seconds, optional |
| `order_in_session` | int | Order as mentioned |
| `notes` | string | Optional — tempo, drop sets, supersets, etc. |

### 2. Confirm with the user

Show a summary before inserting:

```
📅 {DD/MM/YYYY} · Muscu · {duration} min · Feeling {feeling}/10
• {Exercise 1} — {sets}×{reps} @ {weight} kg
• {Exercise 2} — {sets}×{reps} bodyweight
• …

Save? (yes / no)
```

### 3. Insert

Only after confirmation, use the `exec` tool:

```json
{
  "tool": "exec",
  "command": "bash -c 'set -a; source ~/.openclaw/services/life-db/.env; uv run --project ~/.openclaw {baseDir}/scripts/insert_workout.py <json>'"
}
```

Replace `<json>` with the minified JSON payload (no newlines, properly shell-escaped).

### 4. Confirm result

**On `OK`** — respond with exactly this format, nothing more:

```
✅ Muscu · {duration} min · Feeling {feeling}/10 · #{session_id}
{comment}
```

`{comment}` rules — **1 line, max 60 chars, no emoji**:
- feeling ≥ 8 → short hype line
- feeling 5–7 → encouragement
- feeling ≤ 4 → grind acknowledgement

**On `ERROR`** — report the error as-is, do not retry without user input.

## Examples

| User says | Parsed session |
|-----------|---------------|
| "Gym 1h feeling 8. Bench 4x10 80kg, Squat 4x8 100kg, Curl 3x12 15kg" | 3 exercises, 60 min, feeling 8/10 |
| "45 min chest/shoulders. Bench press 5x5 90kg RPE 9, overhead press 4x8 40kg, lateral raises 3x15 10kg" | 3 exercises, 45 min, feeling asked |
| "Quick session 30min: pull-ups 4x8 bodyweight, rows 4x10 60kg" | 2 exercises, 30 min, feeling asked |
