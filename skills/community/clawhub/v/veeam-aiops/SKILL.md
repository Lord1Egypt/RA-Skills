---
name: veeam-aiops
description: >
  Use this skill whenever the user needs to operate Veeam Backup & Replication — a one-shot health overview, list/inspect/start/stop/retry backup jobs, enable/disable jobs, list restore points and start a VM restore, list backup repositories with capacity, list stored backups and their objects, inventory backup infrastructure (managed servers, proxies), and poll/stop async sessions for job/restore progress.
  Always use this skill for "list veeam jobs", "run veeam backup", "start veeam job", "veeam restore", "veeam repository", "veeam backup status", or "veeam session" when the context is explicitly Veeam / Veeam Backup & Replication / VBR.
  Do NOT use when the target is not Veeam Backup & Replication (other backup products, hypervisor lifecycle, or cloud providers are out of scope).
  Preview — common Veeam B&R operations with a built-in governance harness (audit, policy, token budget, undo, risk-tiers).
installer:
  kind: uv
  package: veeam-aiops
argument-hint: "[job id or describe your Veeam task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"env":["VEEAM_AIOPS_CONFIG"],"bins":["veeam-aiops"],"config":["~/.veeam-aiops/config.yaml","~/.veeam-aiops/secrets.enc"]},"optional":{"env":["VEEAM_AIOPS_MASTER_PASSWORD"]},"primaryEnv":"VEEAM_AIOPS_CONFIG","homepage":"https://github.com/AIops-tools/Veeam-AIops","emoji":"💾","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed Veeam Backup & Replication operations (preview). The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency.
  All write operations are audited to a local SQLite DB under ~/.veeam-aiops/ (relocatable via VEEAM_AIOPS_HOME).
  Credentials: Each Veeam target's login password is stored ENCRYPTED in ~/.veeam-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'veeam-aiops init' to onboard, or 'veeam-aiops secret set <target>' to add one. The store is unlocked by a master password from VEEAM_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var VEEAM_<TARGET_NAME_UPPER>_PASSWORD is still honoured as a fallback with a deprecation warning (migrate with 'veeam-aiops secret migrate'). The password is exchanged for a short-lived OAuth2 bearer token at connect time and held only in memory; passwords/tokens are never logged or echoed.
  Destructive operations (job stop, session stop, restore start) require double confirmation at the CLI layer and support --dry-run. All write tools pass through the @governed_tool decorator (pre-check + budget guard + audit + risk-tier gate). Reversible writes (job start/stop/retry, enable/disable) record an inverse undo descriptor; session stop and the VM restore are irreversible and record none.
  Webhooks: none — no outbound network calls beyond the configured Veeam REST API endpoint.
  SSL: verify_ssl defaults to true; disable only for self-signed lab certificates.
  Transitive dependencies: httpx (HTTP client) and the MCP SDK. No post-install scripts or background services.
---

# Veeam AIops (preview)

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by Veeam Software.** "Veeam" is a trademark of its owner. Source code is publicly auditable at [github.com/AIops-tools/Veeam-AIops](https://github.com/AIops-tools/Veeam-AIops) under the MIT license.

Governed Veeam Backup & Replication operations — **21 MCP tools**, every one wrapped with the bundled `@governed_tool` harness: a local unified audit log under `~/.veeam-aiops/`, policy engine, token/runaway budget guard, undo-token recording, and graduated-autonomy risk tiers. Credentials are stored **encrypted** (`~/.veeam-aiops/secrets.enc`, Fernet + scrypt) — never plaintext on disk.

> **Standalone**: the governance harness is bundled in the package (`veeam_aiops.governance`) — veeam-aiops has no external skill-family dependency. Preview: common Veeam operations, not yet exhaustive.

## What This Skill Does

| Category | Tools | Count | Read or Write |
|----------|-------|:-----:|:-------------:|
| **Overview** | health overview | 1 | 1 read |
| **Backup Jobs** | list, get, start, stop, retry, enable, disable | 7 | 2 read / 5 write |
| **Restore** | list restore points (opt. per backup), start VM restore | 2 | 1 read / 1 write |
| **Repositories** | list, get (detail), state (capacity) | 3 | 3 read |
| **Backups** | list stored backups, list backup objects | 2 | 2 read |
| **Infrastructure** | managed servers, proxies | 2 | 2 read |
| **Sessions** | list, get, log, stop (poll/cancel async progress) | 4 | 3 read / 1 write |

## Quick Install

```bash
uv tool install veeam-aiops
veeam-aiops init       # interactive wizard: connection + encrypted password
veeam-aiops doctor
```

## When to Use This Skill

- List/inspect Veeam backup jobs and their last result
- Start or stop a backup job on demand
- Enable or disable a job's schedule
- List available restore points and start a VM restore
- List backup repositories and stored backups
- Poll async sessions to follow job/restore progress

**Do NOT use when** the target is not Veeam Backup & Replication (other backup products, hypervisor VM lifecycle, Kubernetes, or cloud providers are out of scope for this skill).

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| Veeam backup jobs / restore / repositories | **veeam-aiops** (this skill) |
| Hypervisor VM lifecycle (power, snapshot, migrate) | a hypervisor ops skill |
| Container/cluster lifecycle | a cluster ops skill |

## Common Workflows

### Run a backup job and follow it to completion

1. `veeam-aiops job list` → find the job id and confirm `lastResult`
2. `veeam-aiops job start <job_id>` → starts the job (records an inverse `job_stop` undo descriptor)
3. `veeam-aiops session list` → find the running session; `veeam-aiops session get <session_id>` → check `state` / `progressPercent`
4. **Failure branch**: if `session get` shows the session `Failed`, inspect `result`, then re-run `job start` after fixing the cause — do not loop `session get` rapidly (the runaway budget guard will trip a tight poll loop).

### Restore a VM from a restore point

1. `veeam-aiops restore list-points` → identify the correct restore point id
2. `veeam-aiops restore start --restore-point-id <id> --dry-run` → preview the exact API call
3. `veeam-aiops restore start --restore-point-id <id>` → double confirmation required; this is IRREVERSIBLE (overwrites/creates a VM) and records no undo token
4. **Failure branch**: if `doctor` shows the VBR server unreachable or the password env var is missing, fix `~/.veeam-aiops/.env` (chmod 600) before retrying — the restore is never issued against an unauthenticated session.

## Usage Mode

| Scenario | Recommended | Why |
|----------|:-----------:|-----|
| Local/small models (Ollama, Qwen) | **CLI** | fewer tokens than MCP |
| Cloud models (Claude, GPT) | Either | MCP gives structured JSON I/O |
| Automated pipelines | **MCP** | type-safe parameters, audited |

## MCP Tools (21 — 16 read, 5 write)

| Category | Tools | R/W |
|----------|-------|:---:|
| Overview | `overview` | Read |
| Backup Jobs | `job_list`, `job_get` | Read |
| | `job_start`, `job_stop`, `job_retry`, `job_enable`, `job_disable` | Write |
| Restore | `restore_list_points` | Read |
| | `start_vm_restore` | Write |
| Repositories | `repository_list`, `repository_get`, `repository_state` | Read |
| Backups | `backup_list`, `backup_object_list` | Read |
| Infrastructure | `managed_server_list`, `proxy_list` | Read |
| Sessions | `session_list`, `session_get`, `session_log` | Read |
| | `session_stop` | Write |

**Harness features that light up**: write tools with a clean inverse (`job_start`↔`job_stop`, `job_retry`→`job_stop`, `job_enable`↔`job_disable`) pass an `undo=` lambda so the harness records an inverse descriptor (with `_undo_id`) to the undo store. The irreversible `start_vm_restore` and `session_stop` declare no undo; `start_vm_restore` is tagged `risk_level=high`. All 21 tools are audit-logged under `~/.veeam-aiops/` and pass through the policy pre-check + budget/runaway guard + graduated risk-tier gate. Veeam jobs/restores run as async sessions — poll with `session_get` / `session_log` instead of re-issuing (the runaway breaker backs this up). Start any triage with `overview` (jobs by last result, repos near full, running sessions).

## CLI Quick Reference

```bash
veeam-aiops init                                      # onboarding wizard (encrypted password)
veeam-aiops overview [--target <t>]                   # health summary
veeam-aiops job list [--target <t>]
veeam-aiops job get <job_id>
veeam-aiops job start <job_id>
veeam-aiops job stop <job_id> [--dry-run]              # double confirm
veeam-aiops job retry <job_id>
veeam-aiops job enable <job_id>
veeam-aiops job disable <job_id>
veeam-aiops restore list-points [--backup-id <id>]
veeam-aiops restore start --restore-point-id <id> [--dry-run]   # double confirm
veeam-aiops repository list
veeam-aiops repository get <repository_id>
veeam-aiops repository state                           # capacity / free / used%
veeam-aiops session list
veeam-aiops session get <session_id>
veeam-aiops session log <session_id>
veeam-aiops session stop <session_id> [--dry-run]     # double confirm
veeam-aiops backup list
veeam-aiops backup objects <backup_id>
veeam-aiops infra servers
veeam-aiops infra proxies
veeam-aiops secret set <target>                        # store password encrypted
veeam-aiops secret list                               # names only
veeam-aiops secret migrate                            # import legacy plaintext .env
veeam-aiops secret rotate-password
veeam-aiops doctor
veeam-aiops mcp                                        # start MCP server (stdio)
```

See `references/cli-reference.md` for the full command list.

## Troubleshooting

### "Config file not found"
Run `veeam-aiops init` to set up your first target (writes `~/.veeam-aiops/config.yaml` and stores the password encrypted).

### "No password for target '<name>'"
Add it to the encrypted store: `veeam-aiops secret set <name>` (prompts hidden), or run `veeam-aiops init`. For non-interactive use (MCP/CI), also export `VEEAM_AIOPS_MASTER_PASSWORD` so the store can be unlocked without a prompt.

### "Master password not set" / "Wrong master password"
The encrypted store `~/.veeam-aiops/secrets.enc` is unlocked by `VEEAM_AIOPS_MASTER_PASSWORD` (or an interactive prompt). If you forgot it, delete `secrets.enc` and re-run `veeam-aiops init`. Rotate it with `veeam-aiops secret rotate-password`.

### "Authentication/authorization failed (401)"
The username/password is wrong, or the account lacks a Veeam role. Veeam usernames are typically `DOMAIN\\user` or a local Windows account on the VBR server. Confirm the account can log in to the Veeam console.

### "Could not reach Veeam server … check the host/port"
The default REST API port is 9419 — confirm the Veeam Backup & Replication REST API service is running and the port is open. For self-signed certificates set `verify_ssl: false` on the target (lab only).

### "Resource not found (404)"
The job/session/restore-point id is stale. List the parent collection first (`job list`, `session list`, `restore list-points`) to get a current id.

## Audit & Safety

All operations are automatically audited via the bundled `@governed_tool` decorator (`veeam_aiops.governance`):
- Credentials stored **encrypted** in `~/.veeam-aiops/secrets.enc` (Fernet/AES-128 + scrypt key derivation; chmod 600) — never plaintext on disk; the master password is never stored, only a per-store salt + ciphertext
- Every tool call logged to `~/.veeam-aiops/audit.db` (local SQLite audit DB; relocate with `VEEAM_AIOPS_HOME`)
- Policy rules enforced via `~/.veeam-aiops/rules.yaml` (deny rules, maintenance windows, risk tiers)
- Budget / runaway guard caps cumulative tool calls and wall-time, and trips on tight session-poll/retry loops
- Undo store records inverse descriptors for reversible writes (job start/stop/retry, enable/disable)
- Graduated-autonomy risk tiers gate write operations (require a recorded approver for the highest tiers)

The harness is bundled in the package — no external dependency, no manual setup. See `references/setup-guide.md` for security details.

## Contributing & feature requests

This is a preview — coverage is intentionally focused. **Missing a device, action, or feature you need?** Open an issue or pull request at [github.com/AIops-tools/Veeam-AIops](https://github.com/AIops-tools/Veeam-AIops/issues) — feature requests, contributions, and comments are all welcome.

## License

MIT — [github.com/AIops-tools/Veeam-AIops](https://github.com/AIops-tools/Veeam-AIops)
