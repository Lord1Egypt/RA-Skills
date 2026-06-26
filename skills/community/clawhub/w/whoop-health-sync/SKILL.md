---
name: whoop
description: Sync WHOOP health data (recovery, sleep, strain, workouts) to markdown files for AI-powered health insights. Use when user asks about WHOOP data, health metrics, recovery scores, sleep analysis, HRV, strain tracking, or wants daily health reports. Triggers on "WHOOP", "recovery score", "HRV", "sleep debt", "strain", "health sync", "健康数据", "恢复分数", "睡眠", "心率变异性".
---

# WHOOP Health Data Sync

Sync WHOOP wearable data to `health/whoop-YYYY-MM-DD.md` files. Pure Python, zero dependencies.

## Data Coverage

Recovery (score/HRV/RHR/SpO2/skin temp), Sleep (performance/efficiency/stages/respiratory rate/sleep need/balance), Day Strain (strain/calories/HR), Workouts (sport/duration/strain/HR/zones/distance), Weekly summaries.

## Setup

### 1. Create WHOOP Developer App

1. Go to https://developer-dashboard.whoop.com/
2. Create Application → Redirect URI: `http://localhost:9527/callback` → select all `read:*` + `offline` scopes
3. Note Client ID and Client Secret

### 2. Store Credentials

**Env vars:**
```bash
export WHOOP_CLIENT_ID="your-id"
export WHOOP_CLIENT_SECRET="your-secret"
```

**Or 1Password:** Create Login item named `whoop` (username=Client ID, password=Client Secret).

### 3. Authorize (one-time)

**Local (browser on same machine):**
```bash
python3 scripts/auth.py
```

**Remote server (headless):**
```bash
python3 scripts/auth.py --print-url
# User opens URL in browser, authorizes, copies callback URL back
python3 scripts/auth.py --callback-url "http://localhost:9527/callback?code=xxx&state=yyy"
```

Tokens auto-refresh via `offline` scope. Authorize once, runs forever.

## Usage

```bash
python3 scripts/sync.py              # Sync today
python3 scripts/sync.py --days 7     # Last 7 days
python3 scripts/sync.py --weekly     # Weekly summary
python3 scripts/sync.py --date 2026-03-07  # Specific date
```

Output: `~/.openclaw/workspace/health/whoop-YYYY-MM-DD.md`

## Cron (daily auto-sync)

```bash
openclaw cron add \
  --name whoop-daily \
  --schedule "0 10 * * *" \
  --timezone Asia/Shanghai \
  --task "Run: python3 ~/.openclaw/workspace/skills/whoop/scripts/sync.py --days 2. Then read the generated markdown files and send me the latest day's report."
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `No tokens found` | Run `auth.py` first |
| `Token refresh failed (403)` | Re-run `auth.py` to re-authorize |
| `error code: 1010` | Cloudflare block — uses curl to avoid. Check network |
| `No data for date` | WHOOP finalizes sleep after waking; try later |

## Agent Notes

- When user asks to re-authorize: run `auth.py --print-url`, send URL, wait for callback URL
- After authorization: verify with `sync.py --days 1`
- Token exchange uses `curl` to bypass Cloudflare blocking Python urllib
