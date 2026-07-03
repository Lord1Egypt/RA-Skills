# ClawHub Download Tracker

Track download counts for your ClawHub-published skills. Automatically logs trends, detects changes, and pushes notifications via Feishu. Supports daily, weekly, and monthly reports.

## Why This Tool?

If you publish skills on ClawHub, you want to know:
- How many downloads am I getting?
- Is it growing or stalling?
- Which skill is performing best?

This tracker answers all three with **zero dependencies beyond Python stdlib** — no databases, no third-party analytics, no cloud sync.

## Features

- 📊 **Snapshot Collection** — fetches current download counts via `clawhub inspect`
- 📈 **Trend Tracking** — records deltas in CSV for historical analysis
- ⏰ **Scheduled Reports** — daily, weekly, monthly summaries with per-slug breakdowns
- 💬 **Feishu Push** — automatic notifications on collection and report generation
- 🔒 **File Locking** — safe under launchd/cron high-frequency triggers
- ➕ **CLI Management** — `add` / `remove` / `list` subcommands, no manual CSV editing

## Quick Start

### 1. Install

```bash
clawhub install clawhub-download-tracker
```

### 2. Configure Feishu (optional, only for push notifications)

Create `~/.openclaw/workspace/data/clawhub-tracker/.env`:

```
CLAWHUB_FEISHU_APP_ID=cli_xxx
CLAWHUB_FEISHU_APP_SECRET=your_secret
CLAWHUB_FEISHU_USER_OPEN_ID=ou_xxx
```

Without these, the tracker still works — it just won't push to Feishu.

### 3. Add a skill to monitor

```bash
python3 ~/.openclaw/workspace/skills/clawhub-download-tracker/clawhub_tracker.py add my-skill "My Skill Display Name"
```

### 4. Run a snapshot

```bash
python3 ~/.openclaw/workspace/skills/clawhub-download-tracker/clawhub_tracker.py
```

Output:
```
📊 ClawHub · 07/01 17:41
──────────────────────────────
  simple-ledger: 1008 dl ·
  model-throughput-tester: 262 dl ·
  skill-download-tracker: 154 dl ·
──────────────────────────────
3 skills · 1424 total · 0 changed
```

### 5. Generate reports

```bash
clawhub_tracker.py report daily     # Today
clawhub_tracker.py report weekly    # Last 7 days
clawhub_tracker.py report monthly   # Current month
```

## All Commands

| Command | Description |
|---------|-------------|
| `clawhub_tracker.py` | Collect snapshot + Feishu push |
| `clawhub_tracker.py report daily` | Daily report |
| `clawhub_tracker.py report weekly` | Weekly report (last 7 days) |
| `clawhub_tracker.py report monthly` | Monthly report (current month) |
| `clawhub_tracker.py add <slug> [note]` | Add skill to monitor |
| `clawhub_tracker.py remove <slug>` | Remove from monitor (history preserved) |
| `clawhub_tracker.py list` | List monitored skills with current downloads |

## Scheduling with launchd

A wrapper script `clawhub_tracker.sh` sets up PATH for the cron/launchd environment. Example plist (`~/Library/LaunchAgents/com.you.clawhub-tracker.plist`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.you.clawhub-tracker</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/you/.openclaw/workspace/skills/clawhub-download-tracker/clawhub_tracker.sh</string>
    </array>
    <key>StartInterval</key><integer>3600</integer>
    <key>RunAtLoad</key><true/>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.you.clawhub-tracker.plist
```

## File Structure

```
~/.openclaw/workspace/skills/clawhub-download-tracker/
├── SKILL.md                  # Agent trigger & execution guide
├── README.md                 # This file (user-facing)
├── README.zh.md              # Chinese version
├── clawhub_tracker.py        # Main script: collection + report + Feishu push
├── clawhub_tracker.sh        # launchd wrapper (sets PATH)
└── test_clawhub_tracker.py   # Tests

~/.openclaw/workspace/data/clawhub-tracker/
├── skills.csv                # Monitored skills (managed via add/remove)
├── checklog.csv              # History (only delta ≠ 0 records)
├── last_state.json           # Latest snapshot per slug
├── reports/                  # Monthly report archive
└── tracker.log               # Run logs
```

## Data Source

All download counts come directly from the ClawHub registry via `clawhub inspect <slug> --json`. **No third-party analytics or scraping.**

## Security

- **No hardcoded credentials** — Feishu tokens read from env vars or `.env` file
- **Slug validation** — input slugs validated against injection patterns before subprocess execution
- **File locking** — `fcntl.flock` prevents concurrent writes under launchd high-frequency triggers
- **Atomic writes** — `last_state.json` written via temp file + rename
- **Local-only data** — CSV logs and reports stay under `~/.openclaw/workspace/data/clawhub-tracker/`
- **Network access** — only contacts `open.feishu.cn` (Feishu push) and ClawHub registry (download stats)

## Testing

```bash
python3 test_clawhub_tracker.py
```

Tests cover: core collection, report generation, file locking, slug validation, credential handling, CSV I/O edge cases.

## License

MIT-0 (free to use, modify, redistribute, no attribution required)

## Links

- ClawHub: https://clawhub.com/skills/clawhub-download-tracker
- Issues: https://github.com/openclaw/clawhub/issues
