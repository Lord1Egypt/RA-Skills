---
name: clawhub-download-tracker
description: Monitor download counts for your ClawHub-published skills. Track changes over time, generate daily/weekly/monthly reports, and push notifications via Feishu.
triggerWords:
  - clawhub download
  - download tracker
  - download monitoring
  - clawhub stats
metadata:
  openclaw:
    requires:
      bins: [python3, clawhub]
    tags:
      [
        clawhub,
        download-tracker,
        monitoring,
        skill-analytics,
        clawhub-tracker,
      ]
    permissions:
      file:
        read:
          [
            "~/.openclaw/workspace/data/clawhub-tracker/**",
          ]
        write: ["~/.openclaw/workspace/data/clawhub-tracker/**"]
      exec:
        scripts: ["*.py", "*.sh"]
      network:
        domains:
          [
            "open.feishu.cn",
          ]
---

## Overview

A CLI tool that fetches official download counts for skills published on ClawHub, stores history in local CSV, and pushes snapshots/reports via Feishu.

**Use when:** User wants to monitor their ClawHub skill downloads, set up automated tracking, or generate trend reports.

**Do NOT use for:** Real-time analytics (this is periodic snapshots, not streaming), other registries (only ClawHub), individual user analytics (skill-level only).

## Quick Commands

```bash
# Snapshot (collect + Feishu push)
python3 ~/.openclaw/workspace/skills/clawhub-download-tracker/clawhub_tracker.py

# Reports
python3 .../clawhub_tracker.py report daily
python3 .../clawhub_tracker.py report weekly
python3 .../clawhub_tracker.py report monthly

# Manage monitor list
python3 .../clawhub_tracker.py add <slug> [note]
python3 .../clawhub_tracker.py remove <slug>
python3 .../clawhub_tracker.py list
```

## Workflow

### Snapshot collection

```
1. Load skills.csv (managed by add/remove)
2. For each slug: clawhub inspect <slug> --json → extract stats.downloads
3. Compare to last_state.json
4. If delta ≠ 0 → append to checklog.csv + update last_state
5. Build summary text
6. Archive to reports/YYYY-MM.md
7. Push to Feishu (if configured)
```

### Report generation

```
1. Read checklog.csv (only delta ≠ 0 records)
2. Filter by date range (last 1d / 7d / month-to-date)
3. Build report with: per-skill start→end, cumulative delta, peak time, total
4. Print + archive + Feishu push
```

### Add/remove skills

```
add <slug>     → append to skills.csv (auto-create with header if missing)
remove <slug>  → remove from skills.csv (historical checklog preserved)
list           → show monitor list with last known download counts
```

## Prerequisites

- `clawhub` CLI installed (auto-detected via `shutil.which` with fallback to `/opt/homebrew/bin/clawhub`)
- Python 3 (built-in on macOS)
- Feishu credentials (only needed for push notifications):
  - `CLAWHUB_FEISHU_APP_ID`
  - `CLAWHUB_FEISHU_APP_SECRET`
  - `CLAWHUB_FEISHU_USER_OPEN_ID`

  Configure via env vars or `~/.openclaw/workspace/data/clawhub-tracker/.env`

## Storage Strategy

- `checklog.csv` — only records with `delta ≠ 0` (sparse, keeps file small)
- `last_state.json` — latest snapshot per slug (avoids re-scanning checklog on each run)
- `reports/YYYY-MM.md` — monthly archive of all outputs
- `tracker.log` — run history with errors
- File locking via `fcntl.flock` — safe under concurrent launchd triggers

## Data Files

```
~/.openclaw/workspace/data/clawhub-tracker/
├── skills.csv         # slug,note
├── checklog.csv       # timestamp,slug,downloads,delta
├── last_state.json    # {slug: {downloads, ts}}
├── reports/           # YYYY-MM.md archives
├── tracker.log        # Run logs
└── .tracker.lock      # File lock (transient)
```

## Data Source

Fetches official `stats.downloads` via `clawhub inspect <slug> --json`. Direct from ClawHub registry — **no third-party APIs**.

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Slug not found in ClawHub | Mark as fetch failed, skip |
| Invalid slug format | Reject (regex validation, prevents injection) |
| Missing .env | Skip Feishu push, continue with local files |
| Empty skills.csv | Send "no skills to monitor" notice to Feishu, exit |
| Concurrent runs | Second instance detects lock, exits gracefully |
| checklog missing (e.g. migration) | Fall back to last_state.json for delta |

## See Also

- `README.md` — full user-facing docs (installation, launchd setup, security)
- `README.zh.md` — Chinese version
- `test_clawhub_tracker.py` — test suite
