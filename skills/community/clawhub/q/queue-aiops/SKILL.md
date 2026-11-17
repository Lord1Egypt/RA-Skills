---
name: queue-aiops
slug: queue-aiops
displayName: "Queue AIops"
summary: "Governed redis + rabbitmq ops: memory/latency/backlog/churn RCA, policies. 28 tools."
license: MIT
homepage: https://github.com/AIops-tools/Queue-AIops
tags: [aiops, mcp, governance, queue]
description: >
  Use this skill whenever the user needs to operate a redis cache or a rabbitmq broker — a one-shot overview, redis memory posture (used vs maxmemory, eviction policy, fragmentation), SLOWLOG and a SCAN-budgeted big-key sample (never KEYS *), connected clients, CONFIG get/set, rabbitmq queues with backlog depth, connections/channels, policies and node watermark alarms, four flagship RCAs (redis memory pressure, redis latency/slowlog, rabbitmq queue backlog, connection churn on both platforms), and governed writes (set a config parameter, kill a client, declare/purge/delete a queue, set/delete a policy).
  Always use this skill for "redis", "rabbitmq", "maxmemory", "eviction", "evicted keys", "big key", "slowlog", "why is my cache slow", "queue backlog", "messages piling up", "no consumers", "unacked messages", "memory watermark", "connection churn", "purge a queue", "rabbitmq policy" when the context is a redis or rabbitmq deployment.
  Do NOT use when the target is something other than a redis/rabbitmq broker (a hypervisor, storage appliance, backup product, container-orchestration cluster, database server, monitoring stack, or OT/industrial equipment) — route those to the appropriate other AIops-tools skill. Managed cloud queue services and other broker products are out of scope.
  Governed broker operations with a built-in governance harness (audit, policy, token budget, undo, risk-tiers). Behaviour is validated by a mock-based test suite; see docs/VERIFICATION.md for the live-verification checklist.
installer:
  kind: uv
  package: queue-aiops
argument-hint: "[a queue/key/client id, or describe your cache/broker task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["queue-aiops","uvx"]},"optional":{"env":["QUEUE_AIOPS_CONFIG","QUEUE_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/Queue-AIops","emoji":"📬","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed broker operations across redis (RESP wire protocol via the redis Python client; password optional — auth-less lab instances are supported — TLS optional) and rabbitmq (management HTTP API /api/..., HTTP Basic auth with a monitoring/management-tagged user). Each target in the config names its own platform, and a name-keyed platform registry selects the protocol shape, so one config can span a mixed estate. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency.
  All write operations are audited to a local SQLite DB under ~/.queue-aiops/ (relocatable via QUEUE_AIOPS_HOME).
  Credentials: the redis password (optional) or the rabbitmq management password is stored ENCRYPTED in ~/.queue-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'queue-aiops init' to onboard (it asks for the platform), or 'queue-aiops secret set <target>' to add one. The store is unlocked by a master password from QUEUE_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var QUEUE_<TARGET_NAME_UPPER>_SECRET is still honoured as a fallback with a deprecation warning (migrate with 'queue-aiops secret migrate'). The secret is presented as AUTH at connect time (redis) or HTTP Basic auth (rabbitmq) and held only in memory; secrets are never logged or echoed.
  State-changing operations pass through the @governed_tool decorator (budget guard + audit + risk-tier labelling). purge_queue and delete_queue are risk=high with dry_run + double confirmation at the CLI; purge is irreversible (priorState = the message count about to be destroyed), and delete_queue's undo re-declares the captured queue definition — the messages are NOT restored. Reversible writes (redis_config_set, set_policy, delete_policy, declare_queue) capture the real fetched before-state and record an inverse undo descriptor.
  Safety: the redis surface is a typed command allow-list (no generic passthrough) and big-key sampling is SCAN-based under a hard budget — never KEYS *. rabbitmq path segments (queue/policy names and the default vhost '/') are percent-encoded centrally.
  Webhooks: none — no outbound network calls beyond the configured redis instances / rabbitmq management API.
  Transitive dependencies: the redis Python client, httpx (HTTP client), and the MCP SDK. No post-install scripts or background services.
---

# Queue AIops

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by the Redis or RabbitMQ projects or their respective owners.** Redis and RabbitMQ are trademarks of their respective owners. Source at [github.com/AIops-tools/Queue-AIops](https://github.com/AIops-tools/Queue-AIops) under the MIT license.

Governed broker operations — **28 MCP tools** across **redis** (RESP client) and
**rabbitmq** (management HTTP API), every one wrapped with the bundled
`@governed_tool` harness: a local unified audit log under `~/.queue-aiops/`,
policy engine, token/runaway budget guard, undo-token recording, and
descriptive risk tiers. A per-target `platform` field selects the
protocol shape, so one config can span a mixed estate. The redis password /
rabbitmq management password is stored **encrypted**
(`~/.queue-aiops/secrets.enc`, Fernet + scrypt) — never plaintext on disk.

> **Standalone**: the governance harness is bundled in the package
> (`queue_aiops.governance`) — no external skill-family dependency. Behaviour is
> covered by a mock-based test suite; `docs/VERIFICATION.md` is the checklist for a
> live run (both platforms are free/self-hostable, so a lab container is enough).

## What This Skill Does

| Group | Tools | Count | R/W |
|-------|-------|:-----:|:---:|
| **Overview** | queue_overview | 1 | read |
| **redis** | redis_server_info, redis_memory_stats, redis_clients, redis_slowlog, redis_config_get, redis_keyspace, redis_big_keys | 7 | read |
| **rabbitmq** | rabbitmq_overview, list_queues, queue_detail, list_connections, list_channels, list_policies, node_health | 7 | read |
| **Flagship analyses** | redis_memory_pressure_rca, redis_latency_rca, rabbitmq_queue_backlog_rca, connection_churn_analysis | 4 | read |
| **Writes** | redis_config_set, redis_kill_client, declare_queue, set_policy, delete_policy | 5 | write (med) |
| **Writes** | purge_queue, delete_queue | 2 | write (**high**) |
| **Undo** | undo_list, undo_apply | 2 | read / write |

The four flagship analyses are transparent heuristics that report their numbers,
never a black-box verdict: `redis_memory_pressure_rca` reads used-vs-maxmemory +
eviction policy + fragmentation + the big-key sample into a cause + action;
`redis_latency_rca` digests the SLOWLOG by command pattern and adds fork/AOF
stall signals; `rabbitmq_queue_backlog_rca` classifies each deep queue (no
consumers / unacked pileup / rate deficit) and reports watermark alarms that
block all publishers; `connection_churn_analysis` works on both platforms and
pins churn to client sources.

## Quick Install

```bash
uv tool install queue-aiops
queue-aiops init       # wizard: pick platform (redis/rabbitmq) + encrypted secret
queue-aiops doctor
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/queue-aiops
openclaw skills info queue-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Get a one-shot snapshot (`overview` / `redis_server_info` / `rabbitmq_overview`)
- Investigate cache memory pressure (`analyze memory`) → cause + action
  (raise maxmemory vs fix eviction policy vs split big keys)
- Chase latency (`analyze latency`, `redis slowlog`) → O(N) command patterns,
  blocked clients, fork/AOF stalls
- Triage a growing queue (`analyze backlog`, `rabbitmq queues`) → per-queue
  cause (no consumers / unacked pileup / slow consumers) + watermark alarms
- Spot connection churn or leaks (`analyze churn`, `redis clients`,
  `rabbitmq connections`) — clients grouped by source
- Safely change state: `redis config-set` (undo = prior value), `rabbitmq
  set-policy`/`delete-policy` (undo = prior policy), `declare-queue`, and the
  high-risk `purge`/`delete-queue` (dry-run + double confirmation; messages are
  not restorable)

**Do NOT use when** the target is not a redis/rabbitmq broker — route
hypervisor, storage, backup, cluster/orchestration, database, network,
monitoring-stack, or OT/industrial work to the appropriate other AIops-tools
skill.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| redis / rabbitmq cache & broker ops | **queue-aiops** (this skill) |
| A non-broker platform (hypervisor, storage, backup, cluster, database, network, monitoring stack, OT edge) | the appropriate **other AIops-tools** skill |
| Managed cloud queue services / other broker products | out of scope for this tool |

## Common Workflows

### 1. Redis is near maxmemory and starting to evict

1. `queue-aiops doctor` → confirm the broker is reachable and the credential (if any)
   works before you read numbers off it.
2. `queue-aiops redis memory` → used vs `maxmemory`, the eviction policy in force, and
   the fragmentation ratio, straight from `INFO memory`.
3. `queue-aiops analyze memory --used-pct 85` → findings in check order, each citing its measured
   number (order is not severity — weigh them all): **noeviction near the limit** (the dangerous one — writes will start failing
   with OOM rather than evicting), active eviction in progress, fragmentation versus real
   swapping, and oversized keys.
4. `queue-aiops redis bigkeys --count 500` → a SCAN-budgeted sample of the largest keys,
   reported **with its coverage %** so you know how much of the keyspace was actually
   examined. A low coverage number means "no big key found" is not yet an answer.
5. `queue-aiops redis keyspace` → which database the growth is in, to point the fix at
   the right workload.
6. If the policy is the problem: `queue-aiops redis config-get maxmemory*` to read the
   current values, then
   `queue-aiops redis config-set maxmemory-policy allkeys-lru --dry-run` and re-run for
   real (double-confirm; the prior value is captured from `CONFIG GET` as the undo
   descriptor).
7. **Failure branch**: switching a cache from `noeviction` to an eviction policy means
   Redis will start **deleting data** — if that instance is being used as a datastore
   rather than a cache, this is the wrong fix and you need memory instead. Reverse it
   immediately with `queue-aiops undo list` → `undo apply <id>`, which restores the
   **prior** policy rather than a default. Note `config-set` changes the running config
   only; if it must survive a restart, persist it in the config file too — the undo store
   cannot help you with a value the broker forgot on its own.

### 2. Redis got slow

1. `queue-aiops redis slowlog --limit 50` → the slowest entries the broker itself
   recorded.
2. `queue-aiops analyze latency --slow-us 10000` → the slowlog digested **by command
   pattern**, with O(N) commands flagged and an incremental variant suggested
   (`KEYS` → `SCAN`, `SMEMBERS` → `SSCAN`), plus blocked-client counts and fork/AOF stall
   signals read out of `INFO persistence`.
3. `queue-aiops redis info` → confirm whether the stalls line up with background saves
   (a fork stall is a persistence problem, not a query problem).
4. `queue-aiops redis clients` → who is connected, and how many are blocked;
   `queue-aiops analyze churn` → whether clients are reconnecting constantly, which shows
   up as latency but is really a client-configuration bug.
5. If one client is pathological: `queue-aiops redis kill-client --addr <ip:port>
   --dry-run` then for real (double-confirm).
6. **Failure branch**: `kill-client` is **irreversible and records no undo** — a killed
   connection cannot be un-killed, and a well-behaved client will simply reconnect,
   which fixes nothing while your kill is audited as a write. If latency does not
   improve, the cause is more likely the O(N) command pattern from step 2: fix the
   caller, not the connection. Killing clients in a loop will trip the runaway budget
   guard.

### 3. A RabbitMQ queue keeps growing

1. `queue-aiops rabbitmq overview` and `queue-aiops rabbitmq nodes` → check first for
   **memory or disk watermark alarms**, which block every publisher on the node and make
   every queue look broken at once.
2. `queue-aiops rabbitmq queues --vhost /` → queues sorted deepest-backlog-first.
3. `queue-aiops analyze backlog --vhost / --top 20` → the per-queue cause: **no consumers
   attached**, consumers connected but **not acking** (an unacked pile-up), or a publish
   rate simply outpacing delivery — each citing the measured counts.
4. `queue-aiops rabbitmq queue <name>` → that queue's detail: consumer count, ready vs
   unacked split, and its arguments.
5. `queue-aiops rabbitmq connections` and `queue-aiops rabbitmq channels` → confirm
   whether the consumers exist at all, and whether their prefetch is starving throughput.
6. To cap unbounded growth while the consumer is fixed:
   `queue-aiops rabbitmq set-policy backlog-cap '^orders\.' '{"max-length": 100000}'
   --apply-to queues --dry-run`, then re-run for real (reversible — the prior policy is
   captured for undo).
7. **Failure branch**: do **not** reach for `rabbitmq purge` as a first response — it is
   **irreversible, risk=high, and destroys real messages**; if the cause from step 3 was
   "no consumers", those messages are the backlog your consumers still need. Purge only
   with explicit sign-off, a `--dry-run` read first, and the CLI double confirmation.
   A `max-length` policy also **drops messages** once the cap is hit — if that is not
   acceptable, `queue-aiops undo apply <id>` restores the prior policy and the real fix
   is consumer capacity.

### 4. Retire a queue, reversibly

1. `queue-aiops overview` → the broker-wide picture across configured targets.
2. `queue-aiops rabbitmq queue <name> --vhost /` → confirm it is genuinely idle: zero
   consumers, zero ready, zero unacked. A queue with messages is not a queue you retire.
3. `queue-aiops rabbitmq policies` → check no policy still targets its name pattern, so
   you are not leaving a dangling rule behind.
4. `queue-aiops rabbitmq delete-queue <name> --vhost / --dry-run` → preview.
5. Re-run without `--dry-run` (double-confirm, risk=high) — the write
   captures the queue's definition first, so the undo descriptor **re-declares exactly
   that queue** (durability and auto-delete flags included).
6. `queue-aiops rabbitmq queues` → confirm it is gone and nothing else changed.
7. **Failure branch**: `queue-aiops undo apply <id>` re-declares the queue from the
   captured definition — but it restores the queue, **not its messages**, which are gone
   with it. Bindings created outside this tool are not captured either. If the queue
   turns out to have been in use, expect to re-create bindings by hand; that asymmetry is
   why step 2 (proving it is idle) matters more than the undo does.

## Governance & Safety

The skill delivers reads and writes and records them; it does **not** decide
whether a write is permitted. That is your agent's judgement, or the permission
of the account you connect it with (a Redis ACL user restricted to read
commands, a RabbitMQ management user with only the `monitoring` tag — writes
then fail at the broker). There is no read-only switch, policy file, or approval
gate.

- **Audit is the guarantee, and it is not bypassable.** Every operation — MCP
  and CLI alike — is logged to `~/.queue-aiops/audit.db` (relocatable via
  `QUEUE_AIOPS_HOME`): params (secrets redacted), outcome summary, status, duration, and
  the risk tier. The CLI writes the same row the MCP path does.
- `QUEUE_AUDIT_APPROVED_BY` / `QUEUE_AUDIT_RATIONALE` are optional annotations
  recorded on the audit row (who/why); they are never required and never block.
- **Runaway guard** — a safety backstop, not authorization: the same call looped
  in a tight window trips a circuit breaker. Disable with `QUEUE_RUNAWAY_MAX=0`.
- Writes support `--dry-run` / `dry_run=True` and double confirmation at the CLI;
  CLI writes execute through the governed twins, so they are audited too.
- Reversible writes capture the real fetched before-state and record an
  inverse descriptor; `purge_queue` and `redis_kill_client` are irreversible
  and record priorState only. `delete_queue`'s undo restores the queue
  *definition*, never its messages — the descriptor says so.
- Big-key sampling is SCAN-budgeted (never `KEYS *`); the redis surface is a
  typed command allow-list; rabbitmq paths are centrally percent-encoded
  (default vhost `/` included).

## References

- `references/capabilities.md` — full tool + platform + API/command reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — onboarding, credentials, and connectivity
