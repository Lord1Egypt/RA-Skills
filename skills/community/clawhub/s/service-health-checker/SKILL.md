---
name: uptime-monitor
description: Monitor uptime of websites/services and alert when down. Use when checking if a website is reachable, monitoring service health, or getting alerted on downtime.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl"] },
        "install": [],
      },
  }
---

# Uptime Monitor

Monitor HTTP endpoints and alert when services go down.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MONITOR_URLS` | Yes | — | Comma-separated list of URLs to monitor |
| `ALERT_WEBHOOK_URL` | No | — | Webhook URL to send alerts (Discord, Slack, etc.) |
| `CHECK_INTERVAL` | No | `60` | Interval in seconds between checks |
| `ALERT_EMAIL` | No | — | Email address for alert notifications |

## Scripts

### check.sh — HTTP Health Check

Performs HTTP check with response time measurement.

```bash
./scripts/check.sh <url>
```

**Output:**
```
OK|https://example.com|200|245ms
FAIL|https://example.com|000|timeout
```

**Exit code:** 0 = up, 1 = down

### alert.sh — Send Alert

Sends alert via webhook or email when a service is down.

```bash
./scripts/alert.sh <url> <status_code> <response_time> <error_message>
```

### report.sh — Uptime Report

Generates a daily uptime summary from the log file.

```bash
./scripts/report.sh
```

**Output:** Markdown-formatted report with uptime % per URL.

## Usage Example

```bash
export MONITOR_URLS="https://example.com,https://api.example.com"
export ALERT_WEBHOOK_URL="https://discord.com/api/webhooks/..."
export CHECK_INTERVAL=60

# Run a single check
./scripts/check.sh https://example.com

# Generate report
./scripts/report.sh
```

## Notes

- Uses `curl` with a 10-second timeout for checks
- Logs results to `~/.openclaw/workspace/skills/uptime-monitor/logs/status.log`
- Alert webhook expects a JSON payload (compatible with Discord/Slack/PagerDuty)
