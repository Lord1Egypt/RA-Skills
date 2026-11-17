# VMware AVI Setup Guide

Complete installation, configuration, and AI platform integration guide for the current `vmware-avi` release. Refer to `RELEASE_NOTES.md` in the repository for version-specific changes.

## Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | >= 3.10 | Runtime |
| uv | >= 0.4 | Package manager and tool runner |
| avisdk | >= 22.1 | AVI Controller API (auto-installed) |
| kubernetes (Python) | >= 28.0 | K8s API client for AKO operations (auto-installed) |
| kubectl | any recent | Required for AKO pod/ingress/sync operations |
| helm | >= 3.x | Required for AKO config show/diff/upgrade |
| vmware-policy | >= 1.0.0 | Audit and policy engine (auto-installed) |

**Optional**: `kubeconfig` file with access to clusters running AKO (only needed for AKO mode).

## Installation

### Standard Install (recommended)

```bash
uv tool install vmware-avi==2.5.2
```

This installs the CLI (`vmware-avi`, with `vmware-avi mcp` subcommand for the MCP server in v1.5.15+), the legacy `vmware-avi-mcp` entry point (for backward compatibility), and all Python dependencies in an isolated environment.

### Development Install

```bash
git clone --branch v2.5.2 https://github.com/vmware-skills/VMware-AVI.git
cd VMware-AVI
uv pip install -e ".[dev]"
```

### Alternative Deployment: Container / Smithery

For platforms that prefer containerized MCP servers (e.g., Smithery registry, Kubernetes-hosted agents, isolated CI runners), `vmware-avi` ships a `Dockerfile` and `smithery.yaml` at the repository root (added v1.5.22).

#### Docker

Build and run the MCP server in a container. The image uses `python:3.12-slim` with `uv` for dependency installation and runs `python -m vmware_avi.mcp_server` on stdio (no port exposed — MCP uses stdin/stdout).

```bash
git clone --branch v2.5.2 https://github.com/vmware-skills/VMware-AVI.git
cd VMware-AVI

# Build
docker build -t vmware-avi-mcp:2.5.2 .

# Run — mount your config directory into the container
docker run --pull=never -i --rm \
  -v ~/.vmware-avi:/root/.vmware-avi:ro \
  -e VMWARE_AVI_CONFIG=/root/.vmware-avi/config.yaml \
  vmware-avi-mcp:2.5.2
```

These commands run the image built locally above; `--pull=never` prevents a missing local image from falling back to a registry. The version tag identifies this build, not an immutable digest.


The container's `CMD` is `python -m vmware_avi.mcp_server`, which is wired through `vmware_avi/mcp_server/__main__.py` to the same FastMCP entry point as the CLI subcommand. All 28 tools are available.

#### Smithery

`vmware-avi` is published on the [Smithery](https://smithery.ai) registry. The `smithery.yaml` at the repo root declares:

- `startCommand.type: stdio` — Smithery launches the server over stdio
- `configSchema.properties.config_path` — optional override for the config file location
- `commandFunction` — invokes the `vmware-avi mcp` entry point with `VMWARE_AVI_CONFIG` set from the user's Smithery config

Users can install via the Smithery UI or CLI without managing Python environments locally. Smithery handles the container build and stdio bridge automatically.

#### When to use which deployment

| Deployment | Best For |
|------------|----------|
| `uv tool install vmware-avi==2.5.2` + `vmware-avi mcp` | Local developer workstation, single-user CLI + MCP |
| Docker image | Self-hosted agents, CI runners, isolated environments, multi-user servers |
| Smithery | Zero-install agent integration, registry-managed discovery, hosted-MCP workflows |

### Verify Installation

```bash
vmware-avi doctor
```

The `doctor` command checks all of the following:
- Config directory and files exist
- `.env` file permissions are 600
- avisdk and kubernetes Python packages installed
- kubectl and helm binaries in PATH
- kubeconfig file exists
- AVI Controller(s) reachable
- vmware-policy package installed

## AVI Controller Configuration

### Step 1: Generate config templates

```bash
vmware-avi init
```

This creates two files in `~/.vmware-avi/`:
- `config.yaml` -- connection targets and AKO settings
- `.env` -- passwords (auto-set to chmod 600)

### Step 2: Edit config.yaml

```yaml
# ~/.vmware-avi/config.yaml
controllers:
  - name: prod-avi
    host: avi-controller.example.com
    username: admin
    api_version: "22.1.4"
    tenant: admin
    port: 443
    verify_ssl: true
    environment: production   # scopes policy rules; see the field table below

  - name: staging-avi
    host: avi-staging.example.com
    username: admin
    api_version: "22.1.4"
    tenant: admin
    verify_ssl: false    # lab/self-signed certs only
    environment: staging

default_controller: prod-avi

ako:
  kubeconfig: ~/.kube/config
  default_context: ""        # empty = use current-context
  namespace: avi-system
```

**TLS verification**: `verify_ssl` defaults to `true` when omitted — keep it on for any real controller; the
account is privileged, and with verification off anyone on the network path can impersonate the controller and
capture its password. For a certificate issued by a private CA, trust that CA rather than turning verification off.
`verify_ssl: false` (like `staging-avi` above) is for an isolated lab controller with a self-signed certificate
only, never for production.

**config.yaml fields**:

| Field | Required | Default | Description |
|-------|:--------:|---------|-------------|
| `controllers[].name` | Yes | -- | Unique identifier for this controller |
| `controllers[].host` | Yes | -- | Controller hostname or IP |
| `controllers[].username` | No | `admin` | API username |
| `controllers[].api_version` | No | `22.1.4` | AVI API version string |
| `controllers[].tenant` | No | `admin` | AVI tenant name |
| `controllers[].port` | No | `443` | Controller HTTPS port |
| `controllers[].verify_ssl` | No | `true` | TLS certificate verification |
| `controllers[].environment` | Optional | -- | Free-form label (`production` / `staging` / `lab`). An environment-scoped `deny` rule in `~/.vmware/rules.yaml` can match on it to block writes (e.g. freeze `production`); a controller with no label is simply not matched by such a rule. Read-only operations are never affected. |
| `default_controller` | No | first entry | Which controller to use by default |
| `ako.kubeconfig` | No | `~/.kube/config` | Path to kubeconfig file |
| `ako.default_context` | No | current-context | K8s context for AKO operations |
| `ako.namespace` | No | `avi-system` | Namespace where AKO is deployed |

### Step 3: Set passwords in .env

```bash
# ~/.vmware-avi/.env
PROD_AVI_PASSWORD=your-secure-password-here
STAGING_AVI_PASSWORD=another-password-here
```

Password environment variable naming convention: `<CONTROLLER_NAME>_PASSWORD` where the controller name is uppercased and hyphens are replaced with underscores.

| Controller Name | Environment Variable |
|-----------------|---------------------|
| `prod-avi` | `PROD_AVI_PASSWORD` |
| `staging-avi` | `STAGING_AVI_PASSWORD` |
| `my-lab` | `MY_LAB_PASSWORD` |

### Step 4: Verify connectivity

```bash
vmware-avi doctor
vmware-avi vs list          # quick smoke test
```

## AKO / Kubernetes Configuration

AKO operations require a valid kubeconfig with access to the cluster(s) where AKO is deployed.

### kubeconfig Setup

```bash
kubectl --context my-cluster get pods -n avi-system   # verify access
kubectl config get-contexts                            # list all contexts
```

If your AKO is deployed in a non-default namespace, update `ako.namespace` in config.yaml. AKO config commands (`config-show`, `config-diff`, `config-upgrade`) require Helm 3.x:

```bash
helm repo add ako https://projects.registry.vmware.com/chartrepo/ako
helm repo update
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

## Limiting which tools are offered

By default the MCP server offers every tool. To offer only read tools, start it with `--expose read`, or set
`VMWARE_AVI_MCP_EXPOSE=read` in the MCP client's `env` block (useful when the client launches `vmware-avi mcp` itself). To offer
chosen write tools as well, add `--allow-write` with a comma-separated list (or `VMWARE_AVI_MCP_ALLOW_WRITE`):

```bash
vmware-avi mcp --expose read --allow-write disable_lb_pool_member
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
  `vmware_policy.exposure.restrict_tools(mcp, skill="avi", expose="read", allow_write=[...])` before running it,
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
vmware-avi mcp --transport https --host 0.0.0.0 --port 8443 \
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
- Each audit row records the caller as `token:<name>`. Calls run side by side: each holds its own session to a
  Controller (or Kubernetes context), up to `VMWARE_MCP_POOL_SIZE` (default 2) sessions per target. Each Controller
  session is a login on the Controller; a call waits at most 300 s for a free one.
- **Everyone who can reach the endpoint acts with this server's account.** Tokens identify callers; they grant
  nothing on the platform. Run one endpoint per privilege level (for example a read-only account behind
  `--expose read`, and a separate endpoint for operators).
- **Several people or roles on one endpoint:** run `vmware-audit roles enable` once, then give each token a role (`vmware-audit token create NAME --role reader`, or a role in `roles.yaml` naming tools and targets; vmware-policy ≥ 1.24.0). A role limits what the token may call on this endpoint; it cannot grant more than the account has. See vmware-policy's README, "Roles for network callers".

## Security

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware", "NSX", and "AVI" are trademarks of Broadcom.

### Password Management

- Passwords are **never** stored in `config.yaml` -- only in `.env`
- The `.env` file must have `chmod 600` permissions (owner read/write only)
- `vmware-avi doctor` warns if `.env` permissions are too open
- Never commit `.env` files to version control

### Audit Logging

All operations (CLI and MCP) are recorded via vmware-policy:

- **Location**: `~/.vmware/audit.db` (SQLite, WAL mode)
- **Contents**: timestamp, tool name, parameters, result, user identity
- **Query**: `vmware-audit log --last 20`

### Policy Rules

Optional deny rules and maintenance windows can be configured in `~/.vmware/rules.yaml` (managed by vmware-policy). Example: block `set_virtual_service_enabled` disable during business hours.

### Destructive Operation Safety

| Operation | Safety Measures |
|-----------|----------------|
| VS disable | CLI: double confirmation prompt. MCP `set_virtual_service_enabled`: previews `blast_radius` unless `confirm=true` |
| Pool member disable | CLI: double confirmation prompt (graceful drain). MCP: previews unless `confirm=true`; refuses the pool's only enabled member |
| AKO restart | CLI: double confirmation prompt. MCP: previews unless `confirm=true`; refuses a terminating pod |
| AKO config upgrade | CLI: defaults to `--dry-run`; double confirmation for actual apply. MCP: previews (with `helm --dry-run` output) unless `confirm=true`; refuses a failing dry-run |
| AKO sync force | CLI: double confirmation prompt. MCP: previews unless `confirm=true` |

### Read-Only Operation

To run the agent read-only, give it a read-only AVI service account (RBAC).

### Data Sanitization

All text returned from AVI Controller APIs is processed through `_sanitize()`:
- Truncated to 500 characters maximum
- C0/C1 control characters stripped
- Prevents prompt injection via API response content

### TLS Verification

- Enabled by default (`verify_ssl: true`)
- Set `verify_ssl: false` only for lab environments with self-signed certificates
- Production deployments should always use valid TLS certificates

## AI Platform Compatibility

vmware-avi supports MCP (Model Context Protocol) integration with the following platforms.

### Claude Code (Claude Desktop / CLI)

Add to `~/.claude.json` (global) or `.mcp.json` (project-level):

```json
{
  "mcpServers": {
    "vmware-avi": {
      "command": "vmware-avi",
      "args": ["mcp"],
      "env": {
        "VMWARE_AVI_CONFIG": "~/.vmware-avi/config.yaml"
      }
    }
  }
}
```

> v1.5.15+ recommends the single-command form `vmware-avi mcp`. Pre-1.5.15 used
> `uvx --from vmware-avi==2.5.2 vmware-avi-mcp`, which still works but re-resolves from
> PyPI on each launch and breaks behind corporate TLS proxies. The legacy
> `vmware-avi-mcp` entry point is also kept for backward compatibility.

### Cursor

Add to `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "vmware-avi": {
      "command": "vmware-avi",
      "args": ["mcp"],
      "env": {
        "VMWARE_AVI_CONFIG": "~/.vmware-avi/config.yaml"
      }
    }
  }
}
```

### Windsurf / Cline / Qwen / Other MCP-compatible Agents

Use the same JSON block as above, placed in the platform-specific config file:

| Platform | Config File |
|----------|-------------|
| Windsurf | `~/.windsurf/mcp.json` |
| Cline (VS Code) | Cline MCP settings panel |
| Qwen / other | Any MCP stdio transport config |

### Ollama / Local Models

For local models with limited context windows, prefer CLI mode over MCP:

```bash
# CLI produces ~2K tokens vs ~8K for MCP JSON
vmware-avi vs list
vmware-avi ako status
```

If your Ollama setup supports MCP via a bridge (e.g., `mcp-bridge`), use the same `vmware-avi mcp` command (v1.5.15+).

## Troubleshooting

### "Config file not found" on first run

```bash
vmware-avi init    # generates ~/.vmware-avi/config.yaml and .env
```

### "Password not found" error

The environment variable name must match `<CONTROLLER_NAME>_PASSWORD` with the controller name uppercased and hyphens replaced by underscores. Check:

```bash
# For controller "prod-avi", inject PROD_AVI_PASSWORD via a secret manager.
# Or edit the owner-only ~/.vmware-avi/.env locally; never paste secrets in commands.
```

### "Controller unreachable" in doctor

1. Verify the `host` and `port` in config.yaml are correct
2. Test network connectivity: `curl --cacert /path/to/controller-ca.pem https://avi-controller.example.com/api/cluster`
3. For a self-signed certificate on an isolated lab controller only, set `verify_ssl: false` on that entry; for a private-CA certificate, trust that CA instead of turning verification off
4. Check if a firewall or VPN is blocking port 443

### MCP server not starting

1. Verify the CLI is on PATH: `which vmware-avi`
2. Confirm the `mcp` subcommand: `vmware-avi mcp --help` (v1.5.15+)
3. Check that `~/.vmware-avi/config.yaml` exists (MCP server loads config on startup)
4. Legacy: `which vmware-avi-mcp` and `vmware-avi-mcp --help` still work
5. Never use `python -m vmware_avi.mcp_server` — always use `vmware-avi mcp` (v1.5.15+) or the legacy `vmware-avi-mcp` entry point

### `invalid peer certificate: UnknownIssuer` (uvx)

A corporate TLS proxy is intercepting `https://pypi.org` and uv's bundled cert
store doesn't trust the proxy CA. Fixes (in order of preference):

1. Use the v1.5.15+ form `vmware-avi mcp` — no PyPI roundtrip needed.
2. Tell uv to use the system cert store: `export UV_NATIVE_TLS=true` (or pass
   `--native-tls` to `uvx`).
3. Point uv at an explicit CA bundle: `export SSL_CERT_FILE=/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem`

### kubectl / helm not found

```bash
# macOS
brew install kubectl helm
```

For Linux, see https://kubernetes.io/docs/tasks/tools/ and https://helm.sh/docs/intro/install/.

### AKO namespace not found

Update `ako.namespace` in config.yaml to match your deployment (default: `avi-system`).

### Permission denied on .env file

```bash
chmod 600 ~/.vmware-avi/.env
```

### MCP 2.5 legacy argument migration

The deprecated `confirmed` and `dry_run` MCP write-tool aliases are removed in
2.5. Old arguments fail validation without executing a write. Omit `confirm` for
a preview; pass `confirm=true` for execution through the existing fresh
measurement, Policy and audit gate. CLI dry-run flags are unchanged.
