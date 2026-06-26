---
name: strava-api
description: Official Strava OAuth integration for OpenClaw. Use to connect/authorize Strava, store+refresh tokens, and fetch workout/activity data (runs/rides/etc.) for today/yesterday or a date range. Use for generating training summaries, weekly mileage, activity lists, and for feeding the Wellness hub with normalized workout data.
---

# Strava (Official API)

Keep this skill source-only: connect to Strava, fetch activities, normalize output. Delivery is channel-agnostic.

## Configuration

Required env vars:

- `STRAVA_CLIENT_ID`
- `STRAVA_CLIENT_SECRET`
- `STRAVA_REDIRECT_URI`

Optional:

- `STRAVA_TOKEN_PATH` (default: `~/.config/openclaw/strava/token.json`)
- `STRAVA_TZ` (default: `Asia/Shanghai`)

## Connect (OAuth)

Choose one mode:

- **Phone/remote mode (recommended):**

```bash
python3 scripts/strava_oauth_login.py
```

- **Desktop loopback mode (optional):** if you are authorizing in a browser on the same machine that runs OpenClaw and your `STRAVA_REDIRECT_URI` is a loopback URL (e.g. `http://127.0.0.1:58539/callback`):

```bash
python3 scripts/strava_oauth_login.py --loopback
```

## Fetch activities for a day (json output)

```bash
python3 scripts/strava_fetch_activities.py --date today --out /tmp/strava_today.json
```

## Notes

- API details: `references/strava_api.md`