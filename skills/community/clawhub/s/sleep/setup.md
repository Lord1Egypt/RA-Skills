# Setup — Sleep

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

Sleep is where advice inflation does damage: one measured intervention beats five tips. Triage first, protocol second, referral without hesitation when the Red Flags table says so. Be calm and concrete; never moralize about the user's schedule.

## How To Load Preferences

1. Read `~/Clawic/data/sleep/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `wake_anchor: none` (derive from a 7-day diary), `time_format: 24h`, `units: metric`, `tracker: none`.
3. Read `~/Clawic/data/sleep/memory.md` for prior context (protocol state, schedule, household). Absence is fine; proceed without comment.
4. Check for an active protocol: `diary.md` or a `trip-<destination>.md` with recent dates means a protocol is mid-flight — resume it, do not restart.

Work from defaults immediately. Never open with questions about schedules, goals, or how the user slept.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User states their wake time, clock format, units, or names their tracker → update the matching key in `~/Clawic/data/sleep/config.yaml`.
- User reveals a schedule pattern, household constraint, substance habit, risk stance, or reporting preference → record it under the relevant preference area (schedule, household, substances, risk posture, reporting) in `~/Clawic/data/sleep/memory.md`.
- User corrects earlier guidance → update the stored value so you don't repeat it.

If the user has said nothing, store nothing.

## What Memory Holds

See `memory-template.md` for the file format. Track their schedule reality (work pattern, chronotype as observed), active protocol and its week, red flags already screened, and substance habits — but only from what they actually reveal. Observations never overwrite a declared preference without the user's confirmation.
