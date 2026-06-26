# Token Burn Monitor

Real-time token consumption monitoring dashboard for [OpenClaw](https://openclaw.ai) agents.

You're running agents 24/7. They're burning tokens across models, sessions, cron jobs. But how much? Which agent is the money pit? Which prompt costs 10x more than it should? This skill gives you a live dashboard to answer all of that.

![Node.js](https://img.shields.io/badge/Node.js-18%2B-339933?logo=node.js&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue)
![Version](https://img.shields.io/badge/version-5.3.0-brightgreen)

## What You Get

- **Per-agent cost breakdown** — see exactly how much each agent burns daily, split by model (Claude, GPT, Gemini, MiniMax, etc.)
- **Per-call drill-down** — expand any agent to see individual API calls: what tools were called, token split (input/output/cache read/cache write/reasoning), and cost. User prompts are redacted by default for privacy (opt-in via config)
- **Cache efficiency tracking** — cache hit rate per agent, so you know if your context caching is actually saving money
- **30-day cost history** — daily bar chart with per-agent stacking, spot trends and anomalies at a glance
- **Cron job health** — all scheduled jobs, their last run status, duration, consecutive errors, and next run time
- **Model pricing table** — built-in pricing for Anthropic, OpenAI, Google, MiniMax, with custom overrides
- **Swappable themes** — don't like the default dark UI? Drop your own `index.html` in `themes/` and go
- **Zero dependencies** — pure Node.js, no `npm install`, no build step

## Install

### One-click install via ClawHub

Tell your Claw:

```
Install the token-burn-monitor skill from ClawHub and start it.
```

Or run manually:

```bash
npx clawhub install token-burn-monitor
```

### Via skills.sh

```bash
npx skills add KasparChen/burn-monitor-skill
```

### Via GitHub (manual)

```bash
git clone https://github.com/KasparChen/burn-monitor-skill.git
cd burn-monitor-skill
bash start.sh
```

## Quick Start

Once installed, the dashboard runs on **http://localhost:3847** by default.

```bash
bash start.sh            # Start (default port 3847)
bash start.sh status     # Check if running
bash start.sh restart    # Restart after config change
bash start.sh stop       # Stop
```

## Customization Guide

Everything below can be done by telling your Claw in natural language. Copy-paste the prompts directly.

### Change the port

> **Prompt:** `The token-burn-monitor is conflicting with another service on port 3847. Change it to port 4200 and restart.`

Or set the `PORT` env var: `PORT=4200 bash start.sh`

### Give your agents display names and icons

By default, agents are auto-discovered from your agents directory. But they show up as raw IDs like `main`, `klaw`. To customize:

> **Prompt:** `Open the token-burn-monitor config.json. Set the display name for agent "main" to "Karl" and "klaw" to "Klaw the Builder". Then restart the dashboard.`

The resulting config:

```json
{
  "agents": {
    "main": { "name": "Karl", "icon": "/assets/karl.png" },
    "klaw": { "name": "Klaw the Builder", "icon": null }
  }
}
```

### Add pricing for a custom model

The dashboard ships with pricing for Claude Opus/Sonnet, GPT-4o, Gemini, MiniMax. If you use a model that's not listed, costs will show as estimates.

> **Prompt:** `Add model pricing for "deepseek/deepseek-chat" to the token-burn-monitor config: input $0.32, output $0.89, cache read $0.16, cache write $0.32 per 1M tokens, provider is DeepSeek. Restart after.`

```json
{
  "modelPricing": {
    "deepseek/deepseek-chat": {
      "input": 0.32,
      "output": 0.89,
      "cacheRead": 0.16,
      "cacheWrite": 0.32,
      "provider": "DeepSeek"
    }
  }
}
```

### Create a custom theme

The default theme is a dark dashboard. If you want something different — minimal, retro, neon, whatever:

> **Prompt:** `Read the API.md file in the token-burn-monitor skill, then create a new theme called "minimal" — a clean white theme with just the essentials: total cost, per-agent table, and the 30-day chart. Put it in themes/minimal/index.html and switch the config to use it.`

Your Claw will read the API contract, build the HTML, and switch the config for you.

### Show user prompts in per-call breakdown

User prompts are **redacted by default** — the API returns `"[redacted]"` for all prompt fields. To see what triggered each API call (useful for debugging expensive prompts), explicitly opt in:

> **Prompt:** `In the token-burn-monitor config.json, set "showPrompts" to true and restart the dashboard.`

**Privacy note:** When enabled, up to 300 characters of each user prompt will be visible in the dashboard. Only enable this on a trusted machine where you are the sole user.

### Point to a different agents directory

If your agents aren't in the default location:

> **Prompt:** `Set the OPENCLAW_AGENTS_DIR environment variable to /path/to/my/agents and restart the token-burn-monitor.`

## Architecture

```
server.js              Core API server (stable, don't touch)
themes/default/        Default dark dashboard theme
themes/<custom>/       Your custom themes go here
API.md                 Full API contract (7 endpoints, all JSON)
config.default.json    Default config template
config.json            Your config (create from default, gitignored)
start.sh               Service management (start/stop/restart/status)
setup.sh               Post-install info
```

## API

All endpoints return JSON. API only accepts requests from localhost. Full reference in [API.md](./API.md).

| Endpoint | Returns |
|---|---|
| `GET /api/config` | Agent names and icons |
| `GET /api/stats?date=YYYY-MM-DD` | All agents aggregated for a date (defaults to today) |
| `GET /api/agent/:id?date=YYYY-MM-DD` | Single agent detail with per-call message breakdown |
| `GET /api/history?days=N` | Daily cost history for last N days (default 30) |
| `GET /api/pricing` | Full model pricing table |
| `GET /api/crons` | All scheduled cron jobs grouped by agent |
| `GET /api/cron/:jobId/runs` | Run history for a specific cron job |

## Security

- **Localhost only** — server binds to `127.0.0.1`, only accessible from the local machine
- **No shell execution** — zero `child_process` usage; all data read from filesystem
- **No outbound network** — default theme uses system fonts, makes zero external requests
- **No CORS** — no cross-origin headers are set; API is same-origin only
- **GET-only** — all non-GET requests are rejected with 405
- **Prompts redacted** — user prompts show as `[redacted]` by default, explicit opt-in required
- **CSP enforced** — HTML responses include `Content-Security-Policy` with `connect-src 'self'` and `font-src 'self'`
- **Path traversal guard** — theme static file serving is sandboxed to the theme directory
- **Imports** — `server.js` only imports `http`, `fs`, `path` from Node.js stdlib

## Troubleshooting

| Problem | Fix |
|---|---|
| No data showing | Verify `OPENCLAW_AGENTS_DIR` points to correct agents directory |
| Port conflict | `PORT=4000 bash start.sh` or set `"port"` in config.json |
| Theme not loading | Check `themes/<name>/index.html` exists |
| Wrong cost numbers | Add correct model pricing to `config.json` → `modelPricing` |
| Agents missing | They're auto-discovered. Check if the agent directory has session files |
| Prompts showing [redacted] | Set `"showPrompts": true` in config.json and restart |

## Links

- **ClawHub:** `npx clawhub install token-burn-monitor`
- **GitHub:** [KasparChen/burn-monitor-skill](https://github.com/KasparChen/burn-monitor-skill)
- **skills.sh:** `npx skills add KasparChen/burn-monitor-skill`

## License

MIT
