# truenas-aiops CLI reference

> Preview / mock-only. Endpoint paths are modelled against the documented
> TrueNAS SCALE REST v2.0 API and need live verification.

## Setup & diagnostics

```bash
truenas-aiops init                      # interactive onboarding wizard
truenas-aiops doctor [--skip-auth]      # config + secret store + connectivity (/system/info)
truenas-aiops mcp                       # start the MCP server (stdio transport)
```

## Secrets (encrypted store ~/.truenas-aiops/secrets.enc)

```bash
truenas-aiops secret set <target> [--value <key>]   # store API key (hidden prompt if no --value)
truenas-aiops secret list                            # names only — values never shown
truenas-aiops secret rm <target>
truenas-aiops secret migrate                         # import legacy plaintext .env (TRUENAS_<T>_APIKEY)
truenas-aiops secret rotate-password                 # re-encrypt under a new master password
```

## Read commands

```bash
truenas-aiops overview [--target <t>]    # pools (capacity/health), alerts by level, running services
truenas-aiops system [--target <t>]      # version / hostname / memory / cores / uptime
truenas-aiops pool list
truenas-aiops pool get <pool_id>
truenas-aiops pool status <pool_id>      # health + scan + topology summary
truenas-aiops pool scrub-status <pool_id>
truenas-aiops pool capacity              # size / allocated / free / used% per pool
truenas-aiops dataset list
truenas-aiops dataset get <dataset_id>   # e.g. tank/data
truenas-aiops snapshot list [--dataset <tank/data>]
truenas-aiops disk list
truenas-aiops disk smart                 # S.M.A.R.T. self-test results per disk
truenas-aiops alert list
truenas-aiops service list
truenas-aiops replication list
truenas-aiops replication cloudsync
```

## Write commands (governed; risk tier in parentheses)

```bash
truenas-aiops pool scrub-start <pool_name>            # (medium) start an integrity scrub
truenas-aiops dataset create <tank/path> [--dry-run]  # (medium) create a ZFS dataset
truenas-aiops snapshot create <dataset> <name>        # (medium) records inverse snapshot_delete undo
truenas-aiops snapshot delete <dataset@name> [--dry-run]   # (high) double confirm — IRREVERSIBLE
truenas-aiops service restart <service> [--dry-run]   # (medium) double confirm — smb/nfs/ssh/...
```

## Common options

- `--target, -t <name>` — target name from `config.yaml` (omit to use the default/first target)
- `--dry-run` — print the API call that would be made, change nothing
- Destructive commands (`snapshot delete`, `service restart`) require two confirmations
