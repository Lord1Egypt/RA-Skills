# iOS exporter (Shortcuts) — Apple Health → Wellness Bridge

Goal: push a daily health aggregate from iPhone to the Wellness Bridge without installing an App.

Reality check:
- Shortcuts’ direct Health access varies by iOS version and installed actions.
- If some metrics cannot be read automatically, fall back to partial upload (e.g. steps + sleep duration only) or manual inputs.

## What users will do

1) In OpenClaw, start the bridge + tunnel and copy:
- Sync URL (tunnel host)
- Token

2) Create an iOS Shortcut named **"Wellness Sync"**.

3) Add actions:

### A) Inputs (one-time)
- Ask for Input (Text): **Sync URL** (e.g. `https://xxxxx.trycloudflare.com`)
- Ask for Input (Text): **Token**

Tip: for usability, store Sync URL + Token in iCloud Drive as a small JSON file and have the shortcut read it.

### B) Health reads (best-effort)
Add Health-related actions available on the user’s phone, for example:
- Get Health Sample (Steps) for Today → Sum
- Get Health Sample (Walking + Running Distance) for Today → Sum
- Get Sleep (or Health Sample: Sleep Analysis) for Today → Total duration
- Get Resting Heart Rate for Today → Most recent
- Get Weight for Today → Most recent

If an action is not available, omit that field (partial uploads are OK).

### C) Build JSON
Use a Dictionary, then Convert Dictionary to JSON:

Required keys:
- `date`: Today formatted as `YYYY-MM-DD`
- `source`: `apple_health`
- `timezone`: e.g. `Asia/Shanghai`
- `generated_at`: current time (ISO string)

Optional sections:
- `activity.steps`
- `activity.distance_km`
- `sleep.duration_minutes`
- `body.weight_kg`
- `vitals.resting_hr_bpm`

### D) POST to the bridge
Use **Get Contents of URL**:
- Method: POST
- URL: `Sync URL` + `/ingest`
- Headers:
  - `Authorization` = `Bearer <Token>`
  - `Content-Type` = `application/json`
- Request Body: the JSON string from step C

### E) Automation
Create a Personal Automation:
- Time of Day: e.g. 08:30 daily
- Run Shortcut: Wellness Sync

## Troubleshooting

- If you get 401: token mismatch (regenerate via `python3 scripts/wellness_bridge.py init --reset`)
- If you get network error: tunnel URL changed (restart cloudflared/ngrok and update Sync URL)
- Validate bridge:
  - `curl http://127.0.0.1:8787/health`
  - `python3 scripts/wellness_bridge.py status`
