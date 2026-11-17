> Detailed usage and architecture reference. [Quick overview](../../../README.md).


# VMware Aria

[![PyPI](https://img.shields.io/pypi/v/vmware-aria)](https://pypi.org/project/vmware-aria/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#readme-license)

English | [中文](detailed-guide-CN.md)

Maintainer: Wei Zhou · [zhouwei008@gmail.com](mailto:zhouwei008@gmail.com)

Community-maintained open-source project; not an official VMware or Broadcom product.

[Overview](#readme-overview) · [Quick Start](#readme-quick-start) · [MCP Configuration](#readme-mcp-configuration) · [Capabilities and Workflows](#readme-capabilities-and-workflows) · [Safety and Audit](#readme-safety-and-audit) · [Troubleshooting](#readme-troubleshooting) · [Companion Skills](#readme-companion-skills) · [Reference](#readme-reference) · [License](#readme-license)

<a id="readme-overview"></a>

## Product version versus feature evidence

Aria Operations / vRealize Operations 8.x and the renamed VCF Operations 9.x
family are recognized. A 9.1.1.0 release is not unsupported merely because an
example or bundled API snapshot names 9.1. Use `get_aria_health` / CLI `health status`
and the actual response for the requested operation. A successful query establishes
only its observed scope; a 401/403 or an individual missing/unindexed path does not
establish whole-product incompatibility. Version floors, Policy and indexed-path
allowlists remain in force. Full live-tool coverage on 9.1.1.0 is not established.

## Overview

Runs locally over stdio by default; configure required targets and credentials on your own machine.

> **Note**: In VCF 9.0 and later, **VMware Aria Operations** has been rebranded as **VCF Operations**. This skill works against both names — the `/suite-api/` REST endpoints are unchanged.


AI-assisted monitoring and capacity planning for VMware Aria Operations (vRealize Operations) via the Model Context Protocol (MCP).


MCP uses local stdio by default. Opt-in HTTPS opens the configured listener and requires TLS plus caller authentication; it is a network service, not a local-only mode. Credential examples create owner-only placeholder files without overwriting existing files; edit secrets locally.

Container examples build a local version-tagged image and run it with `--pull=never`, avoiding registry fallback. A local version tag is not an immutable image digest.

### Overview

`vmware-aria` exposes 46 MCP tools for interacting with Aria Operations through natural language AI agents (Claude Code, Cursor, Goose, etc.):

| Category | Tools | Type |
|----------|-------|------|
| **Resources** | list, get, metrics, health badge, top consumers, metric keys, properties, relationships | Read-only (8) |
| **Alerts** | list, get, investigate (alert→resource), acknowledge, cancel, definitions, notes (list / add), recommendations | Read + 3 Write (9) |
| **Alert Definitions** | symptom definitions, create, enable/disable, delete | Read + 3 Write (4) |
| **Capacity** | overview, remaining, time-remaining, rightsizing | Read-only (4) |
| **Reports** | definitions, generate, list, get, delete | Read + 2 Write (5) |
| **Anomaly** | list anomalies, risk badge | Read-only (2) |
| **Health** | platform health, collector groups, Aria node memory/swap/heap, adapter collection state | Read-only (4) |
| **Maintenance** | start / end resource maintenance, maintenance schedules | Read + 2 Write (3) |
| **Fleet / PromQL** (VCF Ops 9.1) | fleet certificates, password accounts, VCF domains, diagnostic findings, real-time PromQL query | Read-only (5) |
| **Raw API** | search the API operation index, GET one indexed path — for reads no tool above covers | Read-only (2) |

**Total**: 46 tools — 36 read-only, 10 write

Full agent instructions: [`skills/vmware-aria/SKILL.md`](../../../skills/vmware-aria/SKILL.md).

<a id="readme-quick-start"></a>

## Quick Start

Requires Python `>=3.10` and `uv`.

```bash
uv tool install vmware-aria==2.4.7
vmware-aria --help
```

Target, credential and local data setup: [setup guide](../../../skills/vmware-aria/references/setup-guide.md).

<details>
<summary>Installation and configuration details (including offline setup)</summary>

### Quick Start

```bash
# Install
uv tool install vmware-aria==2.4.7

# Configure
mkdir -p ~/.vmware-aria
cat > ~/.vmware-aria/config.yaml << 'EOF'
targets:
  prod:
    host: aria-ops.example.com
    username: admin
    port: 443
    verify_ssl: true
    auth_source: LOCAL
default_target: prod
EOF

# Set password (never in config.yaml)
(
  umask 077
  set -C  # Refuse existing files; edit an existing .env locally instead
  cat > ~/.vmware-aria/.env <<'EOF'
VMWARE_ARIA_PROD_PASSWORD=REPLACE_IN_LOCAL_EDITOR
EOF
)
# Before continuing, edit .env locally; never type live secrets into shell commands.

# Verify setup
vmware-aria doctor
```

This writes placeholders only. Enter passwords or tokens using a local editor after creation; do not paste live credentials into terminal commands, chat or commits. If the file exists, the command refuses to overwrite it; edit the existing file after checking its permissions are `600`.

On macOS, v2.4.3 honors the system proxy bypass list for Aria targets. If an
older installation reaches TCP/443 but token acquisition ends with a TLS close,
upgrade and rerun `vmware-aria doctor`. `doctor --skip-auth` checks TCP only.

#### Offline / Air-Gapped Install (from source)

This project uses the modern PEP 517 build system (hatchling), so there is **no
`setup.py`** by design — that is expected, not a missing file. If you cloned the
source and hit `ERROR: File "setup.py" or "setup.cfg" not found ... editable mode
currently requires a setuptools-based build`, your `pip` is older than 21.3 and
cannot do an *editable* (`-e`) install with a non-setuptools backend. Editable
mode is a developer convenience, not needed to run the tool — do one of:

```bash
# From the source tree — a normal (non-editable) install builds a wheel:
pip install .              # NOT  pip install -e .

# ...or upgrade pip first, and editable works too:
pip install --upgrade pip && pip install -e .
```

For a **truly air-gapped host**, build the wheels on a connected machine and copy
them over — the target then needs no network:

```bash
# On a connected machine, collect this package + its dependencies as wheels:
pip wheel . -w dist        # → dist/*.whl   (or: uv build, for just this package)

# Copy dist/ to the air-gapped host, then install offline:
pip install --no-index --find-links dist vmware-aria
```


### Authentication

Aria Operations uses **vRealizeOpsToken** authentication:

```
POST /suite-api/api/auth/token/acquire
{"username": "admin", "password": "...", "authSource": "LOCAL"}
→ {"token": "abc123", "validity": 1765182896000}  # validity = expiry epoch ms

Subsequent requests: Authorization: vRealizeOpsToken abc123
```

Tokens have a 6-hour sliding validity (extended on each call, per the official spec); the client re-acquires automatically 60 seconds before expiry. The `validity` field is the expiry timestamp in epoch milliseconds, not a duration.


</details>

<a id="readme-mcp-configuration"></a>

## MCP Configuration

Copy this configuration into your MCP client's local stdio settings. The client must be able to find `uvx`; the initial package installation requires access to a package index.

```json
{
  "mcpServers": {
    "vmware-aria": {
      "command": "uvx",
      "args": ["--from", "vmware-aria==2.4.7", "vmware-aria-mcp"],
      "env": {
        "VMWARE_ARIA_CONFIG": "~/.vmware-aria/config.yaml"
      }
    }
  }
}
```

The following sections retain preinstalled CLI alternatives and product-specific MCP options.

<details>
<summary>Preinstalled CLI and additional MCP options</summary>

### MCP Setup (Claude Code)

After `uv tool install vmware-aria==2.4.7`, add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "vmware-aria": {
      "command": "vmware-aria",
      "args": ["mcp"],
      "env": {
        "VMWARE_ARIA_CONFIG": "~/.vmware-aria/config.yaml"
      }
    }
  }
}
```

> **v1.5.15+** uses the single-command form `vmware-aria mcp`. The legacy
> `vmware-aria-mcp` console script is still kept for backward compatibility.
> If you must use `uvx --from vmware-aria==2.4.7 vmware-aria mcp` (no install) and hit
> `invalid peer certificate: UnknownIssuer` behind a corporate TLS proxy, set
> `UV_NATIVE_TLS=true` or use the recommended `vmware-aria mcp` form above.

Then use natural language:
- *"Show me the top 10 CPU consumers right now"*
- *"List all CRITICAL alerts and acknowledge them"*
- *"How long until the prod cluster runs out of memory?"*
- *"Which VMs are over-provisioned? Show rightsizing recommendations"*
- *"Are there any anomalies on vm-web-01?"*


</details>

<a id="readme-capabilities-and-workflows"></a>

## Capabilities and Workflows

### CLI Examples

```bash
# List top CPU consumers
vmware-aria resource top --metric 'cpu|usage_average' --top 10

# Check active CRITICAL alerts
vmware-aria alert list --criticality CRITICAL

# Acknowledge an alert
vmware-aria alert acknowledge <alert-id>

# Fetch 4-hour CPU + memory metrics for a VM ("missing" says why a key has no points)
vmware-aria resource metrics <vm-id> --metrics 'cpu|usage_average,mem|usage_average' --hours 4

# Check cluster capacity
vmware-aria capacity remaining <cluster-id>
vmware-aria capacity time-remaining <cluster-id>

# Find rightsizing opportunities (vCPU / memory now → recommended, direction, actionable)
vmware-aria capacity rightsizing

# Check Aria platform health: HEALTHY / DEGRADED / DOWN / UNKNOWN, per service, plus version
vmware-aria health status
vmware-aria health collectors

# Is the Aria node short of memory? Which adapter stopped collecting?
vmware-aria health node
vmware-aria health adapters

# Look up the metric keys a VM reports before querying them
vmware-aria resource keys <vm-id> --filter 'mem|'

# Put a host in maintenance for 2 hours before planned work, then end it (asks once; --dry-run prints the API call)
vmware-aria maintenance start <host-id> --duration 120
vmware-aria maintenance end <host-id>

# Record who is handling an alert, and read what Aria recommends
vmware-aria alert note-add <alert-id> "Taking this: rebooting esx-03"
vmware-aria alert recommendations <alert-id>
```

<a id="readme-safety-and-audit"></a>

## Safety and Audit

### Security

- Passwords loaded from env vars or `.env` file, never from `config.yaml`
- Every MCP tool call and every CLI command that reaches Aria audit-logged to `~/.vmware/audit.db` (via vmware-policy); CLI write operations (alert acknowledge/cancel, alert notes, alert definition management, report generate/delete, resource maintenance start/end) also append to `~/.vmware-aria/audit.log`
- API responses sanitized (control chars stripped, 500-char limit) to prevent prompt injection
- MCP destructive writes (alert acknowledge/cancel, alert definition and report delete, maintenance start/end) take `confirm` (default `false`): without `confirm=true` they return a `blast_radius` of what would change and change nothing; `confirm=true` is refused on a blocker (e.g. a resource already in maintenance) or an unreadable field. The old `confirmed` alias was removed in 2.4.2; a call that passes it is refused as an unknown argument
- TLS verification is on by default; for a private CA set `SSL_CERT_FILE` to a bundle with your CA (see setup guide). `verify_ssl: false` is for isolated self-signed labs only

##### Official Broadcom References

- **REST APIs**: <https://developer.broadcom.com/xapis> — VCF Operations API (formerly Aria Operations suite-api)
- **SDKs**: <https://developer.broadcom.com/sdks> — VCF Python SDK
- **CLI Tools**: <https://developer.broadcom.com/tools> — PowerCLI 9.1 includes "VCF Operations (formerly vRealize Operations Manager)" cmdlets

<!-- usage: remote-and-exposure -->

### Remote access (HTTPS) and limiting tools

By default `vmware-aria mcp` speaks stdio to one local client and offers every tool. Two options change that
(vmware-policy ≥ 1.21.0).

**Serve over HTTPS** so clients on other machines can connect. Every caller needs a bearer token:

```bash
vmware-audit token create alice          # prints the token once; give it to alice
vmware-audit token list                  # names only
vmware-audit token revoke alice          # refused from its next request, no restart
vmware-aria mcp --transport https --host 0.0.0.0 --port 8443 \
    --cert /etc/vmware-mcp/server.pem --key /etc/vmware-mcp/server-key.pem \
    --public-name mcp.example.com
```

Connect a client (Claude Code shown; any MCP client that supports streamable HTTP and custom headers works):

```bash
claude mcp add --transport http vmware-aria https://mcp.example.com:8443/mcp \
    --header "Authorization: Bearer $VMWARE_MCP_TOKEN"
```

```json
{
  "mcpServers": {
    "vmware-aria": {
      "type": "http",
      "url": "https://mcp.example.com:8443/mcp",
      "headers": { "Authorization": "Bearer ${VMWARE_MCP_TOKEN}" }
    }
  }
}
```

- The server will not start without a token, refuses Host/Origin values outside `--public-name`, and checks
  before it binds that unauthenticated requests get 401. Use a certificate your clients trust for those names.
- Behind a TLS-terminating reverse proxy on the same machine use `--transport http --host 127.0.0.1
  --public-name mcp.example.com` and pass the `Authorization` header through.
- Behind a load balancer or gateway on another machine, keep `--transport https` (a self-signed certificate is
  fine), list in `--public-name` the host name the balancer sends as `Host`, and have it forward `Authorization`.
  Its health probe can use `GET /healthz`, which needs no token and returns only `{"status": "ok"}`
  (vmware-policy ≥ 1.23.0).
- Send `traceparent` or `X-Request-ID` with each request to have it stored on the audit row;
  `vmware-audit log --correlation-id ID` then finds the calls behind one platform request.
- The audit log records each caller as `token:<name>`. Calls run side by side: each holds its own session to a
  target, up to `VMWARE_MCP_POOL_SIZE` (default 2) sessions per target. Each session is a login on the target; a
  call waits at most 300 s for a free one.
- **Everyone who can reach the endpoint acts with this server's account.** Tokens identify callers; they grant
  nothing on the platform. Run one endpoint per privilege level.
- **Several people or roles on one endpoint:** run `vmware-audit roles enable` once, then give each token a role (`vmware-audit token create NAME --role reader`, or a role in `roles.yaml` naming tools and targets; vmware-policy ≥ 1.24.0). A role limits what the token may call on this endpoint; it cannot grant more than the account has. See vmware-policy's README, "Roles for network callers".

**Offer only read tools, plus the writes you choose:**

```bash
vmware-aria mcp --expose read --allow-write acknowledge_alert
# or: VMWARE_ARIA_MCP_EXPOSE=read VMWARE_ARIA_MCP_ALLOW_WRITE=acknowledge_alert vmware-aria mcp
```

Tools not offered do not appear in the client's tool list. A bad value or an unknown write tool stops the server
(exit 2). This limits what clients are offered; it is not authorization, so the account itself should be
least-privilege.

Details: `skills/vmware-aria/references/setup-guide.md` ("Serving MCP over HTTPS", "Limiting which tools are offered").

<a id="readme-troubleshooting"></a>

## Troubleshooting

For installation issues, see the installation instructions on this page. Check CLI arguments with `--help` before operating. Include only a minimal, redacted example when reporting a problem.

<a id="readme-companion-skills"></a>

## Companion Skills

The VMware Skills family contains 14 MCP servers and the shared Policy library. Choose tools by responsibility: [vmware-skills](https://github.com/vmware-skills).

<a id="readme-reference"></a>

## Reference

Release history: [RELEASE_NOTES.md](../../../RELEASE_NOTES.md).

Read-only self-test with your own model and agent host: [model-fit self-test](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

### Upgrading to 2.0

2.0 renames 4 of its MCP tools so every name starts with a verb (e.g. `findings_list` → `list_findings`, `fleet_certificate_list` → `list_fleet_certificates`, `fleet_domain_list` → `list_fleet_domains`). The full old → new table is in
[RELEASE_NOTES.md](../../../RELEASE_NOTES.md#v200--mcp-tools-renamed-verb-first). Nothing else changes: same tools, parameters,
safety gates and CLI commands. If an agent prompt, script or `~/.vmware/rules.yaml` names a tool, update it — though deny
rules written with the old names keep working with vmware-policy ≥ 1.18 (`vmware-audit policy` lists any rule the
renames widened), and vmware-pilot ≥ 1.13 translates old names in saved workflows.
If an install older than 2.0 shares that `rules.yaml`, give it vmware-policy ≥ 1.18.2 too: it matches each rule
against both the old and the new name, so one file serves both.

### Architecture

```
User (natural language)
  ↓
AI Agent (Claude Code / Goose / Cursor)
  ↓  [reads SKILL.md]
vmware-aria MCP server (stdio transport)
  ↓  [HTTPS + vRealizeOpsToken]
Aria Operations Suite API
  ↓
VMs / Hosts / Clusters / Alerts / Capacity
```

#### Companion Skills

| Skill | Scope | Tools | Install |
|-------|-------|:-----:|---------|
| **[vmware-aiops](https://github.com/vmware-skills/VMware-AIops)** ⭐ entry point | VM lifecycle, deployment, guest ops, clusters | 60 | `uv tool install vmware-aiops` |
| **[vmware-monitor](https://github.com/vmware-skills/VMware-Monitor)** | Read-only monitoring, alarms, events, VM info | 32 | `uv tool install vmware-monitor` |
| **[vmware-nsx](https://github.com/vmware-skills/VMware-NSX)** | NSX networking: segments, gateways, NAT, IPAM | 33 | `uv tool install vmware-nsx-mgmt` |
| **[vmware-nsx-security](https://github.com/vmware-skills/VMware-NSX-Security)** | DFW microsegmentation, security groups, Traceflow | 22 | `uv tool install vmware-nsx-security` |
| **[vmware-avi](https://github.com/vmware-skills/VMware-AVI)** | AVI / NSX ALB load balancing, AKO K8s operations | 28 | `uv tool install vmware-avi` |
| **[vmware-storage](https://github.com/vmware-skills/VMware-Storage)** | Datastores, iSCSI, vSAN | 12 | `uv tool install vmware-storage` |
| **[vmware-vks](https://github.com/vmware-skills/VMware-VKS)** | Tanzu Namespaces, TKC cluster lifecycle | 23 | `uv tool install vmware-vks` |
| **[vmware-harden](https://github.com/vmware-skills/VMware-Harden)** | Compliance baselines, drift detection | 8 | `uv tool install vmware-harden` |

<a id="readme-license"></a>

## License

MIT — see [LICENSE](https://opensource.org/license/mit/)

### Transient request recovery

Only GET requests are automatically retried after a transport failure or a
502/503/504 response. Writes are sent once even when a retry budget is supplied:
a missing response may mean the change already took effect. Inspect the target
before retrying a write. A single authentication recovery after an explicit
rejection is handled separately. This boundary has synthetic HTTP contract
coverage; it does not establish positive appliance compatibility.
