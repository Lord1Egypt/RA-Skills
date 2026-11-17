---
name: proxy-aiops
slug: proxy-aiops
displayName: "Proxy AIops"
summary: "Governed Traefik + Caddy + HAProxy ops: routes, upstreams, certs, 5xx RCA. 28 tools."
license: MIT
homepage: https://github.com/AIops-tools/Proxy-AIops
tags: [aiops, mcp, governance, proxy]
description: >
  Use this skill whenever the user needs to operate a Traefik, Caddy or HAProxy reverse proxy / load balancer — a one-shot overview, routes (routers / caddy routes / frontends) with host/path matching, services and server-level upstream health, middlewares, TLS certificate inventory with an expiry sweep, traffic and 5xx error counters, config snapshot/search, four flagship RCAs (backend health, cert expiry, error rate, route conflicts), and governed writes (caddy config set/delete/load with prior-config capture; haproxy server drain/maint/ready and weight).
  Always use this skill for "Traefik", "Caddy", "HAProxy", "reverse proxy", "load balancer", "upstream down", "502/503/504 errors", "bad gateway", "cert expiring", "TLS certificate", "route not matching", "which route serves this host", "drain a server", "server weight", "redirect loop" when the context is a Traefik/Caddy/HAProxy edge.
  Do NOT use when the target is something other than a Traefik/Caddy/HAProxy proxy (a hypervisor, storage appliance, backup product, container-orchestration cluster, multi-vendor router/switch config, or OT/industrial equipment) — route those to the appropriate other AIops-tools skill. Do NOT use for firewall rules — use firewall-aiops. Managed cloud load balancers are out of scope.
  Governed proxy operations with a built-in governance harness (audit, policy, token budget, undo, risk-tiers). Behaviour is validated by a mock-based test suite; see docs/VERIFICATION.md for the live-verification checklist.
installer:
  kind: uv
  package: proxy-aiops
argument-hint: "[a route/service/backend name, a hostname, or describe your proxy task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["proxy-aiops","uvx"]},"optional":{"env":["PROXY_AIOPS_CONFIG","PROXY_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/Proxy-AIops","emoji":"🔀","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed reverse-proxy operations across Traefik (API /api/..., metrics-text counters via /metrics), Caddy (admin API, default localhost:2019 — carries the write surface) and HAProxy (Data Plane API v2 /v2/..., HTTP Basic auth). Each target in the config names its own platform, and a name-keyed platform registry selects the API shape; an explicit support matrix raises teaching errors for ops a platform cannot do (traefik writes → its providers; caddy error counters → access logs; haproxy certs → the .pem pipeline), never a silent no-op. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency.
  All write operations are audited to a local SQLite DB under ~/.proxy-aiops/ (relocatable via PROXY_AIOPS_HOME).
  Credentials: the HAProxy Data Plane API password (required) or an optional Basic-auth credential for Traefik/Caddy is stored ENCRYPTED in ~/.proxy-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Traefik and Caddy usually run unauthenticated on localhost, so their secret is optional (no store entry = no auth header). Run 'proxy-aiops init' to onboard (it asks for the platform), or 'proxy-aiops secret set <target>'. The store is unlocked by a master password from PROXY_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var PROXY_<TARGET_NAME_UPPER>_SECRET is still honoured as a fallback with a deprecation warning (migrate with 'proxy-aiops secret migrate'). Secrets are never logged or echoed.
  State-changing operations pass through the @governed_tool decorator (budget guard + audit + risk-tier labelling). delete_config_path and load_config (full config replace) are risk=high with dry_run + double confirmation at the CLI. Reversible writes (set_config_value, delete_config_path, load_config, set_server_state, set_server_weight) capture the real fetched before-state and record an inverse undo descriptor whose params replay against the tool's own signature.
  Webhooks: none — no outbound network calls beyond the configured proxy APIs, plus (only when the operator runs the cert sweep with probing) a bounded TLS handshake per inventoried domain.
  SSL: verify_ssl defaults to true; disable only for self-signed lab certs.
  Transitive dependencies: httpx (HTTP client), cryptography (secret store + cert parsing), and the MCP SDK. No post-install scripts or background services.
---

# Proxy AIops

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by Traefik Labs, the Caddy project, HAProxy Technologies, or the HAProxy project.** Traefik, Caddy and HAProxy are trademarks of their respective owners. Source at [github.com/AIops-tools/Proxy-AIops](https://github.com/AIops-tools/Proxy-AIops) under the MIT license.

Governed reverse-proxy operations — **28 MCP tools** across **Traefik** (API +
`/metrics`), **Caddy** (admin API) and **HAProxy** (Data Plane API v2), every
one wrapped with the bundled `@governed_tool` harness: a local unified audit
log under `~/.proxy-aiops/`, policy engine, token/runaway budget guard,
undo-token recording, and descriptive risk tiers. A per-target
`platform` field selects the API shape, so the same tools work on all three
proxies and one config can span a mixed edge. An explicit **support matrix**
raises teaching errors for ops a platform cannot do — never a silent no-op.
Credentials are stored **encrypted** (`~/.proxy-aiops/secrets.enc`, Fernet +
scrypt) — never plaintext on disk; Traefik/Caddy secrets are optional
(unauthenticated localhost is the common case).

> **Standalone**: the governance harness is bundled in the package
> (`proxy_aiops.governance`) — no external skill-family dependency. Behaviour is
> covered by a mock-based test suite; `docs/VERIFICATION.md` is the checklist for a
> live run (all three platforms are free/self-hostable, so a small lab is enough).

## What This Skill Does

| Group | Tools | Count | R/W |
|-------|-------|:-----:|:---:|
| **Status** | proxy_overview, version_info, list_entrypoints | 3 | read |
| **Routes** | list_routes, route_detail, find_route | 3 | read |
| **Services** | list_services, service_detail, list_upstreams, upstream_detail, list_middlewares | 5 | read |
| **Certificates** | list_certificates | 1 | read |
| **Traffic** | traffic_stats, error_counters | 2 | read |
| **Config** | config_snapshot, search_config, get_config_value | 3 | read |
| **Flagship analyses** | backend_health_rca, cert_expiry_sweep, error_rate_rca, route_conflict_analysis | 4 | read |
| **Writes (caddy)** | set_config_value (med), delete_config_path (**high**), load_config (**high**) | 3 | write |
| **Writes (haproxy)** | set_server_state, set_server_weight | 2 | write (med) |
| **Undo** | undo_list, undo_apply | 2 | read / write |

The four flagship analyses are transparent heuristics that report their
numbers, never a black-box verdict: `backend_health_rca` groups down upstreams
per service and maps the health-check failure class (connection refused / L4
timeout / TLS / L7 / DNS / maint) to a cause + action; `cert_expiry_sweep`
buckets certs by days-to-expiry with per-platform renewal hints;
`error_rate_rca` ranks services by 5xx share vs the fleet baseline and maps
the dominant code (502/503/504/500) to a cause; `route_conflict_analysis`
finds shadowed routes, dead routes, and redirect loops.

## Quick Install

```bash
uv tool install proxy-aiops
proxy-aiops init       # wizard: pick platform (traefik/caddy/haproxy) + optional encrypted secret
proxy-aiops doctor
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/proxy-aiops
openclaw skills info proxy-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Get a one-shot snapshot (`overview` / `version_info` / `list_entrypoints`)
- Investigate 502/503/504 spikes (`error_rate_rca`) → dominant code → cause
- Find why an upstream/backend is down (`list_upstreams`, `backend_health_rca`)
- Sweep TLS cert expiry across the edge (`certs --sweep` / `cert_expiry_sweep`)
- Audit routing hygiene (`route_conflict_analysis` — shadowed/dead routes,
  redirect loops) and answer "which route serves this host?" (`find_route`)
- Safely drain/return an haproxy server (`set_server_state`, reversible +
  undo-recorded) or adjust its weight (`set_server_weight`)
- Safely edit caddy config (`set_config_value` / `delete_config_path` /
  `load_config` — prior config captured, undo replays the restore)

**Do NOT use when** the target is not a Traefik/Caddy/HAProxy proxy — route
hypervisor, storage, backup, cluster, network-device, or OT/industrial work to
the appropriate other AIops-tools skill. Do NOT use for firewall rules — use
firewall-aiops.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| Traefik / Caddy / HAProxy proxy ops | **proxy-aiops** (this skill) |
| Firewall rules / NAT / gateway health | **firewall-aiops** |
| A non-proxy platform (hypervisor, storage, backup, cluster, network devices, OT edge) | the appropriate **other AIops-tools** skill |
| Managed cloud load balancers | out of scope for this tool |

## Common Workflows

### 1. A 5xx spike — is it the app or the backend?

1. `proxy-aiops doctor` → confirm the proxy's API is reachable before you trust any
   number that follows.
2. `proxy-aiops overview` → the one-shot picture: platform/version, entrypoints, and
   route/service counts, so you know the blast radius.
3. `proxy-aiops analyze errors --rate 5 --min-requests 100` → services ranked by 5xx
   share against the fleet baseline, with the **dominant status code mapped to a cause**
   (503 no upstream available / 502 connection failed / 504 timeout / 500 app error).
   The `--min-requests` floor keeps a single failed request on a quiet service from
   outranking a real incident.
4. `proxy-aiops analyze health --service <name>` → the same service from the backend
   side: which servers are failing their health check and what class of failure it is.
   If the servers are healthy, the 5xx is coming from **the application**, and no amount
   of proxy work will fix it — hand it off.
5. If one server is the problem, take it out of rotation gracefully:
   `proxy-aiops services upstreams <backend>` to get the exact server name, then
   `proxy-aiops server state <backend> <server> drain --dry-run` and re-run for real
   (double-confirm; the prior state is captured as the undo descriptor). `drain` lets
   in-flight connections finish — reach for `maint` only when you need it out *now*.
6. Re-run `proxy-aiops analyze errors` to confirm the rate dropped.
7. **Failure branch**: if draining one server just moves the load onto the next one to
   fall over, you are shedding capacity you do not have — put it straight back with
   `proxy-aiops undo list` → `undo apply <id>` (restores the **prior** state, not a
   hardcoded `ready`) before you drain a second. Note `server state` / `server weight`
   are **haproxy runtime** operations; on a traefik or caddy target the tool raises a
   teaching error naming the right mechanism rather than silently doing nothing.

### 2. Certificates about to expire

1. `proxy-aiops certs --sweep --warn-days 30 --critical-days 7` → the TLS domain
   inventory with each cert **live-probed** on port 443 and bucketed
   expired / critical / warning, plus a renewal hint.
2. `proxy-aiops certs --sweep --port 8443` for any entrypoint not on 443 —
   the sweep probes one port at a time, so a non-standard listener needs its own pass.
3. `proxy-aiops overview` and `proxy-aiops routes list` → map each expiring domain back
   to the routes that actually serve it, so you renew what is in use and ignore what is
   not.
4. Renew through the platform's own mechanism (ACME for traefik/caddy), then re-run the
   sweep to confirm the new expiry date.
5. **Failure branch**: on a **haproxy** target the sweep returns a teaching note rather
   than results — haproxy serves certs from `.pem` files on disk, outside this tool's
   API surface, so check those with your file-level tooling. If a probe fails to connect,
   distinguish "cert is bad" from "port is closed" with
   `proxy-aiops routes find <host>` before assuming a certificate problem.

### 3. "Why is this hostname hitting the wrong backend?"

1. `proxy-aiops routes find <host> --path /api` → best-matching routes, most specific
   first. This is the direct answer to "who serves this request".
2. `proxy-aiops routes show <route-id>` → the full rule, priority, middlewares, and the
   service it points at.
3. `proxy-aiops analyze conflicts` → **shadowed** routes (fully covered by an earlier or
   higher-priority route), **dead** routes (the service is missing, or has zero servers
   up), and redirect loops — each finding names the covering route or the missing
   service rather than just flagging a number.
4. `proxy-aiops services show <service>` and `proxy-aiops services upstreams <service>`
   → confirm the service the route resolves to actually has healthy servers behind it.
5. Fix the ordering/priority at its source: on **caddy** via `proxy-aiops config set`
   (recipe 4); on **traefik**, in the provider that generated the route (labels, file
   provider, CRD) — traefik's API is read-only, and the tool says so explicitly instead
   of pretending to write.
6. **Failure branch**: if `routes find` returns nothing, the request is not matching any
   route at all — check `proxy-aiops overview` for the entrypoints and confirm the
   listener you think you are hitting exists. A "dead route" finding whose service is
   missing usually means a config was applied referencing a service that was never
   created; fixing the route without creating the service just moves the 404.

### 4. Edit a caddy config subtree, reversibly

1. `proxy-aiops config snapshot` → the whole current config; take this **before** you
   change anything, so you have an out-of-band copy independent of the undo store.
2. `proxy-aiops config search <needle>` → locate the config path holding the value you
   want (searching beats guessing at caddy's nested JSON paths).
3. `proxy-aiops config get <path>` → read the exact current subtree you are about to
   replace.
4. `proxy-aiops config set <path> '<json>' --dry-run` → preview the write.
5. Re-run without `--dry-run` (double-confirm) — the prior subtree is fetched and
   captured, and an inverse undo descriptor is recorded with an `_undo_id`.
6. Validate: `proxy-aiops routes list`, `proxy-aiops analyze conflicts`, and
   `proxy-aiops analyze errors` → confirm the edit did what you meant and did not
   shadow an existing route.
7. **Failure branch**: `proxy-aiops undo list` → `undo apply <id>` restores the captured
   subtree exactly. If the config is too broken for a targeted undo, the
   `config snapshot` from step 1 is your fallback via `load_config` — but note
   `load_config` and `config delete` are **risk=high** with `--dry-run` + double
   confirmation at the CLI. `load_config` replaces the *entire* config, so it is a
   last resort, not a first instinct.

## Governance & Safety

The skill delivers reads and writes and records them; it does **not** decide
whether a write is permitted. That is your agent's judgement, or the permission
of the account you connect it with (a read-only HAProxy Data Plane API role, a
scoped Traefik/Caddy admin API — writes then fail at the server). There is no
read-only switch, policy file, or approval gate.

- **Audit is the guarantee, and it is not bypassable.** Every operation — MCP and CLI alike — is logged to `~/.proxy-aiops/audit.db` (relocatable via `PROXY_AIOPS_HOME`): params (secrets redacted), outcome summary, status, duration, and the risk tier. The CLI writes the same row the MCP path does.
- `PROXY_AUDIT_APPROVED_BY` / `PROXY_AUDIT_RATIONALE` are optional annotations recorded on the audit row (who/why); they are never required and never block.
- **Runaway guard** — a safety backstop, not authorization: the same call looped in a tight window trips a circuit breaker. Disable with `PROXY_RUNAWAY_MAX=0`.
- Writes support `--dry-run` / `dry_run=True` and double confirmation at the CLI; CLI writes execute through the same governed tools, so they are audited + undo-recorded.
- Reversible writes capture the real fetched before-state and record an inverse descriptor that replays against the tool's own signature.
- Traefik targets accept no writes at all — the support matrix teaches you to
  edit the provider source instead.

## References

- `references/capabilities.md` — full tool + platform + API-path reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — onboarding, credentials, and connectivity
- `docs/VERIFICATION.md` — live-verification checklist (what the mock suite covers, and what a real-proxy run must prove)
