# ClawDoctor

Self-healing monitor for OpenClaw. Watches your gateway, crons, sessions, auth, and budget — sends Telegram alerts and auto-fixes what it can.

Built for people running OpenClaw in production who got tired of checking if things were still alive.

**Homepage:** https://clawdoctor.dev | **Source:** https://github.com/turleydesigns/clawdoctor

## Install

```bash
npm install -g clawdoctor
```

Requires Node 18+, Linux.

## Quick Start

```bash
# Configure (interactive)
clawdoctor init

# Start monitoring daemon
clawdoctor start
```

## Commands

```bash
clawdoctor init                               # Interactive setup
clawdoctor start                              # Start monitoring daemon
clawdoctor start --dry-run                    # Run without taking healing actions
clawdoctor stop                               # Stop daemon
clawdoctor status                             # Live health check of all monitors
clawdoctor log                                # Show recent events
clawdoctor log -n 100                         # Show 100 events
clawdoctor log -w GatewayWatcher -s critical  # Filter by watcher/severity
clawdoctor install-service                    # Install as systemd user service
clawdoctor plan                               # Show current plan and features
clawdoctor activate <key>                     # Activate a license key
clawdoctor snapshots                          # List healer action snapshots (rollback points)
clawdoctor audit                              # Show healer audit trail
```

## What It Monitors

| Monitor | What It Watches | Interval |
|---------|-----------------|----------|
| **GatewayWatcher** | OpenClaw gateway process running | 30s |
| **CronWatcher** | Cron jobs for failures and overdue runs | 60s |
| **SessionWatcher** | Agent sessions for errors, aborts, stuck sessions | 60s |
| **AuthWatcher** | Auth token expiry (warns at 24h, 4h, 1h) | 60s |
| **BudgetWatcher** | Daily API spend vs configured limit | 5m |
| **CostWatcher** | Per-session token costs vs rolling average | 5m |

## What It Fixes

| Healer | Trigger | Action |
|--------|---------|--------|
| **ProcessHealer** | Gateway down | Restarts via `openclaw gateway restart`, verifies recovery |
| **CronHealer** | Cron failing repeatedly | Logs failure with manual rerun command |
| **SessionHealer** | Session stuck >2h | Kills session; alerts first if cost >$10 |
| **AuthHealer** | Auth failures detected | Attempts `openclaw auth refresh`; alerts if fails |
| **BudgetHealer** | Daily spend exceeded | Requests approval: kill sessions, increase limit, or ignore |

All healing actions are logged with a snapshot for rollback. Risky actions require Telegram approval before executing.

## Alerts

Telegram alerts, rate-limited to max 1 per monitor per 5 minutes:

```
🔴 ClawDoctor Alert
Monitor: GatewayWatcher
Event: Gateway process not found
Action: openclaw gateway restart
Status: Back online
─────
Time: 2026-03-15 03:14 UTC
Host: devbox
```

## Configuration

Config lives at `~/.clawdoctor/config.json`:

```json
{
  "openclawPath": "/root/.openclaw",
  "watchers": {
    "gateway": { "enabled": true, "interval": 30 },
    "cron": { "enabled": true, "interval": 60 },
    "session": { "enabled": true, "interval": 60 },
    "auth": { "enabled": true, "interval": 60 },
    "budget": { "enabled": true, "interval": 300 },
    "cost": { "enabled": true, "interval": 300 }
  },
  "healers": {
    "processRestart": { "enabled": true },
    "cronRetry": { "enabled": false },
    "sessionKill": { "enabled": true },
    "authRefresh": { "enabled": true }
  },
  "alerts": {
    "telegram": {
      "enabled": true,
      "botToken": "your-bot-token",
      "chatId": "your-chat-id"
    }
  },
  "dryRun": false,
  "retentionDays": 7
}
```

Events stored in `~/.clawdoctor/events.db` (SQLite, 7-day retention by default).

## Systemd

```bash
clawdoctor install-service
systemctl --user daemon-reload
systemctl --user enable clawdoctor
systemctl --user start clawdoctor
```

## Non-Interactive Setup

```bash
clawdoctor init \
  --openclaw-path ~/.openclaw \
  --telegram-token TOKEN \
  --telegram-chat CHATID \
  --auto-fix \
  --no-prompt
```

## Plans

| Feature | Free | Diagnose ($9/mo) | Heal ($19/mo) |
|---------|------|-----------------|--------------|
| Monitors | 5 | Up to 20 | Unlimited |
| Event history | 7 days | 30 days | 90 days |
| Alerts | Local only | Telegram, Slack, Discord | Everything in Diagnose |
| Smart alerts with root cause | - | Yes | Yes |
| Known-issue pattern matching | - | Yes | Yes |
| Auto-fix (restart, retry) | - | - | Yes |
| Approval flow for risky fixes | - | - | Yes |
| Full audit trail and rollback | - | - | Yes |

Get a license key at https://clawdoctor.dev, then:

```bash
clawdoctor activate <your-key>
```

Or set via env:

```bash
export CLAWDOCTOR_KEY=your-key
```

## License

MIT
