# VMware NSX Security — Setup Guide

## Prerequisites

- NSX Manager 3.x or 4.x (NSX-T)
- An NSX admin account with DFW read/write permissions
- Python 3.10+ and `uv` installed

## 1. Install

```bash
uv tool install vmware-nsx-security==1.17.3
```

Verify:
```bash
vmware-nsx-security --help
```

## 2. Create Config Directory

```bash
mkdir -p ~/.vmware-nsx-security
```

## 3. Create Config File

Copy the example and edit:

```bash
# From the package source directory
cp config.example.yaml ~/.vmware-nsx-security/config.yaml
```

Or create manually:

```yaml
# ~/.vmware-nsx-security/config.yaml
targets:
  nsx-prod:
    host: nsx-manager.example.com
    username: admin
    port: 443
    verify_ssl: true
    environment: production   # Which environment this is — see below
  nsx-lab:
    host: 10.0.0.50
    username: admin
    port: 443
    verify_ssl: false   # Allow self-signed cert in lab
    environment: lab

default_target: nsx-prod
```

**TLS verification**: `verify_ssl` defaults to `true` when omitted. If NSX Manager's certificate is issued by a private/enterprise CA, keep `verify_ssl: true` and point the `SSL_CERT_FILE` environment variable at a PEM bundle that contains that CA — in your shell, or in the MCP server's `env` block. `verify_ssl: false` disables certificate and hostname checks entirely; use it only for an isolated lab NSX Manager, never for a production target.

**`environment` (optional label)**: policy scopes its rules by this value, so an environment-scoped `deny` rule in `~/.vmware/rules.yaml` can match on it — for example, to freeze state-changing writes on `production`. Any label you like works (`production`, `staging`, `lab`, `dc2-prod`); the target's *name* is not used for it.

A target with no label is simply not matched by such a rule. Read-only operations are never affected either way. Run `vmware-audit policy` to see the rules currently in force.

## 4. Set Passwords

Passwords are **never** stored in `config.yaml`. Use environment variables or a `.env` file:

```bash
# Create .env file
(
  umask 077
  set -C  # Refuse existing files; edit an existing .env locally instead
  cat > ~/.vmware-nsx-security/.env <<'EOF'
VMWARE_NSX_SECURITY_NSX_PROD_PASSWORD=REPLACE_IN_LOCAL_EDITOR
VMWARE_NSX_SECURITY_NSX_LAB_PASSWORD=REPLACE_IN_LOCAL_EDITOR
EOF
)
# Before continuing, edit .env locally; never type live secrets into shell commands.
```

This writes placeholders only. Enter passwords or tokens using a local editor after creation; do not paste live credentials into terminal commands, chat or commits. If the file exists, the command refuses to overwrite it; edit the existing file after checking its permissions are `600`.

**Password variable naming convention**: `VMWARE_NSX_SECURITY_<TARGET>_PASSWORD`
where `<TARGET>` is the target name uppercased with hyphens → underscores.

## 5. Verify Setup

```bash
vmware-nsx-security doctor
```

All checks should show PASS:
- Config file
- .env permissions (owner-only 600)
- Config parse (N targets configured)
- Password (set for each target)
- Network (TCP reachable on port 443)
- NSX auth (session created)
- NSX version (vX.Y.Z)
- MCP server import

## 6. Configure MCP Server

### Claude Code

Add to `~/.claude.json` (or `.claude.json` in your project):

```json
{
  "mcpServers": {
    "vmware-nsx-security": {
      "command": "vmware-nsx-security",
      "args": ["mcp"],
      "env": {
        "VMWARE_NSX_SECURITY_CONFIG": "~/.vmware-nsx-security/config.yaml"
      }
    }
  }
}
```

### Cursor

In Cursor Settings → MCP Servers:

```json
{
  "vmware-nsx-security": {
    "command": "vmware-nsx-security",
    "args": ["mcp"],
    "env": {
      "VMWARE_NSX_SECURITY_CONFIG": "${HOME}/.vmware-nsx-security/config.yaml"
    }
  }
}
```

### Goose

```json
{
  "mcpServers": {
    "vmware-nsx-security": {
      "command": "vmware-nsx-security",
      "args": ["mcp"],
      "env": {
        "VMWARE_NSX_SECURITY_CONFIG": "~/.vmware-nsx-security/config.yaml"
      }
    }
  }
}
```

> v1.5.15+ recommends the single-command form `vmware-nsx-security mcp`. Pre-1.5.15 used
> `uvx --from vmware-nsx-security==1.17.3 vmware-nsx-security-mcp`, which still works but re-resolves
> from PyPI on each launch and breaks behind corporate TLS proxies. The legacy
> `vmware-nsx-security-mcp` entry point is also kept for backward compatibility.

## Limiting which tools are offered

By default the MCP server offers every tool. To offer only read tools, start it with `--expose read`, or set
`VMWARE_NSX_SECURITY_MCP_EXPOSE=read` in the MCP client's `env` block (useful when the client launches `vmware-nsx-security mcp` itself). To offer
chosen write tools as well, add `--allow-write` with a comma-separated list (or `VMWARE_NSX_SECURITY_MCP_ALLOW_WRITE`):

```bash
vmware-nsx-security mcp --expose read --allow-write apply_vm_tag
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
  `vmware_policy.exposure.restrict_tools(mcp, skill="nsx_security", expose="read", allow_write=[...])` before running it,
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
vmware-nsx-security mcp --transport https --host 0.0.0.0 --port 8443 \
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
- Each audit row records the caller as `token:<name>`. Calls run side by side, with or without a target: each
  target keeps up to `VMWARE_MCP_POOL_SIZE` sessions (default 2), and each session is a login on the target. A call
  that finds them all busy waits at most 300 s for one.
- **Everyone who can reach the endpoint acts with this server's account.** Tokens identify callers; they grant
  nothing on the platform. Run one endpoint per privilege level (for example a read-only account behind
  `--expose read`, and a separate endpoint for operators).
- **Several people or roles on one endpoint:** run `vmware-audit roles enable` once, then give each token a role (`vmware-audit token create NAME --role reader`, or a role in `roles.yaml` naming tools and targets; vmware-policy ≥ 1.24.0). A role limits what the token may call on this endpoint; it cannot grant more than the account has. See vmware-policy's README, "Roles for network callers".

## 7. Docker (Optional)

Build and run as a container:

```bash
docker-compose up --build
```

Mount your config:
```yaml
# docker-compose.yml already mounts ~/.vmware-nsx-security:/root/.vmware-nsx-security:ro
```

## Companion Skill Setup

For full NSX coverage, also install:

```bash
# NSX networking: segments, gateways, NAT, routing
uv tool install vmware-nsx-mgmt

# vSphere monitoring
uv tool install vmware-monitor
```

Configure each with its own config directory:
- NSX networking: `~/.vmware-nsx/config.yaml`
- NSX security: `~/.vmware-nsx-security/config.yaml`
- Monitor: `~/.vmware-monitor/config.yaml`

Both `vmware-nsx` and `vmware-nsx-security` can point to the same NSX Manager hosts — the config files are separate because the password env vars differ.

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

## Running the Agent Read-Only

To run the agent read-only, give it a read-only NSX service account (RBAC) — writes are then refused by NSX itself, on every surface, which no env var or config switch could guarantee.

## Security Notes

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware" and "NSX" are trademarks of Broadcom.

- **Source Code**: Fully open source at [github.com/vmware-skills/VMware-NSX-Security](https://github.com/vmware-skills/VMware-NSX-Security) (MIT). The `uv` installer fetches the `vmware-nsx-security` package from PyPI, which is built from this GitHub repository. We recommend reviewing the source code and commit history before deploying in production.
- `config.yaml` should be readable only by your user: `chmod 600 ~/.vmware-nsx-security/config.yaml`
- `.env` must be `chmod 600` — the doctor check warns if it is too permissive
- Use a dedicated read/write NSX account for security operations, not the global `admin` superuser
- Audit logs are written to `~/.vmware/audit.db` (SQLite WAL mode, via vmware-policy)
- By default the MCP server uses local stdio, started on demand by the agent, without a listener. Opt-in HTTPS opens the configured listener and requires TLS plus caller authentication
