# Red Alert Skill — Endpoint Inventory (v1.2.0)

This file documents **all external endpoints/channels this skill uses in code**.

## 1) REST Endpoints Used by Skill

### `GET https://api.tzevaadom.co.il/alerts-history`
- **Used by:** `scripts/analyze.mjs`
- **Purpose:** Pull recent alert history (nationwide), then filter locally by city/time (`--city`, `--since`).
- **Auth:** None
- **Notes:** Returns a bounded recent window (not full long-term archive).

### `GET https://redalert.orielhaim.com/api/status`
- **Used by:** `scripts/status.sh`
- **Purpose:** Service health/status check.
- **Auth:** None
- **Headers used:** `Accept: application/json`

## 2) Socket.IO Channels Used by Skill

### Base URL
- `https://redalert.orielhaim.com`

### Namespaces
- `/` (default) — used by `scripts/realtime.mjs`, `scripts/listener.mjs`, `scripts/listener-daemon.mjs`
- `/test` — optional in `scripts/realtime.mjs --test`

### Auth
- Optional: `auth: { apiKey: process.env.RED_ALERT_API_KEY }`
- If `RED_ALERT_API_KEY` is not set, connection is attempted unauthenticated.

### Subscribed Event Names (as implemented)
- `alert`
- `rockets`
- `missiles` (daemon)
- `hostileAircraftIntrusion`
- `tsunami`
- `earthquake`
- `terroristInfiltration`

Connection lifecycle events used:
- `connect`
- `disconnect`
- `connect_error`

## 3) Skill-Adjacent Endpoint (Not used by scripts yet)

### `POST https://redalert.orielhaim.com/api/access-request`
- **Observed in docs frontend bundle**.
- **Current skill usage:** Not called by existing scripts.
- **Potential future usage:** Programmatic access-request flow.

## 4) Quick Verification Commands

```bash
# Status endpoint
curl -s -H "Accept: application/json" "https://redalert.orielhaim.com/api/status"

# History endpoint
curl -s "https://api.tzevaadom.co.il/alerts-history" | head -c 500

# Realtime listener (default namespace)
node /data/clawd/skills/red-alert/scripts/realtime.mjs --duration 20

# Realtime listener (test namespace)
node /data/clawd/skills/red-alert/scripts/realtime.mjs --test --duration 20
```

## 5) Scope Clarification

This inventory is intentionally limited to the skill’s actual code paths.
It does **not** claim to enumerate every endpoint available in the provider’s public docs.
