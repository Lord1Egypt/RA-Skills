# VMware Storage Capabilities

All 11 MCP tools exposed by `vmware-storage-mcp`, organized by category.

## Automation Level Reference

Each operation is classified by autonomy level per the Enterprise Harness Engineering framework:

| Level | Meaning | Agent autonomy | Examples in this skill |
|:-:|---|---|---|
| **L1** | Read-only, raw data | Always auto-run | `list_all_datastores`, `browse_datastore`, `scan_datastore_images`, `list_cached_images`, `storage_iscsi_status`, vSAN status queries |
| **L2** | Read + analysis / recommendation | Always auto-run | datastore capacity analysis, image registry queries, iSCSI target health correlation |
| **L3** | Single write — user must approve | Only after explicit confirmation; high-risk ops require double-confirm + `--dry-run` (see Confirm column) | `storage_iscsi_enable`, `storage_iscsi_add_target`, `storage_iscsi_remove_target`, vSAN cluster ops |
| **L4** | Multi-step plan / apply workflow | Plan generation auto; apply gated by user approval | *(roadmap — multi-host iSCSI rollout, vSAN expansion plans)* |
| **L5** | Auto-remediation from learned pattern | Pattern library only; requires `risk:low` + `reversible:true` + `repeatable:true` + signed approval | **PoC pattern (v1.5.16+)**: [`patterns/iscsi-target-stale-rescan.yaml`](../../../patterns/iscsi-target-stale-rescan.yaml) — scans for stale iSCSI devices (`devices_inaccessible_count > 0`, missing expected devices, or `last_rescan_age_minutes > 60`); action: invoke `storage_rescan` on the affected `(host, target)`; classified low-risk because the rescan is idempotent and non-destructive (no data, config, or VM state is modified). Schema only — **not yet enforced by the runtime**. |

**Notes**:
- L1/L2 tools are always safe for agents to call without confirmation.
- L3 tools always pass through the `@vmware_tool` decorator: connection check → policy check → audit log → double-confirm.
- L5 PoC pattern (`patterns/iscsi-target-stale-rescan.yaml`, v1.5.16+) is a **reference design**: it documents the candidate trigger / action / validation / circuit-breaker shape under `schema_version: 1` (see [vmware-policy auto-remediation pattern docs](https://github.com/zw008/VMware-Policy/blob/main/docs/auto-remediation-patterns.md)). The pattern is `approval.status: poc_unsigned` and will only become live after `success_count_required: 5` + `failure_count_max: 0` + `distinct_operators_required: 2` + `days_observed: 90` are met and the pattern is signed.

## Datastore (4 tools)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `list_all_datastores` | List datastores with capacity, usage %, VM count | `target` (string, optional) | Low | No |
| `browse_datastore` | Browse files with optional path and glob pattern | `datastore` (string, **required**), `path` (string, optional), `pattern` (string, optional), `target` (string, optional) | Low | No |
| `scan_datastore_images` | Find OVA/ISO/OVF/VMDK deployable images in a datastore | `datastore` (string, **required**), `target` (string, optional) | Low | No |
| `list_cached_images` | Query local image registry with type/datastore filters | `image_type` (string, optional), `datastore` (string, optional) | Low | No |

## iSCSI (5 tools)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `storage_iscsi_status` | Show adapter status, HBA device, IQN, configured send targets | `host` (string, **required**), `target` (string, optional) | Low | No |
| `storage_iscsi_enable` | Enable software iSCSI adapter on a host | `host` (string, **required**), `target` (string, optional) | Medium | Yes |
| `storage_iscsi_add_target` | Add iSCSI send target (IP + port) and rescan storage | `host` (string, **required**), `address` (string, **required**), `port` (integer, default: 3260), `target` (string, optional) | Medium | Yes |
| `storage_iscsi_remove_target` | Remove iSCSI send target and rescan storage | `host` (string, **required**), `address` (string, **required**), `port` (integer, default: 3260), `target` (string, optional) | Medium | Yes |
| `storage_rescan` | Rescan all HBAs and VMFS volumes on a host | `host` (string, **required**), `target` (string, optional) | Low | No |

## vSAN (2 tools)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `vsan_health` | Cluster health summary with disk group details per host | `cluster` (string, **required**), `target` (string, optional) | Low | No |
| `vsan_capacity` | Total/used/free capacity in GB and usage percentage | `cluster` (string, **required**), `target` (string, optional) | Low | No |

## Risk Level Definitions

| Level | Meaning | Examples |
|-------|---------|---------|
| **Low** | Read-only query, no state change | `list_all_datastores`, `browse_datastore`, `vsan_health`, `storage_iscsi_status`, `storage_rescan` |
| **Medium** | State change affecting storage configuration, but recoverable | `storage_iscsi_enable`, `storage_iscsi_add_target`, `storage_iscsi_remove_target` |

## Tool Counts by Risk Level

| Risk | Count | Tools |
|------|:-----:|-------|
| Low | 8 | All read-only tools + `storage_rescan` |
| Medium | 3 | `storage_iscsi_enable`, `storage_iscsi_add_target`, `storage_iscsi_remove_target` |

> Note: `storage_rescan` triggers a host-level HBA rescan which is non-destructive (discovery only) and classified as Low risk. The iSCSI write tools (`enable`, `add_target`, `remove_target`) are Medium risk because they modify the host's iSCSI configuration, but changes are reversible.

## Input Validation

| Parameter | Validation | Error on Invalid |
|-----------|-----------|-----------------|
| `address` (IP) | `ipaddress.ip_address()` — accepts IPv4 and IPv6 | `ISCSIError: Invalid IP address` |
| `port` | Integer in range 1-65535 | `ISCSIError: Port must be 1-65535` |
| `host` | Looked up by exact name match in vSphere inventory | `HostNotFoundError` |
| `cluster` | Looked up by exact name match in vSphere inventory | `VSANError: Cluster not found` |
| `datastore` | Looked up by exact name match (case-sensitive) | `Datastore not found` |

## Audit Coverage

All 11 tools are wrapped with `@vmware_tool` from vmware-policy, which provides:

- **Pre-execution**: Policy rule check against `~/.vmware/rules.yaml` (deny rules, maintenance windows)
- **Post-execution**: Audit log entry written to `~/.vmware/audit.db` (SQLite WAL mode)
- **Input sanitization**: All vSphere API response text processed through `sanitize()` (truncation + control character cleanup)

## Read/Write Split

| Type | Count | Tools |
|------|:-----:|-------|
| Read | 6 | `list_all_datastores`, `browse_datastore`, `scan_datastore_images`, `list_cached_images`, `storage_iscsi_status`, `vsan_health`, `vsan_capacity` |
| Write | 5 | `storage_iscsi_enable`, `storage_iscsi_add_target`, `storage_iscsi_remove_target`, `storage_rescan` |

> Write tools require explicit parameters (host name, IP address) and support `--dry-run` in CLI mode. All write operations are audit-logged with timestamp, user, target, operation, parameters, and result.

## Connection Requirements

| Requirement | Datastore Tools | iSCSI Tools | vSAN Tools |
|-------------|:---------------:|:-----------:|:----------:|
| vCenter connection | Required | Not required (direct ESXi OK) | Required |
| ESXi host access | Via vCenter | Direct or via vCenter | Via vCenter |
| pyVmomi | Required | Required | Required |
| vSAN SDK | Not required | Not required | Recommended (for full health) |

## Runtime Requirements

| Requirement | Minimum | Notes |
|-------------|---------|-------|
| Python | 3.10+ | Lowered from 3.11 in v1.5.27 for Goose sandbox / Ubuntu 22.04 compatibility. Tested on 3.10 / 3.11 / 3.12. |
| OS | macOS, Linux | stdio MCP transport — no network listener required |
