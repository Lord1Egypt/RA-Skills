# truenas-aiops capabilities

> 25 MCP tools (19 read, 6 write). Routes are resolved against the appliance's
> own method list and were cross-checked on live TrueNAS SCALE 25.04 and 26
> appliances; see docs/VERIFICATION.md for what remains unverified.

## Read tools (19)

| Tool | REST (modelled) | Returns |
|------|----------------|---------|
| `overview` | fan-out | pools (capacity/health), alerts by level, running services |
| `system_info` | `GET /system/info` | version, hostname, memory, cores, uptime |
| `pool_health_rca` | `GET /pool` | worst-first findings: bad ZFS state, read/write/checksum/scan error counts, capacity over 80%/90% |
| `alert_and_capacity_rca` | `POST /alert/list` + `GET /pool/dataset` | worst-first findings: active alerts by level + datasets near quota/available ceiling |
| `pool_list` | `GET /pool` | id, name, status, healthy, size/allocated/free |
| `pool_get` | `GET /pool/id/{id}` | single pool detail |
| `pool_status` | `GET /pool/id/{id}` | health + scan + topology summary |
| `scrub_status` | `GET /pool/id/{id}` | scrub function/state/percentage |
| `pool_capacity` | `GET /pool` | size/allocated/free + used% per pool |
| `dataset_list` | `GET /pool/dataset` | id, name, type, pool, used/available |
| `dataset_get` | `GET /pool/dataset/id/{id}` | single dataset detail |
| `snapshot_list` | `GET /zfs/snapshot` | `{snapshots, returned, limit, truncated}` — id, dataset, name, used (opt. filter by dataset; default limit 200) |
| `disk_list` | `GET /disk` | name, serial, model, size, pool |
| `smart_test_results` | `GET /smart/test/results` | latest S.M.A.R.T. self-test per disk |
| `alert_list` | `POST /alert/list` | level, message, class, dismissed |
| `service_list` | `GET /service` | name, state (RUNNING/STOPPED), enable |
| `replication_list` | `GET /replication` | name, direction, transport, state (PENDING/RUNNING/FINISHED/ERROR, never absent), error, lastSnapshot, lastRun |
| `cloudsync_list` | `GET /cloudsync` | description, direction, path, state (the last run's job state; null until it runs) |
| `undo_list` | governance store | recorded reversible writes / not-yet-applied undo tokens |

## Write tools (6)

| Tool | Risk | REST (modelled) | Undo / safety |
|------|------|----------------|---------------|
| `pool_scrub_start` | medium | `POST /pool/scrub/run` | captures prior scan state; no undo (non-destructive); `dry_run` |
| `dataset_create` | medium | `POST /pool/dataset` | no undo (deletion out of scope); `dry_run` |
| `snapshot_create` | medium | `POST /zfs/snapshot` | records inverse `snapshot_delete` undo descriptor; `dry_run` |
| `snapshot_delete` | **high** | `DELETE /zfs/snapshot/id/{id}` | captures BEFORE state; IRREVERSIBLE, no undo; CLI double-confirm + `dry_run` |
| `service_restart` | medium | `POST /service/restart` | captures prior state; no undo; refuses a name absent from `service_list`, and refuses `ssh` without `confirm=True` (out-of-band recovery path); guards also fire under `dry_run`; CLI double-confirm |
| `undo_apply` | medium | governance store | executes a recorded inverse; itself governed; single-use; supports dry-run |

## Out of scope (by design)

- Pool/dataset **deletion** and any bulk-data-destroying operation
- Running/overwriting replication or cloud-sync jobs
- Sharing config (SMB/NFS/iSCSI share CRUD), users/groups, apps/VMs
- Anything outside a single TrueNAS SCALE appliance

Want one of these? Open an issue or PR — feedback and contributions welcome.
