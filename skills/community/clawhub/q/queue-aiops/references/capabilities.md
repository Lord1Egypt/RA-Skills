# queue-aiops — full capability reference

## Platforms

| Platform | Protocol | Auth | Default port |
|----------|----------|------|:---:|
| `redis` | RESP wire protocol via the `redis` Python client (30s socket timeouts, `decode_responses=True`) | `AUTH` password — **optional** (auth-less lab instances supported); TLS optional (`use_tls`, `verify_ssl`) | 6379 |
| `rabbitmq` | Management HTTP API (`/api/...`) via httpx (30s timeout) | HTTP Basic — management user (needs the `monitoring` or `management` tag) | 15672 |

A name-keyed platform registry (`queue_aiops/platform.py`) maps each target's
`platform` field to its protocol shape. New broker families are additive
registry entries — the ops/CLI/MCP layers don't change.

### redis command surface (typed allow-list — no generic passthrough)

`PING`, `INFO [section]`, `SLOWLOG GET`, `CLIENT LIST`, `CLIENT KILL ID/ADDR`,
`CONFIG GET`, `CONFIG SET`, `MEMORY STATS`, `MEMORY USAGE`, `SCAN`
(budgeted), `DBSIZE`. Never `KEYS *`.

Big-key sampling budget (named constants in `ops/redis_reads.py`):
`SCAN_BUDGET_KEYS=10000`, `SCAN_PAGE=500`, `MEMORY_SAMPLE_MAX=200`,
`TOP_KEYS=20`. `coveragePct` reports how partial the walk was.

### rabbitmq management-API paths (all interpolated segments percent-encoded)

`/api/overview`, `/api/nodes`, `/api/whoami`, `/api/queues[/{vhost}[/{name}]]`,
`/api/queues/{vhost}/{name}/contents` (purge), `/api/connections`,
`/api/channels`, `/api/consumers`, `/api/policies[/{vhost}[/{name}]]`.
The default vhost `/` is sent as `%2F`.

## Tools (28)

### Overview (1)

| Tool | Returns |
|------|---------|
| `queue_overview(target?)` | Platform-dispatched one-shot: redis → version/role, memory posture, clients, ops/sec, hit rate, key count; rabbitmq → version, queue/message totals, connections/channels/consumers, rates, node alarms. Partial failures degrade into an `errors` list. |

### redis reads (7)

| Tool | Returns |
|------|---------|
| `redis_server_info` | version, mode, role, uptime, clients, blocked clients, ops/sec, hit rate |
| `redis_memory_stats` | usedBytes vs maxmemoryBytes (+ usedPctOfMax), maxmemory policy, fragmentation ratio, RSS/peak, key count |
| `redis_clients` | clients (bounded 200) + grouped `bySource` (ip without port), busiest first |
| `redis_slowlog(count?)` | slowlog entries, slowest first (durationUs, command folded to one string) |
| `redis_config_get(pattern?)` | CONFIG GET glob → sorted parameter map |
| `redis_keyspace` | per-db keys/expires/avgTtl + expiry coverage % |
| `redis_big_keys(top?)` | SCAN-budgeted big-key sample, largest first, with budget + coveragePct |

### rabbitmq reads (7)

| Tool | Returns |
|------|---------|
| `rabbitmq_overview` | version, cluster, queue/message totals, object counts, publish/deliver/ack rates, connection/channel churn rates |
| `list_queues(vhost?)` | queues deepest-backlog first: messages/ready/unacked, consumers, rates, memory |
| `queue_detail(vhost, name)` | one queue: counts, rates, durable/auto_delete/arguments, node, consumer utilisation |
| `list_connections` | connections + grouped `byPeerHost` (connection + channel counts) |
| `list_channels` | channels most-unacked first: unacked, prefetch, consumer count |
| `list_policies(vhost?)` | policies: pattern, apply-to, priority, definition |
| `node_health` | per node: mem used/limit + alarm, disk free/limit + alarm, fd/socket usage |

### Flagship analyses (4) — transparent heuristics, injectable telemetry

| Tool | Thresholds (named constants) | Verdicts |
|------|------------------------------|----------|
| `redis_memory_pressure_rca(used_pct?, telemetry?)` | `DEFAULT_USED_PCT=85`, `FRAG_HIGH_RATIO=1.5`, `FRAG_SWAP_RATIO=0.8`, `BIG_KEY_MIN_BYTES=10MiB` | noeviction near limit (writes will OOM) / eviction pressure / active eviction / fragmentation / likely swapping / oversized sampled keys |
| `redis_latency_rca(slow_us?, telemetry?)` | `SLOW_US=10000`, `FORK_STALL_US=100000`, heavy-command set (O(N)/blocking) | slow command patterns (heavy ones get an incremental-variant action) / blocked clients / fork stall / delayed AOF fsync / persistence job running / dataset loading |
| `rabbitmq_queue_backlog_rca(vhost?, top?, queues?, nodes?)` | `BACKLOG_MIN_MESSAGES=1000`, `UNACKED_PCT_HIGH=50`, `RATE_DEFICIT_FACTOR=1.2` | per queue: no consumers / unacked pileup / publish outpaces delivery / residual backlog; global: memory & disk watermark alarms (publishers blocked) |
| `connection_churn_analysis(snapshot?, history?)` | `CHURN_RATE_HIGH=1/s`, `CHANNELS_PER_CONN_HIGH=20`, `REDIS_CONN_RATE_HIGH=5/s` | redis: reconnect-per-operation churn, maxclients rejections; rabbitmq: connection churn, channel-leak ratio, growth vs a prior snapshot; both: clients grouped by source |

All four accept injected telemetry for pure analysis (no live pull), and every
finding carries `cause`, `action`, and `evidence` numbers.

### Governed writes (7)

| Tool | Risk | Prior state captured | Undo |
|------|:---:|----------------------|------|
| `redis_config_set(parameter, value)` | medium | prior value via CONFIG GET (param name validated) | set the prior value back |
| `redis_kill_client(client_id?/addr?)` | medium | the client's CLIENT LIST row (who/where/last command) | none — connection gone (clients reconnect) |
| `declare_queue(vhost, name, durable?, auto_delete?, arguments?)` | medium | whether the queue existed | delete the queue — only when newly created |
| `set_policy(vhost, name, pattern, definition, priority?, apply_to?)` | medium | the prior policy (or "did not exist") | restore prior policy, or delete-if-new |
| `delete_policy(vhost, name)` | medium | the policy's full definition | re-create the captured policy |
| `purge_queue(vhost, name)` | **high** | message count about to be destroyed | none — messages unrecoverable |
| `delete_queue(vhost, name)` | **high** | full queue definition + message count | re-declare the captured definition (**messages NOT restored**) |

Every write takes `dry_run` (MCP) / `--dry-run` + double-confirm (CLI); the two
high-risk writes (`purge_queue`, `delete_queue`) are gated by that same dry-run
preview + double confirmation at the CLI, nothing more.

### Undo (2)

| Tool | Returns |
|------|---------|
| `undo_list(limit?)` | recorded undo descriptors, newest first, with their `_undo_id` |
| `undo_apply(undo_id, dry_run?)` | replays the recorded inverse (governed like any other write) |

## Environment variables

| Variable | Purpose |
|----------|---------|
| `QUEUE_AIOPS_HOME` | Relocate `~/.queue-aiops` (audit/undo/config state) |
| `QUEUE_AIOPS_CONFIG` | Explicit config.yaml path for the MCP server |
| `QUEUE_AIOPS_MASTER_PASSWORD` | Unlock the encrypted secret store non-interactively |
| `QUEUE_AUDIT_APPROVED_BY` / `QUEUE_AUDIT_RATIONALE` | Optional approver/rationale annotations recorded on the audit row |
| `QUEUE_MAX_TOOL_CALLS` / `QUEUE_MAX_TOOL_SECONDS` | Budget ceilings |
| `QUEUE_RUNAWAY_MAX` / `QUEUE_RUNAWAY_WINDOW_SEC` | Runaway-loop breaker tuning |
| `QUEUE_<TARGET>_SECRET` | Legacy plaintext secret fallback (deprecated) |
