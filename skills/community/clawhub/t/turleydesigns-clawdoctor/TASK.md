# AgentWatch — Phase 0 Build Task

## What You're Building

AgentWatch: a self-healing monitor for OpenClaw. npm CLI package that monitors gateway, crons, and sessions, sends Telegram alerts, and auto-fixes what it can.

## Project Setup

- **Directory:** `/home/coder/agentwatch`
- **Package name:** `agentwatch` (available on npm, confirmed)
- **Language:** Node.js (TypeScript compiled to JS)
- **Target:** npm global install (`npm install -g agentwatch`)

## Architecture

### CLI Commands

```bash
agentwatch init      # Interactive setup: detect OpenClaw, configure alerts
agentwatch start     # Start monitoring daemon (foreground or systemd)
agentwatch stop      # Stop daemon
agentwatch status    # Show current health of all monitors
agentwatch log       # Show recent events from local SQLite
agentwatch version   # Show version
```

### `agentwatch init` Flow

1. Auto-detect OpenClaw install path (`~/.openclaw/`)
2. Verify gateway is installed (`which openclaw`)
3. Ask for Telegram bot token + chat ID for alerts
4. Ask for alert preferences (what to monitor, auto-fix on/off)
5. Write config to `~/.agentwatch/config.json`
6. Create SQLite DB at `~/.agentwatch/events.db`
7. Offer to install systemd service

### Watchers (all read-only, OpenClaw-specific)

1. **GatewayWatcher** — checks if `openclaw gateway` process is running
   - Method: check for PID file or `pgrep -f "openclaw"` or systemd status
   - Interval: every 30 seconds
   - On failure: trigger ProcessHealer

2. **CronWatcher** — monitors OpenClaw cron execution
   - Reads: `~/.openclaw/state/cron-*.json` files for last-run timestamps
   - Detects: crons that should have run but didn't, crons that errored
   - Interval: every 60 seconds

3. **SessionWatcher** — monitors agent session health
   - Reads: `~/.openclaw/agents/*/sessions/*.jsonl` (newest files only)
   - Detects: sessions with errors, aborted sessions, sessions that ran too long
   - Interval: every 60 seconds

4. **AuthWatcher** — detects auth failures in logs
   - Reads: gateway logs (stdout/systemd journal)
   - Pattern matches: 401, 403, "token expired", "auth failed", "unauthorized"
   - Interval: every 60 seconds

5. **CostWatcher** — detects cost anomalies
   - Reads: session JSONL files for token counts / cost metadata
   - Detects: session cost > 3x rolling average (last 20 sessions)
   - Interval: every 5 minutes

### Healers (auto-fix, Phase 0 green-tier only)

1. **ProcessHealer** — restarts gateway
   - Action: `openclaw gateway restart` (or `systemctl restart openclaw-gateway`)
   - Verify: check process is running after 10s
   - Alert: always notify on restart (success or failure)

2. **CronHealer** — retries failed cron
   - Action: log the failure + suggest manual rerun command in alert
   - Phase 0 does NOT auto-rerun crons (too risky without understanding the cron)
   - Alert: include cron name, last run time, error if available

### Alerter

**TelegramAlerter** — sends alerts via Telegram Bot API
- Uses bot token + chat ID from config
- Rate limit: max 1 alert per monitor per 5 minutes (prevent spam)
- Format:
  ```
  🔴 AgentWatch Alert
  Monitor: GatewayWatcher
  Event: Gateway process not found
  Action: Restarted via openclaw gateway restart
  Status: ✅ Back online
  ─────
  Time: 2026-03-15 03:14 UTC
  Host: devbox
  ```
- For info/recovered events, use 🟢 instead of 🔴

### EventStore

- SQLite database at `~/.agentwatch/events.db`
- Schema:
  ```sql
  CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    watcher TEXT NOT NULL,
    severity TEXT NOT NULL,  -- info, warning, error, critical
    event_type TEXT NOT NULL,
    message TEXT NOT NULL,
    details TEXT,  -- JSON blob
    action_taken TEXT,
    action_result TEXT,
    created_at TEXT DEFAULT (datetime('now'))
  );
  ```
- `agentwatch log` reads from this
- Retain 7 days by default (configurable)

### Config File (`~/.agentwatch/config.json`)

```json
{
  "openclawPath": "/root/.openclaw",
  "watchers": {
    "gateway": { "enabled": true, "interval": 30 },
    "cron": { "enabled": true, "interval": 60 },
    "session": { "enabled": true, "interval": 60 },
    "auth": { "enabled": true, "interval": 60 },
    "cost": { "enabled": true, "interval": 300 }
  },
  "healers": {
    "processRestart": { "enabled": true },
    "cronRetry": { "enabled": false }
  },
  "alerts": {
    "telegram": {
      "enabled": true,
      "botToken": "...",
      "chatId": "..."
    }
  },
  "dryRun": false,
  "retentionDays": 7
}
```

### Daemon

- `agentwatch start` runs the daemon in foreground (can be backgrounded with &)
- On start: run all watchers once immediately, then on interval
- Graceful shutdown on SIGTERM/SIGINT
- PID file at `~/.agentwatch/agentwatch.pid`
- Optional: `agentwatch install-service` creates a systemd unit file

## File Structure

```
agentwatch/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts          # CLI entry point (commander.js)
│   ├── config.ts         # Config loading/saving
│   ├── daemon.ts         # Main daemon loop
│   ├── watchers/
│   │   ├── base.ts       # BaseWatcher abstract class
│   │   ├── gateway.ts    # GatewayWatcher
│   │   ├── cron.ts       # CronWatcher
│   │   ├── session.ts    # SessionWatcher
│   │   ├── auth.ts       # AuthWatcher
│   │   └── cost.ts       # CostWatcher
│   ├── healers/
│   │   ├── base.ts       # BaseHealer abstract class
│   │   ├── process.ts    # ProcessHealer
│   │   └── cron.ts       # CronHealer
│   ├── alerters/
│   │   └── telegram.ts   # TelegramAlerter
│   ├── store.ts          # SQLite EventStore
│   └── utils.ts          # Shared utilities
├── README.md
└── .gitignore
```

## Dependencies

Keep minimal:
- `commander` — CLI framework
- `better-sqlite3` — SQLite (no async needed, simpler)
- `node-fetch` or built-in fetch — Telegram API calls

Do NOT use: express, fastify, or any web framework. This is a CLI tool, not a server.

## Key Constraints

1. **OpenClaw-specific.** All paths assume `~/.openclaw/` structure. No abstraction for other frameworks.
2. **No cloud/API in Phase 0.** Everything is local. No external API calls except Telegram alerts.
3. **No root required.** Should work running as the same user that runs OpenClaw.
4. **Minimal dependencies.** Keep the npm package small and fast to install.
5. **TypeScript compiled to JS.** Ship compiled JS in npm package.
6. **Must work on Linux.** macOS nice-to-have but not required for Phase 0.

## Testing

Write basic tests for:
- Config validation
- Event store CRUD
- Each watcher's detection logic (mock file system)
- Telegram alert formatting
- Rate limiting logic

Use Node's built-in test runner (`node:test`) or vitest. Keep it simple.

## README.md

Write a solid README with:
- One-line description
- Install command
- Quick start (init → start)
- What it monitors (list)
- What it fixes (list)
- Configuration reference
- "Built by people who run 20+ OpenClaw agents in production"

## What NOT to Build

- Landing page (I'll handle this separately)
- Stripe/billing integration (Phase 1)
- Cloud dashboard (Phase 1)
- Multi-framework support (Phase 3)
- Docker support (not needed yet)

## Quality Bar

- Clean TypeScript, no `any` types
- All watchers tested
- `agentwatch init` works end-to-end
- `agentwatch start` runs stable for 10+ minutes without crash
- `agentwatch status` shows meaningful output
- README is good enough to ship
