# vmware-vdi — CLI Reference

All commands accept `--target/-t <name>` (config target) and `--config/-c <path>` (alternate config file).
Destructive commands accept `--dry-run` (preview only) and interactively double-confirm.

## Setup & diagnostics
```bash
vmware-vdi init [--force] [--skip-test]     # friendly setup: prompt, write config + .env, test, discover pools
vmware-vdi doctor                           # config / credentials / connectivity checks
vmware-vdi mcp                              # run the MCP server (stdio) — the primary MCP entry point
```

## Monitoring & statistics (read-only)
```bash
vmware-vdi health                           # session totals, problem machines, pool availability
vmware-vdi stats                            # concurrency by state/protocol, busiest pools
vmware-vdi utilization                      # per-pool total/available/in-use/error + utilization %
vmware-vdi events [--severity ERROR]        # recent Horizon audit events (newest first)
```

## Sessions
```bash
vmware-vdi session list [--user U] [--pool P] [--state CONNECTED|DISCONNECTED|PENDING]
vmware-vdi session logoff [--id S] [--user U] [--dry-run]        # kicks the user; double-confirm
vmware-vdi session disconnect [--id S] [--user U] [--dry-run]    # state preserved; double-confirm
vmware-vdi session message "<text>" [--user U] [--id S] [--type INFO|WARNING|ERROR]
```

## Machines
```bash
vmware-vdi machine list [--pool P] [--state AGENT_UNREACHABLE|ERROR|...]
vmware-vdi machine reset --id M [--dry-run]                      # hard reset; double-confirm
vmware-vdi machine maintenance --id M --enter|--exit [--dry-run] # double-confirm
vmware-vdi machine remove --id M [--dry-run]                     # deletes VM (instant clone); double-confirm
```

## Pools, images, tasks
```bash
vmware-vdi pool list
vmware-vdi pool set-enabled --id P --enable|--disable [--dry-run]  # disable stops NEW sessions
vmware-vdi pool push-image --id P [--force-logoff] [--dry-run]     # recreates EVERY desktop; double-confirm
vmware-vdi images                                                  # instant-clone base VMs + snapshots
vmware-vdi task status --pool P [--task T]                        # track an image push / provisioning
vmware-vdi task cancel --pool P --task T [--dry-run]              # double-confirm
```

## Farms, apps, entitlements
```bash
vmware-vdi farm list
vmware-vdi app-pool list
vmware-vdi ad-search "<name>"                                     # resolve AD user/group → SID
vmware-vdi entitlement list --pool P
vmware-vdi entitlement add --pool P --sid <SID> [--sid <SID> ...] [--dry-run]
vmware-vdi entitlement remove --pool P --sid <SID> [--dry-run]   # double-confirm
```
