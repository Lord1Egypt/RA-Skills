---
name: xcpng-aiops
slug: xcpng-aiops
displayName: "XCP-ng AIops"
summary: "Governed XCP-ng ops via Xen Orchestra — 29 MCP tools with audit, budget, undo guards."
license: MIT
homepage: https://github.com/AIops-tools/XCPng-AIops
tags: [aiops, mcp, governance, xcpng]
description: >
  Use this skill whenever the user needs to operate an XCP-ng virtualization fleet through Xen Orchestra — a one-shot fleet health overview; VMs (list/get/RRD stats), hosts, pools, storage repositories (SRs) and VDIs, VM snapshots, backup jobs and run logs, XO tasks; four RCA analyses (VM health, SR usage, backup-job failures, pool patch & HA posture); and governed writes (VM start/stop/reboot/migrate, snapshot create/delete/revert, SR rescan).
  Always use this skill for "xcp-ng vm", "xen orchestra", "xo backup failed", "sr full", "orphaned vdi", "xcp-ng snapshot", "migrate vm to another host", "xcp-ng patches", or "pool HA" when the context is explicitly XCP-ng / Xen Orchestra / a Xen-based fleet.
  Do NOT use when the target is not an XCP-ng fleet managed by Xen Orchestra — other hypervisors (Do NOT use for Proxmox VE — use proxmox-aiops), NAS/storage appliances, backup software suites, container clusters, and network devices are out of scope (negative routing hints only).
  Common XCP-ng-via-XO operations with a built-in governance harness (audit, policy, token budget, undo, risk-tiers).
installer:
  kind: uv
  package: xcpng-aiops
argument-hint: "[vm/sr/snapshot uuid or describe your XCP-ng task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["xcpng-aiops","uvx"]},"optional":{"env":["XCPNG_AIOPS_CONFIG","XCPNG_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/XCPng-AIops","emoji":"🖥️","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed XCP-ng operations via Xen Orchestra's REST API /rest/v0. REQUIRES a Xen Orchestra instance (XO from sources or the Xen Orchestra Appliance, 5.x) — XO is the management plane; direct per-host XAPI access is out of scope for v0.1. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency.
  All write operations are audited to a local SQLite DB under ~/.xcpng-aiops/ (relocatable via XCPNG_AIOPS_HOME).
  Credentials: Each XO target's personal authentication token is stored ENCRYPTED in ~/.xcpng-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'xcpng-aiops init' to onboard, or 'xcpng-aiops secret set <target>' to add one (create the token in the XO UI: user menu → Personal tokens, or `xo-cli --createToken`). The store is unlocked by a master password from XCPNG_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var XCPNG_<TARGET_NAME_UPPER>_TOKEN is still honoured as a fallback with a deprecation warning (migrate with 'xcpng-aiops secret migrate'). The token is sent in headers (Authorization: Bearer + authenticationToken cookie) at request time and held only in memory; tokens are never logged or echoed.
  Destructive operations (snapshot delete/revert, vm stop/reboot/migrate) require double confirmation at the CLI layer and support --dry-run; every write MCP tool takes a dry_run preview. A dry_run MAY read (that is how it can tell you the call would be refused) but never writes, records no undo, and is audited like any other governed call. All write tools pass through the @governed_tool decorator (budget guard + audit + risk-tier labelling). vm_start↔vm_stop record each other as inverses; vm_migrate records migrating back to the captured source host; snapshot_create records deleting the REAL snapshot id XO returned; snapshot_delete and snapshot_revert are high-risk and irreversible (capture BEFORE state, record no undo). vm_stop refuses the VM declared as running Xen Orchestra (xo_self_vm_uuid on the target) because stopping XO removes the API vm_start would travel over; that guard is opt-in and fails open when undeclared, since XO's REST API exposes no self endpoint.
  Webhooks: none — no outbound network calls beyond the configured Xen Orchestra REST API endpoint.
  SSL: verify_ssl defaults to true; disable only for self-signed lab certificates.
  Transitive dependencies: httpx (HTTP client) and the MCP SDK. No post-install scripts or background services.
  Verification status: mock-validated; no recorded end-to-end run against a live Xen Orchestra instance yet. Endpoint paths are modelled against the documented Xen Orchestra REST /rest/v0 API and need live verification — action names may differ across XO releases. See docs/VERIFICATION.md.
---

# XCP-ng AIops

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by Vates, the XCP-ng project, or the Xen Orchestra project.** "XCP-ng", "Xen Orchestra", and "Xen" are trademarks of their owners. Source code is publicly auditable at [github.com/AIops-tools/XCPng-AIops](https://github.com/AIops-tools/XCPng-AIops) under the MIT license.

Governed XCP-ng operations via **Xen Orchestra's REST API** — **29 MCP tools**, every one wrapped with the bundled `@governed_tool` harness: a local unified audit log under `~/.xcpng-aiops/`, policy engine, token/runaway budget guard, undo-token recording, and descriptive risk tiers. The XO authentication token is stored **encrypted** (`~/.xcpng-aiops/secrets.enc`, Fernet + scrypt) — never plaintext on disk.

> **Requires a Xen Orchestra instance** (5.x with `/rest/v0`) — XO is the management plane; per-host XAPI is out of scope for v0.1. **Standalone**: the governance harness is bundled in the package (`xcpng_aiops.governance`) — xcpng-aiops has no external skill-family dependency. Coverage is common operations, not exhaustive; verification status and the live-run checklist are in `docs/VERIFICATION.md`.

## What This Skill Does

| Category | Tools | Count | Read or Write |
|----------|-------|:-----:|:-------------:|
| **Overview** | fleet health overview | 1 | 1 read |
| **VMs** | list, get, RRD stats, health RCA | 4 | 4 read |
| | start, stop, reboot, migrate | 4 | 4 write (medium) |
| **Hosts** | list, get | 2 | 2 read |
| **Pools** | list, get, patch & HA posture RCA | 3 | 3 read |
| **SRs / VDIs** | list, get, VDI list (orphan filter), usage RCA | 4 | 4 read |
| | rescan | 1 | 1 write (medium) |
| **Snapshots** | list | 1 | 1 read |
| | create (medium), delete (high), revert (high) | 3 | 3 write |
| **Backups** | jobs, run logs, failure RCA | 3 | 3 read |
| **Tasks** | list | 1 | 1 read |

## Quick Install

```bash
uv tool install xcpng-aiops
xcpng-aiops init       # interactive wizard: XO URL + encrypted token
xcpng-aiops doctor     # XO reachability + token validity + pool count
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/xcpng-aiops
openclaw skills info xcpng-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Triage an XCP-ng fleet (`overview`): pools, hosts, VMs by state, SRs near full, recent backup failures
- Root-cause an unhealthy VM (`vm health-rca`): halted unexpectedly, paused, guest tools missing, CPU/memory pressure
- Root-cause storage pressure (`sr usage-rca`): SRs ranked near-full, thin-provision overcommit, orphaned VDIs with reclaimable bytes
- Root-cause backup failures (`backup failure-rca`): vdi-chain / quiesce / transport / storage-full classification
- Check patch & HA posture (`pool posture`): missing patches, pending reboots, version skew, HA state
- Snapshot a VM before a risky change; start/stop/reboot/migrate VMs under governance

**Do NOT use when** the target is not an XCP-ng fleet managed by Xen Orchestra — other hypervisors (Do NOT use for Proxmox VE — use proxmox-aiops), NAS/storage appliances, backup software suites, Kubernetes/containers, and network devices are out of scope for this skill.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| XCP-ng VMs / hosts / pools / SRs / snapshots / XO backups | **xcpng-aiops** (this skill) |
| Proxmox VE operations | **proxmox-aiops** |
| NAS/storage appliance operations | a storage-appliance ops skill |
| Backup-software suite job/restore operations | a backup-software ops skill |
| Container/cluster lifecycle | a cluster ops skill |

## Common Workflows

Each recipe starts from a read or an RCA and ends in a governed write. Every
write accepts `--dry-run`; destructive ones also double-confirm.

### 1. "Patch a pool without breaking live migration"

1. `xcpng-aiops overview` → fleet snapshot: pools, hosts, VMs by state, SRs near full, recent backup failures.
2. `xcpng-aiops pool posture` → the RCA: hosts missing patches, hosts pending reboot, **version skew** across the pool's hosts, and multi-host pools without HA.
3. `xcpng-aiops host missing-patches <host-uuid>` → what exactly is outstanding on the host you plan to take first.
4. `xcpng-aiops vm list --state Running` → the VMs that must move off that host.
5. For each: `xcpng-aiops vm migrate <vm-uuid> <dest-host-uuid> --dry-run`, then re-run for real (double confirm; the REAL source host is captured before the move and the inverse "migrate back" is recorded).
6. `xcpng-aiops undo list` → confirm a migrate-back token exists for every VM you moved, before you touch the host.
7. Patch and reboot the host in XO, then `xcpng-aiops pool posture` again to confirm the skew cleared.

**Failure branch**: if `pool posture` reports version skew *before* you start, stop — live migration between mismatched host versions can be refused or unsafe. Bring the hosts to a common version first. If a migration fails mid-run, do not retry blindly: `xcpng-aiops vm get <vm-uuid>` to see where the VM actually landed, and `xcpng-aiops task list` for the failing XO task, since a half-finished migrate leaves the VM on one side or the other.

### 2. "This VM keeps going unhealthy"

1. `xcpng-aiops vm health-rca` → findings with cause + action: halted unexpectedly (auto-poweron / HA restart priority set), paused or suspended VMs, running VMs without guest tools, CPU/memory pressure from RRD stats.
2. `xcpng-aiops vm get <vm-uuid>` → the VM's configuration and current power state.
3. `xcpng-aiops vm stats <vm-uuid>` → the RRD series behind a pressure finding, so you confirm sustained pressure rather than one spike.
4. If it is halted and should be running: `xcpng-aiops vm start <vm-uuid>` (the inverse `vm_stop` is recorded).
5. If it is wedged and needs a bounce: `xcpng-aiops vm reboot <vm-uuid> --dry-run`, then for real (double confirm; add `--force` only for a hard reboot — **no undo** either way).
6. `xcpng-aiops vm health-rca` again to confirm the finding cleared.

**Failure branch**: if a clean shutdown or clean reboot hangs, the finding "no guest tools" is usually the real cause — clean actions need the guest agent. Do not escalate straight to `--force`; a hard action risks filesystem damage. Snapshot first (recipe 3), then use `--force` deliberately.

### 3. "Snapshot before a risky change, and roll back cleanly"

1. `xcpng-aiops vm list` → confirm the exact VM uuid.
2. `xcpng-aiops sr usage-rca` → make sure the SR has room; snapshots grow it, and a snapshot on a near-full SR is how you take the pool down.
3. `xcpng-aiops snapshot create <vm-uuid> pre-change` → XO returns the new snapshot's id, and an inverse `snapshot_delete` for **that** id is recorded.
4. `xcpng-aiops snapshot list --vm <vm-uuid>` → confirm the snapshot exists before you change anything.
5. Make your change. If it went wrong: `xcpng-aiops snapshot revert <snapshot-uuid>` (double confirm — replaces current state, **IRREVERSIBLE**, no undo).
6. When you are satisfied: `xcpng-aiops snapshot delete <snapshot-uuid> --dry-run`, then without `--dry-run` (double confirm — **IRREVERSIBLE**, BEFORE state captured for the audit record, no undo).

**Failure branch**: if `sr usage-rca` flags the SR as near-full or thin-provision overcommitted, do not snapshot — reclaim first (recipe 4). If a revert is refused or leaves the VM halted, check `xcpng-aiops task list` for the XO task; and never leave snapshots stacked long-term, because unmerged chains are the usual root cause of the vdi-chain backup failures in recipe 4.

### 4. "Backups have been failing every night and storage is filling up"

1. `xcpng-aiops backup failure-rca` → failed/skipped/interrupted runs grouped by job and classified: **vdi-chain** (coalesce not finished), **quiesce** (guest VSS), **transport** (remote unreachable), **storage-full**, unknown.
2. `xcpng-aiops backup logs -n 20` → the raw recent runs behind that classification.
3. `xcpng-aiops sr usage-rca` → SRs ranked by physical fullness, thin-provision overcommit, and **orphaned VDIs** (attached to no VM) with reclaimable bytes per SR.
4. `xcpng-aiops sr vdis --sr <sr-uuid> --orphaned-only` → the specific orphaned VDIs worth reclaiming on that SR.
5. For a **vdi-chain** classification: let the coalesce finish, stop stacking snapshots (`xcpng-aiops snapshot list`), then `xcpng-aiops sr rescan <sr-uuid> --dry-run` and for real (lowest-impact write) so XO re-reads the SR.
6. For **storage-full**: reclaim space, then re-run `sr usage-rca` to confirm the SR dropped below the near-full threshold.
7. `xcpng-aiops backup logs -n 20` after the next scheduled run to confirm it went green.

**Failure branch**: a **transport** classification is not an XCP-ng problem — the backup remote is unreachable, so fix the remote in the XO UI (Settings → Remotes); rescanning the SR will not help. A **quiesce** classification means the guest agent could not freeze the filesystem: fix guest tools on that VM rather than disabling quiesce fleet-wide. If `sr rescan` does not shrink the chain, the coalesce is still running — wait rather than rescanning in a loop, which will trip the runaway budget guard.

## Usage Mode

| Scenario | Recommended | Why |
|----------|:-----------:|-----|
| Local/small models | **CLI** | fewer tokens than MCP |
| Cloud models (Claude, GPT) | Either | MCP gives structured JSON I/O |
| Automated pipelines | **MCP** | type-safe parameters, audited |

## MCP Tools (29 — 19 read, 8 write, 2 undo)

| Category | Tools | R/W |
|----------|-------|:---:|
| Overview | `overview` | Read |
| VMs | `vm_list`, `vm_get`, `vm_stats`, `vm_health_rca` | Read |
| | `vm_start`, `vm_stop`, `vm_reboot`, `vm_migrate` | Write |
| Hosts | `host_list`, `host_get` | Read |
| Pools | `pool_list`, `pool_get`, `pool_patch_ha_posture` | Read |
| SRs / VDIs | `sr_list`, `sr_get`, `vdi_list`, `sr_usage_rca` | Read |
| | `sr_rescan` | Write |
| Snapshots | `snapshot_list` | Read |
| | `snapshot_create`, `snapshot_delete`, `snapshot_revert` | Write |
| Backups | `backup_job_list`, `backup_log_list`, `backup_failure_rca` | Read |
| Tasks | `task_list` | Read |
| Undo | `undo_list`, `undo_apply` | Read + replay |

**Harness features that light up**: `vm_start`↔`vm_stop` record each other as inverses (with `_undo_id`); `vm_migrate` captures the REAL source host BEFORE moving and records "migrate back"; `snapshot_create` captures the REAL snapshot id from the XO response and records "delete THAT snapshot". `snapshot_delete` and `snapshot_revert` are `risk_level=high`, capture BEFORE state, and declare no undo (irreversible). Every write takes `dry_run=True` (may read, never writes; no undo; audited). All 29 tools are audit-logged under `~/.xcpng-aiops/` and pass through the budget/runaway guard, each carrying a descriptive risk tier into its audit row. Start any triage with `overview`.

## CLI Quick Reference

```bash
xcpng-aiops init                                    # onboarding wizard (encrypted XO token)
xcpng-aiops overview [--target <t>]                 # fleet health summary
xcpng-aiops vm list [--state Running] [--pool <uuid>]
xcpng-aiops vm get <vm_uuid>
xcpng-aiops vm stats <vm_uuid> [-g minutes]
xcpng-aiops vm health-rca [<vm_uuid>]               # RCA: cause + action
xcpng-aiops vm start <vm_uuid> [--dry-run]
xcpng-aiops vm stop <vm_uuid> [--force] [--dry-run]      # double confirm; refuses the declared XO VM
xcpng-aiops vm reboot <vm_uuid> [--force] [--dry-run]    # double confirm
xcpng-aiops vm migrate <vm_uuid> <host_uuid> [--dry-run] # double confirm
xcpng-aiops host list / get <host_uuid> / missing-patches <host_uuid>
xcpng-aiops pool list / get <pool_uuid>
xcpng-aiops pool posture [<pool_uuid>]              # RCA: patches / reboots / skew / HA
xcpng-aiops sr list / get <sr_uuid>
xcpng-aiops sr vdis [--sr <uuid>] [--orphaned-only]
xcpng-aiops sr usage-rca                            # RCA: near-full / overcommit / orphans
xcpng-aiops sr rescan <sr_uuid> [--dry-run]
xcpng-aiops snapshot list [--vm <uuid>]
xcpng-aiops snapshot create <vm_uuid> <name> [--dry-run]
xcpng-aiops snapshot delete <snapshot_uuid> [--dry-run]   # double confirm, IRREVERSIBLE
xcpng-aiops snapshot revert <snapshot_uuid> [--dry-run]   # double confirm, IRREVERSIBLE
xcpng-aiops backup jobs / logs [-n 50]
xcpng-aiops backup failure-rca [-n 50]              # RCA: vdi-chain / quiesce / transport
xcpng-aiops task list [--status failure]
xcpng-aiops secret set <target> / list / rm <target> / migrate / rotate-password
xcpng-aiops doctor                                  # XO reachability + token + pool count
xcpng-aiops mcp                                     # start MCP server (stdio)
```

See `references/cli-reference.md` for the full command list, and
`references/agent-guardrails.md` when driving these tools with a smaller /
local model (the guardrails the tool enforces for you, and a ready system prompt).

## Troubleshooting

### "Config file not found"
Run `xcpng-aiops init` to set up your first target (writes `~/.xcpng-aiops/config.yaml` and stores the XO token encrypted).

### "No XO authentication token for target '<name>'"
Add it to the encrypted store: `xcpng-aiops secret set <name>` (prompts hidden), or run `xcpng-aiops init`. Create the token in the XO UI (user menu → Personal tokens) or with `xo-cli --createToken`. For non-interactive use (MCP/CI), also export `XCPNG_AIOPS_MASTER_PASSWORD` so the store can be unlocked without a prompt.

### "Master password not set" / "Wrong master password"
The encrypted store `~/.xcpng-aiops/secrets.enc` is unlocked by `XCPNG_AIOPS_MASTER_PASSWORD` (or an interactive prompt). If you forgot it, delete `secrets.enc` and re-run `xcpng-aiops init`. Rotate it with `xcpng-aiops secret rotate-password`.

### "Authentication/authorization failed (401/403)"
The XO token is wrong, expired, or revoked, or the XO account lacks permission. Regenerate the token in the XO UI (user menu → Personal tokens) and update it: `xcpng-aiops secret set <name>`.

### "Could not reach Xen Orchestra … check the XO URL"
Confirm the XO web UI is reachable at the configured `url` and that `api_path` is `/rest/v0` (XO 5.x). For self-signed certificates set `verify_ssl: false` on the target (lab only).

### "Resource not found (404)"
The VM/SR/snapshot uuid is stale, or this XO release lacks the endpoint. List the parent collection first (`vm list`, `sr list`, `snapshot list`) to get a current uuid.

### Doctor says "manages no pools yet"
Your XO instance is reachable but has no XCP-ng servers connected — add them in the XO UI (Settings → Servers).

## Audit & Safety

The skill delivers reads and writes and records them; it does **not** decide
whether a write is permitted. That is your agent's judgement, or the permission
of the Xen Orchestra account whose token you connect it with (give that XO user
a read-only ACL or scope its token down — writes then fail at Xen Orchestra).
There is no read-only switch, policy file, or approval gate.

- **Audit is the guarantee, and it is not bypassable.** Every operation — MCP and CLI alike — is logged to `~/.xcpng-aiops/audit.db` (relocatable via `XCPNG_AIOPS_HOME`): params (secrets redacted), outcome summary, status, duration, and the risk tier. The CLI writes the same row the MCP path does.
- The XO token is stored **encrypted** in `~/.xcpng-aiops/secrets.enc` (Fernet/AES-128 + scrypt key derivation; chmod 600) — never plaintext on disk; the master password is never stored, only a per-store salt + ciphertext.
- `XCPNG_AUDIT_APPROVED_BY` / `XCPNG_AUDIT_RATIONALE` are optional annotations recorded on the audit row (who/why); they are never required and never block.
- **Budget / runaway guard** — a safety backstop, not authorization: caps cumulative tool calls and wall-time, and trips on tight task-poll loops.
- Writes support `--dry-run` / `dry_run=True` and double confirmation at the CLI; CLI writes execute through the same governed tools, so they are audited + undo-recorded.
- Reversible writes (`vm_start`/`vm_stop`/`vm_migrate`/`snapshot_create`) capture the real before-state and record a replayable inverse descriptor; `snapshot_delete`/`snapshot_revert` are `risk=high`, irreversible, and declare no undo.
- **Risk tier** is a descriptive label on the audit row derived from `risk_level`; it gates nothing.

The harness is bundled in the package — no external dependency, no manual setup. See `references/setup-guide.md` for security details.

## Contributing & feature requests

Coverage is intentionally focused. **Missing a capability you need, or hit an endpoint that differs on your Xen Orchestra version?** Open an issue or pull request at [github.com/AIops-tools/XCPng-AIops](https://github.com/AIops-tools/XCPng-AIops/issues) — feature requests, contributions, and comments are all welcome.

## License

MIT — [github.com/AIops-tools/XCPng-AIops](https://github.com/AIops-tools/XCPng-AIops)
