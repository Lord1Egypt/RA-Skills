---
name: token-usage-optimizer
version: 1.0.5
description: Maximize your Claude Code subscription value with smart usage monitoring and burn rate optimization. Track 5-hour session and 7-day weekly quotas, get one-time alerts, and daily reports showing if you're under/over-using your $20-200/month plan. Ultra-lightweight (10min cache, minimal API calls). Perfect for Pro, Max 100, and Max 200 subscribers who want to get every dollar's worth.
metadata:
  clawdbot:
    emoji: "📊"
    os:
      - darwin
      - linux
    requires:
      bins:
        - curl
        - date
        - grep
---

# Token Usage Optimizer

**Version:** 1.0.5

**Get the most out of your Claude Code subscription** by monitoring usage in real-time and optimizing your daily burn rate.

## Why Use This?

You're paying $20-200/month for Claude Code. Are you:
- ✅ Using it to its full potential?
- ❌ Hitting limits too early?
- ❌ Leaving quota unused at reset?

This skill tracks your **5-hour session** and **7-day weekly** quotas, calculates your **daily burn rate**, and tells you if you should use more or throttle back.

## Features

- 📊 **Burn Rate Tracking** — Are you under/over/on-pace for optimal usage?
- ⚡ **Smart Alerts** — One-time warnings when SESSION > 50% (no spam)
- 🎯 **Plan-Aware** — Auto-detects Pro ($20), Max 100 ($100), Max 200 ($200)
- 💾 **Ultra-Lightweight** — 10-minute cache, minimal API calls
- 📅 **Daily Reports** — Evening summary: SESSION, WEEKLY, burn rate
- 🔄 **Token Health Check** — Hourly check + alert if manual refresh needed (~once per week)

## Quick Start

### 1. Setup

Run the setup wizard to configure your OAuth tokens:

```bash
cd {baseDir}
./scripts/setup.sh
```

You'll need:
- **Access Token** (`sk-ant-oat01-...`)
- **Refresh Token** (`sk-ant-ort01-...`)

See `references/token-extraction.md` for how to get these.

### 2. Check Usage

```bash
./scripts/check-usage.sh
```

Output:
```
SESSION=22.0
WEEKLY=49.0
BURN_RATE=OK
CACHED_AT=1771583780
```

### 3. Human-Readable Report

```bash
./scripts/report.sh
```

Output:
```
📊 Claude Code Daily Check:

⏱️  SESSION (5h): 22%
📅 WEEKLY (7d): 49%

⚪ На темпі — оптимальне використання
```

## Burn Rate Interpretation

- **🟢 UNDER** — You're under-using your subscription. Use more to get your money's worth!
- **⚪ OK** — On pace. Optimal usage for your plan.
- **🔴 OVER** — Over-burning. You'll hit limits before reset.

## Daily Budget by Plan

| Plan | Monthly | Weekly Budget | Daily Budget |
|------|---------|---------------|--------------|
| Pro | $20 | ~14% | ~2% |
| Max 100 | $100 | ~14% | ~2% |
| Max 200 | $200 | ~14% | ~2% |

*(7-day window resets weekly, so ~14% per day = 100% per week)*

## Integration with Heartbeat

Add to your `HEARTBEAT.md`:

```markdown
### Evening Check (18:00-20:00)
- Claude Code usage: `/path/to/token-usage-optimizer/scripts/report.sh`
```

## Alert Thresholds

- **SESSION > 50%** → 🟡 One-time warning (won't repeat until next reset)
- **WEEKLY > 80%** → 🟡 One-time warning

Alerts use state tracking (`/tmp/claude-usage-alert-state`) to avoid spam.

## Cache

Default: `/tmp/claude-usage.cache` with 10-minute TTL.

Override:
```bash
CACHE_FILE=/custom/path CACHE_TTL=300 ./scripts/check-usage.sh
```

## Files

- `scripts/setup.sh` — Initial token configuration
- `scripts/check-usage.sh` — Core usage checker (cached, burn rate calc)
- `scripts/report.sh` — Human-readable daily report
- `references/api-endpoint.md` — Anthropic OAuth API docs
- `references/token-extraction.md` — How to get OAuth tokens
- `references/plans.md` — Claude Code subscription tiers

## API Endpoint

```
GET https://api.anthropic.com/api/oauth/usage
Authorization: Bearer <access-token>
anthropic-beta: oauth-2025-04-20
```

Response:
```json
{
  "five_hour": {
    "utilization": 22.0,
    "resets_at": "2026-02-20T14:00:00.364238+00:00"
  },
  "seven_day": {
    "utilization": 49.0,
    "resets_at": "2026-02-24T10:00:01.364256+00:00"
  }
}
```

## Requirements

- `curl` — API requests
- `date` — Timestamp parsing
- `grep`, `cut`, `printf` — Text parsing

No external dependencies (jq, etc.).

## Privacy

Tokens are stored in `{baseDir}/.tokens` (gitignored).

Never share your access/refresh tokens.

## Token Health Check (Recommended)

OAuth tokens work for ~1 week, then need manual refresh. Set up 30-minute health check for better reliability:

```bash
# Add cron job to check token health every 30 minutes
openclaw cron add \
  --name "claude-token-refresh" \
  --every 30m \
  --announce \
  --message "Запусти {baseDir}/scripts/auto-refresh-cron.sh"
```

**What it does:**
- ✅ Token valid → silent (no spam)
- 🔴 Token expired → **one-time alert** with manual refresh instructions

**Manual refresh (once per week, 30 seconds):**
```bash
claude auth login
# Browser opens → sign in to claude.ai → done!
```

Tokens auto-sync to `{baseDir}/.tokens` after successful login.

## Troubleshooting

**"No token configured"**
→ Run `./scripts/setup.sh`

**"Token expired" / "API request failed"**
→ OAuth tokens expire after ~1 week
→ Manual refresh: `claude auth login` (browser opens → sign in → done)
→ Set up hourly health check to get alerts before expiry (see above)

**Burn rate shows empty**
→ API response missing `resets_at` — try again in a few minutes

**Auto-refresh failed**
→ OAuth refresh endpoint may have changed
→ Manual refresh: `claude auth login` → copy new tokens → run `./scripts/setup.sh`

## Changelog

### v1.0.5 (2026-02-22)
- 🐛 **Bugfix:** Fixed token extraction in `auto-refresh-cron.sh` (removed quotes handling)
- ⚡ **Performance:** Reduced cron interval from 1h to 30m for more reliable token refresh
- 📝 Improved reliability of OAuth token sync with `~/.claude/.credentials.json`

### v1.0.4 (2026-02-21)
- 🔄 Replaced automatic refresh with health check + manual refresh workflow
- 📚 Updated documentation with manual refresh instructions
- ⏰ Health check alerts when manual refresh needed (~once per week)

### v1.0.3 (2026-02-20)
- ⏱️ Fixed auto-refresh interval (hourly instead of 5h)
- 📊 Improved burn rate calculation accuracy

## Contributing

Found a bug or have a feature request?
→ Open an issue on ClawHub: https://clawhub.ai/friday/token-usage-optimizer

## License

MIT
