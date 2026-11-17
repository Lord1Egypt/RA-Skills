# Setup Guide

Complete setup and security guide for `vmware-aria`.

## Prerequisites

- Python 3.10+
- VMware Aria Operations / vRealize Operations 8.x, or VCF Operations 9.x. VCF Operations 9.1.1.0 is a 9.x product version; feature availability is assessed per endpoint, not by an exact-release whitelist.
- Network access to Aria Ops on port 443 (HTTPS)
- Aria Operations credentials:
  - Read operations: `ReadOnly` role minimum
  - Alert acknowledge/cancel: `PowerUser` role or higher

## Product version versus feature evidence

The product was renamed VCF Operations in the 9.x line. Do not infer "unsupported"
from an example that names only 8.x/9.1 or from the version of the bundled API index.
Use `vmware-aria health status` / MCP `get_aria_health` to read the product version,
then judge the requested operation from its response. A successful inventory query
is evidence for that query, not certification of every tool. A 401/403 indicates an
authentication/permission problem; a 404 or an unindexed raw path concerns that
operation and does not by itself establish whole-product incompatibility. Existing
minimum-version declarations, Policy checks and the indexed-path allowlist still apply.
No full live-compatibility result for 9.1.1.0 is claimed by this guidance.

## Installation

### Via uv (recommended)

```bash
uv tool install vmware-aria==2.4.7
```

### Via pip

```bash
pip install vmware-aria==2.4.7
```

### From source

```bash
git clone --branch v2.4.7 https://github.com/vmware-skills/VMware-Aria.git
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
(
  umask 077
  set -C  # Refuse existing files; edit an existing .env locally instead
  cat > ~/.vmware-aria/.env <<'EOF'
VMWARE_ARIA_PROD_PASSWORD=REPLACE_IN_LOCAL_EDITOR
EOF
)
# Before continuing, edit .env locally; never type live secrets into shell commands.
```

This writes placeholders only. Enter passwords or tokens using a local editor after creation; do not paste live credentials into terminal commands, chat or commits. If the file exists, the command refuses to overwrite it; edit the existing file after checking its permissions are `600`.

**Option B — injected environment**: have your secret manager or launcher set
`VMWARE_ARIA_PROD_PASSWORD` in the process environment. Do not type the secret in
a terminal command or include it in MCP configuration committed to source control.

Password variable naming convention: `VMWARE_ARIA_<TARGET_UPPER>_PASSWORD`
- Target `prod` → `VMWARE_ARIA_PROD_PASSWORD`
- Target `aria-lab` → `VMWARE_ARIA_ARIA_LAB_PASSWORD`

### 4. Verify setup

```bash
vmware-aria doctor
```

Expected output: All checks PASS. WARN rows (an unreadable version, a DEGRADED or UNKNOWN platform) do not fail the doctor; FAIL rows do.

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
    host: aria-lab.example.com
    username: admin
    port: 443
    verify_ssl: true     # private CA? see "TLS Certificate Verification" below
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

## TLS Certificate Verification

`verify_ssl` defaults to `true`: a target that omits the key is verified. The
client trusts the public CA bundle shipped with Python's `certifi` package, **not**
the operating-system trust store, so adding your CA to macOS Keychain or
`/etc/pki` does not change what `vmware-aria` accepts.

**Appliance signed by a private or enterprise CA** — keep `verify_ssl: true` and
point `SSL_CERT_FILE` at the PEM certificate of the CA that signed the Aria
Operations certificate:

```bash
export SSL_CERT_FILE=/path/to/aria-ca.pem
vmware-aria doctor
```

For the MCP server, add `"SSL_CERT_FILE": "/path/to/aria-ca.pem"` to the
server's `env` block next to `VMWARE_ARIA_CONFIG`. `SSL_CERT_FILE` replaces the
default bundle for the whole process; if that process must also reach public
HTTPS (for example `uvx` resolving packages from PyPI), point it at a bundle that
contains both your CA and the public roots.

**Isolated lab only** — `verify_ssl: false` disables certificate *and* hostname
checking for that one target. The username and password are then sent to
whatever answers at that address, so use it only on a lab network you control,
never for production or for a target reached over a network you do not trust.

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
> If using `uvx --from vmware-aria==2.4.7 vmware-aria mcp` and you hit
> `invalid peer certificate: UnknownIssuer` behind a corporate TLS proxy,
> set `UV_NATIVE_TLS=true` or use the recommended form above.

### With Cursor

Add to `.cursor/mcp.json` in your project (see `examples/mcp-configs/cursor.json`).

### With Goose

Add to `~/.config/goose/config.yaml` (see `examples/mcp-configs/goose.json`).

---

## Limiting which tools are offered

By default the MCP server offers every tool. To offer only read tools, start it with `--expose read`, or set
`VMWARE_ARIA_MCP_EXPOSE=read` in the MCP client's `env` block (useful when the client launches `vmware-aria mcp` itself). To offer
chosen write tools as well, add `--allow-write` with a comma-separated list (or `VMWARE_ARIA_MCP_ALLOW_WRITE`):

```bash
vmware-aria mcp --expose read --allow-write acknowledge_alert
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
  `vmware_policy.exposure.restrict_tools(mcp, skill="aria", expose="read", allow_write=[...])` before running it,
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
vmware-aria mcp --transport https --host 0.0.0.0 --port 8443 \
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
  target, up to `VMWARE_MCP_POOL_SIZE` (default 2) sessions per target. Each session is a login on the target; a
  call waits at most 300 s for a free one.
- **Everyone who can reach the endpoint acts with this server's account.** Tokens identify callers; they grant
  nothing on the platform. Run one endpoint per privilege level (for example a read-only account behind
  `--expose read`, and a separate endpoint for operators).
- **Several people or roles on one endpoint:** run `vmware-audit roles enable` once, then give each token a role (`vmware-audit token create NAME --role reader`, or a role in `roles.yaml` naming tools and targets; vmware-policy ≥ 1.24.0). A role limits what the token may call on this endpoint; it cannot grant more than the account has. See vmware-policy's README, "Roles for network callers".

## Behind an MCP gateway

A gateway (one MCP endpoint in front of several servers, for example vmware-monitor, vmware-aria and
vmware-log-insight) works with these servers as they are: each backend runs as in
[Serving MCP over HTTPS](#serving-mcp-over-https), and the gateway is just another client. Tool names do not
collide across vmware-monitor, vmware-aria and vmware-log-insight, so the gateway needs no prefixes. What to
decide:

- **Who the backend sees.** If the gateway calls every backend with one token of its own, every audit row says
  `token:<gateway>` and per-caller roles stop meaning anything. To keep per-person audit and roles, have the gateway
  **forward each caller's own `Authorization` header** to the backend. Servers on one host with the same `OPS_HOME`
  (default `~/.vmware`) share one token file, so one token per person works on all of them. A backend session is
  bound to the token that opened it, so the gateway must open a backend session per caller, not share one. If the gateway does
  its own authentication instead, give it a token per backend and accept that audit identifies the gateway, not
  the person; forward `traceparent` or `X-Request-ID` so `vmware-audit log --correlation-id ID` still ties calls to
  one platform request.
- **Read-only does not depend on the gateway.** Keep the layers on each backend: a read-only platform account (the
  real boundary), `--expose read` so write tools are never offered, and deny rules in `~/.vmware/rules.yaml`. A
  gateway misconfiguration then cannot turn into a write.
- **Tool list size is the main cost, not the extra hop.** The hop adds milliseconds; platform calls take hundreds
  of milliseconds to seconds. But clients put every offered tool's schema into the model's context on every turn.
  Even with `--expose read`, the schemas of vmware-monitor, vmware-aria and vmware-log-insight together come to
  about 30,000 tokens or more. Offer the gateway's clients a curated subset, or group
  tools per task, rather than passing all of them through.
- **Timeouts and sessions.** Set the gateway's per-call timeout above the longest call you expect: a call can wait
  up to 300 s for a free session to a busy target. A backend MCP session expires after 30 minutes idle; the gateway
  must start a new session when the backend answers 404 for an old one, as the MCP specification requires.
- **Scaling.** Run one backend endpoint per privilege level, not one per caller. Add sessions per target with
  `VMWARE_MCP_POOL_SIZE` before adding processes. Point the gateway's health checks at `GET /healthz`.

## Docker Deployment

### Build and run

```bash
docker build -t vmware-aria:2.4.7 .
docker run --pull=never -i \
  -v ~/.vmware-aria:/root/.vmware-aria:ro \
  -e VMWARE_ARIA_CONFIG=/root/.vmware-aria/config.yaml \
  vmware-aria:2.4.7
```

These commands run the image built locally above; `--pull=never` prevents a missing local image from falling back to a registry. The version tag identifies this build, not an immutable digest.

### Using docker-compose

```bash
# Inject VMWARE_ARIA_PROD_PASSWORD through your secret manager/launcher first.
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

## Read-Only Operation

To run the agent read-only, give it a read-only Aria service account (RBAC).

## Architecture

```
User (natural language)
  |
AI Agent (Claude Code / Goose / Cursor)
  | reads SKILL.md
vmware-aria CLI or MCP server (stdio transport)
  | Aria Operations Suite API (REST/JSON over HTTPS)
  | POST /suite-api/api/auth/token/acquire → vRealizeOpsToken
Aria Operations Manager
  |
VMs / Hosts / Clusters / Datastores / Alerts / Capacity
```

By default the MCP server uses local stdio without a listener; opt-in HTTPS opens a listener and requires TLS plus caller authentication. Connections to Aria Ops use HTTPS on port 443 with vRealizeOpsToken authentication (6-hour sliding token validity, auto-refreshed).

## Security Notes

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware" and "Aria" are trademarks of Broadcom.

- **Source Code**: Fully open source at [github.com/vmware-skills/VMware-Aria](https://github.com/vmware-skills/VMware-Aria) (MIT). The `uv` installer fetches the `vmware-aria` package from PyPI, which is built from this GitHub repository. We recommend reviewing the source code and commit history before deploying in production.
- **Never** store passwords in `config.yaml` — use env vars or `.env` file
- `.env` file must be `chmod 600` (owner read/write only)
- TLS verification is on by default (`verify_ssl: true`); trust a private CA with `SSL_CERT_FILE` rather than disabling verification (see [TLS Certificate Verification](#tls-certificate-verification))
- By default the MCP server uses local stdio without a listener. Opt-in HTTPS requires TLS plus caller authentication and opens the configured listener
- Audit log at `~/.vmware/audit.db` (SQLite WAL, via vmware-policy) records all write operations (alert acknowledge/cancel, alert definition management, report generate/delete)
- Tokens have a 6-hour sliding validity (extended on each call); the client re-acquires automatically 60 seconds before expiry. Requests carry `Authorization: vRealizeOpsToken <token>`

---

## Troubleshooting

### Connection refused on port 443

```bash
# Test connectivity
vmware-aria doctor
# Or manually, verifying the certificate against your CA
curl --cacert /path/to/aria-ca.pem https://aria-ops.example.com/suite-api/api/versions/current
```

Check: firewall rules, VPN connectivity, Aria Ops service status. Any HTTP
response (even 401) means the network path and certificate are fine; a curl
certificate error means the CA file is not the one that signed the appliance
certificate.

### "401 Unauthorized" on token acquire

Verify:
1. Username and password are correct
2. `auth_source` matches the authentication source name in Aria Ops
3. The user account is not locked

### "the body is not JSON" or "response carried no 'token' field"

Aria Operations answered with a success status but not with suite-api JSON — a
login page, an SSO redirect, or a proxy in front of the node answers like this.
Every tool reports it as an error naming the method, path, HTTP status and
content type (`NonJsonBodyError`) instead of a JSON decode traceback; during
token acquisition it is reported as "most likely not an Aria Operations suite-api
endpoint" (`NotSuiteApiError`). Check that `host` and `port` for the target reach
the Aria Operations node itself.

### Self-signed certificate error

Export the CA that signed the Aria Ops certificate as PEM and set
`SSL_CERT_FILE=/path/to/aria-ca.pem` (see
[TLS Certificate Verification](#tls-certificate-verification)). Installing it
into the system trust store has no effect: the client uses the `certifi` bundle.
`verify_ssl: false` is for isolated labs only.

### Metrics return empty list

The metric key may not apply to this resource kind, or collection has not started yet. The `missing` list in the output says which: `not_collected_for_resource` (try one of its `similar_keys`), `no_data_in_window`, `resource_reports_no_stat_keys`, or `undetermined` (the stat-key list could not be read or is in an unrecognised form). You can also browse available metric keys in the Aria Ops UI: navigate to the resource → Metrics tab.
