---
name: session-log-analyzer
description: View and analyze session logs, generate PDF reports, and sync to Notion. Supports daily automated reporting via cron.
version: 1.2.1
author: gora050
tags: [logs, debugging, pdf, notion, reporting, automation]
license: MIT
metadata:
  openclaw:
    requires:
      bins: [python3]
      env: [NOTION_API_KEY, NOTION_REPORTS_DB_ID]
    install:
      - id: notion-client
        kind: pip
        package: notion-client
        label: "Install Notion SDK (pip)"
      - id: nano-pdf
        kind: skill
        package: nano-pdf
        label: "Install nano-pdf skill"
---

# Session Log Analyzer

Analyze agent session logs, generate PDF reports, and sync them to Notion — manually or on a daily schedule.

## Features

- **Log Analysis**: Parse JSONL session logs, compute statistics (session counts, skill invocations, success rates, errors)
- **PDF Report Generation**: Produce formatted PDF analysis reports via `nano-pdf`
- **Notion Sync**: Upload generated reports to a Notion database
- **Daily Automation**: Cron-driven pipeline that runs at 2:00 AM, generates a dated PDF, and syncs to Notion

## Quick Start

### Manual Analysis

```bash
cd scripts && python3 analyze_logs.py
```

### Manual Notion Sync

```bash
export NOTION_API_KEY="your-key"
export NOTION_REPORTS_DB_ID="your-db-id"
cd scripts && python3 sync_to_notion.py
```

### Daily Automated Report

The daily report pipeline is managed by `tmux_scripts/daily-log-report.sh`. It:

1. Runs `analyze_logs.py` to generate a dated PDF report
2. Syncs the PDF to Notion via `sync_to_notion.py`
3. Logs all output for debugging

To set up the cron schedule inside your tmux session:

```bash
# Add to crontab (runs at 2:00 AM daily)
(crontab -l 2>/dev/null; echo "0 2 * * * /root/.openclaw/workspace/tmux_scripts/daily-log-report.sh >> /root/.openclaw/workspace/pdfs/daily_report.log 2>&1") | crontab -
```

Or simply start the dev tmux session — the cron job is registered automatically:

```bash
./tmux_scripts/start_dev_session.sh
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `NOTION_API_KEY` | Yes (for Notion sync) | Notion integration API key |
| `NOTION_REPORTS_DB_ID` | Yes (for Notion sync) | Notion database ID for reports |

## File Structure

```
scripts/analyze_logs.py       — Log analysis & PDF generation
scripts/sync_to_notion.py     — Notion sync logic
tmux_scripts/daily-log-report.sh — Daily cron pipeline script
session_logs/                  — Raw JSONL session log files
pdfs/                          — Generated PDF reports
```

## Changelog

- **1.2.1** — 新增每日自动生成日志分析报告并同步至Notion的定时任务功能
- **1.1.0** — Added PDF report generation and Notion sync support
- **1.0.0** — Initial release — view and analyze session logs
