---
name: clawdoctor
description: Self-healing monitor for OpenClaw gateways, crons, and agent sessions. Use when you need to watch if OpenClaw is running, get Telegram alerts on failures, auto-restart the gateway, detect missed crons or stuck sessions, or monitor token costs. Install with `npm install -g clawdoctor`.
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

# ClawDoctor

Self-healing monitor for OpenClaw. Watches your gateway, crons, and agent sessions, sends Telegram alerts, and auto-fixes what it can.

**Site:** https://clawdoctor.dev  
**npm:** https://www.npmjs.com/package/clawdoctor  
**GitHub:** https://github.com/turleydesigns/clawdoctor

## Install

```bash
npm install -g clawdoctor
```

## Quick Start

```bash
# Interactive setup (Telegram bot token, chat ID, plan key)
clawdoctor init

# Start monitoring daemon
clawdoctor start

# Check health of all monitors
clawdoctor status
```

## Commands

```bash
clawdoctor init              # Interactive setup
clawdoctor start             # Start monitoring daemon
clawdoctor start --dry-run   # Run without taking healing actions
clawdoctor stop              # Stop daemon
clawdoctor status            # Live health check of all monitors
clawdoctor log               # Show recent events from local database
clawdoctor log -n 100        # Show last 100 events
clawdoctor log -w GatewayWatcher -s critical  # Filter by watcher/severity
clawdoctor install-service   # Install as systemd user service
```

## What It Monitors

| Monitor | What It Watches | Interval |
|---------|-----------------|----------|
| **GatewayWatcher** | `openclaw` process running | 30s |
| **CronWatcher** | `~/.openclaw/state/cron-*.json` for missed/failed crons | 60s |
| **SessionWatcher** | Agent session files for errors, aborts, stuck sessions | 60s |
| **AuthWatcher** | Gateway logs for 401/403/token expired patterns | 60s |
| **CostWatcher** | Session token costs — flags if >3x rolling average | 5m |

## What It Fixes

| Healer | Action |
|--------|--------|
| **ProcessHealer** | Restarts gateway via systemctl or `openclaw gateway restart`, then verifies |
| **CronHealer** | Logs failure and includes manual rerun command in the alert |

## Pricing

| Tier | Price | Monitors | History | Auto-fix | Alerts |
|------|-------|----------|---------|----------|--------|
| **Watch** | Free | 5 | 7 days | ✗ | Local only |
| **Diagnose** | $9/mo | 20 | 30 days | ✗ | ✅ Telegram |
| **Heal** | $19/mo | Unlimited | 90 days | ✅ | ✅ Telegram |

- **Buy Diagnose ($9/mo):** https://buy.stripe.com/7sY14g2fsex33F08U51ck01
- **Buy Heal ($19/mo):** https://buy.stripe.com/eVq28k2fsdsZ7Vg6LX1ck02

## Alerts

Telegram alerts with rate limiting (max 1 per monitor per 5 minutes):

```
🔴 ClawDoctor Alert
Monitor: GatewayWatcher
Severity: critical
Message: openclaw process not found
```

## Notes

- Config stored at `~/.clawdoctor/config.json`
- Events stored in SQLite at `~/.clawdoctor/events.db`
- Free tier: 5 monitors, local alerts only, no auto-fix
- Paid tiers activated via license key from https://clawdoctor.dev
