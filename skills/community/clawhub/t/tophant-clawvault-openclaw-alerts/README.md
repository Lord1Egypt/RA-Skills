# ClawVault OpenClaw Alerts Skill

Push high-risk ClawVault security events and daily security reports through OpenClaw agent messaging.

The skill reads ClawVault's existing dashboard REST API and sends notifications through `openclaw agent`, so any communication channels already connected to the target OpenClaw agent can receive the message through OpenClaw's normal delivery path.

## Prerequisites

- ClawVault installed and dashboard running on `http://127.0.0.1:8766`
- OpenClaw installed
- At least one OpenClaw agent configured, usually `main`

## Installation

**From local repo:**

```bash
cp -r skills/tophant-clawvault-openclaw-alerts ~/.openclaw/skills/
openclaw restart
```

## Quick Start

```bash
# Configure OpenClaw delivery
/tophant-clawvault-openclaw-alerts configure --agent main --session-id clawvault-alerts

# Optional: ask OpenClaw to deliver through a configured communication channel
/tophant-clawvault-openclaw-alerts configure --deliver --channel slack --reply-to '#security-alerts'

# Send a test notification
/tophant-clawvault-openclaw-alerts send-test

# Send eligible high-risk events once
/tophant-clawvault-openclaw-alerts run-once

# Send today's report immediately
/tophant-clawvault-openclaw-alerts daily-report

# Run continuously
/tophant-clawvault-openclaw-alerts start
/tophant-clawvault-openclaw-alerts status
/tophant-clawvault-openclaw-alerts stop
```

## Commands

| Category | Commands |
|---|---|
| **Configuration** | `configure`, `status` |
| **Delivery test** | `send-test` |
| **Realtime alerts** | `run-once`, `start`, `stop` |
| **Daily report** | `daily-report` |

7 commands total. See [SKILL.md](./SKILL.md) for complete reference with examples.

## Configuration

The skill stores configuration and state in `~/.ClawVault/openclaw-alerts/`:

- `config.yaml` - dashboard URL, OpenClaw agent/session, thresholds, and schedule
- `state.json` - deduplication keys, rate-limit windows, last report date, and daemon heartbeat
- `daemon.pid` - background process id
- `alerts.log` - daemon stdout/stderr

Defaults are privacy-first: raw prompt previews, full file paths, and command text are not sent.

## Event Filtering

Realtime alerts are sent for events from `/api/scan-history` when any configured high-risk condition matches:

- `threat_level` is `high` or `critical`
- `max_risk_score` is at least `7.0`
- `action` is `block`, `ask_user`, or `sanitize`

The skill deduplicates events and applies per-minute/per-hour rate limits to prevent notification storms.

## Daily Reports

Daily reports combine:

- ClawVault summary and budget
- Dashboard monitor overview
- Recent high-risk events
- Local scan history
- File monitor alerts

Reports are redacted and intended as a short operational summary, not a raw log export.

## Support

- **Repository:** https://github.com/tophant-ai/ClawVault
- **Issues:** https://github.com/tophant-ai/ClawVault/issues

## License

MIT © 2026 Tophant SPAI Lab
