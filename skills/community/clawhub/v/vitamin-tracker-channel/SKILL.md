---
name: vitamin-tracker-channel
version: 1.0.1
description: Manage vitamin/supplement reminders across configurable daily time slots via cron jobs. Use when adjusting supplement schedules, adding/removing supplements, or handling vitamin-related channel interactions. Triggers on "vitamin", "supplement", "vitamin reminder", "vitamin schedule".
env:
  VITAMIN_CHANNEL_ID:
    description: Channel ID for vitamin reminders
    required: true
  VITAMIN_TIMEZONE:
    description: IANA timezone for scheduling (e.g. America/New_York)
    required: true
  WORKSPACE:
    description: Root workspace directory for data files
    required: false
---

# Vitamin Tracker Channel

Manage supplement reminders across configurable daily time slots using OpenClaw cron jobs.

## Configuration

Set the following environment variables:
- `VITAMIN_CHANNEL_ID` — the channel to post reminders in
- `VITAMIN_TIMEZONE` — IANA timezone for scheduling (e.g. `America/New_York`, `Europe/Berlin`)
- `WORKSPACE` — root workspace directory (defaults to `~/.openclaw/workspace`)

Supplement names and schedules are configured in `VITAMINS.md` in the workspace root. Edit the schedule section to match your regimen.

## Schedule Format

`VITAMINS.md` should have a `## Schedule` section with time labels and HH:MM times, followed by `### Label` subsections listing supplements:

```markdown
## Schedule

- Breakfast: 09:00
- Lunch: 13:00
- Dinner: 18:00

### Breakfast

- Multivitamin
- Vitamin C
- Vitamin D₃

### Lunch

- Fiber (keep 2h away from minerals)

### Dinner

- Magnesium
```

## Update Script

After editing `VITAMINS.md`, run the update script to sync all cron jobs:

```bash
python3 scripts/update_vitamin_crons.py
```

This reads `VITAMINS.md`, removes existing vitamin cron jobs, and recreates them with the updated schedule.

## What the Script Handles

- Parses the `## Schedule` section for times
- Parses each `### Label` section for supplement lists
- Creates one cron job per time slot (up to 5 configurable slots)
- Formats reminder messages: "Vitamin reminder: Breakfast time. Take Multivitamin, Vitamin C, and Vitamin D₃."
- Removes old jobs before recreating to avoid duplicates

## Cron Job Naming

Jobs are named `vitamins-{label}-reminder` (e.g. `vitamins-breakfast-reminder`, `vitamins-lunch-reminder`).

## Runtime Requirements

- `python3` — the update script is Python
- `openclaw` CLI — the script calls `openclaw cron` to manage jobs

## Data Access

This skill:
- **Reads** `$WORKSPACE/VITAMINS.md` — your supplement schedule (user-created)
- **Manages cron jobs** via the `openclaw cron` CLI — removes existing vitamin jobs, then recreates them
- **Posts messages** to the configured channel via cron delivery (requires network when cron fires)
- **No data files written** — schedule lives in VITAMINS.md, state is in the cron system

**Note:** The update script removes all existing `vitamins-*-reminder` cron jobs before recreating them. Back up existing jobs if needed.

## Required Files

- `scripts/update_vitamin_crons.py` — cron job sync script (included in bundle)
- `$WORKSPACE/VITAMINS.md` — supplement schedule (user-created, not included)
