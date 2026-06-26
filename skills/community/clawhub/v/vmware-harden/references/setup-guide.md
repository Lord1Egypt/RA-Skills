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
uv tool install vmware-harden
vmware-harden --help
vmware-harden-mcp --help   # MCP server entry point (separate console script)
```

This installs both `vmware-harden` (CLI) and `vmware-harden-mcp` (MCP
stdio server) into a single isolated venv that `uv tool` manages.

### Source install (development)

```bash
git clone https://github.com/zw008/VMware-Harden.git
cd VMware-Harden
uv venv && source .venv/bin/activate
uv pip install -e .
```

### Alternative Deployment: Container / Smithery

For platforms that prefer containerized MCP servers (e.g., Smithery registry, Kubernetes-hosted agents, isolated CI runners), `vmware-harden` ships a `Dockerfile` and `smithery.yaml` at the repository root (added v1.5.22).

#### Docker

Build and run the MCP server in a container. The image uses `python:3.12-slim` with `uv` for dependency installation and runs `python -m mcp_server` on stdio (no port exposed — MCP uses stdin/stdout).

```bash
git clone https://github.com/zw008/VMware-Harden.git
cd VMware-Harden

# Build
docker build -t vmware-harden-mcp .

# Run — mount your Twin DuckDB directory into the container
docker run -i --rm \
  -v ~/.vmware-harden:/root/.vmware-harden \
  -e VMWARE_HARDEN_DB=/root/.vmware-harden/twin.duckdb \
  vmware-harden-mcp
```

The container's `CMD` is `python -m mcp_server`, which is wired through `mcp_server/__main__.py` to the same FastMCP entry point as the installed `vmware-harden-mcp` console script. All 6 read-only tools are available.

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
- `commandFunction` — invokes `python -m mcp_server` with `VMWARE_HARDEN_DB` set from the user's Smithery config

Users can install via the Smithery UI or CLI without managing Python environments locally. Smithery handles the container build and stdio bridge automatically.

#### When to use which deployment

| Deployment | Best For |
|------------|----------|
| `uv tool install vmware-harden` + `vmware-harden-mcp` | Local developer workstation, single-user CLI + MCP |
| Docker image | Self-hosted agents, CI runners, isolated environments, multi-user servers |
| Smithery | Zero-install agent integration, registry-managed discovery, hosted-MCP workflows |

## Configuration

`vmware-harden` is intentionally near-stateless. The only on-disk
artifacts it owns are:

| Path | Purpose | Created by |
|------|---------|-----------|
| `~/.vmware-harden/twin.duckdb` | Twin store: snapshots, violations, drift, suggestions | First `scan` |
| `~/.vmware-harden/baselines/*.yaml` | User-imported baselines | `baseline import` |

Override the Twin path either per-command (`--db /path/to/twin.duckdb`)
or globally via the `VMWARE_HARDEN_DB` environment variable consumed by
the MCP server.

### Anthropic API key for the advisor

```bash
export ANTHROPIC_API_KEY=sk-ant-...
# or persist in ~/.vmware-harden/.env (chmod 600) and source it in your shell.
```

When the variable is unset, the advisor uses `MockProvider` and prints
`WARN: ANTHROPIC_API_KEY not set — using MockProvider (stub suggestions).`

## MCP client setup

The MCP server is a single console script: `vmware-harden-mcp`.
Spawning the entry point directly (rather than `uvx --from ...`) avoids
re-resolving PyPI on every launch and is **strongly recommended in
corporate environments with TLS proxies** — see the workaround section
below.

Working configuration templates ship under
`examples/mcp-configs/` in the repository.

### Claude Desktop / Claude Code

`~/.claude/settings.json` (Claude Code) or the MCP section of your
Claude Desktop config:

```json
{
  "mcpServers": {
    "vmware-harden": {
      "command": "vmware-harden-mcp",
      "args": [],
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
      "command": "vmware-harden-mcp",
      "env": { "VMWARE_HARDEN_DB": "~/.vmware-harden/twin.duckdb" }
    }
  }
}
```

### Cline / Continue / Goose / VS Code Copilot

Use the same `command: vmware-harden-mcp` shape; consult the agent's
own MCP docs for the precise key names. Ready-made templates are in
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

If `uvx --from vmware-harden vmware-harden-mcp` reports
`invalid peer certificate: UnknownIssuer`, your network has a MitM TLS
proxy whose CA is not in `uv`'s bundled webpki store (踩坑 #25).

**Preferred fix**: don't use `uvx` for the MCP server. Install once with
`uv tool install vmware-harden` and configure the MCP client to spawn
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
uv tool install --upgrade vmware-harden
# or, if you bring your own mcp package:
pip install -U 'mcp[cli]>=1.14'
```

Python 3.10 is supported from v1.5.27 onward; older versions of this
skill required Python 3.11+.

### `mcp` command exits with "Python 3.10+ required"

The `mcp_cmd()` guard exits 1 when run on Python 3.9 or earlier. Install
Python 3.10+ (e.g. `uv python install 3.12`) and re-install
`vmware-harden` against that interpreter.

## Security

> **Disclaimer**: This is a community-maintained open-source project and
> is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or
> Broadcom Inc.** "VMware" and "vSphere" are trademarks of Broadcom.
> Source code is publicly auditable at
> [github.com/zw008/VMware-Harden](https://github.com/zw008/VMware-Harden)
> under the MIT license.

- **No credentials of its own.** All vSphere / NSX authentication lives
  in the upstream skills (`~/.vmware-aiops/.env`,
  `~/.vmware-nsx-security/.env`, etc.) under `chmod 600`.
- **No outbound network calls** beyond:
  1. Upstream sibling-skill collectors during `scan`.
  2. Optional `api.anthropic.com` calls when `ANTHROPIC_API_KEY` is set
     and the user invokes `advise`.
  3. The local web dashboard, bound to `127.0.0.1` by default.
- **TLS verification**: full system TLS verification on the Anthropic
  call. Vendor TLS handling for vSphere/NSX is delegated to the upstream
  skills (no opt-out path lives in this codebase).
- **Prompt-injection protection**: the advisor builds its LLM context
  exclusively from typed Twin queries (rule id, severity, structured
  evidence). Any free-text fields are passed through `_sanitize()` —
  truncation to 500 chars and stripping C0/C1 control characters.
- **Least privilege**: all 6 MCP tools are read-only with respect to
  managed VMware resources. Remediation execution is intentionally not
  exposed; agents that need to apply a fix must invoke **vmware-pilot**,
  which adds approval gates and audit logging.
- **Audit log**: every MCP tool call is recorded by the `@vmware_tool`
  decorator into `~/.vmware/audit.db` (SQLite WAL via `vmware-policy`).
  View with `vmware-audit log --last 20`.
