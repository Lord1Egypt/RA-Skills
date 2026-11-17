# ZY Action Platform API Quick Reference (for the script / generic pass-through)

> This file is the endpoint basis for the built-in commands and the `request` pass-through of `scripts/zy_platform.py`. Paths are relative to the product API root by default (direct `http://127.0.0.1:<port>/api/v1`). APIs evolve; the bundled `API 接入及测试方法参考.txt` and `docs/**` in the release package are the authoritative source. On conflict, the platform's actual responses and bundled docs win.

## 0. Conventions

- **Base URLs**: direct local `http://127.0.0.1:18080`~`:18084` (AIP/Foundry/Apollo/Gotham/Swift); gateway `http://<host>/<product prefix>/v1` with prefixes `api`(Foundry)/`aip-api`/`apollo-api`/`gotham-api`/`swift-api`. **Remote (non-loopback) hosts must use `https://<host>/...`; the script rejects remote plaintext http.**
- **Auth**: everything except `health` and the login endpoint requires header `Authorization: Bearer <JWT>`. Login endpoint:
  - `POST /api/v1/auth/login`, body `{"username":"...","password":"..."}`. Preview with `login --dry-run` and obtain user consent before sending credentials.
  - A fresh install seeds `admin/admin1` per product (overridable via env vars); self-registration via `POST /api/v1/auth/register`.
  - **Response formats differ (script auto-handles)**: AIP/Apollo/Gotham/Swift return flat `{"token": ...}` (Gotham/Swift also carry `refresh_token`); Foundry wraps an envelope `{"code":0,"data":{"token":...}}`.
- **Token cache (security model)**:
  - Cache key is the tuple `scheme|host|port|product|api-root`; when the current request origin differs from the cached origin the token is **not attached automatically** — re-login or pass an explicit `--token`.
  - Storage prefers the OS credential store (python `keyring` module); fallback file `~/.workbuddy/zy_action_session.json` (dir 0700 / file 0600 / atomic replacement / symlinks rejected / expired entries purged / no usernames stored).
  - Token expiry comes from the JWT `exp` claim; without `exp` a conservative 24-hour cap applies. `logout [--all] [--forget-host]` clears safely.
- **Response envelope**: Foundry/Gotham/Apollo successes are mostly `{"code":0,"message":"ok","data":{...}}` (Apollo adds `request_id`); AIP login/chat/health return bare JSON. `code != 0` means business failure.
- **HTTP statuses**: 401=token invalid/missing (re-login); 404=route absent in this version (verify via `request`/docs first); 400=bad args; 5xx=server error.
- **Script exit codes**: 0 success / 1 argument error or local/security-policy refusal / 2 network unreachable or timeout (including HTTPS certificate failure) / 3 HTTP error (4xx/5xx non-401, including blocked cross-origin redirects) / 4 auth failure (401) / 5 business envelope code≠0.
- **Security policy (script-enforced)**: remote plaintext http, base-urls with userinfo/fragments, cross-origin redirects, unconfirmed remote origins (need `--trust-host`), sensitive pass-through segments etc. are refused with exit 1 and a stderr "security policy" message.

## 0.1 Pass-through (request) Allowlist

- Method fixed set GET/HEAD/POST/PUT/PATCH/DELETE; **only GET/HEAD by default**; write methods need explicit `--allow-write` after a `--dry-run` confirmation with the user.
- Read-only family allowlist (any path segment matching enables GET/HEAD): `datasets metrics ontology dashboards reports search graph timeline map entities ingestion workflows executions datasources deployments drift bundles agents desired-states docs audit catalog nexus charts sync events nodes stats features objects preview`; server-root `health` is allowed separately.
- Sensitive-segment denylist (any path segment matching → refused): `auth register password passwd users user admin administrator rbac roles permissions config settings license system database databases sql exec execute debug internal actuator tokens keys secrets sessions`.
- Writes are allowed only for paths whose first segment is `chat` or `ontology` (e.g. `chat`, `ontology/semantic-search`).
- Tokens: pass-through never attaches the cached token by default; with user consent add `--with-token` (origin binding still enforced) or pass `--token`. Approved writes are recorded to the local audit log `~/.workbuddy/zy_action_audit.log` (no credentials, no tokens).

## 0.2 Downloaded Artifact Verification

- Before installing run `verify-artifact --file <file> --sha256 <value from the official release page>`; continue only when `"match": true`; then verify the digital signature (expected publisher: ZY Tech / zyinfo.pro) and confirm with the user before executing.

## 1. LightAIP (aip, 18080) — NLQ & Automation

| Script command | Method + path | Notes |
| --- | --- | --- |
| `chat --query "…"` | POST `/chat` | NLQ natural-language query. Body `{"query":"…"}`. Response contains `intent/confidence/data_source_name/sql_query/query_result{columns,rows}/visualization/fix_attempts/rejected`; `rejected=true` means it failed — relay `message`. |
| `workflow-list` | GET `/workflows` | List automation workflows (`?page=&page_size=`). Use each item's `id`, `name`, `description`. |
| `workflow-run --workflow-id <id>` | POST `/workflows/{id}/run` | Run once; returns `data.execution_id`, `status`, `nodes[]`, `outputs` (node id → result). Optional `--params '{"region":"east"}'`. |
| `workflow-status --execution-id <eid>` | GET `/workflows/executions/{eid}` | Execution detail: `execution` (status etc.) + `nodes[]` (node_type/status/output/error). Status values: `pending/running/completed/failed/cancelled`. |
| `workflow-cancel --execution-id <eid>` | POST `/workflows/executions/{eid}/cancel` | Cancel an execution. |
| `datasource-list` | GET `/datasources` | Datasource list (incl. demo DB). |
| `audit-list` | GET `/audit/logs` | Audit logs (admin). |
| `health` | GET `/health` | Public. `{status,checks:{database,vector,llm_gateway,disk_space}}`. |

## 2. LightFoundry (foundry, 18081) — Data / Ontology / Metrics

| Script command | Method + path | Notes |
| --- | --- | --- |
| `datasource-list` | GET `/datasources` | Datasource list. |
| `dataset-list` | GET `/datasets` | Dataset list (`?status=&limit=`). |
| `dataset-preview --dataset-id <id>` | GET `/datasets/{id}/preview?limit=` | Row preview (default 50, max 500). |
| `ontology-objects` | GET `/ontology/objects` | Ontology object types (order/customer/product…). |
| `ontology-search --query "…"` | POST `/ontology/semantic-search` | **Recommended**: semantic search over ontology/metrics/objects. Body `{"query":"…","limit":10}`. |
| `metric-list` | GET `/metrics` | Metric list (also `/metrics/catalog`). |
| `dashboard-list` | GET `/dashboards` | Dashboard list. |
| `report-list` | GET `/reports` | Report list. |
| (pass-through) | GET `/charts`, `/sync/targets`, `/audit/events`, `/nexus/search?q=` | Version-dependent. |
| `health` | GET `/health` | Public `{status:"ok",service:"zy-action-foundry"}`. |

## 3. LightGotham (gotham, 18083) — Intelligence Analysis

| Script command | Method + path | Notes |
| --- | --- | --- |
| `search --query "…" --limit 5` | GET `/search?q=&limit=` | Unified search across four data domains (resolved entities / graph nodes / timeline / geo features), `data.categories[]`. |
| `graph-nodes` | GET `/graph/nodes` | Knowledge-graph nodes (ABAC-filtered). |
| `graph-stats` | GET `/graph/stats` | Graph statistics (nodes/edges). |
| `entity-list` | GET `/ingestion/entities` | Multi-source resolved entity list. |
| `timeline-events` | GET `/timeline/events` | Timeline events (optional `?range=`). |
| `map-features` | GET `/map/features` | Map features (points/polygons). |
| `report-list` | GET `/reports` | Intel report list. |
| `health` | GET `/health` | Public `{status:"ok",service:"zy-action-gotham"}`. |

## 4. LightApollo (apollo, 18082) — Deployment Platform

| Script command | Method + path | Notes |
| --- | --- | --- |
| `apollo-docs` | GET `/docs` | **Public**: full protected-route inventory (method/path/perm), public routes, error-code map. Use it to introspect the actual version first. |
| `desired-state-list` | GET `/desired-states` | Desired-state list. |
| `deployment-list` | GET `/deployments` | Deployment list. |
| `deployment-status --deployment-id <id>` | GET `/deployments/{id}` | Deployment detail. |
| `drift-list` | GET `/drift/events` | Drift events. |
| `bundle-list` | GET `/bundles` | Bundle artifact list. |
| `agent-list` | GET `/agents` | Spoke Agent node list. |
| `health` | GET `/health` | Public `{status:"ok",service:"zy-action-apollo"}`. |

## 5. LightSwift (swift, 18084)

Health check only: `GET /health`, `GET /api/health` (public). To verify a login, `login --product swift`.

## 6. Non-built-in Endpoints: curl / Pass-through Examples

```
# curl direct example (log in first to get a token):
curl -s -X POST http://127.0.0.1:18080/api/v1/auth/login -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"admin1"}'

# pass-through: Foundry metric catalog (GET allowed by default, no token attached)
python3 scripts/zy_platform.py request --product foundry --method GET --path=metrics/catalog
# pass-through with query (add --with-token after user consent when auth is needed)
python3 scripts/zy_platform.py request --product gotham --method GET --path=search --query-str 'q=orders&limit=3' --with-token
# pass-through with body (POST needs --allow-write; preview with --dry-run and confirm first)
python3 scripts/zy_platform.py request --product aip --method POST --path=chat --data '{"query":"Top 5 sales by region"}' --allow-write
```

> Note: Windows Git Bash may convert leading-`/` arguments into paths, so `--path` must **not start with `/`** (the script joins it to the API root).
