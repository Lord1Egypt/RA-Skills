---
name: truenas-aiops
slug: truenas-aiops
displayName: "TrueNAS AIops"
summary: "Governed TrueNAS SCALE storage ops — 25 MCP tools with audit, budget, undo guards."
license: MIT
homepage: https://github.com/AIops-tools/TrueNAS-AIops
tags: [aiops, mcp, governance, truenas]
description: >
  Use this skill whenever the user needs to operate TrueNAS SCALE storage — a one-shot health overview, system info, read-only diagnostics / RCA (pool health, alerts & dataset capacity), inspect ZFS pools (list/get/status, capacity, scrub status, start a scrub), datasets (list/get/create), snapshots (list/create/delete), physical disks and S.M.A.R.T. self-test results, system alerts, services (list/restart), and replication / cloud-sync tasks.
  Always use this skill for "list truenas pools", "truenas dataset", "create zfs snapshot", "start a scrub", "diagnose truenas pool health", "why is my pool degraded", "truenas disk health", "truenas smart test", "truenas alerts", "restart truenas service", or "truenas replication" when the context is explicitly TrueNAS / TrueNAS SCALE / a ZFS NAS appliance.
  Do NOT use when the target is not a TrueNAS SCALE appliance — other NAS/storage products, backup software, hypervisor VM lifecycle, container clusters, and network devices are out of scope (negative routing hints only).
  Common TrueNAS SCALE operations with a built-in governance harness (audit, policy, token budget, undo, risk-tiers). Live-verified against real TrueNAS SCALE 25.04 and 26 appliances over both transports; see docs/VERIFICATION.md for what is and is not covered.
installer:
  kind: uv
  package: truenas-aiops
argument-hint: "[pool/dataset/snapshot id or describe your TrueNAS task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["truenas-aiops","uvx"]},"optional":{"env":["TRUENAS_AIOPS_CONFIG","TRUENAS_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/TrueNAS-AIops","emoji":"🗄️","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed TrueNAS SCALE storage operations. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency.
  All write operations are audited to a local SQLite DB under ~/.truenas-aiops/ (relocatable via TRUENAS_AIOPS_HOME).
  Credentials: Each TrueNAS target's API key is stored ENCRYPTED in ~/.truenas-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'truenas-aiops init' to onboard, or 'truenas-aiops secret set <target>' to add one (create the key in the TrueNAS UI: Credentials → API Keys). The store is unlocked by a master password from TRUENAS_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var TRUENAS_<TARGET_NAME_UPPER>_APIKEY is still honoured as a fallback with a deprecation warning (migrate with 'truenas-aiops secret migrate'). The API key is sent as an Authorization: Bearer header at request time and held only in memory; keys are never logged or echoed.
  Destructive operations (snapshot delete, service restart) require double confirmation at the CLI layer and support --dry-run. All write tools pass through the @governed_tool decorator (budget guard + audit + risk-tier labelling). snapshot_create records an inverse snapshot_delete undo descriptor; snapshot_delete is high-risk and irreversible (captures BEFORE state, records no undo).
  Webhooks: none — no outbound network calls beyond the configured TrueNAS REST API endpoint.
  SSL: verify_ssl defaults to true; disable only for self-signed lab certificates.
  Transitive dependencies: httpx (HTTP client) and the MCP SDK. No post-install scripts or background services.
  Routes are resolved against the appliance's own method list and were cross-checked on live 25.04 and 26 appliances; S.M.A.R.T. on failing media remains unverified (see docs/VERIFICATION.md).
---

# TrueNAS AIops

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by iXsystems or the TrueNAS project.** "TrueNAS" is a trademark of its owner. Source code is publicly auditable at [github.com/AIops-tools/TrueNAS-AIops](https://github.com/AIops-tools/TrueNAS-AIops) under the MIT license.

Governed TrueNAS SCALE storage operations — **25 MCP tools**, every one wrapped with the bundled `@governed_tool` harness: a local unified audit log under `~/.truenas-aiops/`, policy engine, token/runaway budget guard, undo-token recording, and descriptive risk tiers. The TrueNAS API key is stored **encrypted** (`~/.truenas-aiops/secrets.enc`, Fernet + scrypt) — never plaintext on disk.

> **Standalone**: the governance harness is bundled in the package (`truenas_aiops.governance`) — truenas-aiops has no external skill-family dependency. **Verification**: coverage focuses on common TrueNAS operations and is not exhaustive, but it is no longer mock-only — reads, governed writes with audit + undo, the WebSocket transport, degraded-pool RCA, replication and cloud-sync have all been exercised against live TrueNAS SCALE 25.04 and 26 appliances. `docs/VERIFICATION.md` records exactly what was checked and what is still open.

## What This Skill Does

| Category | Tools | Count | Read or Write |
|----------|-------|:-----:|:-------------:|
| **Overview / System** | health overview, system info | 2 | 2 read |
| **Diagnostics / RCA** | pool health RCA, alert & capacity RCA | 2 | 2 read |
| **Pools** | list, get, status, scrub status, capacity | 5 | 5 read |
| | scrub start | 1 | 1 write (medium) |
| **Datasets** | list, get | 2 | 2 read |
| | create | 1 | 1 write (medium) |
| **Snapshots** | list | 1 | 1 read |
| | create (medium), delete (high) | 2 | 2 write |
| **Disks** | list, S.M.A.R.T. results | 2 | 2 read |
| **Alerts** | list | 1 | 1 read |
| **Services** | list | 1 | 1 read |
| | restart | 1 | 1 write (medium) |
| **Replication** | replication tasks, cloud-sync tasks | 2 | 2 read |

## Quick Install

```bash
uv tool install truenas-aiops
truenas-aiops init       # interactive wizard: connection + encrypted API key
truenas-aiops doctor
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/truenas-aiops
openclaw skills info truenas-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Triage a TrueNAS appliance (`overview`): pool capacity/health, alerts, running services
- Root-cause a degraded/full pool (`diagnose pool-health`) or a wall of alerts (`diagnose alerts`) — worst-first findings that cite the measured number
- List/inspect ZFS pools, datasets, and snapshots
- Create a snapshot before a risky change; start a pool scrub
- Check disk health and S.M.A.R.T. self-test results
- List and restart system services (smb/nfs/ssh)
- Inspect replication and cloud-sync tasks

**Do NOT use when** the target is not a TrueNAS SCALE appliance — other NAS/storage or backup products, hypervisor VM lifecycle, Kubernetes/containers, and network devices are out of scope for this skill.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| TrueNAS pools / datasets / snapshots / ZFS health | **truenas-aiops** (this skill) |
| Backup software job/restore operations | a backup-software ops skill |
| Hypervisor VM lifecycle (power, snapshot, migrate) | a hypervisor ops skill |
| Container/cluster lifecycle | a cluster ops skill |

## Common Workflows

### Root-cause a degraded or full pool (start here)

1. `truenas-aiops diagnose pool-health` → worst-first findings: bad ZFS state (DEGRADED/FAULTED/OFFLINE), non-zero read/write/checksum/scan error counters, and pools over 80%/90% capacity — each citing the measured number
2. `truenas-aiops pool status <pool_id>` → inspect the topology / scan detail the finding cited
3. `truenas-aiops pool scrub-start <pool_name>` → kick an integrity scrub (governed, medium risk); poll with `pool scrub-status`
4. `truenas-aiops diagnose alerts` → cross-check active alerts by level and any datasets nearing their quota/available ceiling

### Snapshot a dataset before a change, then roll back if needed

1. `truenas-aiops dataset list` → confirm the dataset id (e.g. `tank/data`)
2. `truenas-aiops snapshot create tank/data pre-change` → records an inverse `snapshot_delete` undo descriptor
3. Make your change; if it went wrong, the snapshot is your recovery point
4. `truenas-aiops snapshot delete tank/data@pre-change --dry-run` → preview; then without `--dry-run` (double confirm) — IRREVERSIBLE, captures BEFORE state, no undo

### Scrub a pool and follow it

1. `truenas-aiops pool list` → find the pool name and health
2. `truenas-aiops pool scrub-start tank` → starts the integrity scrub
3. `truenas-aiops pool scrub-status <pool_id>` → check `state` / `percentage`; do not re-issue (the runaway budget guard backs a tight poll loop)

## Usage Mode

| Scenario | Recommended | Why |
|----------|:-----------:|-----|
| Local/small models | **CLI** | fewer tokens than MCP |
| Cloud models (Claude, GPT) | Either | MCP gives structured JSON I/O |
| Automated pipelines | **MCP** | type-safe parameters, audited |

## MCP Tools (25 — 19 read, 6 write)

| Category | Tools | R/W |
|----------|-------|:---:|
| Overview / System | `overview`, `system_info` | Read |
| Diagnostics / RCA | `pool_health_rca`, `alert_and_capacity_rca` | Read |
| Pools | `pool_list`, `pool_get`, `pool_status`, `scrub_status`, `pool_capacity` | Read |
| | `pool_scrub_start` | Write |
| Datasets | `dataset_list`, `dataset_get` | Read |
| | `dataset_create` | Write |
| Snapshots | `snapshot_list` | Read |
| | `snapshot_create`, `snapshot_delete` | Write |
| Disks | `disk_list`, `smart_test_results` | Read |
| Alerts | `alert_list` | Read |
| Services | `service_list` | Read |
| | `service_restart` | Write |
| Replication | `replication_list`, `cloudsync_list` | Read |
| Undo (governance) | `undo_list` | Read |
| | `undo_apply` | Write |

**Harness features that light up**: `snapshot_create` passes an `undo=` lambda so the harness records an inverse `snapshot_delete` descriptor (with `_undo_id`) to the undo store. `snapshot_delete` is tagged `risk_level=high`, captures the snapshot's BEFORE state, and declares no undo (it is irreversible). `pool_scrub_start`, `dataset_create`, and `service_restart` are `medium` risk and capture prior state where relevant. All 25 tools are audit-logged under `~/.truenas-aiops/` and pass through the budget/runaway guard, with a descriptive risk-tier label on each audit row. Start any triage with `overview`.

## CLI Quick Reference

```bash
truenas-aiops init                                    # onboarding wizard (encrypted API key)
truenas-aiops overview [--target <t>]                 # health summary
truenas-aiops system [--target <t>]                   # version / hostname / memory / uptime
truenas-aiops diagnose pool-health                    # RCA: pool state / error counters / capacity (worst first)
truenas-aiops diagnose alerts                         # RCA: active alerts by level + datasets near full
truenas-aiops pool list
truenas-aiops pool get <pool_id>
truenas-aiops pool status <pool_id>
truenas-aiops pool scrub-status <pool_id>
truenas-aiops pool capacity                           # size / allocated / free / used%
truenas-aiops pool scrub-start <pool_name>
truenas-aiops dataset list
truenas-aiops dataset get <dataset_id>                # e.g. tank/data
truenas-aiops dataset create <tank/path> [--dry-run]
truenas-aiops snapshot list [--dataset tank/data] [--limit 200]
truenas-aiops snapshot create <dataset> <name>
truenas-aiops snapshot delete <dataset@name> [--dry-run]   # double confirm, IRREVERSIBLE
truenas-aiops disk list
truenas-aiops disk smart                              # S.M.A.R.T. self-test results
truenas-aiops alert list
truenas-aiops service list
truenas-aiops service restart <service> [--dry-run]   # double confirm (smb/nfs/ssh)
truenas-aiops replication list
truenas-aiops replication cloudsync
truenas-aiops secret set <target>                     # store API key encrypted
truenas-aiops secret list                             # names only
truenas-aiops secret migrate                          # import legacy plaintext .env
truenas-aiops secret rotate-password
truenas-aiops doctor
truenas-aiops mcp                                     # start MCP server (stdio)
```

See `references/cli-reference.md` for the full command list, and
`references/agent-guardrails.md` when driving these tools with a smaller /
local model (enforced guardrails, ready-to-paste system prompt).

## Troubleshooting

### "Config file not found"
Run `truenas-aiops init` to set up your first target (writes `~/.truenas-aiops/config.yaml` and stores the API key encrypted).

### "No API key for target '<name>'"
Add it to the encrypted store: `truenas-aiops secret set <name>` (prompts hidden), or run `truenas-aiops init`. Create the key in the TrueNAS UI under Credentials → API Keys. For non-interactive use (MCP/CI), also export `TRUENAS_AIOPS_MASTER_PASSWORD` so the store can be unlocked without a prompt.

### "Master password not set" / "Wrong master password"
The encrypted store `~/.truenas-aiops/secrets.enc` is unlocked by `TRUENAS_AIOPS_MASTER_PASSWORD` (or an interactive prompt). If you forgot it, delete `secrets.enc` and re-run `truenas-aiops init`. Rotate it with `truenas-aiops secret rotate-password`.

### "Authentication/authorization failed (401/403)"
The API key is wrong or revoked, or the account lacks permission. Regenerate the key in the TrueNAS UI (Credentials → API Keys) and update it: `truenas-aiops secret set <name>`.

### "Could not reach TrueNAS … check the host/port"
Confirm the TrueNAS web/REST endpoint is reachable on the configured port (default 443) and `api_path` is `/api/v2.0`. For self-signed certificates set `verify_ssl: false` on the target (lab only).

### "Resource not found (404)"
The pool/dataset/snapshot id is stale. List the parent collection first (`pool list`, `dataset list`, `snapshot list`) to get a current id.

## Audit & Safety

The skill delivers reads and writes and records them; it does **not** decide
whether a write is permitted. That is your agent's judgement, or the permission
of the account you connect it with (scope the TrueNAS API key to a
limited-privilege account and writes then fail at the appliance). There is no
read-only switch, policy file, or approval gate.

- API key stored **encrypted** in `~/.truenas-aiops/secrets.enc` (Fernet/AES-128 + scrypt key derivation; chmod 600) — never plaintext on disk; the master password is never stored, only a per-store salt + ciphertext.
- **Audit is the guarantee, and it is not bypassable.** Every operation — MCP and CLI alike — is logged to `~/.truenas-aiops/audit.db` (relocatable via `TRUENAS_AIOPS_HOME`): params (secrets redacted), outcome summary, status, duration, and the risk tier. The CLI writes the same row the MCP path does.
- `TRUENAS_AUDIT_APPROVED_BY` / `TRUENAS_AUDIT_RATIONALE` are optional annotations recorded on the audit row (who/why); they are never required and never block.
- **Runaway guard** — a safety backstop, not authorization: cumulative tool calls and wall-time are capped, and a tight scrub/poll loop trips a circuit breaker.
- Writes support `--dry-run` / `dry_run=True` and double confirmation at the CLI; CLI writes execute through the same governed tools, so they are audited + undo-recorded.
- Reversible writes capture the real fetched before-state and record an inverse descriptor (e.g. `snapshot_create` → `snapshot_delete`) that replays against the tool's own signature.

The harness is bundled in the package — no external dependency, no manual setup. See `references/setup-guide.md` for security details.

## Contributing & feature requests

Coverage is intentionally focused, and what has actually been verified against live appliances is recorded in `docs/VERIFICATION.md`. **Missing a capability you need, or hit an endpoint that needs fixing for your TrueNAS version?** Open an issue or pull request at [github.com/AIops-tools/TrueNAS-AIops](https://github.com/AIops-tools/TrueNAS-AIops/issues) — feature requests, contributions, and comments are all welcome.

## License

MIT — [github.com/AIops-tools/TrueNAS-AIops](https://github.com/AIops-tools/TrueNAS-AIops)
