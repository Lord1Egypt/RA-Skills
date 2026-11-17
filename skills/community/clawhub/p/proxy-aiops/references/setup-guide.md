# proxy-aiops — setup guide

## 1. Enable each platform's API

- **traefik** — expose the API: `--api=true` with a router on `api@internal`
  (or `--api.insecure=true` in a lab, which serves it on `:8080`). For
  error-rate analysis also enable the metrics endpoint
  (Traefik's metrics provider serves `/metrics`).
- **caddy** — the admin API is on `localhost:2019` by default (the `admin`
  key in the config controls the listener). proxy-aiops needs plain HTTP
  reachability to it; keep it bound to localhost or an internal network.
- **haproxy** — run the **Data Plane API** sidecar (`dataplaneapi`) pointing at
  haproxy.cfg, with a userlist user. Note the listen address (default `:5555`)
  and the user/password.

## 2. Onboard

```bash
uv tool install proxy-aiops
proxy-aiops init
```

The wizard asks for: target name → platform (`traefik` / `caddy` / `haproxy`)
→ API base URL (per-platform default offered) → TLS verification (default ON;
answer No only for self-signed lab certs) → credentials:

- **haproxy**: Data Plane API username + password (password stored encrypted —
  required).
- **traefik / caddy**: optional Basic-auth username/password — leave both
  empty for the common unauthenticated-localhost case (no store entry means no
  auth header is sent).

## 3. Verify

```bash
proxy-aiops doctor
```

Doctor checks config, the encrypted store (and its permissions), per-target
secrets (respecting which platforms need one), then probes each target's cheap
health/info endpoint: traefik `/api/version`, caddy `/config/`, haproxy
`/v2/info`.

## 4. Wire up an MCP client

```json
{
  "mcpServers": {
    "proxy-aiops": {
      "command": "uvx",
      "args": ["--from", "proxy-aiops", "proxy-aiops-mcp"],
      "env": { "PROXY_AIOPS_MASTER_PASSWORD": "your-master-password" }
    }
  }
}
```

MCP clients do not inherit your shell profile: set
`PROXY_AIOPS_MASTER_PASSWORD` in the `env` block whenever any target has a
stored secret, and `PROXY_AIOPS_CONFIG` / `PROXY_AIOPS_HOME` if you relocated
state.

## Config file

`~/.proxy-aiops/config.yaml`:

```yaml
targets:
  - name: edge1
    platform: traefik
    base_url: http://192.0.2.10:8080
    verify_ssl: true
  - name: caddy1
    platform: caddy
    base_url: http://127.0.0.1:2019
  - name: lb1
    platform: haproxy
    base_url: http://192.0.2.20:5555
    username: dpapi
```

Secrets never live here — only in `secrets.enc` (or the deprecated
`PROXY_<TARGET>_SECRET` env fallback).

## Troubleshooting

- **401/403** — haproxy: wrong Data Plane API user/password; traefik/caddy: a
  Basic-auth layer is in front (store a secret) or a stale secret is stored
  (remove it with `proxy-aiops secret rm <target>`).
- **404 on every call** — the API is not enabled (traefik `api@internal`
  router missing; caddy admin listener disabled; dataplaneapi not running).
- **Connection refused** — check `base_url` (scheme + port) and that the
  endpoint is bound beyond localhost if proxy-aiops runs on another host.
- **cert sweep returns unknowns** — the probe needs TCP reach to each domain
  on the TLS port (default 443, max 25 domains, 5s each).
