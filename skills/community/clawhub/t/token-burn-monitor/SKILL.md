---
name: token-burn-monitor
description: "Real-time token consumption monitoring dashboard for OpenClaw agents. Tracks per-agent token usage, cost breakdown by model, cache hit rates, cron job status, and 30-day historical trends. Use when setting up cost monitoring, checking daily token burn, or reviewing cron job health. User prompts are redacted by default."
env:
  OPENCLAW_AGENTS_DIR:
    description: "Path to OpenClaw agents directory"
    default: "/home/node/.openclaw/agents"
    required: false
  OPENCLAW_HOME:
    description: "Path to OpenClaw home directory (for cron data)"
    default: "/home/node/.openclaw"
    required: false
  PORT:
    description: "Server port"
    default: "3847"
    required: false
permissions:
  filesystem:
    read:
      - "$OPENCLAW_AGENTS_DIR/*/sessions/*.jsonl"
      - "$OPENCLAW_HOME/cron/jobs.json"
  network:
    listen: "127.0.0.1:$PORT"
    outbound: none
  shell: none
---

# Token Burn Monitor

Zero-dependency Node.js dashboard. Core API + swappable frontend themes.

## Architecture

```
server.js          → Core API (stable, don't modify)
themes/default/    → Default dark dashboard theme
themes/<custom>/   → User/agent-generated themes
API.md             → API contract for theme developers
config.json        → Port, theme, agents, pricing overrides
```

## Quick Start

```bash
bash start.sh            # Start (default port 3847)
bash start.sh status     # Check status
bash start.sh restart    # Restart after config change
bash start.sh stop       # Stop
```

## Configuration

Copy `config.default.json` to `config.json`:

```json
{
  "port": 3847,
  "theme": "default",
  "agents": {
    "main": { "name": "Karl", "icon": "/assets/karl.png" }
  },
  "modelPricing": {}
}
```

- **theme**: Directory name under `themes/`. Default: `"default"`
- **agents**: Display names/icons. Auto-discovered; config only overrides display.
- **port**: Also settable via `PORT` env var.
- **modelPricing**: Override/add model pricing ($/1M tokens).

Set `OPENCLAW_AGENTS_DIR` to override agent directory (default: `/home/node/.openclaw/agents`).

## Themes

Themes live in `themes/<name>/`. Minimum: one `index.html` that fetches data from the API.

To create a custom theme:
1. Read `API.md` for all available endpoints
2. Create `themes/my-theme/index.html`
3. Set `"theme": "my-theme"` in config.json
4. Restart

The default theme (`themes/default/`) is a full reference implementation.

## API Overview

All endpoints return JSON. GET-only. Server binds to localhost. Full docs in `API.md`.

| Endpoint | Description |
|---|---|
| `GET /api/config` | Agent names and icons |
| `GET /api/stats?date=` | All agents aggregated |
| `GET /api/agent/:id?date=` | Single agent with per-call breakdown |
| `GET /api/history?days=` | 30-day cost history |
| `GET /api/pricing` | Model pricing table |
| `GET /api/crons` | Scheduled jobs (read from filesystem) |
| `GET /api/cron/:id/runs` | Job run history |

## Security

- Server binds to `127.0.0.1` by default (localhost only)
- No shell execution — all data read from filesystem
- No outbound network requests — default theme uses system fonts
- User prompts redacted by default (`[redacted]`), opt-in via `showPrompts: true` in config
- HTML responses include CSP: `connect-src 'self'; font-src 'self'`
- GET-only — all other HTTP methods rejected

## Troubleshooting

- **No data**: Verify `OPENCLAW_AGENTS_DIR` points to correct agents directory.
- **Port conflict**: `PORT=4000 bash start.sh`
- **Theme not loading**: Check `themes/<name>/index.html` exists.
