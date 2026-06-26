# Setup Guide

Complete setup and security guide for `vmware-storage`.

## Prerequisites

- Python 3.10+
- vCenter Server 6.7+ or standalone ESXi 6.7+
- Network access to vCenter/ESXi on port 443 (or custom port)

## Installation

### Via uv (recommended)

```bash
uv tool install vmware-storage
```

### Via pip

```bash
pip install vmware-storage
```

### From source

```bash
git clone https://github.com/zw008/VMware-Storage.git
cd VMware-Storage
pip install -e .
```

## Configuration

### 1. Create config directory

```bash
mkdir -p ~/.vmware-storage
```

### 2. Create config.yaml

```bash
cp config.example.yaml ~/.vmware-storage/config.yaml
```

Edit `~/.vmware-storage/config.yaml`:

```yaml
targets:
  - name: my-vcenter          # Target identifier (used in CLI --target flag)
    host: vcenter.example.com  # Hostname or IP
    username: administrator@vsphere.local
    type: vcenter              # "vcenter" or "esxi"
    port: 443
    verify_ssl: false          # Set true if using valid certs

  - name: esxi-standalone
    host: 10.0.0.50
    username: root
    type: esxi
    port: 443
    verify_ssl: false

notify:
  webhook_url: ""              # Optional: webhook for notifications
```

The first target in the list is the default (used when `--target` is not specified).

### 3. Create .env for credentials

Passwords are **never stored in config.yaml**. They must be set as environment variables via the `.env` file.

```bash
echo "VMWARE_MY_VCENTER_PASSWORD=your_password" > ~/.vmware-storage/.env
echo "VMWARE_ESXI_STANDALONE_PASSWORD=root_password" >> ~/.vmware-storage/.env
chmod 600 ~/.vmware-storage/.env
```

**Naming convention**: `VMWARE_<TARGET_NAME_UPPER>_PASSWORD` where `<TARGET_NAME_UPPER>` is the target `name` from config.yaml, uppercased, with hyphens replaced by underscores.

Examples:
| Target name | Environment variable |
|-------------|---------------------|
| `my-vcenter` | `VMWARE_MY_VCENTER_PASSWORD` |
| `esxi-standalone` | `VMWARE_ESXI_STANDALONE_PASSWORD` |
| `prod01` | `VMWARE_PROD01_PASSWORD` |

### 4. Verify setup

```bash
vmware-storage doctor
```

This runs six checks: config file, .env file, targets, network connectivity, authentication, and MCP server module.

Use `--skip-auth` if vCenter is temporarily unreachable:

```bash
vmware-storage doctor --skip-auth
```

## MCP Server Configuration

### Claude Code / Claude Desktop

Add to your MCP config (`~/.claude.json` or Claude Desktop settings):

```json
{
  "mcpServers": {
    "vmware-storage": {
      "command": "vmware-storage",
      "args": ["mcp"],
      "env": {
        "VMWARE_STORAGE_CONFIG": "~/.vmware-storage/config.yaml"
      }
    }
  }
}
```

> v1.5.15+ recommends the single-command form `vmware-storage mcp`. Pre-1.5.15 used
> `uvx --from vmware-storage vmware-storage-mcp`, which still works but re-resolves from
> PyPI on each launch and breaks behind corporate TLS proxies. The legacy
> `vmware-storage-mcp` entry point is also kept for backward compatibility.

### Goose

Add to `~/.config/goose/config.yaml`:

```yaml
extensions:
  vmware-storage:
    type: stdio
    cmd: vmware-storage
    args:
      - mcp
    env:
      VMWARE_STORAGE_CONFIG: "~/.vmware-storage/config.yaml"
```

### Docker

```bash
docker compose up -d
```

Or run manually:

```bash
docker run -d \
  -v ~/.vmware-storage:/root/.vmware-storage:ro \
  -e VMWARE_STORAGE_CONFIG=/root/.vmware-storage/config.yaml \
  vmware-storage
```

### Password obfuscation at rest

On first load, any plaintext `*_PASSWORD` value in `.env` is automatically
rewritten to a grep-safe `b64:<encoded>` form and decoded transparently at
runtime, so a casual `grep` of the file no longer reveals the password. Values
are read and written through python-dotenv's own parser, so the stored secret
never drifts from what you configured (quotes, inline comments, and trailing
whitespace are handled correctly).

> **This is obfuscation, not encryption.** Anyone who can read the file can
> still decode it. For real secrecy at rest, do not store the password in `.env`
> at all — inject it from a secret manager (HashiCorp Vault, CyberArk, AWS
> Secrets Manager, or a Kubernetes Secret) into the `*_PASSWORD` environment
> variable at process start. The code reads the env var either way.

## Security Details

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware" and "vSphere" are trademarks of Broadcom.

### Credential Safety

- Passwords are **only loaded from environment variables** (via `.env` file), never from `config.yaml`
- The `.env` file permissions are checked at startup; a warning is logged if permissions are wider than `600` (owner read/write only)
- The `doctor` command verifies `.env` permissions and reports failures

### Audit Logging

All operations are logged to `~/.vmware/audit.db` (SQLite WAL mode, via vmware-policy).

Each audit entry records:
- **timestamp**: UTC ISO 8601
- **target**: Which vCenter/ESXi was acted on
- **operation**: What was done (e.g., `iscsi_enable`, `iscsi_add_target`, `query`)
- **resource**: What resource was affected (host name, datastore name)
- **parameters**: Full parameter set passed to the operation
- **before_state / after_state**: State snapshots (when available)
- **result**: Operation outcome
- **user**: OS username who initiated the operation

Example audit entry:

```json
{
  "timestamp": "2026-03-25T10:30:00+00:00",
  "target": "my-vcenter",
  "operation": "iscsi_add_target",
  "resource": "esxi-01",
  "parameters": {"host_name": "esxi-01", "address": "10.0.0.100", "port": 3260},
  "before_state": {},
  "after_state": {},
  "result": "iSCSI target 10.0.0.100:3260 added to host 'esxi-01' and storage rescanned.",
  "user": "admin"
}
```

Read-only operations (list, browse, scan, status, health, capacity) are also logged with `operation: "query"` for complete traceability.

### Double Confirmation on Destructive Operations

CLI write commands require two separate confirmation prompts before executing:

1. First prompt: "Are you sure?" (default: No)
2. Second prompt: "This modifies host storage configuration. Confirm again?" (default: No)

Both must be answered `y` for the operation to proceed. This applies to:
- `iscsi enable`
- `iscsi add-target`
- `iscsi remove-target`

### Dry-Run Mode

All write commands support `--dry-run` to preview what would happen without making changes:

```bash
vmware-storage iscsi enable esxi-01 --dry-run
# Output: [DRY-RUN] Would enable software iSCSI on host 'esxi-01'

vmware-storage iscsi add-target esxi-01 10.0.0.100 --dry-run
# Output: [DRY-RUN] Would add iSCSI target 10.0.0.100:3260 to host 'esxi-01' and rescan
```

### Prompt Injection Defense

Datastore file names and paths returned from vSphere are sanitized before output via the `_sanitize()` function:

- Strips C0/C1 control characters (U+0000-U+0008, U+000B, U+000C, U+000E-U+001F, U+007F-U+009F)
- Preserves newlines and tabs
- Truncates to 500 characters maximum

This prevents malicious file names on datastores from injecting prompts or instructions when the data flows to downstream LLM agents.

### Input Validation

- **IP addresses**: Validated via Python's `ipaddress.ip_address()` before any iSCSI operation
- **Ports**: Validated to be in range 1-65535
- **Datastore names**: Case-sensitive lookup; returns a clear error if not found
- **Host names**: Looked up via vSphere inventory; raises `HostNotFoundError` if not found
- **Cluster names**: Looked up via vSphere inventory; raises `VSANError` if not found

### Transport Security

- The MCP server uses **stdio transport** (local only) -- no network listener is opened
- vSphere connections use SSL/TLS on port 443 by default
- SSL certificate verification can be enabled per-target via `verify_ssl: true` in config.yaml

### What This Skill Cannot Do

This skill has **no VM operations**. It cannot:
- Power on, power off, or restart VMs
- Create, clone, or delete VMs
- Deploy OVA/OVF templates
- Run commands inside guest VMs
- Modify VM configuration (CPU, memory, network)

For VM operations, use `vmware-aiops`.

## Multi-Target Setup

You can configure multiple vCenter/ESXi targets and switch between them:

```yaml
targets:
  - name: prod-vcenter
    host: vcenter-prod.example.com
    username: svc-storage@vsphere.local
    type: vcenter

  - name: dev-vcenter
    host: vcenter-dev.example.com
    username: administrator@vsphere.local
    type: vcenter

  - name: lab-esxi
    host: 10.0.1.50
    username: root
    type: esxi
```

```bash
# Uses first target (prod-vcenter) by default
vmware-storage datastore list

# Explicitly target dev
vmware-storage datastore list --target dev-vcenter

# Target standalone ESXi
vmware-storage iscsi status lab-esxi --target lab-esxi
```

## Version Compatibility

| vSphere / VCF | Support | Notes |
|---------|---------|-------|
| VCF 9.1 / vSphere 9.1 | Full | Released 2026-05-12. pyVmomi+vSAN SDK `<10.0` works via SOAP. |
| VCF 9.0 / vSphere 9.0 | Full | pyVmomi 8.0.3+ with bundled vSAN SDK connects to vSphere 9. |
| 8.0 | Full | vSAN SDK built into pyVmomi 8.0.3+ |
| 7.0 | Full | All storage APIs work |
| 6.7 | Compatible | iSCSI + datastore features work; vSAN limited |

## File Locations

| File | Purpose |
|------|---------|
| `~/.vmware-storage/config.yaml` | Connection targets and settings |
| `~/.vmware-storage/.env` | Passwords (chmod 600) |
| `~/.vmware/audit.db` | Operation audit trail (SQLite WAL, via vmware-policy) |
| `~/.vmware-storage/image_registry.json` | Cached image scan results |
| `~/.vmware-storage/scan.log` | Scanner log output |
