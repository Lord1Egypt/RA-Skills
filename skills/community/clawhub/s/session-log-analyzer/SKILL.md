---
name: session-log-analyzer
description: Analyze agent session logs and generate PDF reports with Notion sync
version: 1.2.0
author: ClawdBot
tags: [logs, analysis, pdf, notion]
requires_bins: [python3]
requires_env: [NOTION_API_KEY, NOTION_REPORTS_DB_ID]
requires_config: []
changelog:
  - version: 1.2.0
    date: 2026-05-07
    changes: "修复日志分析报告生成和Notion同步问题"
  - version: 1.1.0
    date: 2026-05-07
    changes: "修复日志分析报告生成和Notion同步问题"
  - version: 1.0.0
    date: 2026-04-01
    changes: "Initial release"
---

# Session Log Analyzer

Analyze agent session logs and generate PDF reports with optional Notion sync.

## Features

- Parse JSONL session logs and compute statistics
- Generate PDF analysis reports with skill usage breakdown and error summaries
- Sync generated reports to a Notion database

## Usage

### Generate Report

```bash
PYTHONPATH=./lib python3 scripts/analyze_logs.py
```

### Sync to Notion

Set environment variables first:

```bash
export NOTION_API_KEY="your-integration-token"
export NOTION_REPORTS_DB_ID="your-database-id"
PYTHONPATH=./lib python3 scripts/sync_to_notion.py
```

## Report Contents

- Total sessions count
- Skill invocation statistics (success/failure rates)
- Duration totals
- Per-skill usage breakdown
- Recent errors listing

## Configuration

| Variable | Required | Description |
|---|---|---|
| `NOTION_API_KEY` | For sync | Notion integration token |
| `NOTION_REPORTS_DB_ID` | For sync | Target Notion database ID |

## Notes

- Input logs must be in JSONL format with `event`, `session_id`, `skill_used`, `success`, and `duration` fields
- PDF output is saved to `pdfs/session_analysis_report.pdf`
- Notion sync uploads the first 2000 characters of extracted report text