---
name: technitium-dns
description: Monitor and inspect Technitium DNS Server via its HTTP API. Use for read-only health checks, DNS stats, zones, DHCP leases, token/session validation, and proactive alerts about DNS/DHCP issues.
license: MIT
homepage: https://github.com/TechnitiumSoftware/DnsServer
metadata:
  openclaw:
    requires:
      env:
        - TECHNITIUM_URL
        - TECHNITIUM_TOKEN
      bins:
        - python3
---

# Technitium DNS

Use this skill to perform read-only checks against a Technitium DNS Server instance.

## Configuration

Set these environment variables before running scripts:

```bash
export TECHNITIUM_URL="http://dns-server.example:5380"
export TECHNITIUM_TOKEN="..."
```

Technitium v15+ accepts API/session tokens with:

```http
Authorization: Bearer <token>
```

Prefer a dedicated limited/read-only user and a non-expiring API token for monitoring.

## Health Check

Run the bundled helper:

```bash
python3 scripts/technitium_health_check.py
```

Or from another working directory:

```bash
TECHNITIUM_URL="http://dns-server.example:5380" \
TECHNITIUM_TOKEN="..." \
python3 /path/to/technitium-dns/scripts/technitium_health_check.py
```

The script prints JSON:

```json
{
  "ok": true,
  "checked": [],
  "failures": []
}
```

Exit codes:

- `0`: no critical failures
- `1`: one or more monitored checks detected a critical condition
- `2`: configuration or core API/session check failed

## What It Checks

Read-only endpoints:

- `/api/user/session/get` — token/session validity and server info
- `/api/settings/get` — version, uptime timestamp, DNS settings availability
- `/api/dashboard/stats/get?type=LastHour&utc=true` — DNS stats
- `/api/zones/list` — disabled, expired, or sync-failed zones
- `/api/dhcp/leases/list` — DHCP lease visibility, if permitted/used

Alerts/failures are intended for:

- API/server unreachable
- invalid/expired token
- zone `disabled`, `isExpired`, or `syncFailed`
- abnormal SERVFAIL/refused/dropped error rate

DHCP permission failure is reported as a warning in `checked` because many deployments do not use Technitium DHCP or restrict DHCP permissions.

## Proactive Use

For heartbeat/proactive monitoring:

1. Run the health check only when due; avoid checking every wake.
2. If JSON `ok` is true, stay silent.
3. If `ok` is false, summarize only actionable failures.
4. Do not modify settings, zones, DHCP, cache, or logs without explicit user confirmation.

## API Docs

Technitium DNS Server API docs:
https://github.com/TechnitiumSoftware/DnsServer/blob/master/APIDOCS.md
