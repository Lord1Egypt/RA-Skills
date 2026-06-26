# WHOOP → AI Health Reports 🏋️

[中文文档 / Chinese](README_CN.md)

Turn your WHOOP data into daily AI health reports. 5 steps, 10 minutes.

## How It Works

```
WHOOP band → WHOOP API → Markdown files → AI reads & reports
```

Your AI agent syncs recovery, sleep, strain, and workout data daily, then sends you a plain-language health briefing.

## Quick Start

### Step 1: Install the skill

```bash
# OpenClaw users
clawhub install whoop

# Or manual
git clone https://github.com/aikong-cmd/whoop-openclaw.git
cp -r whoop-openclaw ~/.openclaw/workspace/skills/whoop
```

### Step 2: Create a WHOOP Developer App

Go to **https://developer-dashboard.whoop.com** → Create Application:

| Field | Value |
|-------|-------|
| Name | Anything (e.g. "AI Health Sync") |
| Redirect URI | `http://localhost:9527/callback` |
| Scopes | ✅ All `read:*` + `offline` |

Save your **Client ID** and **Client Secret**.

### Step 3: Set credentials

```bash
export WHOOP_CLIENT_ID="your-client-id"
export WHOOP_CLIENT_SECRET="your-client-secret"
```

### Step 4: Authorize (one-time)

**If you have a browser on the same machine:**

```bash
cd ~/.openclaw/workspace/skills/whoop
python3 scripts/auth.py
# Opens browser → log in → authorize → done ✅
```

**If running on a remote server (no browser):**

```bash
python3 scripts/auth.py --print-url
# 1. Open the printed URL in your local browser
# 2. Log in to WHOOP and authorize
# 3. Browser redirects to a page that won't load (normal!)
# 4. Copy the FULL URL from the address bar, then:
python3 scripts/auth.py --callback-url "paste-the-full-url-here"
```

You'll see `✅ Tokens saved`. This only needs to be done once — tokens auto-refresh forever.

### Step 5: Sync your data

```bash
python3 scripts/sync.py           # Today
python3 scripts/sync.py --days 7  # Last 7 days
python3 scripts/sync.py --weekly  # Weekly summary
```

Output goes to `~/.openclaw/workspace/health/whoop-YYYY-MM-DD.md`

**That's it.** Your AI agent can now read these files and answer health questions.

---

## Optional: Daily Auto-Reports

Set up a cron job so your AI sends you a health briefing every morning:

```bash
openclaw cron add \
  --name whoop-daily \
  --schedule "30 10 * * *" \
  --timezone Asia/Shanghai \
  --task "Run: python3 ~/.openclaw/workspace/skills/whoop/scripts/sync.py --days 2. Read the latest health file and send me a report with insights."
```

> ⏰ 10:30 AM recommended — WHOOP finalizes sleep data after you wake up.

## Sample Output

```markdown
# WHOOP — 2026-03-09

## Recovery 🟢
- Recovery Score: 66%
- HRV: 41.4 ms | Resting HR: 62 bpm
- SpO2: 96.3% | Skin Temp: 33.7°C

## Sleep 🟡
- Performance: 61% | In Bed: 5h47m
- Deep 1h25m | REM 1h38m | Light 2h08m | Awake 35m
- Sleep Need: 9h41m → Deficit: 4h29m

## Strain
- Day Strain: 0.1 / 21.0 | Calories: 534 kcal

## Workouts
- Walking · 16m · Strain 4.9 · Avg HR 114 bpm
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `No tokens found` | Run Step 4 (auth.py) |
| `Token refresh failed` | Re-run auth.py |
| `No data for date` | WHOOP needs time after waking; try later |
| Port 9527 in use | `kill $(lsof -ti:9527)` then retry |

## Requirements

- Python 3.10+ and curl (pre-installed on most systems)
- WHOOP membership with an active band

## License

MIT
