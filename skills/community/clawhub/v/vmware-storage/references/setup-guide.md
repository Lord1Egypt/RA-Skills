# Setup Guide

Complete setup and security guide for `vmware-storage`.

## Prerequisites

- Python 3.10+
- vCenter Server 6.7+ or standalone ESXi 6.7+
- Network access to vCenter/ESXi on port 443 (or custom port)

## Installation

### Via uv (recommended)

```bash
uv tool install vmware-storage==2.6.2
```

### Via pip

```bash
pip install vmware-storage==2.6.2
```

### From source

```bash
git clone --branch v2.6.2 https://github.com/vmware-skills/VMware-Storage.git
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
    verify_ssl: true           # Default. Verifies the vCenter certificate
    environment: production    # Which environment this target is — see below

  - name: esxi-standalone
    host: 10.0.0.50
    username: root
    type: esxi
    port: 443
    verify_ssl: true
    environment: lab

notify:
  webhook_url: ""              # Optional: webhook for notifications
```

**Keep `verify_ssl: true`.** These accounts are privileged, and with verification off anyone on the
network path can impersonate vCenter/ESXi and capture the password. If a host uses a self-signed
certificate, add its CA to the system trust store rather than turning verification off. Setting
`verify_ssl: false` on a target is supported only for an isolated lab host, never for production.

The first target in the list is the default (used when `--target` is not specified).

#### `environment` — declare which environment each target is

`environment:` is an optional free-form label. Policy scopes its rules by this
value, so an environment-scoped `deny` rule in `~/.vmware/rules.yaml` can match
on it — for example, to freeze state-changing writes (`iscsi enable`,
`iscsi add-target`, `iscsi remove-target`, `rescan`) on `production`. A target
with no label is simply not matched by such a rule.

Any label works (`production`, `staging`, `lab`, or your own); the target's
*name* is not used for scoping. Read-only operations are never affected. Run
`vmware-audit policy` to see the rules actually in force.

### 3. Create .env for credentials

Passwords are **never stored in config.yaml**. They must be set as environment variables via the `.env` file.

```bash
(
  umask 077
  set -C  # Refuse existing files; edit an existing .env locally instead
  cat > ~/.vmware-storage/.env <<'EOF'
VMWARE_MY_VCENTER_PASSWORD=REPLACE_IN_LOCAL_EDITOR
VMWARE_ESXI_STANDALONE_PASSWORD=REPLACE_IN_LOCAL_EDITOR
EOF
)
# Before continuing, edit .env locally; never type live secrets into shell commands.
```

This writes placeholders only. Enter passwords or tokens using a local editor after creation; do not paste live credentials into terminal commands, chat or commits. If the file exists, the command refuses to overwrite it; edit the existing file after checking its permissions are `600`.

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
> `uvx --from vmware-storage==2.6.2 vmware-storage-mcp`, which still works but re-resolves from
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

Or build and run locally from the checked-out release source:

```bash
docker build -t vmware-storage:2.6.2 .
docker run --pull=never -d \
  -v ~/.vmware-storage:/root/.vmware-storage:ro \
  -e VMWARE_STORAGE_CONFIG=/root/.vmware-storage/config.yaml \
  vmware-storage:2.6.2
```

These commands run the image built locally above; `--pull=never` prevents a missing local image from falling back to a registry. The version tag identifies this build, not an immutable digest.


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

## Limiting which tools are offered

By default the MCP server offers every tool. To offer only read tools, start it with `--expose read`, or set
`VMWARE_STORAGE_MCP_EXPOSE=read` in the MCP client's `env` block (useful when the client launches `vmware-storage mcp` itself). To offer
chosen write tools as well, add `--allow-write` with a comma-separated list (or `VMWARE_STORAGE_MCP_ALLOW_WRITE`):

```bash
vmware-storage mcp --expose read --allow-write enable_iscsi
```

- A read tool is one annotated `readOnlyHint: true`; every other tool counts as a write.
- An unknown setting, or a name that is not a write tool of this server, stops the server before it serves (exit
  code 2), so it never offers more than you asked for. Pre-2.0 tool names are accepted.
- With `--expose read`, the server prints one line to stderr saying what it exposes.
- Flags and environment variables are not mixed: if either flag is given, both environment variables are
  ignored, so a leftover `_ALLOW_WRITE` in the shell cannot widen `--expose read`. A blank flag value counts as
  not given.
- A tool that runs other steps (a plan, workflow or batch tool) carries every write it can execute, including
  writes this setting hides. Expose such a tool only if you would expose those writes too.
- A launcher that imports the server object can call
  `vmware_policy.exposure.restrict_tools(mcp, skill="storage", expose="read", allow_write=[...])` before running it,
  instead of editing the SDK's tool registry.
- This limits what clients are offered. It is **not** authorization: whether a call may change anything is decided by
  the account's permissions, and deny rules in `~/.vmware/rules.yaml` still apply to every exposed tool.
- An agent that can run shell commands can also reach the platform without MCP (SSH, curl, govc, PowerCLI). So
  the service account itself must be least-privilege: exposure and deny rules are guardrails, not the boundary.

## Serving MCP over HTTPS

By default the MCP server speaks stdio to one local client. To let clients on other machines reach it, serve it over
HTTPS. Every caller then needs a bearer token.

```bash
vmware-audit token create alice                      # prints the token once; give it to alice
vmware-storage mcp --transport https --host 0.0.0.0 --port 8443 \
    --cert /etc/vmware-mcp/server.pem --key /etc/vmware-mcp/server-key.pem \
    --public-name mcp.example.com
```

- Clients connect to `https://mcp.example.com:8443/mcp` and send `Authorization: Bearer <token>`.
- `--public-name` lists every host name clients use (comma-separated); requests for any other Host or Origin are
  refused. Use a certificate your clients trust for those names.
- Behind a reverse proxy that terminates TLS (Nginx, HAProxy) on the same machine, use
  `--transport http --host 127.0.0.1 --public-name mcp.example.com` (the names the proxy forwards in `Host`), and
  have the proxy pass the `Authorization` header through.
- Behind a load balancer or gateway on another machine, keep `--transport https` (a self-signed certificate is
  fine: the balancer is the client that has to trust it), list in `--public-name` the host name the balancer sends
  as `Host`, and have it forward `Authorization`. Point its health probe at `GET /healthz`: it needs no token, returns
  only `{"status": "ok"}` and accepts any `Host` (vmware-policy ≥ 1.23.0). Every other path still needs the token.
- Correlation: each audit row stores the caller's `traceparent` trace-id, else its `X-Request-ID` /
  `X-Correlation-ID`. Have the agent platform send one, and `vmware-audit log --correlation-id ID` lists the calls
  behind one platform request.
- `vmware-audit token list` / `token revoke NAME` manage callers; a revoked token is refused from its next request.
  Replace a leaked token under a new name.
- The server will not start without at least one token, and checks before it binds that unauthenticated requests
  are refused.
- Each audit row records the caller as `token:<name>`. Calls run side by side, also on the same target: the server keeps up to `VMWARE_MCP_POOL_SIZE` (default 2) sessions per target, each one a login on that target, and a call waits at most 300 s for a free session (vmware-policy ≥ 1.22.0).
- **Everyone who can reach the endpoint acts with this server's account.** Tokens identify callers; they grant
  nothing on the platform. Run one endpoint per privilege level (for example a read-only account behind
  `--expose read`, and a separate endpoint for operators).
- **Several people or roles on one endpoint:** run `vmware-audit roles enable` once, then give each token a role (`vmware-audit token create NAME --role reader`, or a role in `roles.yaml` naming tools and targets; vmware-policy ≥ 1.24.0). A role limits what the token may call on this endpoint; it cannot grant more than the account has. See vmware-policy's README, "Roles for network callers".

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

### Read-only access

To run the agent read-only, give it a read-only vCenter service account (RBAC) — enforced at the platform.

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

- By default the MCP server uses local **stdio** without a listener. Opt-in HTTPS opens the configured listener and requires TLS plus caller authentication
- vSphere connections use SSL/TLS on port 443 by default
- SSL certificate verification is **on by default** (`verify_ssl: true`); turn it off per target only for an isolated lab host with a self-signed certificate

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
