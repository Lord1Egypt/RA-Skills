# CLI Reference

Complete command reference for `vmware-storage` CLI.

## Global Options

All commands accept these options:

| Option | Description |
|--------|-------------|
| `--target <name>` | Target name from `~/.vmware-storage/config.yaml` (defaults to first target) |
| `--config <path>` | Override config file path |
| `--help` | Show command help |

## Datastore Commands

### `datastore list`

List all datastores with capacity, usage, and VM count.

```bash
vmware-storage datastore list
vmware-storage datastore list --target my-vcenter
```

Output columns: Name, Type, Total GB, Free GB, Usage %, VMs.
Usage above 85% is highlighted in red.

### `datastore browse`

Browse files in a datastore directory. Supports glob pattern filtering.

```bash
# Browse root of a datastore
vmware-storage datastore browse datastore01

# Browse a subdirectory
vmware-storage datastore browse datastore01 --path "iso-images"

# Filter by pattern
vmware-storage datastore browse datastore01 --pattern "*.ova"
vmware-storage datastore browse datastore01 --path "templates" --pattern "*.iso"
```

| Argument/Option | Required | Default | Description |
|----------------|:--------:|---------|-------------|
| `ds_name` | Yes | - | Datastore name (case-sensitive) |
| `--path` | No | `""` (root) | Subdirectory path within the datastore |
| `--pattern` | No | `"*"` | Glob pattern to filter files |

Output: JSON array of file objects with `name`, `size_mb`, `type`, `modified`, `ds_path`.

### `datastore scan-images`

Scan a datastore for deployable images (OVA, ISO, OVF, VMDK).

```bash
vmware-storage datastore scan-images datastore01
vmware-storage datastore scan-images datastore01 --target prod-vcenter
```

| Argument/Option | Required | Default | Description |
|----------------|:--------:|---------|-------------|
| `ds_name` | Yes | - | Datastore name |

Scans for patterns: `*.ova`, `*.ovf`, `*.iso`, `*.vmdk`. Results are sorted by name.

## iSCSI Commands

### `iscsi enable`

Enable the software iSCSI adapter on an ESXi host.

```bash
vmware-storage iscsi enable esxi-01
vmware-storage iscsi enable esxi-01 --dry-run
```

| Argument/Option | Required | Default | Description |
|----------------|:--------:|---------|-------------|
| `host_name` | Yes | - | ESXi host name |
| `--dry-run` | No | `false` | Preview the operation without executing |

**Safety**: Requires double confirmation (two prompts). If the adapter is already enabled, returns current HBA device and IQN without making changes.

### `iscsi status`

Show iSCSI adapter status and configured send targets.

```bash
vmware-storage iscsi status esxi-01
```

| Argument/Option | Required | Default | Description |
|----------------|:--------:|---------|-------------|
| `host_name` | Yes | - | ESXi host name |

Output: JSON with `enabled`, `hba_device`, `iqn`, and `send_targets` (list of address/port pairs).

### `iscsi add-target`

Add an iSCSI send target to a host and automatically rescan storage.

```bash
vmware-storage iscsi add-target esxi-01 192.168.1.100
vmware-storage iscsi add-target esxi-01 10.0.0.50 --port 3261
vmware-storage iscsi add-target esxi-01 192.168.1.100 --dry-run
```

| Argument/Option | Required | Default | Description |
|----------------|:--------:|---------|-------------|
| `host_name` | Yes | - | ESXi host name |
| `address` | Yes | - | iSCSI target IP address (validated) |
| `--port` | No | `3260` | iSCSI target port (1-65535) |
| `--dry-run` | No | `false` | Preview the operation without executing |

**Safety**: Requires double confirmation. IP address and port are validated before any API call. If the target is already configured, returns without making changes. After adding, automatically rescans all HBAs and VMFS volumes.

### `iscsi remove-target`

Remove an iSCSI send target from a host and automatically rescan storage.

```bash
vmware-storage iscsi remove-target esxi-01 192.168.1.100
vmware-storage iscsi remove-target esxi-01 10.0.0.50 --port 3261
vmware-storage iscsi remove-target esxi-01 192.168.1.100 --dry-run
```

| Argument/Option | Required | Default | Description |
|----------------|:--------:|---------|-------------|
| `host_name` | Yes | - | ESXi host name |
| `address` | Yes | - | iSCSI target IP address |
| `--port` | No | `3260` | iSCSI target port |
| `--dry-run` | No | `false` | Preview the operation without executing |

**Safety**: Requires double confirmation. Raises an error if the target is not found (prevents accidental no-ops). Automatically rescans after removal.

### `iscsi rescan`

Rescan all HBAs and VMFS volumes on an ESXi host.

```bash
vmware-storage iscsi rescan esxi-01
vmware-storage iscsi rescan esxi-01 --dry-run
```

| Argument/Option | Required | Default | Description |
|----------------|:--------:|---------|-------------|
| `host_name` | Yes | - | ESXi host name |
| `--dry-run` | No | `false` | Preview the operation without executing |

Calls both `RescanAllHba()` and `RescanVmfs()` on the host storage system.

## vSAN Commands

### `vsan health`

Get vSAN cluster health summary including disk group details.

```bash
vmware-storage vsan health Cluster-Prod
vmware-storage vsan health Cluster-Prod --target my-vcenter
```

| Argument/Option | Required | Default | Description |
|----------------|:--------:|---------|-------------|
| `cluster_name` | Yes | - | Name of the vSAN-enabled cluster |

Output: JSON with `vsan_enabled`, `overall_health`, `host_count`, `disk_groups` (per-host cache/capacity disk info).

### `vsan capacity`

Get vSAN capacity overview (total/used/free) for a cluster.

```bash
vmware-storage vsan capacity Cluster-Prod
```

| Argument/Option | Required | Default | Description |
|----------------|:--------:|---------|-------------|
| `cluster_name` | Yes | - | Name of the vSAN-enabled cluster |

Output: JSON with `total_gb`, `used_gb`, `free_gb`, `usage_pct`, `datastore_name`.

## Diagnostics

### `doctor`

Run environment and connectivity diagnostics.

```bash
vmware-storage doctor
vmware-storage doctor --skip-auth
```

| Option | Description |
|--------|-------------|
| `--skip-auth` | Skip the vSphere authentication check (useful when vCenter is unreachable) |

Checks performed:
1. Config file exists (`~/.vmware-storage/config.yaml`)
2. `.env` file exists with correct permissions (600)
3. Targets are configured in config
4. Network connectivity to all targets (TCP port check with 5s timeout)
5. vSphere authentication (actual login via pyVmomi)
6. MCP server module loads successfully

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Operation failed or doctor check failed |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `VMWARE_STORAGE_CONFIG` | Override config file path (used by MCP server) |
| `VMWARE_<TARGET>_PASSWORD` | Password for a target (e.g., `VMWARE_MY_VCENTER_PASSWORD`) |
