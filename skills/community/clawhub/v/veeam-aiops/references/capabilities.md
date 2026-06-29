# veeam-aiops capabilities

21 MCP tools (16 read, 5 write), each wrapped with the bundled `@governed_tool`
harness. Typical response token estimates assume a small/medium environment.

## Overview (1 — read)

| Tool | R/W | Risk | Typical response tokens |
|------|:---:|:----:|:----------------------:|
| `overview` | R | low | ~150 |

Fan-out health summary: jobs grouped by last result, repositories at/above 85%
used, and currently-running sessions. Call this first to triage an environment.

## Backup Jobs (7 — 2 read, 5 write)

| Tool | R/W | Risk | Undo | Typical response tokens |
|------|:---:|:----:|------|:----------------------:|
| `job_list` | R | low | — | 150–600 (depends on job count) |
| `job_get` | R | low | — | ~120 |
| `job_start` | W | medium | `job_stop` | ~50 |
| `job_stop` | W | medium | `job_start` | ~50 |
| `job_retry` | W | medium | `job_stop` | ~50 |
| `job_enable` | W | medium | `job_disable` | ~40 |
| `job_disable` | W | medium | `job_enable` | ~40 |

REST endpoints: `GET /api/v1/jobs`, `GET /api/v1/jobs/{id}`,
`POST /api/v1/jobs/{id}/{start|stop|retry|enable|disable}`. The write tools
capture the job's prior status/lastResult for context.

## Restore (2 — 1 read, 1 write)

| Tool | R/W | Risk | Undo | Typical response tokens |
|------|:---:|:----:|------|:----------------------:|
| `restore_list_points` | R | low | — | 150–800 |
| `start_vm_restore` | W | high | **none — irreversible** | ~40 |

REST endpoints: `GET /api/v1/restorePoints` (optional `backupIdFilter`),
`POST /api/v1/restore/vm`. `start_vm_restore` is a documented skeleton: the
exact restore endpoint and payload vary by restore type and Veeam version.

## Repositories (3 — read)

| Tool | R/W | Risk | Typical response tokens |
|------|:---:|:----:|:----------------------:|
| `repository_list` | R | low | 100–400 |
| `repository_get` | R | low | ~120 |
| `repository_state` | R | low | 100–400 |

REST endpoints: `GET /api/v1/backupInfrastructure/repositories`,
`GET /api/v1/backupInfrastructure/repositories/{id}`,
`GET /api/v1/backupInfrastructure/repositories/states` (capacity / free / used,
plus a computed used%). `repository_get` merges the static record with its state
row when available.

## Backups (2 — read)

| Tool | R/W | Risk | Typical response tokens |
|------|:---:|:----:|:----------------------:|
| `backup_list` | R | low | 150–800 |
| `backup_object_list` | R | low | 150–800 |

REST endpoints: `GET /api/v1/backups`, `GET /api/v1/backups/{id}/objects`.

## Infrastructure (2 — read)

| Tool | R/W | Risk | Typical response tokens |
|------|:---:|:----:|:----------------------:|
| `managed_server_list` | R | low | 150–600 |
| `proxy_list` | R | low | 150–600 |

REST endpoints: `GET /api/v1/backupInfrastructure/managedServers`,
`GET /api/v1/backupInfrastructure/proxies`. Read-only inventory of where jobs
run and what moves the data.

## Sessions (4 — 3 read, 1 write)

| Tool | R/W | Risk | Undo | Typical response tokens |
|------|:---:|:----:|------|:----------------------:|
| `session_list` | R | low | — | 150–800 |
| `session_get` | R | low | — | ~120 |
| `session_log` | R | low | — | 150–800 |
| `session_stop` | W | medium | **none** | ~40 |

REST endpoints: `GET /api/v1/sessions`, `GET /api/v1/sessions/{id}`,
`GET /api/v1/sessions/{id}/logs`, `POST /api/v1/sessions/{id}/stop`. Sessions
are how Veeam exposes async job/restore progress — poll these instead of
re-issuing the originating operation; read `session_log` to see *why* one failed.

## Harness behavior

- **Encrypted credentials**: passwords are stored in `~/.veeam-aiops/secrets.enc`
  (Fernet + scrypt), unlocked by `VEEAM_AIOPS_MASTER_PASSWORD` or a prompt —
  never plaintext on disk.
- **Audit**: all 21 tools log to `~/.veeam-aiops/audit.db`.
- **Undo store**: the five reversible job writes record an inverse descriptor
  (`_undo_id` on the result); `session_stop` and the high-risk restore record none.
- **Budget/runaway guard**: caps cumulative calls + wall-time and trips tight
  session-poll loops.
- **Risk tiers**: `~/.veeam-aiops/rules.yaml` can require a recorded approver
  for high-tier writes.
- **Sanitize**: all API-returned text is truncated + control-char stripped.
