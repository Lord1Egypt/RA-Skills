---
name: clawdoctor
description: Self-healing doctor for OpenClaw. Monitors gateway, crons, sessions, auth, and costs. Sends Telegram alerts. Auto-restarts gateway when it goes down. Use when you want proactive health monitoring with automatic recovery for your OpenClaw setup.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["clawdoctor"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "clawdoctor",
              "bins": ["clawdoctor"],
              "label": "Install ClawDoctor (npm)",
            },
          ],
      },
  }
---

# ClawDoctor - Self-Healing Doctor for OpenClaw

Monitors your OpenClaw setup and fixes problems before you notice them.

Built for people running OpenClaw in production who got tired of checking if things were still alive.

**npm:** `clawdoctor` | **Version:** 0.2.0 | **License:** MIT

## What It Monitors

| Monitor | What It Watches | Interval |
|---------|-----------------|----------|
| GatewayWatcher | `openclaw` process running | 30s |
| CronWatcher | `~/.openclaw/state/cron-*.json` for missed/failed crons | 60s |
| SessionWatcher | `~/.openclaw/agents/*/sessions/*.jsonl` for errors, aborts, stuck sessions | 60s |
| AuthWatcher | Gateway logs for 401/403/token expired patterns | 60s |
| CostWatcher | Session token costs - flags if >3x rolling average | 5m |

## What It Fixes

| Healer | Action |
|--------|--------|
| ProcessHealer | Restarts gateway via `openclaw gateway restart`, then verifies recovery |
| CronHealer | Logs the failure and includes the manual rerun command in the alert |

## Install

```bash
npm install -g clawdoctor
clawdoctor init
clawdoctor start
```

## When to Use

- You run OpenClaw in production
- You have cron jobs that sometimes fail silently
- You want Telegram alerts when something breaks
- You want the gateway to auto-restart if it goes down

## Commands

```bash
clawdoctor init              # Interactive setup (detects OpenClaw, configures Telegram)
clawdoctor start             # Start monitoring daemon
clawdoctor start --dry-run   # Run without taking healing actions
clawdoctor stop              # Stop daemon
clawdoctor status            # Show current health of all monitors
clawdoctor log               # Show recent events
clawdoctor log -n 100        # Show 100 events
clawdoctor log -w GatewayWatcher -s critical  # Filter by watcher/severity
clawdoctor install-service   # Install as systemd user service
```

## Non-Interactive Setup (for agents)

```bash
clawdoctor init \
  --openclaw-path ~/.openclaw \
  --telegram-token TOKEN \
  --telegram-chat CHATID \
  --auto-fix \
  --no-prompt
```

## Sample Alert

```
Alert: GatewayWatcher
Event: Gateway process not found
Action: openclaw gateway restart
Status: Back online
Time: 2026-03-15 03:14 UTC
Host: devbox
```

Alerts are rate-limited to max 1 per monitor per 5 minutes to avoid spam.

## Configuration

Config lives at `~/.clawdoctor/config.json`. Events stored in `~/.clawdoctor/events.db` (SQLite, 7-day retention).

## Pricing

- **Diagnose** ($9/mo): Monitoring + Telegram alerts
  https://buy.stripe.com/7sY14g2fsex33F08U51ck01
- **Heal** ($19/mo): Everything in Diagnose + auto-healing actions
  https://buy.stripe.com/eVq28k2fsdsZ7Vg6LX1ck02

## Security

- Reads OpenClaw log/state files (read-only)
- Only action taken: `openclaw gateway restart` when gateway is down
- Sends alerts via Telegram Bot API (outbound HTTPS only)
- No data sent to external servers in free tier
- No API keys or conversation content leaves the machine

## More Info

https://clawdoctor.dev
