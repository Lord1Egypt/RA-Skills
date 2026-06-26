---
name: unifi
description: Query and monitor a UniFi network using a UniFi Integration API key (X-API-KEY) plus compatible read-only classic UniFi Network endpoints. Use when the user asks to check UniFi, list UniFi devices, show who is on the network, inspect UniFi clients, review UniFi health, list sites, review WLANs/networks, check alarms, inspect top apps/DPI availability, or get a UniFi dashboard/overview from a Cloud Gateway or UniFi OS console.
---

# UniFi Integration API

Use this skill for **read-only UniFi monitoring** through a UniFi API key.

## Setup

Create the credentials file:

`~/.clawdbot/credentials/unifi/config.json`

Example:

```json
{
  "url": "https://gateway.local",
  "token": "YOUR_API_KEY",
  "site": "default"
}
```

Notes:
- `token` is the UniFi API key
- Requests use header `X-API-KEY: <token>`
- Scripts resolve the site ID automatically from `/proxy/network/integration/v1/sites`
- `site` is used for classic read-only endpoints such as `stat/health`, `stat/alarm`, `rest/networkconf`, and `rest/wlanconf`

## Commands

### Sites

```bash
bash scripts/sites.sh
bash scripts/sites.sh json
```

List available UniFi sites and their IDs.

### Health

```bash
bash scripts/health.sh
bash scripts/health.sh json
```

Show a compact summary with device totals, online/offline counts, roles, and client counts.

### Devices

```bash
bash scripts/devices.sh
bash scripts/devices.sh json
```

Show UniFi infrastructure devices with model, IP, state, firmware, and feature roles.

### Clients

```bash
bash scripts/clients.sh
bash scripts/clients.sh json
```

Show connected clients with type, IP, MAC, connection time, and uplink device ID.

### Dashboard

```bash
bash scripts/dashboard.sh
bash scripts/dashboard.sh json
```

Show a combined overview including:
- site and console info
- UniFi version
- health subsystems
- devices
- networks
- WLANs
- top client list
- recent alarms summary

### Alerts / alarms

```bash
bash scripts/alerts.sh
```

Show recent UniFi alarms. If none exist, report that there are no recent alarms.

### Top apps / DPI

```bash
bash scripts/top-apps.sh
bash scripts/top-apps.sh 15
```

Show top applications by DPI if the gateway returns DPI data. If not, report that no DPI data is currently available.

## Current endpoint coverage

Working endpoints validated on this gateway:
- `/proxy/network/integration/v1/sites`
- `/proxy/network/integration/v1/sites/{siteId}/devices`
- `/proxy/network/integration/v1/sites/{siteId}/clients`
- `/proxy/network/api/s/{site}/stat/health`
- `/proxy/network/api/s/{site}/stat/sysinfo`
- `/proxy/network/api/s/{site}/stat/alarm`
- `/proxy/network/api/s/{site}/stat/sitedpi`
- `/proxy/network/api/s/{site}/rest/networkconf`
- `/proxy/network/api/s/{site}/rest/wlanconf`

Caveats:
- alarms/events may legitimately return zero items
- DPI may return an empty payload even when the endpoint itself is reachable
- some management/config endpoints expose sensitive data; avoid dumping full raw payloads unless explicitly needed

## Workflow

When the user asks:
- **"check UniFi" / "dashboard"** → run `bash scripts/dashboard.sh`
- **"is everything healthy?"** → run `bash scripts/health.sh`
- **"show devices"** → run `bash scripts/devices.sh`
- **"who is on the network?" / "clients"** → run `bash scripts/clients.sh`
- **"what sites exist?"** → run `bash scripts/sites.sh`
- **"any alarms?" / "alerts"** → run `bash scripts/alerts.sh`
- **"top apps" / "traffic" / "DPI"** → run `bash scripts/top-apps.sh`

Always sanity-check the response before reporting back:
- verify the API returned JSON
- verify counts look reasonable
- if alarms or DPI are empty, say they are empty rather than treating that as an auth or endpoint failure
- avoid pasting sensitive management payloads back to the user unless they explicitly ask for raw details
