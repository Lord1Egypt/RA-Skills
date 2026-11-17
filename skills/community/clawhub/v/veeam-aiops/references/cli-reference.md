# veeam-aiops CLI reference

Global options on most commands: `--target / -t <name>` selects a configured
target (default: first target in `config.yaml`).

## Onboarding & secrets

```bash
veeam-aiops init                           # interactive wizard: connection + encrypted password
veeam-aiops secret set <target>            # store/replace a password (prompts hidden)
veeam-aiops secret list                    # names only; values never shown
veeam-aiops secret rm <target>             # delete a stored password
veeam-aiops secret migrate                 # import a legacy plaintext .env into the encrypted store
veeam-aiops secret rotate-password         # re-encrypt the store under a new master password
```

## Overview

```bash
veeam-aiops overview                       # jobs by last result, repos near full, running sessions
```

## Backup jobs

```bash
veeam-aiops job list                       # id, name, type, status, lastResult
veeam-aiops job get <job_id>               # detail for one job (incl. schedule)
veeam-aiops job start <job_id>             # start a backup job (async session)
veeam-aiops job stop <job_id> [--dry-run]  # stop a running job — double confirm
veeam-aiops job retry <job_id>             # retry failed objects (async session)
veeam-aiops job enable <job_id>            # enable the job schedule
veeam-aiops job disable <job_id>           # disable the job schedule
```

## Restore

```bash
veeam-aiops restore list-points [--backup-id <id>] [--limit 100]  # newest restore points first
veeam-aiops restore start --restore-point-id <id> [--dry-run]
                                           # IRREVERSIBLE — double confirm
```

## Repositories

```bash
veeam-aiops repository list                # id, name, type, path
veeam-aiops repository get <repo_id>       # detail incl. capacity/free/used
veeam-aiops repository state               # capacity summary for all repos (used%)
```

## Backups

```bash
veeam-aiops backup list                    # stored backups: id, name, type, time
veeam-aiops backup objects <backup_id>     # protected objects inside a backup
veeam-aiops backup usage <name> [--json]   # backup storage one VM consumes, per backup (VBR 12.3+)
veeam-aiops backup ranking [--limit 20] [--max-backups 100] [--backup <id|name> ...] \
    [--repository <id|name>] [--concurrency 1] [--json]  # largest consumers first; progress on stderr
```

## Infrastructure

```bash
veeam-aiops infra servers                  # managed servers: id, name, type
veeam-aiops infra proxies                  # backup proxies: id, name, type, server
```

## Sessions (async progress)

```bash
veeam-aiops session list [--limit 100]     # newest sessions first: state, result
veeam-aiops session get <session_id>       # poll one session (progressPercent)
veeam-aiops session log <session_id>       # log records (events) of a session
veeam-aiops session stop <session_id> [--dry-run]   # cancel — double confirm
```

## Diagnostics / RCA (read-only)

```bash
veeam-aiops diagnose job-failures [--limit 100] [--since-hours 24]  # triage recent failures; categorize cause
veeam-aiops diagnose repo-capacity         # flag repositories low on free space (<15% / <10%)
```

Both render worst-first findings, each citing the measured signal (session
result + matched error substring, or free% / free bytes) that tripped it.

## Doctor & MCP

```bash
veeam-aiops doctor [--skip-auth]           # config + encrypted store + connectivity check
veeam-aiops mcp                            # start the MCP server (stdio transport)
```

## Notes

- `job start`, `job retry`, and `restore start` kick off **async sessions**.
  Follow progress with `session list` / `session get` / `session log`, not by
  re-issuing the command.
- Destructive commands (`job stop`, `session stop`, `restore start`) require two
  confirmations and accept `--dry-run` to preview the exact API call.
- Credentials live in the encrypted store (`secrets.enc`); set them with
  `veeam-aiops init` or `veeam-aiops secret set`. Export
  `VEEAM_AIOPS_MASTER_PASSWORD` for non-interactive unlock.
