# xcpng-aiops — Capabilities (29 MCP tools: 19 read, 8 write, 2 undo)

All tools go through the bundled `@governed_tool` harness (audit / policy /
budget / undo / risk-tier). XO object ids are uuids; get them from the matching
`*_list` tool first. Every tool takes an optional `target` (XO target name
from config; omit for the default).

**Listing envelopes.** `vm_list`, `sr_list`, `vdi_list`, `snapshot_list`,
`task_list`, `backup_job_list`, `backup_log_list` and `undo_list` return
`{<items>: [...], "returned": N, "limit": L, "truncated": bool}` — read the
items under the named key (`vms`, `srs`, `vdis`, `snapshots`, `tasks`, `jobs`,
`logs`, `undos`). `truncated` is measured, not guessed: filters run first, the
cap after, and `backup_log_list` over-fetches one record. When it is true,
re-run with a higher `limit`. The RCA tools report `inputTruncated` when the
listing they correlated over was itself capped.

**Absent vs empty.** A field XO did not return is `null`, never `""` — do not
infer a value for it.

**Authorization.** The tool records; it does not gate. Whether a write may run
is the agent's decision or the connecting Xen Orchestra account's permissions —
there is no read-only switch or approval gate. See `agent-guardrails.md`.

## Overview

| Tool | Risk | Description |
|------|------|-------------|
| `overview` | low | One-shot fleet health: pools, hosts (disabled / reboot-required / versions), VMs by power state + running-without-tools, SRs near full, recent backup failures. Start any triage here. |

## VMs

| Tool | Risk | Description |
|------|------|-------------|
| `vm_list(power_state?, pool?, limit?)` | low | VMs with power state, host, guest-tools status, sizing. |
| `vm_get(vm_id)` | low | One VM: state, host, OS, tools, tags, start time. |
| `vm_stats(vm_id, granularity?)` | low | Recent RRD averages: cpuAvgPercent, memoryUsedPercent. |
| `vm_health_rca(vm_id?)` | low | **RCA**: halted-unexpectedly (auto-poweron/HA set), paused, suspended, guest-tools-missing, cpu-pressure (≥90%), memory-pressure (≥90%). Cause + severity + evidence + action per finding. Fleet mode caps stats pulls at 5 running VMs. |
| `vm_start(vm_id, dry_run?)` | medium | Start a VM. **Undo: vm_stop** (recorded). |
| `vm_stop(vm_id, force?, dry_run?)` | medium | Clean shutdown (hard with force). **Undo: vm_start** — only recorded if the VM was Running before. Refuses the VM declared as running XO (`xo_self_vm_uuid` on the target); with none declared there is **no** such guard — XO has no self endpoint, so it fails open rather than guess. `dry_run` refuses the declared uuid too, and returns `selfVmHint` (a possible IP coincidence, never a verdict, never a block — on either path). |
| `vm_reboot(vm_id, force?, dry_run?)` | medium | Clean/hard reboot. Prior power state captured; **no undo**. |
| `vm_migrate(vm_id, host_id, dry_run?)` | medium | Live-migrate. Captures the REAL source host before moving; **undo: migrate back to it**. |

## Hosts

| Tool | Risk | Description |
|------|------|-------------|
| `host_list(pool?)` | low | Hosts: version, enabled, reboot-required, memory %, resident VMs. |
| `host_get(host_id)` | low | One host: version, build, memory, tags. |

## Pools

| Tool | Risk | Description |
|------|------|-------------|
| `pool_list()` | low | Pools with master, HA state, default SR. |
| `pool_get(pool_id)` | low | One pool detail. |
| `pool_patch_ha_posture(pool_id?)` | low | **RCA**: patches-missing, reboot-required, version-skew (high — breaks live migration), ha-disabled. Per-host rows + per-pool findings. |

## SRs / VDIs

| Tool | Risk | Description |
|------|------|-------------|
| `sr_list(pool?, limit?)` | low | SRs: capacity, physical usage %, virtual allocation. |
| `sr_get(sr_id)` | low | One SR detail. |
| `vdi_list(sr?, orphaned_only?, limit?)` | low | VDIs; `orphaned_only=true` → disks attached to no VM (reclaim candidates). |
| `sr_usage_rca()` | low | **RCA**: sr-critical (≥95%), sr-near-full (≥85%), sr-overcommitted (allocation > capacity), orphaned-vdis with reclaimable bytes per SR. ISO SRs excluded. |
| `sr_rescan(sr_id, dry_run?)` | medium | Metadata refresh; no data change, no undo. Lowest-impact write, but still a write. |

## Snapshots

| Tool | Risk | Description |
|------|------|-------------|
| `snapshot_list(vm_id?, limit?)` | low | VM snapshots with time and parent VM. |
| `snapshot_create(vm_id, name, dry_run?)` | medium | Snapshot a VM. Captures the REAL new snapshot id from XO's response; **undo: delete THAT snapshot**. |
| `snapshot_delete(snapshot_id, dry_run?)` | **high** | IRREVERSIBLE. Captures BEFORE state (name/time/VM); no undo. |
| `snapshot_revert(snapshot_id, dry_run?)` | **high** | IRREVERSIBLE — replaces the VM's current state. Captures snapshot state; no undo. Take a fresh snapshot first. |

## Backups

| Tool | Risk | Description |
|------|------|-------------|
| `backup_job_list(limit?)` | low | VM backup jobs (id, name, mode). |
| `backup_log_list(limit?)` | low | Recent run logs: status + failed-task messages. |
| `backup_failure_rca(limit?)` | low | **RCA**: failures per job classified — vdi-chain (coalesce), quiesce (guest VSS), transport (remote unreachable), storage-full, unknown. Counts + sample findings + action per class. |

## Tasks

| Tool | Risk | Description |
|------|------|-------------|
| `task_list(status?, limit?)` | low | XO tasks (pending / success / failure). |

## Write semantics

- `dry_run=true` → preview dict (`{"dryRun": true, "would...": {...}}`). A dry-run **may
  read** — resolving ids and evaluating guards is what lets it tell you the call would be
  refused — but **never writes** and records **no undo**. It runs through `@governed_tool`
  like any other call, so it is audited and it can be refused. The CLI `--dry-run` routes
  through the same governed function, so both entry points behave identically.
- Successful reversible writes return `_undo_id` referencing the recorded inverse descriptor in `~/.xcpng-aiops/undo.db`. Undo execution is an external orchestrator's job — recording only.
- High-risk tools (`snapshot_delete`, `snapshot_revert`) require a `dry_run` preview + double confirmation at the CLI. `XCPNG_AUDIT_APPROVED_BY` / `XCPNG_AUDIT_RATIONALE` are optional annotations recorded on the audit row — never required, never blocking.
