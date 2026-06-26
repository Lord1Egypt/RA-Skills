# Vitamin Tracker Channel

An OpenClaw skill that manages vitamin/supplement reminders across configurable daily time slots using cron jobs.

## Setup

1. Create a `VITAMINS.md` in your workspace root with your schedule (see format below)
2. Set the `VITAMIN_CHANNEL_ID` env var to your reminder channel ID
3. Set the `VITAMIN_TIMEZONE` env var to your IANA timezone
4. Run `python3 scripts/update_vitamin_crons.py` to create the cron jobs

## VITAMINS.md Format

```markdown
## Schedule

- Breakfast: 09:00
- Lunch: 13:00
- Early Afternoon: 15:00
- Dinner: 17:00
- Night: 23:00

### Breakfast

- Multivitamin
- Vitamin C
- Vitamin D₃

### Lunch

- Fiber supplement

### Night

- Melatonin
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `VITAMIN_CHANNEL_ID` | Yes | Channel ID for posting reminders |
| `VITAMIN_TIMEZONE` | Yes | IANA timezone (e.g. `America/New_York`) |
| `WORKSPACE` | No | Workspace root path (default: `~/.openclaw/workspace`) |

## What It Does

- Parses your `VITAMINS.md` schedule
- Creates one cron job per time slot
- Posts formatted reminders: "Vitamin reminder: Breakfast time. Take Multivitamin, Vitamin C, and Vitamin D₃."
- Run the script again after editing to update all jobs

## License

MIT
