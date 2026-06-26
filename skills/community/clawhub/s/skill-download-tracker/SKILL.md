---
name: clawhub-download-tracker
description: Monitor download counts for your ClawHub-published skills. Track changes over time with automated alerts.
triggerWords:
  - clawhub download
  - download tracker
  - download monitoring
  - download report
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

Track download counts for skills published on ClawHub. This tool fetches official stats via `clawhub inspect <slug> --json`, stores history in local CSV, and supports scheduled checks, daily/weekly/monthly reports with Feishu push notifications.

## File Structure

```
~/.openclaw/workspace/skills/clawhub-download-tracker/
├── SKILL.md                  # This file
├── clawhub_tracker.py        # Main script: collection + report + Feishu
├── clawhub_tracker.sh        # launchd wrapper (sets PATH)
└── test_clawhub_tracker.py   # Tests (mock data, 19 test cases)

~/.openclaw/workspace/data/clawhub-tracker/
├── skills.csv                # Monitored skills: slug,note
├── checklog.csv              # History: timestamp,slug,downloads,delta
└── reports/                  # Report archive (monthly .md files)
```

## Prerequisites

- `clawhub` CLI installed (auto-detected via `shutil.which` with fallbacks)
- Python 3 (built-in on macOS)
- Feishu 凭证（**必须配置**，无硬编码 fallback）：
  - `CLAWHUB_FEISHU_APP_ID`
  - `CLAWHUB_FEISHU_APP_SECRET`
  - `CLAWHUB_FEISHU_USER_OPEN_ID`

  **配置方式（任选其一）：**
  1. 环境变量：`export CLAWHUB_FEISHU_APP_ID=cli_xxx`
  2. `.env` 文件：在 `~/.openclaw/workspace/data/clawhub-tracker/.env` 中写入 `KEY=VALUE` 格式

## Usage

### 1. Collect Current Downloads (Snapshot + Feishu Push)

```
python3 ~/.openclaw/workspace/skills/clawhub-download-tracker/clawhub_tracker.py
```

Iterates all slugs in `skills.csv`, fetches latest download counts, computes deltas, writes to `checklog.csv`, archives to `reports/`, and sends Feishu notifications.

### 2. Reports

```
python3 ~/.openclaw/workspace/skills/clawhub-download-tracker/clawhub_tracker.py report daily   # Today's report
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

The current monitor list is maintained dynamically in `~/.openclaw/workspace/data/clawhub-tracker/skills.csv`.
