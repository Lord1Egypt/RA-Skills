---
name: tophant-clawvault-openclaw-alerts
version: 0.1.0
description: Push high-risk ClawVault security events and daily security reports through OpenClaw agent messaging
homepage: https://github.com/tophant-ai/ClawVault
user-invocable: true
disable-model-invocation: false
---

# ClawVault OpenClaw Alerts

Send high-risk ClawVault security events and daily security reports through OpenClaw agent messaging.

This skill is operational only: it reads the existing ClawVault dashboard REST API, stores local notification state under `~/.ClawVault/openclaw-alerts/`, and sends messages with `openclaw agent`. It does not modify ClawVault proxy, file monitor, plugin, or detection behavior.

## How to Run

Always execute the bundled Python script:

```bash
python3 SKILL_DIR/clawvault_openclaw_alerts.py <command> [options]
```

Add `--json` to commands that support machine-readable output.

## Quick Start

```bash
# Configure delivery through an OpenClaw agent
python3 SKILL_DIR/clawvault_openclaw_alerts.py configure --agent main --session-id clawvault-alerts --json

# Verify OpenClaw delivery
python3 SKILL_DIR/clawvault_openclaw_alerts.py send-test --json

# Send new high-risk events once
python3 SKILL_DIR/clawvault_openclaw_alerts.py run-once --json

# Send today's security report now
python3 SKILL_DIR/clawvault_openclaw_alerts.py daily-report --json

# Start/stop background monitoring
python3 SKILL_DIR/clawvault_openclaw_alerts.py start --json
python3 SKILL_DIR/clawvault_openclaw_alerts.py status --json
python3 SKILL_DIR/clawvault_openclaw_alerts.py stop --json
```

## Commands

### /tophant-clawvault-openclaw-alerts configure

Create or update `~/.ClawVault/openclaw-alerts/config.yaml`.

```bash
/tophant-clawvault-openclaw-alerts configure --agent main --session-id clawvault-alerts
/tophant-clawvault-openclaw-alerts configure --dashboard-url http://127.0.0.1:8766 --risk-threshold 7.0 --daily-time 09:00
/tophant-clawvault-openclaw-alerts configure --deliver --channel slack --reply-to '#security-alerts'
```

### /tophant-clawvault-openclaw-alerts send-test

Send a test message through the configured OpenClaw agent.

```bash
/tophant-clawvault-openclaw-alerts send-test
/tophant-clawvault-openclaw-alerts send-test --message "ClawVault alert test"
```

### /tophant-clawvault-openclaw-alerts run-once

Poll `/api/scan-history` once, send eligible high-risk events, and update deduplication state.

```bash
/tophant-clawvault-openclaw-alerts run-once
/tophant-clawvault-openclaw-alerts run-once --dry-run
```

### /tophant-clawvault-openclaw-alerts daily-report

Generate and send a daily security report.

```bash
/tophant-clawvault-openclaw-alerts daily-report
/tophant-clawvault-openclaw-alerts daily-report --dry-run
/tophant-clawvault-openclaw-alerts daily-report --date 2026-05-28
```

### /tophant-clawvault-openclaw-alerts start

Start background monitoring. The daemon polls ClawVault for new high-risk events and sends the daily report when the configured local time is reached.

```bash
/tophant-clawvault-openclaw-alerts start
/tophant-clawvault-openclaw-alerts start --foreground
```

### /tophant-clawvault-openclaw-alerts stop

Stop background monitoring.

```bash
/tophant-clawvault-openclaw-alerts stop
/tophant-clawvault-openclaw-alerts stop --force
```

### /tophant-clawvault-openclaw-alerts status

Show daemon, dashboard, OpenClaw, and state status.

```bash
/tophant-clawvault-openclaw-alerts status
```

## Data Sources

- `GET /api/scan-history?limit=200` for realtime high-risk events.
- `GET /api/summary`, `/api/budget`, `/api/monitor/overview`, `/api/local-scan/history`, and `/api/file-monitor/alerts` for daily reports.

## Security Defaults

Notifications are intentionally terse and redacted. By default, this skill does not include raw prompts, input previews, complete file paths, command text, secrets, API keys, private keys, or database URLs. See `SECURITY.md` before enabling optional verbose fields.
