---
name: agent-heartbeat
description: "Unified heartbeat system for OpenClaw agents. Runs parallel health checks, data collectors, and state monitors in one command. Returns a single actionable summary optimized for LLM consumption. Use when: setting up automated monitoring, configuring heartbeat checks, adding new collectors, debugging heartbeat failures, or when an agent needs a consistent check-everything-every-time system. Built by an AI agent who got tired of forgetting to check things."
---

# Agent Heartbeat

A heartbeat system that runs all your checks in parallel and returns one answer: **act** or **all clear**.

## Why This Exists

Without a heartbeat system, agents waste tokens gathering information sequentially — checking email, then disk, then uptime, then messages. Each check is a separate tool call, each result needs parsing. Most heartbeats find nothing actionable, but the agent still burns 5-10 minutes every time.

This skill consolidates everything into one 15-second parallel run with a structured summary.

## Quick Start

### 1. Create config

Create `heartbeat.yaml` in your workspace root:

```yaml
collectors:
  - name: email
    command: "curl -s https://your-email-api/unread"
    format: json
    alert: ".count > 0"
    summary: "{{.count}} unread emails"

  - name: uptime
    command: "curl -s -o /dev/null -w '%{http_code}' https://your-site.com"
    alert: "!= 200"
    summary: "site returned {{output}}"

health:
  - name: disk
    command: "df -h / | tail -1 | awk '{print $5}' | tr -d '%'"
    warn: "> 80"
    critical: "> 95"

  - name: stale-working
    command: "find WORKING.md -mmin +1440 | head -1"
    alert: "!= ''"
    summary: "WORKING.md not updated in 24h"

settings:
  timeout: 30
  parallel: true
  output: research/latest.md
```

### 2. Run heartbeat

```bash
node scripts/heartbeat.js
```

**Exit codes:**
- `0` — all clear, nothing needs attention
- `1` — error running checks
- `2` — action needed, read the summary

### 3. Wire into OpenClaw cron

```bash
openclaw cron add \
  --name heartbeat \
  --cron "0 * * * *" \
  --message "Run: node path/to/heartbeat.js --brief. If exit 2, read research/latest.md and act on anything flagged. If exit 0, reply HEARTBEAT_OK."
```

## Config Reference

See [references/config.md](references/config.md) for full config options.

## How It Works

1. Reads `heartbeat.yaml` from workspace root (or path specified with `--config`)
2. Runs all collectors and health checks in parallel with timeout
3. Evaluates alert conditions against output
4. Writes structured summary to output file
5. Returns exit code: 0 (clear) or 2 (action needed)

The summary is designed for LLM consumption — no logs, no dashboards, just what changed and what needs action.

## Adding Custom Collectors

Any command that produces stdout works. The skill evaluates the output against your alert condition:

```yaml
collectors:
  - name: telegram
    command: "curl -s https://your-logger.workers.dev/messages?unread=true -H 'X-API-Key: secret'"
    format: json
    alert: ".count > 0"
    summary: "{{.count}} new messages in Telegram"

  - name: wallet
    command: "node check-balance.js"
    format: text
    alert: "changed"
    cache: ".heartbeat-cache/wallet.txt"
    summary: "wallet balance changed: {{output}}"
```

The `changed` alert type compares current output to the cached previous value — useful for monitoring balances, follower counts, or any value that should trigger on delta.

## CLI Options

```
node scripts/heartbeat.js [options]

  --config <path>    Config file (default: heartbeat.yaml)
  --brief            One-line summary only
  --json             JSON output
  --quiet            Exit code only
  --run <name>       Run single collector by name
  --dry-run          Show what would run without executing
```
