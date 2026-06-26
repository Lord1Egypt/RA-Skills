---
name: world-meeting-coordination-skill
description: Find the best cross-timezone meeting windows with DST-safe conversion and ranked output (Optimal, Stretch, Avoid). Use when users ask for overlap windows across 2+ cities/timezones, want results anchored to one timezone, or need Telegram-friendly scheduling output with 24h + 12h time formats and +1 day markers.
---

# World Meeting Coordination Skill

Rank meeting windows across timezones in a clean, decision-ready format.

## What this skill does

- Converts candidate slots across multiple timezones (DST-safe via IANA/zoneinfo)
- Scores each slot for comfort
- Returns ranked sections:
  - `Optimal`
  - `Stretch`
  - `Avoid`
- Outputs Telegram-friendly formatting

## Quick start

### Natural-language prompt examples

- "Find the best meeting windows for Chicago, London, and Tel Aviv on March 6, anchored to Chicago time. Return Optimal, Stretch, and Avoid windows with reasons."
- "Find overlap windows for San Francisco, New York, and Berlin on 2026-04-12 in Pacific time, 60-minute meetings."
- "Give me top 3 windows for Chicago, Paris, and Singapore tomorrow in Chicago time, with +1 day markers where needed."

### CLI example

```bash
python3 scripts/meeting_windows.py \
  --date 2026-03-06 \
  --anchor America/Chicago \
  --zones "Chicago=America/Chicago,London=Europe/London,Tel Aviv=Asia/Jerusalem"
```

## Inputs

Required:

- `--date` (YYYY-MM-DD preferred)
- `--zones` (name=IANA timezone pairs)

Optional:

- `--anchor` (default: `America/Chicago`)
- `--duration` meeting length in minutes (default: `60`)
- `--step` slot step size in minutes (default: `60`)
- `--top` top results per category (default: `3`)
- `--my-hours` your preferred hours, e.g. `08:00-16:00`
- `--hours` per-participant hours map, e.g. `London=08:30-17:30,Bangalore=10:00-18:00`

## Onboarding and settings

First interactive run auto-starts onboarding with 3 questions:

1. Your timezone
2. Your preferred meeting hours
3. Your flexibility (`strict`, `balanced`, `flexible`)

### Canonical chat phrase

- `Run world meeting skill setup`

### Also treat these as setup intent

- "set up meeting skill"
- "configure world meeting"
- "update my meeting hours"
- "set my scheduling preferences"
- "change my timezone for meeting windows"
- "show my meeting settings"

### Settings commands

```bash
python3 scripts/meeting_windows.py --setup
python3 scripts/meeting_windows.py --show-settings
```

Settings file location:

- `~/.openclaw/skills/world-meeting-coordination-skill/config.json`

## Output format contract

- Sections: `Optimal`, `Stretch`, `Avoid`
- Numbered items (`1.`, `2.`, ...)
- Anchor-time line first, then participant local lines
- Time format: `24h (12h)`
- `+1 day` marker when local date rolls over
- Spacer line `⠀` between items for Telegram rendering
- Stretch/Avoid include italic reason line: `*Reason: ...*`

## Scoring model (default)

Per participant, local start time is scored:

- In preferred window: `+0`
- Near edge: low penalty
- Outside window: medium penalty
- Overnight/off-hours: high penalty

Total score maps to:

- `Optimal`: low total
- `Stretch`: medium total
- `Avoid`: high total

## Notes

- Prefer IANA timezone names (example: `Europe/London`, not `GMT+0`).
- If user gives city names only, map city -> IANA timezone before running.
- If a category is empty, return the best available windows with a brief note.
