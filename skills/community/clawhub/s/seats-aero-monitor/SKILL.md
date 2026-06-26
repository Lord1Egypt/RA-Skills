---
name: seats-aero-monitor
description: Monitor award availability via Seats.aero API across configurable
  watchers (route/program/cabin/date window), emit UNCONFIRMED alerts on
  none->available transitions, and persist idempotent watcher state in SQLite or JSON.
permalink: openclaw-nexus/skills/seats-aero-monitor/skill
metadata:
  openclaw:
    emoji: ✈️
---

# Seats.aero Monitor Skill

Track award availability from Seats.aero without airline-specific confirmers.

## What This Skill Does

1. Query Seats.aero cached search for multiple watchers.
2. Normalize raw API records into a stable internal schema.
3. Persist watcher config + watcher state in SQLite or JSON for idempotent `new_only` alerting.
4. Return `[UNCONFIRMED / Seats.aero]` alert events for `none -> available` transitions.

## Entry Point

```bash
python3 <skill-dir>/scripts/check_awards.py --watchers-source db

# JSON backend
python3 <skill-dir>/scripts/check_awards.py \
  --state-backend json \
  --state-json /path/to/monitor.json \
  --watchers-source db
```

## Optional Flags

```bash
# Single watcher only
python3 <skill-dir>/scripts/check_awards.py --watchers-source auto --watcher ana_sfo_hnd
```

## Watchers In DB

Import watchers from config into DB:

```bash
python3 <skill-dir>/scripts/check_awards.py --watchers-import --replace-watchers --config /path/to/watchers.json

# Import into JSON state file instead of SQLite
python3 <skill-dir>/scripts/check_awards.py \
  --state-backend json \
  --state-json /path/to/monitor.json \
  --watchers-import --replace-watchers --config /path/to/watchers.json
```

List DB watchers:

```bash
python3 <skill-dir>/scripts/check_awards.py --watchers-list

# List watchers stored in JSON state file
python3 <skill-dir>/scripts/check_awards.py \
  --state-backend json \
  --state-json /path/to/monitor.json \
  --watchers-list
```

Update watchers' date ranges:

```bash
# Update specific watcher by ID
python3 <skill-dir>/scripts/update_watcher_dates.py \
  --watcher pvg_sfo_aeroplan_2026summer --start 2026-08-01 --end 2026-08-15

# Update all watchers from an origin airport
python3 <skill-dir>/scripts/update_watcher_dates.py \
  --origin PVG --start 2026-08-01 --end 2026-08-15

# Dry run (preview changes)
python3 <skill-dir>/scripts/update_watcher_dates.py \
  --origin PVG --start 2026-08-01 --end 2026-08-15 --dry-run

# Update dates in JSON backend
python3 <skill-dir>/scripts/update_watcher_dates.py \
  --state-backend json --state-json /path/to/monitor.json \
  --origin PVG --start 2026-08-01 --end 2026-08-15

# Skip confirmation prompt
python3 <skill-dir>/scripts/update_watcher_dates.py \
  --origin PVG --start 2026-08-01 --end 2026-08-15 --yes

# See all options
python3 <skill-dir>/scripts/update_watcher_dates.py --help
```

Fixed date range support:

1. `fixed_start_date` + `fixed_end_date` (`YYYY-MM-DD`) to track a fixed window (for example, August only).
2. Set both to same day to track one specific date.
3. If fixed dates are set, `window_days` is ignored.

SQLite state DB default path (override via `--state-db` or `SEATS_AERO_DB` env):

- `<skill-dir>/data/monitor.db`  (relative to skill installation)
- Or set `SEATS_AERO_DB=/path/to/monitor.db` in environment

JSON backend requires `--state-backend json --state-json /path/to/monitor.json`.

## Requirements

- **Python**: 3.11+ (uses `str | None` union syntax)
- **SQLite3**: Built into Python standard library; DB file and schema are auto-created on first run when using `--state-backend sqlite`
- **JSON**: No extra dependency; state file is auto-created on first write when using `--state-backend json`
- **Optional**: `brotli` Python package (only needed if Seats.aero API returns Brotli-compressed responses)
- **Seats.aero API Key**: Required for all API calls

## Environment

Set Seats API key before running:

```bash
export SEATS_AERO_API_KEY="pro_xxx..."
```

## Important Limitation

All alerts are candidate signals from Seats.aero. This skill intentionally does not perform airline-side confirmation and marks all alerts as unconfirmed.

This script does not send messages directly; caller/agent should read `data.alert_events` from JSON output and send notifications.