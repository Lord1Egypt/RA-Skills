# proxy-aiops — capabilities reference

## Platforms

| Platform | API | Auth | Default base_url |
|----------|-----|------|------------------|
| `traefik` | Traefik API (`/api/...`) + `/metrics` text | none, or optional HTTP Basic (username + stored secret) | `http://localhost:8080` |
| `caddy` | Admin API (`/config/`, `/load`, `/reverse_proxy/upstreams`) | none, or optional HTTP Basic | `http://localhost:2019` |
| `haproxy` | Data Plane API v2 (`/v2/...`) | HTTP Basic (username + stored secret, **required**) | `http://localhost:5555` |

A per-target `platform` field selects the shape; the ops/CLI/MCP layers are
platform-neutral. Unsupported ops raise **teaching errors** (what to use
instead), never silent empties.

## Support matrix

| Capability | traefik | caddy | haproxy |
|------------|:-------:|:-----:|:-------:|
| version_info | ✅ `/api/version` | teaching note (no version endpoint) | ✅ `/v2/info` |
| list_entrypoints | ✅ `/api/entrypoints` | ✅ server listen addresses | ✅ frontends |
| list_routes / route_detail / find_route | ✅ routers (rule parsed) | ✅ routes (name = config path) | ✅ frontends (ACLs not parsed) |
| list_services / service_detail | ✅ services + serverStatus | ✅ reverse_proxy routes + upstreams | ✅ backends + stats |
| list_upstreams / upstream_detail | ✅ serverStatus map | ✅ `/reverse_proxy/upstreams` (fails→down) | ✅ stats server rows (status + check_status) |
| list_middlewares | ✅ | teaching (inline handlers) | teaching (haproxy.cfg) |
| list_certificates / cert_expiry_sweep | ✅ TLS routers + tls.domains | ✅ TLS listeners + automation subjects | teaching (.pem files) |
| traffic_stats / error_counters | ✅ `/metrics` per-code | teaching (no per-route counters) | ✅ stats (`req_tot`, `hrsp_*`) |
| config_snapshot / search_config | ✅ `/api/rawdata` (read-only) | ✅ `/config/` | teaching |
| get/set_config_value, delete_config_path, load_config | teaching (edit the provider) | ✅ (the write surface) | teaching (use runtime writes) |
| set_server_state / set_server_weight | teaching (provider) | teaching (config tree) | ✅ runtime servers |

## MCP tools (28)

### Reads (21)

| Tool | Returns |
|------|---------|
| `proxy_overview` | platform/version + route/service counts + upstream up/down |
| `version_info` | version/build info |
| `list_entrypoints` | listeners: {name, address} |
| `list_routes(host?)` | normalised routes: {name, hosts, paths, priority, service, tls, enabled, redirectTo}; Traefik rows add `prioritySource` (`explicit`, or `ruleLength` — Traefik's default when priority is unset or 0) |
| `route_detail(name)` | one route's full detail |
| `find_route(host, path)` | routes that would serve a host/path, best first |
| `list_services` | services/backends: {name, serversTotal, serversUp} |
| `service_detail(name)` | one service's detail (+ haproxy servers) |
| `list_upstreams(service?)` | server rows: {service, server, address, status up/down/maint/drain, checkInfo, weight} |
| `upstream_detail(service, server)` | one server row |
| `list_middlewares` | traefik middlewares (teaching elsewhere) |
| `list_certificates(probe?, port?)` | TLS domain inventory (+ live expiry when probed) |
| `traffic_stats` | per-service requests/latency/rate/sessions |
| `error_counters` | per-service status-code counters |
| `config_snapshot` | live config tree / merged dynamic state (sanitised) |
| `search_config(query)` | matching config paths |
| `get_config_value(path)` | one caddy config subtree |
| `backend_health_rca(upstreams?)` | per-service outage/degraded findings + cause + action |
| `cert_expiry_sweep(warn_days?, critical_days?, certs?)` | expiry buckets + renewal hints |
| `error_rate_rca(error_rate_pct?, min_requests?, counters?)` | flagged services, dominant-code cause, vs-fleet baseline |
| `route_conflict_analysis(routes?, services?)` | shadowed/dead routes, redirect loops |

All four analyses accept injected rows for pure offline analysis.

### Writes (5) — all take `dry_run`, all capture prior state

| Tool | Platform | Risk | Undo |
|------|----------|:----:|------|
| `set_config_value(path, value)` | caddy | medium | restore prior subtree (or delete a created path) |
| `delete_config_path(path)` | caddy | **high** | re-create the captured subtree |
| `load_config(config)` | caddy | **high** | re-load the snapshotted full config |
| `set_server_state(backend, server, state)` | haproxy | medium | restore prior admin state (ready/drain/maint) |
| `set_server_weight(backend, server, weight)` | haproxy | medium | restore prior weight (0-256) |

### Undo (2)

| Tool | Returns |
|------|---------|
| `undo_list(limit?)` | recorded undo descriptors, newest first, with their `_undo_id` |
| `undo_apply(undo_id, dry_run?)` | replays the recorded inverse (governed like any other write) |

`undo_apply` is governed like any other write (audited, capturing a before-state
where the inverse is itself reversible). Undo descriptors are recorded to
`~/.proxy-aiops/undo.db`; their params match each tool's own signature
(replayable as-is).

## Modelled API paths (mock-validated)

- traefik: `/api/version`, `/api/overview`, `/api/entrypoints`,
  `/api/http/routers[/{name}]`, `/api/http/services[/{name}]`,
  `/api/http/middlewares`, `/api/rawdata`, `/metrics`
- caddy: `/config/[{path}]`, `/load`, `/reverse_proxy/upstreams`
- haproxy: `/v2/info`, `/v2/services/haproxy/configuration/{frontends|backends|servers|binds}`,
  `/v2/services/haproxy/runtime/servers[/{name}]?backend=...`,
  `/v2/services/haproxy/stats/native`

Every substituted path value is percent-encoded centrally; caddy config paths
reject dot-segments.
