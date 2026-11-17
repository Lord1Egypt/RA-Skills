# Setup Guide

How to install, configure, and wire `vmware-harden` into your AI agent.

## Prerequisites

- **Python 3.10+** and `uv` (https://docs.astral.sh/uv/).
- **Sibling VMware skills** must be installed and configured for the
  collectors that your chosen baseline references:

  | Baseline | Required sibling skill(s) |
  |----------|---------------------------|
  | `cis-vmware-esxi-8.0-subset` | `vmware-aiops` (host inventory + advanced settings) |
  | `vsphere-scg-v8-subset` | `vmware-aiops` |
  | `dengbao-2.0-level3-vmware` | `vmware-aiops`, `vmware-nsx-security` (DFW evidence) |
  | `pci-dss-4.0-vmware-subset` | `vmware-aiops`, `vmware-nsx-security` |
  | Custom YAML | Whatever node types you reference in `applies_to` |

  `vmware-harden` itself **never** opens a vSphere or NSX session — it
  reuses the collectors and credentials owned by the upstream skills.
  This is the single most important property of the install: harden has
  zero credentials of its own.

- **Optional**: `ANTHROPIC_API_KEY` if you want real LLM advice from
  `vmware-harden advise`. Without it, the advisor falls back to a
  deterministic mock template (and writes a stderr warning).

## Installation

### Recommended: PyPI via `uv tool install`

```bash
uv tool install "vmware-harden[collectors]==1.20.0"
vmware-harden --help
vmware-harden mcp --help   # MCP server (CLI subcommand — recommended)
```

This installs `vmware-harden` into a single isolated venv that `uv tool`
manages. That isolation is why the `[collectors]` extra is named here rather
than installed beside it: `scan` imports vmware-aiops, vmware-storage and
vmware-nsx-security, and `uv tool install vmware-aiops` would build a *second*
venv that harden cannot import from. Omit the extra only if this host will
report on an existing twin DB rather than scan. The MCP stdio server is the `vmware-harden mcp` subcommand; the
standalone `vmware-harden-mcp` console script is also installed and remains
supported for backward compatibility.

### Source install (development)

```bash
git clone --branch v1.20.0 https://github.com/vmware-skills/VMware-Harden.git
cd VMware-Harden
uv venv && source .venv/bin/activate
uv pip install -e .
```

### Alternative Deployment: Container / Smithery

For platforms that prefer containerized MCP servers (e.g., Smithery registry, Kubernetes-hosted agents, isolated CI runners), `vmware-harden` ships a `Dockerfile` and `smithery.yaml` at the repository root (added v1.5.22).

#### Docker

Build and run the MCP server in a container. The image uses `python:3.12-slim` with `uv` for dependency installation and runs `python -m vmware_harden.mcp_server` on stdio (no port exposed — MCP uses stdin/stdout).

```bash
git clone --branch v1.20.0 https://github.com/vmware-skills/VMware-Harden.git
cd VMware-Harden

# Build
docker build -t vmware-harden-mcp:1.20.0 .

# Run — mount your Twin DuckDB directory into the container
docker run --pull=never -i --rm \
  -v ~/.vmware-harden:/root/.vmware-harden \
  -e VMWARE_HARDEN_DB=/root/.vmware-harden/twin.duckdb \
  vmware-harden-mcp:1.20.0
```

These commands run the image built locally above; `--pull=never` prevents a missing local image from falling back to a registry. The version tag identifies this build, not an immutable digest.


The container's `CMD` is `python -m vmware_harden.mcp_server`, which is wired through `vmware_harden/mcp_server/__main__.py` to the same FastMCP entry point as the installed `vmware-harden-mcp` console script. All 6 read-only tools are available.

Note: `scan_target` relies on the upstream `vmware-aiops` collectors. To
run scans from inside the container, mount the upstream skill's config
(`~/.vmware-aiops`) into the container as well. Without it, the container
is still useful for read-only Twin queries (`list_violations`,
`list_drift_events`, `get_remediation`, etc.) over a Twin DuckDB that
was scanned on the host.

#### Smithery

`vmware-harden` is publishable to the [Smithery](https://smithery.ai) registry. The `smithery.yaml` at the repo root declares:

- `startCommand.type: stdio` — Smithery launches the server over stdio
- `configSchema.properties.db_path` — optional override for the Twin DuckDB file location
- `commandFunction` — invokes `vmware-harden mcp` with `VMWARE_HARDEN_DB` set from the user's Smithery config

Users can install via the Smithery UI or CLI without managing Python environments locally. Smithery handles the container build and stdio bridge automatically.

#### When to use which deployment

| Deployment | Best For |
|------------|----------|
| `uv tool install vmware-harden==1.20.0` + `vmware-harden-mcp` | Local developer workstation, single-user CLI + MCP |
| Docker image | Self-hosted agents, CI runners, isolated environments, multi-user servers |
| Smithery | Zero-install agent integration, registry-managed discovery, hosted-MCP workflows |

## Configuration

`vmware-harden` is intentionally near-stateless. The only on-disk
artifacts it owns are:

| Path | Purpose | Created by |
|------|---------|-----------|
| `~/.vmware-harden/twin.duckdb` | Twin store: snapshots, violations, drift, suggestions | First `scan` |
| `~/.vmware-harden/baselines/*.yaml` | User-imported baselines | `baseline import` |
| `~/.vmware-harden/advisories-cache.json` | Optional KEV flags / CVSS overlaid on the shipped advisory catalog | `advisories update` |

Override the Twin path either per-command (`--db /path/to/twin.duckdb`)
or globally via the `VMWARE_HARDEN_DB` environment variable, which the MCP
server, every CLI command with `--db`, and `doctor` read (from 1.10.7; `~` is expanded).

### Anthropic API key for the advisor

```bash
export ANTHROPIC_API_KEY=sk-ant-...
# or persist in ~/.vmware-harden/.env (chmod 600) and source it in your shell.
```

When the variable is unset, the advisor uses `MockProvider` and prints
`WARN: ANTHROPIC_API_KEY not set — using MockProvider (stub suggestions).`

## MCP client setup

The MCP server is started with the CLI subcommand `vmware-harden mcp`
(the standalone `vmware-harden-mcp` console script remains available and
is equivalent — it is kept for backward compatibility).
Spawning the installed entry point directly (rather than `uvx --from ...`)
avoids re-resolving PyPI on every launch and is **strongly recommended in
corporate environments with TLS proxies** — see the workaround section
below.

**Whatever starts the server must install the `collectors` extra**, or the
first `scan_target` fails with `CollectorDependencyError`. The Claude Code
plugin (`.mcp.json`), the uvx example (`examples/mcp-configs/uvx-fallback.json`)
and the `Dockerfile` all carry it from 1.10.7 on. An MCP Registry client
cannot: the registry entry names the bare package, so a client that launches
the server from it through uvx gets one that cannot scan — install with
`uv tool install "vmware-harden[collectors]==1.20.0"` and point the client at
`vmware-harden mcp` instead.

Working configuration templates ship under
`examples/mcp-configs/` in the repository.

### Claude Desktop / Claude Code

`~/.claude/settings.json` (Claude Code) or the MCP section of your
Claude Desktop config:

```json
{
  "mcpServers": {
    "vmware-harden": {
      "command": "vmware-harden",
      "args": ["mcp"],
      "env": {
        "VMWARE_HARDEN_DB": "~/.vmware-harden/twin.duckdb"
      }
    }
  }
}
```

### Cursor

`.cursor/mcp.json` in your project (or the global `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "vmware-harden": {
      "command": "vmware-harden",
      "args": ["mcp"],
      "env": { "VMWARE_HARDEN_DB": "~/.vmware-harden/twin.duckdb" }
    }
  }
}
```

### Cline / Continue / Goose / VS Code Copilot

Use the same `command: vmware-harden` + `args: ["mcp"]` shape; consult the
agent's own MCP docs for the precise key names. Ready-made templates are in
`examples/mcp-configs/`.

## Multi-target Twin

The Twin namespaces every node by `target` (the upstream `vmware-aiops`
target name). You can scan many vCenters into the same DuckDB without
collisions:

```bash
vmware-harden scan --target lab-vc01 --baseline cis-vmware-esxi-8.0-subset
vmware-harden scan --target prod-vc  --baseline dengbao-2.0-level3-vmware
vmware-harden report                 # shows the most recent snapshot's violations
```

Drift is computed **per target**: each `scan` call diffs against the
prior snapshot whose `target` matches.

## Aria-aware fallback

If the customer already runs **VMware Aria Operations**, harden is
designed to *complement*, not replace, Aria's compliance pack:

| Capability | Aria Operations | vmware-harden |
|------------|:--:|:--:|
| Real-time inventory & metrics | Yes | No (delegates to vmware-aiops) |
| Anomaly detection / capacity | Yes | No (use **vmware-aria** skill) |
| 等保 2.0 三级 baseline | No (not bundled) | **Yes** |
| Custom YAML baseline | Limited | **Yes** |
| LLM-driven remediation advice | No | **Yes** (`advise`) |
| Approval-gated remediation execution | No | Out of scope — use **vmware-pilot** |

Recommended pattern when Aria is present: keep using Aria for live
monitoring, point harden at the same vCenter for **compliance posture
+ drift + remediation advice**, and surface harden's findings into your
AI agent through MCP.

## Corporate TLS workaround

If `uvx --from vmware-harden==1.20.0 vmware-harden-mcp` reports
`invalid peer certificate: UnknownIssuer`, your network has a MitM TLS
proxy whose CA is not in `uv`'s bundled webpki store (踩坑 #25).

**Preferred fix**: don't use `uvx` for the MCP server. Install once with
`uv tool install vmware-harden==1.20.0` and configure the MCP client to spawn
`vmware-harden-mcp` directly — that path goes through your shell `PATH`
and never hits PyPI again.

**Fallback**: if you must use `uvx`, set:

```bash
export UV_NATIVE_TLS=true
```

This makes `uv` consult the system CA store (which your IT department's
proxy CA is presumably in), and PyPI resolution works again.

## Troubleshooting

### MCP server crashes on launch with `subclass() arg 1 must be a class`

Seen on Python 3.10 environments (e.g. Goose default sandbox, Ubuntu 22.04
system python) where an older `mcp` package (1.10–1.13) was pinned. Under
that combination, FastMCP's `Tool.from_function` calls
`issubclass(param.annotation, Context)` without resolving forward
references, so PEP 604 string annotations (`"str | None"`) blow up the
entire server load. Fixed across v1.5.26–1.5.28 (踩坑 #33).

**Resolution** — upgrade to v1.5.28+ which (a) replaces PEP 604 unions in
`mcp_server/server.py` with `Optional[X]`, and (b) drops
`from __future__ import annotations` from that file so annotations are
real classes:

```bash
uv tool install --upgrade vmware-harden==1.20.0
# or, if you bring your own mcp package:
pip install -U 'mcp[cli]>=1.14'
```

Python 3.10 is supported from v1.5.27 onward; older versions of this
skill required Python 3.11+.

### `mcp` command exits with "Python 3.10+ required"

The `mcp_cmd()` guard exits 1 when run on Python 3.9 or earlier. Install
Python 3.10+ (e.g. `uv python install 3.12`) and re-install
`vmware-harden` against that interpreter.

## Serving MCP over HTTPS

By default the MCP server speaks stdio to one local client. To let clients on other machines reach it, serve it over
HTTPS. Every caller then needs a bearer token.

```bash
vmware-audit token create alice                      # prints the token once; give it to alice
vmware-harden mcp --transport https --host 0.0.0.0 --port 8443 \
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
- Each audit row records the caller as `token:<name>`. Calls naming different targets run in parallel; calls that
  name no target run one at a time, so name the target when several people use one server.
- **Everyone who can reach the endpoint acts with this server's account.** Tokens identify callers; they grant
  nothing on the platform. Run one endpoint per privilege level (for example a read-only account behind
  `--expose read`, and a separate endpoint for operators).
- **Several people or roles on one endpoint:** run `vmware-audit roles enable` once, then give each token a role (`vmware-audit token create NAME --role reader`, or a role in `roles.yaml` naming tools and targets; vmware-policy ≥ 1.24.0). A role limits what the token may call on this endpoint; it cannot grant more than the account has. For a target-limited role, `scan_target`'s target is checked against vmware-aiops' config; the datastore and DFW collectors look the same name up in vmware-storage's and vmware-nsx-security's configs, so a name must mean the same system in all three. See vmware-policy's README, "Roles for network callers".

## Security

> **Disclaimer**: This is a community-maintained open-source project and
> is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or
> Broadcom Inc.** "VMware" and "vSphere" are trademarks of Broadcom.
> Source code is publicly auditable at
> [github.com/vmware-skills/VMware-Harden](https://github.com/vmware-skills/VMware-Harden)
> under the MIT license.

- **No credentials of its own.** All vSphere / NSX authentication lives
  in the upstream skills (`~/.vmware-aiops/.env`,
  `~/.vmware-nsx-security/.env`, etc.) under `chmod 600`.
- **No outbound network calls** beyond:
  1. Upstream sibling-skill collectors during `scan`.
  2. Optional `api.anthropic.com` calls when `ANTHROPIC_API_KEY` is set
     and the user invokes `advise`.
  3. The local web dashboard, bound to `127.0.0.1` by default.
  4. `advisories update`, only when run: public downloads from cisa.gov
     (KEV feed) and, with `--nvd`, nvd.nist.gov (one request per catalogued CVE). Nothing
     about the scanned estate is sent. Audited like any CLI read.
- **TLS verification**: full system TLS verification on the Anthropic
  call. Vendor TLS handling for vSphere/NSX is delegated to the upstream
  skills (no opt-out path lives in this codebase).
- **Prompt-injection protection**: the advisor builds its LLM context
  exclusively from typed Twin queries (rule id, severity, structured
  evidence). Any free-text fields are passed through `_sanitize()` —
  truncation to 500 chars and stripping C0/C1 control characters.
- **Least privilege**: all 8 MCP tools are read-only with respect to
  managed VMware resources. Remediation execution is intentionally not
  exposed; agents that need to apply a fix must invoke **vmware-pilot**,
  which adds approval gates and audit logging.
- **Audit log**: every MCP tool call is recorded by the `@vmware_tool`
  decorator into `~/.vmware/audit.db` (SQLite WAL via `vmware-policy`).
  View with `vmware-audit log --last 20`.
- **Environment scoping**: policy rules can scope by environment, and skills
  that connect to a VMware estate may declare `environment:` (`production` /
  `staging` / `lab`) per target in their own `config.yaml` — an optional label
  an environment-scoped `deny` rule can match on. Harden has no such config and
  needs no declaration: it reports a constant `local`. That is accurate rather
  than an exemption — `scan_target` is its only state-changing
  tool and the state it changes is the snapshot in the local Twin DB, its
  vCenter interaction being read-only collection.

**The account is the boundary.** This skill has no write tools, but an agent that can run shell commands can reach
the platform without it (SSH, curl, govc, PowerCLI). Give the service account only the read privileges it needs;
nothing in the skill can stop the same credentials being used another way.

