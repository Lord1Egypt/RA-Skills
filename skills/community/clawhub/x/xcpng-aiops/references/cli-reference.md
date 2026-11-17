# xcpng-aiops — CLI reference

Global pattern: `xcpng-aiops <group> <command> [args] [--target <t>]`.
`--target/-t` selects a Xen Orchestra target from `~/.xcpng-aiops/config.yaml`
(default: the first one). Write commands support `--dry-run` (prints the API
call, changes nothing) and destructive ones require **double confirmation**.

## Setup & health

```bash
xcpng-aiops init                    # onboarding wizard: XO URL, TLS verify (default yes), encrypted token
xcpng-aiops doctor [--skip-auth]    # config + secret store + XO reachability + pool count
xcpng-aiops overview [-t xo1]       # one-shot fleet health summary (JSON)
xcpng-aiops mcp                     # start the MCP server (stdio)
```

## VMs

```bash
xcpng-aiops vm list [--state Running|Halted|Paused|Suspended] [--pool <pool_uuid>] [--limit 200]
xcpng-aiops vm get <vm_uuid>
xcpng-aiops vm stats <vm_uuid> [--granularity seconds|minutes|hours|days]
xcpng-aiops vm health-rca [<vm_uuid>]          # RCA (fleet-wide when uuid omitted)
xcpng-aiops vm start <vm_uuid> [--dry-run]                 # governed; undo = stop
xcpng-aiops vm stop <vm_uuid> [--force] [--dry-run]        # double confirm; undo = start
xcpng-aiops vm reboot <vm_uuid> [--force] [--dry-run]      # double confirm; no undo
xcpng-aiops vm migrate <vm_uuid> <host_uuid> [--dry-run]   # double confirm; undo = migrate back
```

`--force` = hard power operation (no guest tools needed); default is a clean
guest shutdown/reboot.

## Hosts

```bash
xcpng-aiops host list [--pool <pool_uuid>]
xcpng-aiops host get <host_uuid>
xcpng-aiops host missing-patches <host_uuid>
```

## Pools

```bash
xcpng-aiops pool list
xcpng-aiops pool get <pool_uuid>
xcpng-aiops pool posture [<pool_uuid>]   # RCA: patches / reboots / version skew / HA
```

## Storage (SRs / VDIs)

```bash
xcpng-aiops sr list [--pool <pool_uuid>] [--limit 200]
xcpng-aiops sr get <sr_uuid>
xcpng-aiops sr vdis [--sr <sr_uuid>] [--orphaned-only] [--limit 200]
xcpng-aiops sr usage-rca                 # RCA: near-full / overcommit / orphaned VDIs
xcpng-aiops sr rescan <sr_uuid> [--dry-run]
```

## Snapshots

```bash
xcpng-aiops snapshot list [--vm <vm_uuid>] [--limit 200]
xcpng-aiops snapshot create <vm_uuid> <name> [--dry-run]
xcpng-aiops snapshot delete <snapshot_uuid> [--dry-run]    # double confirm, IRREVERSIBLE
xcpng-aiops snapshot revert <snapshot_uuid> [--dry-run]    # double confirm, IRREVERSIBLE
```

## Backups & tasks

```bash
xcpng-aiops backup jobs [--limit 200]
xcpng-aiops backup logs [--limit 50]
xcpng-aiops backup failure-rca [--limit 50]   # RCA: vdi-chain / quiesce / transport / storage-full
xcpng-aiops task list [--status pending|success|failure] [--limit 200]
```

## Secrets (encrypted store)

```bash
xcpng-aiops secret set <target> [--value <token>]   # omit --value to be prompted (hidden)
xcpng-aiops secret list                             # names only
xcpng-aiops secret rm <target>
xcpng-aiops secret migrate                          # import legacy plaintext .env
xcpng-aiops secret rotate-password                  # re-encrypt under a new master password
```

## Environment variables

| Variable | Purpose |
|----------|---------|
| `XCPNG_AIOPS_MASTER_PASSWORD` | Unlock `secrets.enc` non-interactively (MCP/CI). |
| `XCPNG_AIOPS_HOME` | Relocate `~/.xcpng-aiops` (audit.db, undo.db). |
| `XCPNG_AIOPS_CONFIG` | Alternate config.yaml path for the MCP server. |
| `XCPNG_AUDIT_APPROVED_BY` / `XCPNG_AUDIT_RATIONALE` | Optional approver/rationale annotations recorded on the audit row (never required). |
| `XCPNG_MAX_TOOL_CALLS` / `XCPNG_MAX_TOOL_SECONDS` | Budget ceilings. |
| `XCPNG_RUNAWAY_MAX` / `XCPNG_RUNAWAY_WINDOW_SEC` | Runaway-loop circuit breaker. |
| `XCPNG_<TARGET>_TOKEN` | Legacy plaintext token fallback (deprecated). |

## Truncation

Listing commands cap their output at `--limit` (default 200) and print
`… showing N of more … — truncated, re-run with a higher --limit` when there
was more; the JSON itself carries `"truncated": true`.
