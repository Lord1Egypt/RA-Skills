---
name: screen-reviewer
description: >-
  Monitor computer activities via periodic screenshots, extract text with OCR,
  and generate daily review reports with ROI analysis. Use when the user asks
  about screen monitoring, daily review, time tracking, productivity analysis,
  activity logging, or 复盘.
---

# Screen Reviewer — 电脑行为复盘助手

自动截图 → 结构化日志 → AI 每日复盘报告。

## File Locations

- **Scripts**: `scripts/` (relative to this skill directory)
- **Data**: `~/.screen-reviewer/` (screenshots, logs, reports, config)
- **Config**: `~/.screen-reviewer/config.yaml`
- **Reports**: `~/.screen-reviewer/reports/YYYY-MM-DD-review.md`
- **Venv Python**: `~/.screen-reviewer/venv/bin/python`

## Quick Reference

All commands use `service_manager.py`. Use venv Python to run:

```bash
VENV=~/.screen-reviewer/venv/bin/python
SCRIPTS=<this-skill-dir>/scripts

$VENV $SCRIPTS/service_manager.py start        # Start capture daemon
$VENV $SCRIPTS/service_manager.py stop         # Stop daemon
$VENV $SCRIPTS/service_manager.py status       # Check status + today's stats
$VENV $SCRIPTS/service_manager.py pause        # Pause (daemon stays alive)
$VENV $SCRIPTS/service_manager.py resume       # Resume capturing
$VENV $SCRIPTS/service_manager.py report               # Yesterday's report
$VENV $SCRIPTS/service_manager.py report 2026-03-22     # Specific date
$VENV $SCRIPTS/service_manager.py cleanup      # Delete screenshots > 3 days
$VENV $SCRIPTS/service_manager.py install      # Install macOS auto-start
$VENV $SCRIPTS/service_manager.py uninstall    # Remove auto-start
```

## Setup (first time)

Run from the repo root:

```bash
bash install.sh
```

After setup, grant **Screen Recording** and **Accessibility** permissions:
System Settings → Privacy & Security → Screen Recording → enable Terminal/Python.

## Configuration

Edit `~/.screen-reviewer/config.yaml`:

| Key | Default | Description |
|-----|---------|-------------|
| `capture.interval_seconds` | 5 | Screenshot interval |
| `capture.smart_detect` | true | Skip unchanged frames |
| `capture.change_threshold` | 5 | Min % pixel change to keep frame |
| `capture.jpeg_quality` | 60 | JPEG quality (lower = smaller files) |
| `privacy.blacklist_apps` | [1Password, ...] | Apps to skip |
| `ocr.enabled` | true | Enable text extraction |
| `report.ai_provider` | openai | openai / claude / ollama |
| `report.ai_model` | gpt-4o-mini | Model name |
| `report.api_key_env` | OPENAI_API_KEY | Env var holding the API key |
| `report.generation_hour` | 8 | Auto-report time (with launchd) |
| `cleanup.keep_days` | 3 | Days to keep screenshots |
| `categories.*` | see config | App → value-tier mapping for ROI |

## How It Works

1. **Capture loop** (every 5s): screenshot → detect change → get window info → OCR → JSONL log
2. **Daily report** (8 AM or on-demand): aggregate logs → classify apps → AI generates Markdown report
3. **Cleanup** (with report): delete screenshot dirs older than 3 days

## Log Format

Each line in `~/.screen-reviewer/logs/YYYY-MM-DD.jsonl`:

```json
{"timestamp":"2026-03-22T14:30:05","app":"Cursor","window_title":"capture_daemon.py","screenshot":"screenshots/2026-03-22/14-30-05.jpg","ocr_text":"def main():..."}
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| No screenshots | Grant Screen Recording permission |
| No window titles | Grant Accessibility permission |
| OCR returns empty | Re-run `bash install.sh` to recompile Swift tool |
| Report fails | Set AI API key: `export OPENAI_API_KEY=sk-...` |
| Daemon won't start | Check `~/.screen-reviewer/logs/daemon_stderr.log` |

## When User Asks To...

- **Start monitoring**: Run `service_manager.py start`
- **See today's activity**: Run `service_manager.py status`, then read today's log
- **Generate review**: Run `service_manager.py report [date]`
- **Change settings**: Edit `~/.screen-reviewer/config.yaml`
- **Add app to blacklist**: Append to `privacy.blacklist_apps` in config
- **Check disk usage**: `du -sh ~/.screen-reviewer/screenshots/`
