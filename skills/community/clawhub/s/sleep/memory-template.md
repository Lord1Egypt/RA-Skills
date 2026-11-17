# Memory Template — Sleep

Create `~/Clawic/data/sleep/memory.md` with this structure:

```markdown
# Sleep Memory

## Status
status: ongoing
last: YYYY-MM-DD

## Context
<!-- Schedule reality: work pattern, commitments, observed chronotype -->
<!-- Household: partner schedule, kids, pets, room situation -->

## Protocol State
<!-- Active protocol (insomnia / jet lag / shift / circadian), week number, last SE, next titration date -->
<!-- Red flags screened and cleared, with date -->

## Substance Habits
<!-- Caffeine dose and usual last-dose time, alcohol pattern, THC, prescriptions (never doses to change, only context) -->

## Preferences
<!-- Entries under areas: schedule, household, substances, risk posture, reporting -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning |
|-------|---------|
| `ongoing` | Active protocol or still learning their situation |
| `discharged` | Protocol completed; relapse plan delivered |

## Other Files in `~/Clawic/data/sleep/`

| File | Purpose | Format defined in |
|------|---------|-------------------|
| `config.yaml` | Declared variables (wake_anchor, time_format, units, tracker) + preference-area keys | `SKILL.md` Configuration |
| `diary.md` | The 7-day-plus sleep diary, one line per night; protocol ground truth | `insomnia.md` |
| `trip-<destination>.md` | Per-day jet lag plan table | `jetlag.md` |

config ≠ memory: `config.yaml` is what the user declared; `memory.md` is what you observed.
