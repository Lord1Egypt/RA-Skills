---
name: vmware-vdi
description: >
  Use this skill whenever the user needs to operate a VMware/Omnissa Horizon VDI environment via its
  Connection Server: list and manage desktop pools, RDS farms and published apps, inspect and act on
  user sessions (log off, disconnect, send message), manage desktop machines (reset, maintenance,
  remove), view and change entitlements, read Horizon events/health/statistics, and push instant-clone
  golden images. Always use this skill for "log off VDI user", "reset this desktop", "why is the desktop
  pool not provisioning", "push the new image to the pool", "list Horizon sessions", "who is entitled to
  the pool", "VDI health" — when the context is explicitly Horizon / Omnissa / VDI / desktop-pool /
  RDS-farm. Do NOT use for the underlying vCenter VM lifecycle/power/snapshot/migrate (use vmware-aiops),
  read-only vSphere monitoring (use vmware-monitor), or NSX microsegmentation (use vmware-nsx-security).
  This skill manages the Horizon broker layer; vmware-aiops manages the vCenter VMs backing the desktops.
installer:
  kind: uv
  package: vmware-vdi
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["vmware-vdi","uvx"]},"optional":{"env":["VMWARE_VDI_CONFIG"]}}}
---

# VMware VDI (Horizon)

> Self-test: [guide](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or
> sponsored by VMware, Inc., Broadcom Inc., or Omnissa, LLC.** "VMware", "Horizon", and "Omnissa" are
> trademarks of their respective owners. Source is publicly auditable under the MIT license.

Horizon VDI intelligent operations for the VMware skill family — desktop pools, RDS farms, **user
sessions**, desktop machines, entitlements, events/health/statistics, and instant-clone image push,
through the **Horizon 8 Connection Server REST API** (primary; also targets the latest Omnissa Horizon,
which shares the same `/rest/v1` API lineage).

> **Companion skills**: [vmware-aiops](https://github.com/vmware-skills/VMware-AIops) (the vCenter VMs backing
> the desktops), [vmware-monitor](https://github.com/vmware-skills/VMware-Monitor) (read-only vSphere),
> [vmware-nsx-security](https://github.com/vmware-skills/VMware-NSX-Security) (desktop microsegmentation).

> **Status: v1.0.0 (beta).** Endpoints are verified against the official Horizon Server API; GET-response
> field projections are defensive and pending validation against a live Connection Server (run
> `vmware-vdi init` on a real Horizon once to confirm). Governed by the family harness (audit + policy +
> teaching errors); authorization is delegated to the Horizon admin account's role.

## What This Skill Does

| Category | Tools | Count | Read/Write |
|----------|-------|:-----:|:----------:|
| **Monitoring** | health summary, session list/get, machine list/get, event list | 6 | 6 R |
| **Statistics** | session concurrency stats, per-pool utilization | 2 | 2 R |
| **Management** | pool list/get, farm list, app-pool list, entitlement list, image list, AD search; pool enable/disable, entitlement add/remove | 9 | 7 R / 2 W |
| **Ops actions** | session logoff/disconnect/message, machine reset/maintenance/remove | 6 | 6 W |
| **Tasks** | task status; image push, task cancel | 3 | 1 R / 2 W |

**27 MCP tools (16 read / 11 write).** Reads are strictly non-destructive. Writes preview their blast
radius, are double-confirmed at the CLI, and are audit-logged.

## Quick Install

```bash
uv tool install vmware-vdi==2.4.5
vmware-vdi init      # friendly setup: connect to a Connection Server + discover your pools
vmware-vdi doctor    # verify config / credentials / connectivity
```

## When to Use This Skill

Use vmware-vdi for the **Horizon broker layer**: desktop pools, RDS farms, published apps, **user
sessions** (logoff/disconnect/message), desktop machine state (reset/maintenance/remove), entitlements,
Horizon events/health/statistics, and **instant-clone image push** — when the context is explicitly
Horizon / Omnissa / VDI / desktop-pool / RDS-farm.

**Do NOT use when**: the task is the underlying vCenter VM (power/snapshot/clone/migrate → **vmware-aiops**),
read-only vSphere inventory/alarms (→ **vmware-monitor**), or NSX microsegmentation of the desktops
(→ **vmware-nsx-security**). A Horizon desktop's *backing VM* is aiops; the *session/pool/broker* is vdi.

## Related Skills — Skill Routing

| The user wants… | Skill |
|-----------------|-------|
| Log off / reset / re-image a Horizon desktop or session | **vmware-vdi** (this) |
| Power/snapshot/clone/migrate the backing vCenter VM | vmware-aiops |
| Read-only vSphere inventory / alarms / host health | vmware-monitor |
| Microsegment the desktop pool network | vmware-nsx-security |
| Multi-step VDI workflow with approval + rollback | vmware-pilot |

## Common Workflows

**1. Help-desk: a user's desktop is stuck.**
```
vmware-vdi session list --user alice          # find their session + state
vmware-vdi machine list --state AGENT_UNREACHABLE   # is the desktop broken?
vmware-vdi session logoff --user alice --dry-run    # preview blast radius (which sessions)
vmware-vdi session logoff --user alice        # double-confirm, then logs off + audits
```
*Failure branch*: if `session list` returns a teaching 404/auth error, run `vmware-vdi doctor` — a
read-only Horizon role is enough for the reads but the account must be able to reach the Connection Server.

**2. Patch night: push a new golden image to a pool.**
```
vmware-vdi image list                         # find the base VM + snapshot
vmware-vdi pool push-image --id pool-fin --dry-run   # BLAST RADIUS: N desktops, M logged-in users
vmware-vdi pool set-enabled --id pool-fin --disable  # optional: stop new logins first
vmware-vdi pool push-image --id pool-fin      # double-confirm; returns a task
vmware-vdi task status --pool pool-fin         # track progress
```
*Failure branch*: if the preview shows logged-in users you did not expect, `session send-message --user …`
to warn them, or push with `--force-logoff` only after confirming impact.

**3. Onboard a group to a pool.**
```
vmware-vdi ad-search "Finance"                # resolve the AD group → its SID
vmware-vdi entitlement add --pool pool-fin --sid <SID>
vmware-vdi entitlement list --pool pool-fin   # verify
```
*Failure branch*: `ad-search` returning nothing usually means the domain in `~/.vmware-vdi/config.yaml`
is wrong — re-run `vmware-vdi init --force`.

## Usage Mode

- **CLI** — interactive help-desk work, scripting, small/local models (lower context cost).
- **MCP** — agent-driven operations with structured output; run `vmware-vdi mcp` (an installed console
  script, so no `uvx` network re-resolve — works through enterprise TLS proxies).

## MCP Tools (27 — 16 read, 11 write)

| Category | Tools | R/W |
|----------|-------|:---:|
| Monitoring | `get_vdi_health_summary`, `list_vdi_sessions`, `get_vdi_session`, `list_vdi_machines`, `get_vdi_machine`, `list_vdi_events` | Read |
| Statistics | `get_vdi_session_stats`, `get_desktop_pool_utilization` | Read |
| Management (read) | `list_desktop_pools`, `get_desktop_pool`, `list_farms`, `list_app_pools`, `list_entitlements`, `list_vdi_images`, `search_ad_users` | Read |
| Tasks (read) | `get_vdi_task_status` | Read |
| Ops actions | `logoff_vdi_session`, `disconnect_vdi_session`, `send_vdi_session_message`, `reset_vdi_machine`, `set_vdi_machine_maintenance`, `remove_vdi_machine` | Write |
| Management (write) | `set_desktop_pool_enabled`, `add_entitlement`, `remove_entitlement` | Write |
| Tasks (write) | `push_desktop_pool_image`, `cancel_vdi_task` | Write |

**List envelope**: every `*_list` tool returns `{items, returned, limit, total, truncated, hint}` — read
rows from `items` and check `truncated` before concluding a listing is complete; empty `items` with
`truncated:false` means checked-and-none, not a failure. Lists are fetched with server-side pagination.

**Blast radius (normative)**: `push_desktop_pool_image` recreates **every desktop in the pool** — the highest
single-call blast radius in the family. Its preview states affected-desktop and in-session counts
before any confirm, plus `blast_radius.occupancy`: `determined` when those counts can be believed,
`unknown` when session rows exist that belong to neither a desktop pool nor a farm and so cannot be
ruled out of this pool. An `unknown` occupancy makes `in_session_count` a lower bound and refuses
`confirm=true` — check `list_vdi_sessions`, or pass `acknowledge_unknown_occupancy=true`, which is audited.
Machines that name no desktop pool (`unattributed_desktops`) make the desktop count "at least N" and
refuse `confirm=true` with no override.

**Confirmation gate (MCP)**: the ten gated writes (`logoff_vdi_session`/`disconnect`, `reset_vdi_machine`/
`maintenance`/`remove`, `set_desktop_pool_enabled`, `push_desktop_pool_image`, `cancel_vdi_task`, `add_entitlement`/`remove`)
take `confirm` (default `false`). A call without it returns `blast_radius` — identity, counts, ids (up to
20), `blockers`, `unmeasured` — and changes nothing; the acting response carries it too. Show it to the
user and pass `confirm=true` only after they agree: the user asking earlier is not agreement, they have
not seen it. If anything the blast radius depends on could not be read (a machine's state, a session's
user, a task's state, a pool's enabled flag, the pool's entitlements), `confirm=true` is refused.

**Read/write split**: 16 read-only tools (`[READ]` docstring marker), 11 modify state. All writes are
audit-logged; destructive ones (`logoff_vdi_session`, `reset_vdi_machine`, `remove_vdi_machine`, `set_desktop_pool_enabled`
disable, `remove_entitlement`, `push_desktop_pool_image`, `cancel_vdi_task`) require CLI double-confirmation and
support `--dry-run`.

## CLI Quick Reference

```bash
vmware-vdi init                                          # friendly setup + pool discovery
vmware-vdi health                                        # one-glance VDI health
vmware-vdi stats                                         # session concurrency statistics
vmware-vdi utilization                                   # per-pool desktop utilization
vmware-vdi session list [--user U] [--pool P] [--state CONNECTED]
vmware-vdi session logoff --user U [--dry-run]           # double-confirm
vmware-vdi machine list [--pool P] [--state AGENT_UNREACHABLE]
vmware-vdi machine reset --id M [--dry-run]              # hard reset; double-confirm
vmware-vdi machine maintenance --id M --enter|--exit
vmware-vdi pool list
vmware-vdi pool set-enabled --id P --enable|--disable
vmware-vdi pool push-image --id P [--force-logoff] [--dry-run]   # highest blast radius
vmware-vdi task status --pool P [--task T]
vmware-vdi ad-search "<name>"                            # resolve AD SID for entitlement
vmware-vdi entitlement add|remove --pool P --sid <SID>
```
Full list: `references/cli-reference.md`.

## Troubleshooting

- **`Password not found. Set environment variable: VMWARE_VDI_<TARGET>_PASSWORD`** — run `vmware-vdi init`
  (writes `~/.vmware-vdi/.env`, 0600), or export the var manually.
- **Login fails (HTTP 401/400)** — check `username`/`domain` in `~/.vmware-vdi/config.yaml`; Horizon
  authenticates against the AD `domain`. A local Connection Server admin leaves `domain` blank.
- **`certificate could not be verified`** — for a self-signed lab cert set `verify_ssl: false` for that
  target in the config.
- **A write is refused with "read-only role"** — that is RBAC working as designed. Point the target at a
  Horizon admin role with write privilege, or keep the read-only account for read commands only.
- **`session list --pool` or a push-image preview shows 0 where you expect users** — on your Horizon
  version a field name may differ; this is a beta known-limitation, please file an issue with a minimal, redacted
  `get_vdi_session` example so the projection can be pinned. Remove user identities, session IDs, machine/host names, internal addresses and all credentials before sharing; retain only the fields needed to reproduce the mismatch.

## Audit & Safety

1. **Source Code** — https://github.com/vmware-skills/VMware-VDI (MIT).
2. **Config File Contents** — `config.yaml` holds host/username/domain only; passwords live in
   `~/.vmware-vdi/.env` (0600, obfuscated to `b64:` at rest — obfuscation, not encryption).
3. **Webhook Data Scope** — none. This skill makes no outbound calls except to the configured
   Connection Server.
4. **TLS Verification** — on by default; `verify_ssl: false` is per-target and only for self-signed labs.
5. **Prompt Injection Protection** — all Connection-Server-supplied text (user names, machine/pool names,
   event messages) passes through `vmware_policy.sanitize()` (truncation + control-char stripping).
6. **Least Privilege** — authorization is the Horizon account's job: a read-only Horizon admin role
   refuses every write at the Connection Server, un-bypassably. All writes are recorded in
   `~/.vmware/audit.db`. See `references/setup-guide.md`.

## License

MIT

## Current evidence boundary

After a write timeout or gateway error, inspect the Horizon target before retrying: the write may already have happened. Automatic transient retries apply only to GET reads; explicit authentication recovery is separate. See `references/capabilities.md`.
