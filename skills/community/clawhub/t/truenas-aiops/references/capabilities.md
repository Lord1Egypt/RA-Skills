# truenas-aiops capabilities

> Preview / mock-only. 21 MCP tools (16 read, 5 write). Endpoint paths modelled
> against the documented TrueNAS SCALE REST v2.0 API; need live verification.

## Read tools (16)

| Tool | REST (preview) | Returns |
|------|----------------|---------|
| `overview` | fan-out | pools (capacity/health), alerts by level, running services |
| `system_info` | `GET /system/info` | version, hostname, memory, cores, uptime |
| `pool_list` | `GET /pool` | id, name, status, healthy, size/allocated/free |
| `pool_get` | `GET /pool/id/{id}` | single pool detail |
| `pool_status` | `GET /pool/id/{id}` | health + scan + topology summary |
| `scrub_status` | `GET /pool/id/{id}` | scrub function/state/percentage |
| `pool_capacity` | `GET /pool` | size/allocated/free + used% per pool |
| `dataset_list` | `GET /pool/dataset` | id, name, type, pool, used/available |
| `dataset_get` | `GET /pool/dataset/id/{id}` | single dataset detail |
| `snapshot_list` | `GET /zfs/snapshot` | id, dataset, name, used (opt. filter by dataset) |
| `disk_list` | `GET /disk` | name, serial, model, size, pool |
| `smart_test_results` | `GET /smart/test/results` | latest S.M.A.R.T. self-test per disk |
| `alert_list` | `POST /alert/list` | level, message, class, dismissed |
| `service_list` | `GET /service` | name, state (RUNNING/STOPPED), enable |
| `replication_list` | `GET /replication` | name, direction, transport, state |
| `cloudsync_list` | `GET /cloudsync` | description, direction, path, state |

## Write tools (5)

| Tool | Risk | REST (preview) | Undo / safety |
|------|------|----------------|---------------|
| `pool_scrub_start` | medium | `POST /pool/scrub/run` | captures prior scan state; no undo (non-destructive) |
| `dataset_create` | medium | `POST /pool/dataset` | no undo (deletion out of scope) |
| `snapshot_create` | medium | `POST /zfs/snapshot` | records inverse `snapshot_delete` undo descriptor |
| `snapshot_delete` | **high** | `DELETE /zfs/snapshot/id/{id}` | captures BEFORE state; IRREVERSIBLE, no undo; CLI double-confirm + dry-run |
| `service_restart` | medium | `POST /service/restart` | captures prior state; no undo; CLI double-confirm + dry-run |

## Out of scope (by design)

- Pool/dataset **deletion** and any bulk-data-destroying operation
- Running/overwriting replication or cloud-sync jobs
- Sharing config (SMB/NFS/iSCSI share CRUD), users/groups, apps/VMs
- Anything outside a single TrueNAS SCALE appliance

Want one of these? Open an issue or PR — feedback and contributions welcome.
