# ClawHub Download Tracker

Track download counts for your ClawHub-published skills. Automatically logs trends, detects changes, and pushes notifications via Feishu. Supports daily, weekly, and monthly reports.

## Features

- **Snapshot Collection**: Fetch current download counts for all monitored skills via `clawhub inspect`
- **Trend Tracking**: Records deltas between checks in CSV for historical analysis
- **Scheduled Reports**: Daily, weekly, and monthly summaries with per-slug breakdowns
- **Feishu Push**: Automatic notifications on collection and report generation
- **Lightweight**: No database — pure CSV files, no third-party API dependencies

## Prerequisites

- `clawhub` CLI installed (auto-detected via `shutil.which` with fallback)
- Python 3 (built-in on macOS)
- Feishu credentials (required for push notifications):

  Configure via environment variables or `.env` file:

  | Variable | Description |
  |----------|-------------|
  | `CLAWHUB_FEISHU_APP_ID` | Feishu app ID |
  | `CLAWHUB_FEISHU_APP_SECRET` | Feishu app secret |
  | `CLAWHUB_FEISHU_USER_OPEN_ID` | Target user Open ID |

  Create `~/.openclaw/workspace/data/clawhub-tracker/.env`:
  ```
  CLAWHUB_FEISHU_APP_ID=cli_xxx
  CLAWHUB_FEISHU_APP_SECRET=your_secret
  CLAWHUB_FEISHU_USER_OPEN_ID=ou_xxx
  ```

## File Structure

```
~/.openclaw/workspace/skills/clawhub-download-tracker/
├── SKILL.md                  # Agent trigger & execution guide
├── README.md                 # This file
├── README.zh.md              # Chinese version
├── clawhub_tracker.py        # Main script: collection + report + Feishu push
├── clawhub_tracker.sh        # launchd wrapper (sets PATH)
└── test_clawhub_tracker.py   # Tests (mock data, 26 test cases)

~/.openclaw/workspace/data/clawhub-tracker/
├── skills.csv                # Monitored skills: slug,note
├── checklog.csv              # History: timestamp,slug,downloads,delta
└── reports/                  # Report archive (monthly .md files)
```

## Usage

### 1. Collect Downloads (Snapshot + Feishu Push)

```bash
python3 ~/.openclaw/workspace/skills/clawhub-download-tracker/clawhub_tracker.py
```

Iterates all slugs in `skills.csv`, fetches latest download counts, computes deltas, writes to `checklog.csv`, archives to `reports/`, and sends Feishu notifications.

### 2. Reports

```bash
python3 ~/.openclaw/workspace/skills/clawhub-download-tracker/clawhub_tracker.py report daily   # Today
python3 ~/.openclaw/workspace/skills/clawhub-download-tracker/clawhub_tracker.py report weekly  # Last 7 days
python3 ~/.openclaw/workspace/skills/clawhub-download-tracker/clawhub_tracker.py report monthly # Current month
```

Generates reports from `checklog.csv` history, including:
- Per-slug start → end download counts and cumulative deltas
- Sample count and peak time windows
- Total new downloads and current totals

Reports are printed to stdout, archived to `reports/YYYY-MM.md`, and pushed to Feishu.

### 3. Add / Remove Monitored Skills

Edit `~/.openclaw/workspace/data/clawhub-tracker/skills.csv` directly. Format: `slug,note`

## Data Source

Fetches the official `stats.downloads` field via `clawhub inspect <slug> --json`. Data comes directly from the ClawHub registry — **no third-party APIs involved**.

## Security

- **No hardcoded credentials**: Feishu tokens read from environment variables or `.env` file only
- **Slug validation**: Input slugs are validated against injection patterns before subprocess execution
- **Local data only**: All CSV logs and reports stored locally under `~/.openclaw/workspace/data/clawhub-tracker/`
- **Network access**: Only contacts `open.feishu.cn` for push notifications and ClawHub registry for download stats

## Testing

```bash
python3 ~/.openclaw/workspace/skills/clawhub-download-tracker/test_clawhub_tracker.py
```

26 test cases covering core functionality and security edge cases (slug injection, empty dates, missing credentials, hardcoded credential detection).

## License

MIT-0
