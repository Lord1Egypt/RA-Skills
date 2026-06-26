# Setup Guide

Complete setup and security guide for `vmware-aria`.

## Prerequisites

- Python 3.10+
- VMware Aria Operations 8.x (or vRealize Operations 8.x)
- Network access to Aria Ops on port 443 (HTTPS)
- Aria Operations credentials:
  - Read operations: `ReadOnly` role minimum
  - Alert acknowledge/cancel: `PowerUser` role or higher

## Installation

### Via uv (recommended)

```bash
uv tool install vmware-aria
```

### Via pip

```bash
pip install vmware-aria
```

### From source

```bash
git clone https://github.com/zw008/VMware-Aria.git
cd VMware-Aria
pip install -e .
```

## Configuration

### 1. Create config directory

```bash
mkdir -p ~/.vmware-aria
```

### 2. Create config.yaml

```bash
cp config.example.yaml ~/.vmware-aria/config.yaml
```

Edit `~/.vmware-aria/config.yaml`:

```yaml
targets:
  prod:
    host: aria-ops.example.com    # Aria Ops FQDN or IP
    username: admin
    port: 443
    verify_ssl: true
    auth_source: LOCAL            # LOCAL | LDAP | AD

default_target: prod
```

### 3. Set password

**Option A — .env file (recommended)**:
```bash
cat > ~/.vmware-aria/.env << 'EOF'
VMWARE_ARIA_PROD_PASSWORD=your_password_here
EOF
chmod 600 ~/.vmware-aria/.env
```

**Option B — shell environment**:
```bash
export VMWARE_ARIA_PROD_PASSWORD=your_password_here
```

Password variable naming convention: `VMWARE_ARIA_<TARGET_UPPER>_PASSWORD`
- Target `prod` → `VMWARE_ARIA_PROD_PASSWORD`
- Target `aria-lab` → `VMWARE_ARIA_ARIA_LAB_PASSWORD`

### 4. Verify setup

```bash
vmware-aria doctor
```

Expected output: All checks PASS.

---

## Multiple Targets

```yaml
targets:
  prod:
    host: aria-prod.example.com
    username: admin
    port: 443
    verify_ssl: true
    auth_source: LOCAL

  lab:
    host: 10.0.0.100
    username: admin
    port: 443
    verify_ssl: false    # Allow self-signed cert
    auth_source: LOCAL

default_target: prod
```

Set passwords for each target:
```bash
VMWARE_ARIA_PROD_PASSWORD=prod_pw
VMWARE_ARIA_LAB_PASSWORD=lab_pw
```

Use `--target` to select:
```bash
vmware-aria resource list --target lab
vmware-aria alert list --target prod
```

---

## Authentication (LDAP / Active Directory)

For LDAP or AD authentication, update `auth_source` in config:

```yaml
targets:
  corp:
    host: aria-ops.corp.example.com
    username: jsmith@corp.example.com
    port: 443
    verify_ssl: true
    auth_source: LDAP    # or AD
```

The `auth_source` value must match the configured authentication source name in Aria Ops (Administration > Authentication Sources).

---

## MCP Server Setup

### With Claude Code

Add to `~/.claude.json` (or use `claude mcp add`):

```json
{
  "mcpServers": {
    "vmware-aria": {
      "command": "vmware-aria",
      "args": ["mcp"],
      "env": {
        "VMWARE_ARIA_CONFIG": "/Users/<username>/.vmware-aria/config.yaml"
      }
    }
  }
}
```

> v1.5.15+ recommends `vmware-aria mcp`. Pre-1.5.15 used the legacy
> `vmware-aria-mcp` console script (still kept for backward compatibility).
> If using `uvx --from vmware-aria vmware-aria mcp` and you hit
> `invalid peer certificate: UnknownIssuer` behind a corporate TLS proxy,
> set `UV_NATIVE_TLS=true` or use the recommended form above.

### With Cursor

Add to `.cursor/mcp.json` in your project (see `examples/mcp-configs/cursor.json`).

### With Goose

Add to `~/.config/goose/config.yaml` (see `examples/mcp-configs/goose.json`).

---

## Docker Deployment

### Build and run

```bash
docker build -t vmware-aria .
docker run -i \
  -v ~/.vmware-aria:/root/.vmware-aria:ro \
  -e VMWARE_ARIA_CONFIG=/root/.vmware-aria/config.yaml \
  vmware-aria
```

### Using docker-compose

```bash
# Set password in your shell first
export VMWARE_ARIA_PROD_PASSWORD=your_password

docker-compose up
```

The docker-compose.yml mounts `~/.vmware-aria` read-only into the container.

---

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

## Security Notes

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware" and "Aria" are trademarks of Broadcom.

- **Source Code**: Fully open source at [github.com/zw008/VMware-Aria](https://github.com/zw008/VMware-Aria) (MIT). The `uv` installer fetches the `vmware-aria` package from PyPI, which is built from this GitHub repository. We recommend reviewing the source code and commit history before deploying in production.
- **Never** store passwords in `config.yaml` — use env vars or `.env` file
- `.env` file must be `chmod 600` (owner read/write only)
- Use `verify_ssl: true` in production; only disable for lab environments
- The MCP server uses stdio transport — it runs locally only, no network listener
- Audit log at `~/.vmware/audit.db` (SQLite WAL, via vmware-policy) records all write operations (alert acknowledge/cancel, alert definition management, report generate/delete)
- Tokens have a 6-hour sliding validity (extended on each call); the client re-acquires automatically 60 seconds before expiry. Requests carry `Authorization: vRealizeOpsToken <token>`

---

## Troubleshooting

### Connection refused on port 443

```bash
# Test connectivity
vmware-aria doctor
# Or manually
curl -k https://aria-ops.example.com/suite-api/api/auth/token/acquire
```

Check: firewall rules, VPN connectivity, Aria Ops service status.

### "401 Unauthorized" on token acquire

Verify:
1. Username and password are correct
2. `auth_source` matches the authentication source name in Aria Ops
3. The user account is not locked

### Self-signed certificate error

Set `verify_ssl: false` in config for the target, or install the Aria Ops certificate into the system trust store.

### Metrics return empty list

The metric key may not apply to this resource kind, or collection has not started yet. Browse available metric keys in the Aria Ops UI: navigate to the resource → Metrics tab.
