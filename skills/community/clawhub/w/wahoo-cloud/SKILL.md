---
name: wahoo-cloud
description: Access Wahoo Fitness Cloud API to fetch workouts, download FIT files, and analyze training data (power, HR, cadence, GPS).
homepage: https://cloud-api.wahooligan.com/
metadata: {"clawdbot":{"emoji":"🚴","requires":{"bins":["python3"],"env":["WAHOO_CLIENT_ID","WAHOO_CLIENT_SECRET"]},"primaryEnv":"WAHOO_CLIENT_ID"}}
---

# Wahoo Cloud Skill

Provides programmatic access to Wahoo Fitness Cloud data. This skill manages OAuth2 authentication, workout synchronization, and FIT file processing.

## 🚀 Agent Quickstart

When a user asks about their Wahoo workouts, training, or fitness data, use these workflows:

| User Intent | Action / Command |
| :--- | :--- |
| **"Sync my Wahoo workouts"** | `python3 {baseDir}/scripts/fetch_workouts.py` |
| **"Show my recent rides"** | Query the local SQLite DB: `$WAHOO_BASE_DIR/wahoo.db (default: ~/.wahoo/wahoo.db)` — schema below |
| **"Parse this FIT file"** | `python3 {baseDir}/scripts/parse_fit.py <PATH_TO_FIT>` |
| **"Connect/Set up Wahoo"** | 1. Verify `WAHOO_CLIENT_ID` and `WAHOO_CLIENT_SECRET` exist.<br>2. If missing, ask user to provide them.<br>3. Run `python3 {baseDir}/scripts/oauth_setup.py` |
| **"Token expired / persistent 401 errors"** | Run python3 {baseDir}/scripts/oauth_setup.py to re-authorize. Force-refresh without browser: python3 -c "import sys; sys.path.insert(0,'lib'); import wahoo_auth; wahoo_auth.refresh()" |

## 🛠 Key Workflows

### 1. Authentication & Setup
This skill requires a Wahoo Developer App. 
- **Credentials:** Must be provided as `WAHOO_CLIENT_ID` and `WAHOO_CLIENT_SECRET`.
- **OAuth Flow:** If tokens are missing or expired, run `scripts/oauth_setup.py`. This is an **interactive** process. You must present the URL to the user, wait for them to authenticate, and then ask them to paste the resulting redirect URL/code back into the terminal.
- **Token Storage:** Tokens are stored at $WAHOO_BASE_DIR/secrets/wahoo_tokens.json (controlled by WAHOO_BASE_DIR env var, default ~/.wahoo).

### 2. Data Synchronization
- **Command:** `python3 scripts/fetch_workouts.py`
- **Behavior:** Idempotent. It fetches new workouts, downloads FIT files, and populates the local SQLite database.
- **Database Path:** `$WAHOO_BASE_DIR/wahoo.db (default: ~/.wahoo/wahoo.db)`
- **Rate Limits:** The script automatically handles Wahoo's sandbox rate limits (25 req / 5 min) using exponential backoff.

### 3. Querying Training Data
Once synced, use the following SQL patterns to answer user questions:

- **Recent Workouts:** `SELECT * FROM workouts ORDER BY starts DESC LIMIT 10;`
- **Power/HR Series:** `SELECT timestamp, power_w, heart_rate, cadence FROM records WHERE workout_id = <id> ORDER BY timestamp;`
- **Elevation/GPS:** `SELECT timestamp, position_lat_deg, position_long_deg, enhanced_altitude_m FROM records WHERE workout_id = <id>;`

## ⚠️ Critical Constraints & Pitfalls

- **Rate Limiting:** Wahoo Sandbox is strict. Do not attempt to loop calls rapidly; rely on the `wahoo_api.py` built-in backoff.
- **Data Types:** The Wahoo API returns decimal values as **strings**. Always cast to `float()` before performing mathematical analysis.
- **Metric Conversion:** 
  - Meters to Miles: `m / 1609.34`
  - Meters/Second to MPH: `m/s * 2.237`
- **Workout Summaries:** The `/v1/workouts` list endpoint returns `null` for `workout_summary`. You **must** call `/v1/workouts/<id>` to get specific metrics like NP, TSS, or the FIT file URL.

## Error Reference

| HTTP Code | Meaning | Resolution |
| :--- | :--- | :--- |
| 401 | Token expired/invalid — auto-refresh runs once | Re-run oauth_setup.py if it keeps failing |
| 403 | Insufficient scope | Re-authorize with missing scope in WAHOO_SCOPES |
| 429 | Rate limit | wahoo_api.py backs off automatically, use --limit to reduce call volume |
| 404 | Workout not found | Confirm ID and ownership |
