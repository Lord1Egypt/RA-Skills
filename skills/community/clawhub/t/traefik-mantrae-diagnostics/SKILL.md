---
name: traefik
description: "Inspect and troubleshoot Traefik reverse proxies via read-only API, dashboard, logs, and config checks."
---

# Traefik

Use for Traefik reverse proxy diagnostics: API/dashboard state, routers, services, middlewares, entrypoints, TLS/cert resolver hints, logs, and safe config inspection.

## Configuration

Set connection details through environment variables rather than hard-coding local infrastructure data:

- `TRAEFIK_BASE_URL`: Traefik API/dashboard base URL, for example `https://traefik.example.internal`.
- `MANTRAE_BASE_URL`: Mantrae API base URL, for example `https://mantrae.example.internal`.
- `MANTRAE_TOKEN`: Mantrae bearer token.
- `MANTRAE_USERNAME`, `MANTRAE_EMAIL`, `MANTRAE_PASSWORD`: optional login credentials when no token is provided.
- `MANTRAE_PROFILE_ID`: Mantrae profile id for config/list requests. Defaults to `1`.
- `MANTRAE_CONNECT_IP`: optional IP override when DNS/SNI host must be preserved but the request should connect to a specific IP.

## Safety

- Read-only by default.
- Do not enable `api.insecure=true` on a public interface.
- Do not restart Traefik, Docker, or the VM without Igor's confirmation.
- Before editing Traefik config, make/request a backup of the relevant files.
- Treat `/api/rawdata` and support dumps as sensitive; they can expose routing details and configuration.

## API

Traefik's API is HTTP GET-only for inspection. Useful endpoints:

- `/api/version`
- `/api/overview`
- `/api/entrypoints`
- `/api/http/routers`
- `/api/http/services`
- `/api/http/middlewares`
- `/api/tcp/routers`
- `/api/tcp/services`
- `/api/udp/routers`
- `/api/udp/services`
- `/api/rawdata`
- `/api/support-dump`

The dashboard usually lives at `/dashboard/`. In secure mode the router must match both `/api` and `/dashboard` and point to `api@internal`.

## Mantrae API

Mantrae manages Traefik dynamic configuration through a Connect RPC API. It is not Traefik's runtime dashboard, so use it for config inspection and controlled config changes, not live Traefik health/logs.

- OpenAPI: `${MANTRAE_BASE_URL}/openapi`
- OpenAPI JSON: `${MANTRAE_BASE_URL}/openapi.json`
- Auth: JWT Bearer from `/mantrae.v1.UserService/LoginUser`
- Read-oriented useful methods:
  - `/mantrae.v1.RouterService/ListRouters`
  - `/mantrae.v1.ServiceService/ListServices`
  - `/mantrae.v1.MiddlewareService/ListMiddlewares`
  - `/mantrae.v1.EntryPointService/ListEntryPoints`
  - `/mantrae.v1.UtilService/GetDynamicConfig`
  - `/mantrae.v1.BackupService/ListBackups`
  - `/mantrae.v1.AuditLogService/ListAuditLogs`

Helper:

```bash
MANTRAE_BASE_URL=https://mantrae.example.internal MANTRAE_TOKEN=... python scripts/mantrae_api.py routers
MANTRAE_BASE_URL=https://mantrae.example.internal MANTRAE_USERNAME=... MANTRAE_PASSWORD=... python scripts/mantrae_api.py dynamic-config
MANTRAE_BASE_URL=https://mantrae.example.internal MANTRAE_CONNECT_IP=10.0.0.10 MANTRAE_TOKEN=... python scripts/mantrae_api.py routers --insecure
```

The helper defaults to `MANTRAE_PROFILE_ID=1` and `limit=-1` for list methods unless a custom `--message` JSON overrides those fields.

If DNS does not resolve from the OpenClaw host, test through Traefik IP with curl:

```bash
curl -k --resolve mantrae.example.internal:443:10.0.0.10 https://mantrae.example.internal/openapi.json
```

Do not call create/update/delete/restore endpoints without a fresh backup and Igor's confirmation.

## Helper

```bash
python scripts/traefik_api.py overview
python scripts/traefik_api.py routers
python scripts/traefik_api.py services
python scripts/traefik_api.py rawdata
```

With a custom API URL:

```bash
TRAEFIK_BASE_URL=https://traefik.example.internal python scripts/traefik_api.py overview
```

## Local VM Checks

If SSH access exists:

```bash
ssh -i ~/.ssh/traefik_readonly user@traefik-host 'systemctl status traefik --no-pager'
ssh -i ~/.ssh/traefik_readonly user@traefik-host 'journalctl -u traefik --since "2 hours ago" --no-pager'
ssh -i ~/.ssh/traefik_readonly user@traefik-host 'journalctl -u traefik --since "1 hour ago" --no-pager | grep -E "\" 5[0-9][0-9] "'
ssh -i ~/.ssh/traefik_readonly user@traefik-host 'journalctl -u traefik --since "1 hour ago" --no-pager | grep "router-name@http"'
```

Use systemd logs first. Docker group access is powerful and should be granted only if Traefik actually runs in Docker and logs are not available elsewhere.
Traefik access logs can include long OIDC URLs and state parameters; summarize findings and avoid reposting full sensitive query strings unless Igor explicitly needs them.

## Workflow

1. Check `version` and `overview` through the API.
2. If API is unreachable, check whether dashboard/API is enabled and where it is routed.
3. Inspect routers/services/middlewares for failing routes.
4. Use logs for 404, 502/503, TLS, ACME, provider, and config reload errors.
5. Only propose config changes after identifying the exact failing router/service/middleware.
