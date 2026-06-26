---
name: whoop-health
description: Fetch, analyze, and visualize WHOOP wearable health data via the WHOOP Developer API v2. Use when the user wants to connect their WHOOP band, retrieve recovery scores, HRV, sleep performance, strain, or workout data, analyze health trends, or integrate WHOOP data into a broader workflow. Triggers on phrases like "WHOOP data", "WHOOP API", "WHOOP health", "connect WHOOP", "whoop recovery", "whoop sleep", "whoop strain", or any request to analyze wearable data from a WHOOP device.
---

# WHOOP Health Skill

Integrates with the WHOOP Developer API v2 to retrieve and analyze health/fitness data from a WHOOP band.

## Setup

### 1. Create a Developer App

1. Go to [developer.whoop.com](https://developer.whoop.com) and sign in with your WHOOP account
2. Create a new application; set Redirect URI to `http://localhost:8080/callback`
3. Save **Client ID** and **Client Secret**

### 2. Authenticate

Run the OAuth helper script to get an access token:

```bash
python3 scripts/whoop_auth.py --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
```

This opens a browser for authorization and saves tokens to `~/.whoop_tokens.json`.

### 3. Fetch Data

```bash
# Fetch all data types (last 7 days)
python3 scripts/whoop_fetch.py --days 7

# Fetch specific data types
python3 scripts/whoop_fetch.py --days 30 --types recovery,sleep,workout,cycle

# Output as JSON
python3 scripts/whoop_fetch.py --days 7 --format json --output whoop_data.json

# Output as CSV (one file per data type)
python3 scripts/whoop_fetch.py --days 7 --format csv --output ./whoop_export/
```

## Available Data Types

| Type | Key Metrics |
|------|-------------|
| `recovery` | Recovery score (0–100%), HRV (ms), resting heart rate |
| `sleep` | Sleep performance %, duration, REM/SWS/light/awake stages |
| `workout` | Activity Strain (0–21), avg/max heart rate, calories, sport type |
| `cycle` | Day Strain (0–21), avg heart rate, kilojoules |
| `profile` | Name, email |
| `body_measurement` | Height, weight, max heart rate |

## Analysis Workflows

### Trend Analysis

```bash
python3 scripts/whoop_fetch.py --days 30 --types recovery,sleep --format json --output data.json
```

Then ask: "Analyze my HRV trend and sleep performance over the last 30 days. Identify patterns."

### Recovery vs. Strain Correlation

Fetch `recovery` + `cycle` for 30+ days, then ask for correlation analysis between day Strain and next-day Recovery score.

### Sleep Stage Breakdown

Fetch `sleep` data, request a breakdown of avg time in each stage (REM, SWS, Light, Awake) and flag nights below recommended thresholds.

## Token Management

Tokens are stored at `~/.whoop_tokens.json`. The fetch script auto-refreshes using the refresh token when the access token expires (24h lifetime).

To revoke access: `python3 scripts/whoop_auth.py --revoke`

## API Reference

See `references/api_endpoints.md` for full endpoint list, parameters, and response schemas.

## Environment Variables (alternative to flags)

```bash
export WHOOP_CLIENT_ID=your_client_id
export WHOOP_CLIENT_SECRET=your_client_secret
```
