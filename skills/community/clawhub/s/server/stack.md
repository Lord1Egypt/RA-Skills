# Choosing the Serving Stack

Read before standing up a new box or replacing an edge. The decision is made once and lived with for years, so it is made from constraints, not taste. Defaults live in SKILL.md's Stack Defaults table; this file is the reasoning behind them and the cases where they flip.

**Before recommending anything**, read `## Stack` and `## Services` in `~/Clawic/data/server/memory.md` (or `services.md` if `## Boxes` points there): a second proxy on a box that already has one is not a choice, it is an incident waiting for port 443.

**Contents:** [The Three Questions](#the-three-questions) · [Edge: Who Terminates HTTPS](#edge-who-terminates-https) · [Proxy Comparison](#proxy-comparison) · [Supervisor Comparison](#supervisor-comparison) · [Runtime-Specific Serving](#runtime-specific-serving) · [Sockets vs Ports](#sockets-vs-ports) · [One Box or Several](#one-box-or-several) · [Migrating Between Stacks](#migrating-between-stacks) · [Write It Down](#write-it-down)

## The Three Questions

1. **How many things does the edge route to, and do they change?** One static app → the proxy is a config file you edit twice a year. Containers appearing and disappearing → label-driven routing earns its complexity.
2. **Who owns the certificate?** If the answer is "a CDN in front", the local proxy never sees a private key and the whole ACME layer disappears. If it is "this box", the proxy's renewal story is the deciding feature.
3. **What is already installed and understood?** The best proxy is the one whose error messages the person on call can read. A stack nobody understands fails open at the worst moment.

Everything else — benchmarks, feature matrices — moves the answer far less than these three.

## Edge: Who Terminates HTTPS

| Situation | Terminate at | Why |
|---|---|---|
| Public site, global audience | CDN, re-encrypt or private-network hop to origin | Latency and egress dominate; the origin gets a stable, warm connection pool |
| Single region, own domain | The box, automatic ACME | One less provider in the failure path; certificates renew unattended |
| Regulated or sensitive payload | End to end, terminate on the box only | An edge that decrypts is an edge that holds plaintext |
| Internal service, private network | Terminate at the internal load balancer, or run plaintext inside a trusted subnet | Certificate management for machine-to-machine traffic buys little unless the network is untrusted |
| Client certificates (mTLS) required | Wherever mTLS is verified — that hop must be the terminator | Forwarding a client certificate through a terminator loses the cryptographic proof; headers only carry a claim |

Terminating at a CDN and *also* on the box (full-strict mode) is normal and costs one extra handshake per origin connection, amortized by keepalive. Terminating at the CDN and serving plaintext on a public origin port is not a configuration, it is an exposure (`security.md`).

## Proxy Comparison

| | Caddy | nginx | Traefik | HAProxy |
|---|---|---|---|---|
| Certificates | Automatic, on by default, renewal and reload handled internally | External (certbot/acme.sh) plus a reload hook you must write | Automatic via resolvers, per-router | External, and it wants the full chain concatenated with the key in one file |
| Config style | A few lines per site | Explicit and verbose; every behavior is a directive you can find | Labels and dynamic providers; little static config | Frontend/backend blocks, closest to a load balancer's mental model |
| Best at | Getting HTTPS right with the least surface | Fine control of the request path, and the largest body of existing answers | Containers that come and go without editing files | Very high connection counts, TCP/UDP, sophisticated health checks and queueing |
| Weak at | Directives that simply are not exposed | Manual certificate lifecycle, easy misconfiguration of headers | Debuggability — the routing lives in labels scattered across compose files | HTTP conveniences; static files are not its job |
| Reload | `caddy reload`, graceful | `nginx -s reload`, graceful | Watches the provider, applies automatically | `-sf` seamless reload, graceful |

Defaults that follow: **Caddy** when nobody wants to think about certificates; **nginx** when the team already knows it or the request path needs surgery (`nginx` skill); **Traefik** only with a dynamic container fleet; **HAProxy** when the constraint is connections or non-HTTP protocols, not features.

Running two proxies in series (edge proxy → per-app proxy) is legitimate exactly once: when the inner one belongs to a packaged app you do not control. Otherwise each extra hop adds its own timeout, its own buffer, and one more place `X-Forwarded-For` can be dropped.

## Supervisor Comparison

| | systemd | PM2 | supervisord | Container restart policy |
|---|---|---|---|---|
| Starts at boot | Yes, once enabled | Only via a generated unit or startup script — the step people skip | Via its own service | With the container daemon, if the policy says so |
| Resource limits | Native cgroup limits: memory, CPU, tasks, fds | No real enforcement | No | Native, via the runtime |
| Sandboxing | Extensive (`security.md`) | None | None | Namespace isolation |
| Log handling | journald, structured, rotated by its own rules | Files it manages, rotation via a plugin | Files it manages | Runtime driver |
| Multi-process | One unit per process, or a template unit | Cluster mode built in for Node | Program groups | Replicas via the orchestrator |
| Worth it when | Anything that must survive a reboot on a VM | The team lives in Node tooling and wants `pm2 reload` ergonomics | Legacy boxes, or Python apps in an image that needs several processes | The box is already Compose-shaped |

PM2's real trap: it supervises processes but nothing supervises PM2 unless its startup unit was generated and enabled. A crashed PM2 daemon takes every app with it, silently.

## Runtime-Specific Serving

| Runtime | Serve with | Do not |
|---|---|---|
| Node/Bun | The app's own HTTP server behind a proxy, one process per core | Put it directly on 443 as root, or add a Node proxy in front of a Node app |
| Python WSGI (Django, Flask) | Gunicorn, sync workers for fast handlers, `gthread` for slow clients | Use the framework's dev server; it is single-threaded and unhardened by design |
| Python ASGI (FastAPI, Starlette) | Gunicorn with uvicorn workers, or uvicorn with `--workers` | Mix sync blocking calls into async handlers — one blocked handler stalls the whole loop |
| Ruby (Rails) | Puma, workers × threads; threads only pay off on IO-bound work | Assume threads scale CPU-bound work; MRI's global lock says otherwise |
| PHP | php-fpm pools behind the proxy | Run PHP through CGI, or share one pool between apps with different memory profiles |
| Go/Rust | The compiled binary, directly behind the proxy | Add an application server; there is nothing for it to do |
| Java | The embedded server (Spring Boot, Quarkus) behind the proxy | Deploy a WAR into a separate container unless the platform requires it |
| Static site | Proxy or CDN from disk | Boot a Node process to serve files a proxy serves faster with one directive |

## Sockets vs Ports

Unix domain socket between proxy and app on the same host: no TCP stack, no port to expose, no ephemeral-port exhaustion, and file permissions become the access control. Cost: the socket file needs the right owner and mode (proxy user must have write access), and it does not survive the app moving to another host.

TCP on loopback: trivially portable, observable with standard tooling, and the only option across hosts. Cost: a real port that must be bound to `127.0.0.1` (Rule 7) and a listen backlog that can overflow.

Default to a socket for single-host proxy→app, TCP for anything crossing a machine. Sockets that stop working after a deploy are almost always ownership: the release created a fresh socket as a different user.

## One Box or Several

Splitting is warranted when a resource is genuinely contended, not when the box "feels loaded":

| Signal | Split |
|---|---|
| Database IO starves the app during backups or vacuum | Database onto its own machine first — it is the split with the biggest effect |
| One app's memory spike OOM-kills the others | Either split, or set per-service memory limits and accept that one service dies alone |
| Deploy of app A must not risk app B | Split, or containerize so a bad deploy cannot take the runtime with it |
| CPU saturated at peak with everything already tuned | Add a second app box behind the proxy before making one box bigger |
| "It feels slow" | Measure first (`capacity.md`); most single-box limits are one config value |

Vertical growth is one reboot; horizontal growth introduces shared state, sticky sessions, distributed logs and a health-checked upstream pool. Take vertical until it stops being available or stops being cheaper.

## Migrating Between Stacks

Order that avoids downtime, whatever the direction:

1. Install the new proxy on a **different port** (8443) and configure it fully.
2. Test with an explicit port and a hosts-file override — every route, plus uploads, WebSockets, and one redirect.
3. Move certificates or let the new proxy issue its own for a test subdomain first.
4. Stop the old proxy and start the new one on 80/443 in one window; keep the old config on disk unchanged.
5. Rollback is starting the old one again — which stays true only while you have not deleted its config.

Write the cutover plan to `~/Clawic/data/server/artifacts/cutover-<from>-to-<to>.md` before step 1, and the topology decision (what was chosen, what was rejected, the reason) to `artifacts/decision-<topic>.md`. Both get their `## Boxes` line in `memory.md` in the same turn.

## Write It Down

After a stack is chosen or changed, record it in the same session (`memory-template.md`): the stack itself in `## Stack`, every service it fronts in `## Services` with its listen address and supervisor, the host in the shared `~/Clawic/data/servers/servers.md`, and the reasoning as a decision artifact. A stack choice with no written reason gets re-litigated every time somebody new reads the config.
