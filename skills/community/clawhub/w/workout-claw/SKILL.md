---
name: workout-claw
description: Log workouts, track progress, compute PRs, edit/delete sessions via a local CLI. Local-first, JSON storage.
author: Denys Sychov
version: 0.3.0
triggers:
  - "log workout"
  - "log my workout"
  - "track exercise"
  - "gym session"
  - "what's my PR"
  - "what is my PR"
  - "workout history"
  - "lift history"
  - "today's workout"
  - "last workout"
  - "show last session"
  - "delete workout"
  - "remove session"
  - "edit workout"
  - "fix my workout"
  - "back volume"
  - "chest volume"
  - "leg volume"
  - "how much volume"
  - "muscle volume"
  - "weekly volume"
---

# workout-claw

Local-first gym workout tracker. Plain-JSON storage at `~/.workout-claw/`. Invokable as a CLI by an agent — no MCP server, no daemon.

## When to invoke

User describes a workout session, asks about progress, or wants to see a PR. Examples that should trigger this skill:

- "I just did chest day — bench 4x10 at 60, incline DB 4x12 at 20, triceps 4x12 at 40"
- "Log today's workout"
- "What's my bench PR?"
- "Show my back workouts from the last 4 weeks"
- "What did I do at the gym today?"

## How to invoke

Use the `workout-claw` CLI via Bash. All commands output YAML to stdout, errors to stderr.

### Log a workout

```bash
workout-claw log "bench 4x10@60, incline-db-press 4x12@20, triceps-pushdown 4x12@40"
```

Optional flags:
- `--muscle <group>` — `back | legs | chest | shoulders | arms | core | full | cardio | other`. If omitted, inferred from weekday (Mon=back, Wed=legs, Fri=chest per `~/.life/domains/health.md`).
- `--cardio "<entry>"` — e.g. `"incline-walk 20min @4.5kmh i6"` (minutes, speed kmh, incline)
- `--note "<text>"` — free-text note
- `--date YYYY-MM-DD` — override date
- `--time HH:MM` — override time

### Input syntax

`<exercise> <sets>x<reps>@<weight>` per entry, comma-separated for multiple exercises.

- Multi-word exercise names use dashes: `incline-db-press`, `barbell-row`
- Bodyweight: `pullups 4x10@bw`
- All weights in kg

### Query history

```bash
workout-claw history --muscle chest --weeks 4
workout-claw history --exercise bench
```

### Get a PR

```bash
workout-claw pr bench
```

Returns best estimated 1RM via Epley formula: `weight × (1 + reps/30)`.

### Cross-day muscle volume (v0.3+)

```bash
workout-claw volume --muscle back --weeks 4
workout-claw volume --muscle chest --weeks 8
```

Aggregates volume **per exercise**, not per session. Pullups on chest day count toward `back` volume; triceps-pushdown counts toward `arms`. Returns total kg lifted, sets, reps, days trained, and a per-date breakdown.

**This is the right query for tracking weekly volume per muscle group** — far more accurate than `history --muscle X` which is session-grain.

### Summary of today

```bash
workout-claw summary
workout-claw summary --date 2026-05-15
```

### Most recent session

```bash
workout-claw last
```

Returns the latest session across all dates — useful for "what did I do at the gym?" without naming a date.

### Delete a session

```bash
workout-claw delete <session-id>
```

Session IDs come from the `id` field in any `log` / `summary` / `last` output. No confirmation prompt — the CLI is non-interactive by design.

### Edit a session

```bash
workout-claw edit <session-id>
```

Opens the session JSON in `$EDITOR` (defaults to `vi`). On save: validates JSON, refuses to save if the `id` was changed. On parse error: original session unchanged. Useful for fixing typos in exercise names or set counts without a full delete + re-log.

**Agent note:** `edit` requires an interactive editor, so the agent should not invoke this in a Telegram round-trip. Instead, when a user asks to fix a logged workout via Telegram, prefer `delete` + `log` again, or hand back the session ID and tell the user to run `workout-claw edit <id>` from their terminal.

## Data location

- `~/.workout-claw/logs/<date>.json` — one JSON file per day, array of sessions
- Schema: see `src/lib/types.ts` in the workout-claw repo

## Notes for the agent

- After logging, relay the YAML summary back to the user in a readable form (don't dump raw YAML)
- If the user names an exercise that doesn't match the dash-naming convention, normalize before invoking (e.g. "incline DB press" → `incline-db-press`)
- Session-level `--muscle` is inferred from weekday — only set explicitly if the user names a non-standard split (e.g. arm day on a Tuesday). **Per-exercise muscle tags are inferred automatically** at log time via name lookup (pullups→back, bench→chest, etc.), so no extra input is needed.
- When user describes cardio separately, use `--cardio` flag. When they describe both lifting + cardio in one breath, use both.
- For "how much back/chest/leg volume?" questions, prefer **`volume --muscle X`** over `history --muscle X` — volume aggregates per-exercise, history filters per-session.
