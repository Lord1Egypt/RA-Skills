# Agent Instructions — Screen Reviewer

Automated daily productivity review system: screenshots → structured logs → AI reports.

## Install

```bash
bash install.sh
```

Requires macOS 12+, Python 3.9+, Xcode Command Line Tools.
After install, grant Screen Recording + Accessibility permissions in System Settings.

## Commands

```bash
VENV=~/.screen-reviewer/venv/bin/python
SM=scripts/service_manager.py

$VENV $SM start              # Start capture daemon
$VENV $SM stop               # Stop daemon
$VENV $SM status             # Show status + today's stats
$VENV $SM pause              # Pause capturing
$VENV $SM resume             # Resume capturing
$VENV $SM report [YYYY-MM-DD]  # Generate review report (default: yesterday)
$VENV $SM cleanup [days]     # Clean old screenshots (default: 3 days)
$VENV $SM install            # Install macOS auto-start (launchd)
$VENV $SM uninstall          # Remove auto-start
```

## Key Paths

| What | Path |
|------|------|
| Config | `~/.screen-reviewer/config.yaml` |
| Daily logs | `~/.screen-reviewer/logs/YYYY-MM-DD.jsonl` |
| Reports | `~/.screen-reviewer/reports/YYYY-MM-DD-review.md` |
| Screenshots | `~/.screen-reviewer/screenshots/YYYY-MM-DD/` |
| Python venv | `~/.screen-reviewer/venv/` |
| Skill definition | `skill/SKILL.md` |

## Configuration

Edit `~/.screen-reviewer/config.yaml` to change:
- `capture.interval_seconds` — screenshot interval (default 5)
- `capture.smart_detect` — skip unchanged frames (default true)
- `privacy.blacklist_apps` — apps to never capture
- `report.ai_provider` — openai / claude / ollama
- `report.ai_model` — model name
- `report.api_key_env` — env var name holding the API key
- `cleanup.keep_days` — days to keep screenshots (default 3)
- `categories.*` — app-to-value mapping for ROI analysis
