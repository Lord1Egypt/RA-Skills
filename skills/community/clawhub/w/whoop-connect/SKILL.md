---
name: whoop-connect
description: "Connect WHOOP wearable to OpenClaw — fetch and store recovery, sleep, HRV, strain, and workout data locally. Use when: user asks about recovery, sleep quality, HRV, heart rate, strain, workout stats, or any WHOOP data. NOT for: Apple Health, Oura, Garmin, or other non-WHOOP devices."
user-invocable: true
metadata: {"openclaw":{"emoji":"💚","homepage":"https://github.com/Belugary/whoop-connect","requires":{"bins":["python3"],"env":["WHOOP_CLIENT_ID","WHOOP_CLIENT_SECRET"]},"primaryEnv":"WHOOP_CLIENT_ID","install":[{"kind":"uv","package":"requests flask"}]}}
---

# whoop-connect

Connect your WHOOP band to OpenClaw so your agent can fetch your recovery, sleep, HRV, strain, and workout data.

Setup (once)

WHOOP does not have a public API. To access your own data, you need to register a personal developer app (free, takes 5 minutes). This gives you OAuth credentials so the skill can read your data on your behalf. All data stays local in `~/.whoop/whoop.db` — nothing is uploaded anywhere.

- Register at https://developer.whoop.com (sign in with your WHOOP account, create an app, get Client ID and Client Secret). Full walkthrough: `{baseDir}/references/setup-guide.md`
- Set env vars: `WHOOP_CLIENT_ID`, `WHOOP_CLIENT_SECRET`
- First invocation auto-creates config and runs OAuth

**When env vars are missing**, explain to the user: "WHOOP requires a free developer account to access your data via API. It takes about 5 minutes — I can walk you through it step by step." Then follow `{baseDir}/references/setup-guide.md`.

If config missing: `python3 {baseDir}/scripts/setup.py --init`, then ask user's language and `python3 {baseDir}/scripts/setup.py --set language=zh` (or `en`).
If token missing: `python3 {baseDir}/scripts/whoop_client.py auth`.
If deps missing: `bash {baseDir}/scripts/install.sh`.

Common commands

- Today's recovery: `python3 {baseDir}/scripts/whoop_client.py recovery --days 1`
- Last night's sleep: `python3 {baseDir}/scripts/whoop_client.py sleep --days 1`
- Recent workouts: `python3 {baseDir}/scripts/whoop_client.py workout --days 7`
- Weekly strain: `python3 {baseDir}/scripts/whoop_client.py cycle --days 7`
- Multi-day summary: `python3 {baseDir}/scripts/whoop_client.py trends --days 7`
- Single metric history: `python3 {baseDir}/scripts/db.py trends --metric <name> --days N`
- Profile: `python3 {baseDir}/scripts/whoop_client.py profile`
- Body measurements: `python3 {baseDir}/scripts/whoop_client.py body`
- Force sync: `python3 {baseDir}/scripts/daily_sync.py --days 2`
- Start auto-sync daemon: `python3 {baseDir}/scripts/auto_sync.py`
- Single sync check: `python3 {baseDir}/scripts/auto_sync.py --once`
- Auto-sync with custom interval: `python3 {baseDir}/scripts/auto_sync.py --interval 10`

Use `--json` for raw data when combining multiple queries. Use `--days N` to match user's time range ("this week" = 7, "this month" = 30).

Available metrics: `recovery_score`, `hrv`, `resting_hr`, `spo2`, `skin_temp`, `strain`, `sleep_duration`, `sleep_efficiency`, `sleep_performance`, `respiratory_rate`

Settings

- Change setting: `python3 {baseDir}/scripts/setup.py --set <key>=<value>`
- Show config: `python3 {baseDir}/scripts/setup.py --show`
- Re-run wizard: `python3 {baseDir}/scripts/setup.py`

Keys: `language` (en/zh), `detail_level` (compact/detailed), `units` (metric/imperial), `push_recovery`, `push_sleep`, `push_workout`, `webhook_enabled` (bool), `webhook_port` (int), `sync_interval` (int, minutes — polling interval when webhook is off, default 5), `sync_interval_webhook` (int, minutes — fallback interval when webhook is on, default 20), `daily_api_limit` (int, default 10000)

Users may change settings in natural language (e.g. "switch to Chinese", "use detailed mode"). Map to `--set` accordingly.

Auto-sync

The skill supports automatic data syncing with adaptive intervals:

- **No webhook**: polls WHOOP API every `sync_interval` minutes (default 5) as the primary data source
- **Webhook enabled**: webhook delivers real-time events; auto-sync polls every `sync_interval_webhook` minutes (default 20) as fallback
- **Dedup**: only new, scored records trigger notifications; already-seen data is silently skipped
- **API guard**: tracks daily API calls and pauses when `daily_api_limit` (default 10,000) is reached
- Start daemon: `python3 {baseDir}/scripts/auto_sync.py`
- Single check: `python3 {baseDir}/scripts/auto_sync.py --once`

Webhook (optional)

For real-time push, set up webhooks — see `{baseDir}/references/setup-guide.md` § "Optional: Webhook Setup". Set `webhook_enabled=true` in config. The webhook server writes a heartbeat file so auto-sync can detect if webhook is healthy and reduce polling frequency automatically.

Notes

- Never fabricate health data. If a command returns empty or errors, say so.
- Never expose WHOOP_CLIENT_ID, WHOOP_CLIENT_SECRET, or token contents in output.
- Never delete DB files or config without explicit user confirmation.
- Confirm before changing user settings.
- Respect `language` and `detail_level` from config.
- If WHOOP API returns 429, the client auto-retries. Do not flood.

Troubleshooting

- `ModuleNotFoundError`: `bash {baseDir}/scripts/install.sh`
- `WHOOP_CLIENT_ID must be set`: check env vars
- `No refresh token`: `python3 {baseDir}/scripts/whoop_client.py auth`
- `401 Unauthorized`: re-authorize with `auth`
- `500 Server Error`: transient WHOOP-side issue, retry in a few minutes
- Empty results: widen `--days`; data may not be scored yet

References

- `{baseDir}/references/setup-guide.md` — New user onboarding + webhook setup
- `{baseDir}/references/api-reference.md` — WHOOP API v2 field documentation
- `{baseDir}/references/webhook-events.md` — Webhook event types and payload format
- WHOOP Developer Docs: https://developer.whoop.com/docs/developing/user-data/recovery
- WHOOP API Reference: https://developer.whoop.com/api
