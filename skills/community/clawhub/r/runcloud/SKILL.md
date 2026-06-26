---
name: runcloud
description: >
  Query Runcloud servers, databases, web apps, services, cronjobs, deployments,
  and health via the Runcloud API v3. Trigger when the user mentions Runcloud,
  wants server stats/health, lists databases or web apps, or triggers a
  non-destructive action like a deployment or service restart on a managed server.
homepage: https://runcloud.io/docs/api/v3/doc-625011
metadata: {"clawdbot":{"emoji":"☁️","requires":{"bins":["jq"],"env":["RUNCLOUD_API_TOKEN"]}}}
---

<!-- version: 1.0 | updated: 2026-04-09 -->

# Runcloud Skill

Query and monitor Runcloud-managed servers via the Runcloud API v3.

## Setup

1. Open Workspace → Settings → API Management in the Runcloud dashboard
2. Generate an API token
3. Set environment variables:
   ```bash
   export RUNCLOUD_API_TOKEN="your-api-token"
   export RC="https://manage.runcloud.io/api/v3"
   export AUTH="Authorization: Bearer $RUNCLOUD_API_TOKEN"
   ```

All requests go to `$RC` and include the bearer token header `$AUTH`.

## Usage

All commands use curl to hit the Runcloud API v3 and pipe through `jq` for
readable output. Replace `{serverId}`, `{webappId}`, `{databaseId}`, and
`{cronjobId}` with real IDs (fetch them from the corresponding list endpoint).

### Ping (auth check)
```bash
curl -s -H "$AUTH" "$RC/ping" | jq
```

### List servers
```bash
curl -s -H "$AUTH" "$RC/servers?page=1&perPage=40" | jq '.data[] | {id, name, ipAddress, provider, online}'
```

### Get server
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}" | jq
```

### Get server stats
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}/stats" | jq
# -> { "stats": { "webApplication": n, "database": n, "cronJob": n, "supervisor": n }, "country": "..." }
```

### Get hardware info
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}/hardwareinfo" | jq
# -> kernel, processor, cpu cores, memory, disk, load average, uptime
```

### Get latest server health
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}/health/latest" | jq
# -> { totalMemory, availableMemory, usedMemory, totalDiskSpace, availableDiskSpace, usedDiskSpace, loadAverage, updated_at }
```

### List services
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}/services" | jq
# -> { beanstalk, httpd, mariadb, memcached, nginx, redis, supervisor } each with { realName, name, memory, cpu, running, version }
```

### List web applications
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}/webapps?page=1&perPage=40" | jq '.data[] | {id, name, rootPath, publicPath, phpVersion}'
```

### Get web application
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}/webapps/{webappId}" | jq
```

### List databases
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}/databases?page=1&perPage=40" | jq '.data[] | {id, name, collation, created_at}'
```

### Get database
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}/databases/{databaseId}" | jq
```

### List database users
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}/databaseusers?page=1&perPage=40" | jq '.data[] | {id, username, created_at}'
```

### List system users
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}/users?page=1&perPage=40" | jq '.data[] | {id, username, created_at}'
```

### List cron jobs
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}/cronjobs?page=1&perPage=40" | jq '.data[] | {id, label, username, time, command, enabled}'
```

### Get cron job
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}/cronjobs/{cronjobId}" | jq
```

### List supervisor jobs
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}/supervisors?page=1&perPage=40" | jq '.data[] | {id, name, command, user, running}'
```

### List SSL certificates
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}/webapps/{webappId}/ssl" | jq
```

### List domains for a web app
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}/webapps/{webappId}/domains" | jq '.data[] | {id, name, type}'
```

### List deployments
```bash
curl -s -H "$AUTH" "$RC/servers/{serverId}/webapps/{webappId}/git/deployments?page=1&perPage=40" | jq '.data[] | {id, status, commit_hash, created_at}'
```

## Non-destructive writes (POST)

These endpoints *trigger* safe actions — they do not create billable resources
or delete anything. Still, confirm with the operator before running them on a
production server.

### Trigger a new deployment
```bash
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" \
  "$RC/servers/{serverId}/webapps/{webappId}/git/deployments" | jq
```

### Test a cron job (runs once now)
```bash
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" \
  "$RC/servers/{serverId}/cronjobs/{cronjobId}/test" | jq
```

### Restart a service
```bash
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"action":"restart"}' \
  "$RC/servers/{serverId}/services/{serviceRealName}/action" | jq
# serviceRealName examples: nginx-rc, apache2-rc, mysql, redis-server, supervisor
```

### Deploy Let's Encrypt SSL
```bash
curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"provider":"letsencrypt","enableHttp":true,"enableHsts":false,"ssl_protocol_id":1}' \
  "$RC/servers/{serverId}/webapps/{webappId}/ssl" | jq
```

## Notes

- **Auth:** every request needs `Authorization: Bearer $RUNCLOUD_API_TOKEN`. The token grants full workspace access — treat it like a password.
- **Pagination:** array endpoints accept `?page=N&perPage=M` (max `perPage=40`). Responses wrap data in `{ "data": [...], "meta": { "pagination": {...} } }`.
- **Rate limiting:** check the `X-RateLimit-Limit` and `X-RateLimit-Remaining` headers on every response; a `429` means back off and retry later.
- **Finding IDs:** `serverId`, `webappId`, `databaseId`, `cronjobId` all come from the matching list endpoint — always list first if you don't know the ID.
- **v3 is still in progress:** if an endpoint 404s, the v2 path at `https://manage.runcloud.io/api/v2` usually mirrors it one-to-one. Docs index: https://runcloud.io/docs/api/v3/doc-625011
- **Safety:** this skill deliberately omits every DELETE, resource create, and password-change endpoint. Do not add them without an explicit operator request.

## Examples

```bash
# Health snapshot of every server (one-liner)
curl -s -H "$AUTH" "$RC/servers?perPage=40" \
  | jq -r '.data[].id' \
  | while read id; do
      echo "=== server $id ==="
      curl -s -H "$AUTH" "$RC/servers/$id/health/latest" \
        | jq '{loadAverage, usedMemory, availableMemory, usedDiskSpace}'
    done

# Find a specific server by name
curl -s -H "$AUTH" "$RC/servers?perPage=40" \
  | jq '.data[] | select(.name | contains("prod"))'

# Flag servers whose load average is above 1.0
curl -s -H "$AUTH" "$RC/servers?perPage=40" \
  | jq -r '.data[].id' \
  | while read id; do
      load=$(curl -s -H "$AUTH" "$RC/servers/$id/health/latest" | jq '.loadAverage')
      awk -v l="$load" -v i="$id" 'BEGIN{ if (l+0 > 1.0) print "HOT:", i, l }'
    done

# Count web apps, databases, and cronjobs on a server
curl -s -H "$AUTH" "$RC/servers/{serverId}/stats" \
  | jq '.stats'
```
