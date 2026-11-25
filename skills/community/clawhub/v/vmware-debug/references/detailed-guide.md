> Detailed usage and architecture reference. [Quick overview](../../../README.md).


# VMware Debug

[![PyPI](https://img.shields.io/pypi/v/vmware-debug)](https://pypi.org/project/vmware-debug/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#readme-license)

English | [中文](detailed-guide-CN.md)

Maintainer: Wei Zhou · [zhouwei008@gmail.com](mailto:zhouwei008@gmail.com)

Community-maintained open-source project; not an official VMware or Broadcom product.

[Overview](#readme-overview) · [Quick Start](#readme-quick-start) · [MCP Configuration](#readme-mcp-configuration) · [Capabilities and Workflows](#readme-capabilities-and-workflows) · [Safety and Audit](#readme-safety-and-audit) · [Troubleshooting](#readme-troubleshooting) · [Companion Skills](#readme-companion-skills) · [Reference](#readme-reference) · [License](#readme-license)

<a id="readme-overview"></a>

## Overview

Runs locally over stdio by default; see below for data sources and execution boundaries.

> **Disclaimer**: Community-maintained open-source project, **not affiliated with,
> endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware" and
> "vSphere" are trademarks of Broadcom. Source is publicly auditable under the MIT
> license.

The diagnostic brain of the VMware skill family. You bring the symptom (an error,
a log dump, a slow VM); this skill runs a systematic investigation, correlates
events from the other skills into one timeline, ranks root-cause hypotheses, and
tells you what to check next. It makes **no VMware API calls** and never executes
fixes; case operations write a local ledger under `$OPS_HOME`, and every tool also
writes a separate audit trail. Default stdio has no listener; optional authenticated
HTTPS uses caller tokens and TLS certificate/key files. Remediation is routed to `vmware-aiops` (single op) or
`vmware-pilot` (multi-step, gated), mirroring the `vmware-harden → vmware-pilot`
advisor/executor split.

See [`skills/vmware-debug/SKILL.md`](../../../skills/vmware-debug/SKILL.md) for the full
methodology, the event-envelope contract, and symptom routing.

<a id="readme-quick-start"></a>

## Quick Start

Requires Python `>=3.10` and `uv`.

```bash
uv tool install vmware-debug==2.4.0
vmware-debug --help
```

Target, credential and local data setup: [setup guide](../../../skills/vmware-debug/references/setup-guide.md).

<details>
<summary>Installation and configuration details (including offline setup)</summary>

### Install

```bash
uv tool install vmware-debug==2.4.0
vmware-debug categories          # see which symptom categories it can diagnose
```


### Offline / Air-Gapped Install (from source)

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
pip install --no-index --find-links dist vmware-debug
```

<!-- usage: remote-and-exposure -->


</details>

<a id="readme-mcp-configuration"></a>

## MCP Configuration

Copy this configuration into your MCP client's local stdio settings. The client must be able to find `uvx`; the initial package installation requires access to a package index.

```json
{
  "mcpServers": {
    "vmware-debug": {
      "command": "uvx",
      "args": ["--from", "vmware-debug==2.4.0", "vmware-debug-mcp"]
    }
  }
}
```

Debug needs no vCenter target configuration or VMware account credentials; case operations write a local ledger and tool calls have a separate audit trail.

<a id="readme-capabilities-and-workflows"></a>

## Capabilities and Workflows

### MCP tools (14 — 7 read, 7 write)

The seven writes go to the local case ledger only; none reaches a VMware system.

**Correlation** — stateless, for a single look:

| Tool | What |
|---|---|
| `build_incident_timeline` | [READ] Correlate pre-fetched events → timeline + spikes + ranked hypotheses + next-check ideas |
| `list_symptom_categories` | [READ] List recognised symptom categories + what to check for each |

**Investigation ledger** — for an incident you will reason about over time:

| Tool | What |
|---|---|
| `open_case` | [WRITE] Define the event; returns a case id and the grade this environment can reach |
| `get_case_readiness` | [READ] What grade this environment can reach, per symptom category, **before** you start |
| `get_case_knowledge` | [READ] Which knowledge formats are accepted, what is mounted, and which entries apply to a case |
| `plan_case` | [READ] What to fetch next — skill, tool and purpose per step; recomputed from the case's current state |
| `list_cases` | [READ] Cases, newest first |
| `get_case` | [READ] One case: scope, ledger sizes, grade history |
| `record_case_hypothesis` | [WRITE] Register a candidate explanation, or read the ledger of what supports and refutes each |
| `submit_case_evidence` | [WRITE] Record one retrieved fact, with its source, query and time basis |
| `record_case_gap` | [WRITE] Record what could **not** be retrieved, and how to close it |
| `record_case_timeline` | [WRITE] Correlate everything the case has collected into one timeline |
| `grade_case` | [WRITE] Recompute the conclusion grade from the ledger and record it |
| `close_case` | [WRITE] Record the final grade, archive, and name what was left open |

**Event envelope**: `{ts, source, severity, entity, text, fields}`. The agent normalizes events from each source
into this shape before handing them to debug, so debug has zero runtime dependency on the other packages.
**Keep each event's `event_type` in `fields`** — the classifier matches it as well as the text, and most modern
vSphere events are `EventEx`: the text is a generic boilerplate sentence, and only `eventTypeId` says what the
event actually is.

### Common Workflows

1. Use `vmware-debug categories` to select a symptom category.
2. Collect relevant evidence with Monitor, Aria or Log Insight and normalize it into `events.json` using the event envelope; Debug itself does not connect to those systems.
3. Run `vmware-debug triage --events events.json` and inspect the timeline, hypotheses and next checks.
4. If there are no events or a source is unreachable, check the source tool's configuration and connectivity and retain the evidence gap; missing data is not a healthy result.
5. Hand an evidence-backed fix to AIops or Pilot under that tool's execution gates.

<a id="readme-safety-and-audit"></a>

## Safety and Audit

### Security

CLI policy refusals print the reason and rule, exit with code 1, and retain one `denied` audit row.

The diagnostic engine connects to no vCenter/NSX/Aria and needs no VMware account credentials.
Default stdio has no listener; optional HTTPS requires caller tokens and TLS files. Every tool writes
a separate audit row in `~/.vmware/audit.db`. Case tools also write the local ledger: evidence, gaps, hypotheses and
grade history are append-only; `timeline.md` is regenerated from the evidence, and `case.json` holds the current
grade and status. The same holds with several writers: every write to a case first takes that case's lock file
(`.ledger.lock`, exclusive create), so two processes writing the same case in a shared `$OPS_HOME` are serialized
instead of dropping each other's entries; every file is written under a temporary name and then moved into place,
so a reader never sees a half-written file (on a file system without hard links, a new evidence file is instead
created in place: still never overwritten, but it can be read half-written). A lock left behind by a crashed
process is reported together with its holder and never deleted automatically; delete it by hand once you have
confirmed no process is writing that case. Released versions 1.11.3 and earlier do not take this lock, so every
machine sharing a case directory must upgrade. See [SECURITY.md](../../../SECURITY.md).

### Remote access (HTTPS) and limiting tools

By default `vmware-debug mcp` speaks stdio to one local client and offers every tool. Two options change that
(vmware-policy ≥ 1.21.0).

**Serve over HTTPS** so clients on other machines can connect. Every caller needs a bearer token:

```bash
vmware-audit token create alice          # prints the token once; give it to alice
vmware-audit token list                  # names only
vmware-audit token revoke alice          # refused from its next request, no restart
vmware-debug mcp --transport https --host 0.0.0.0 --port 8443 \
    --cert /etc/vmware-mcp/server.pem --key /etc/vmware-mcp/server-key.pem \
    --public-name mcp.example.com
```

Connect a client (Claude Code shown; any MCP client that supports streamable HTTP and custom headers works):

```bash
claude mcp add --transport http vmware-debug https://mcp.example.com:8443/mcp \
    --header "Authorization: Bearer $VMWARE_MCP_TOKEN"
```

```json
{
  "mcpServers": {
    "vmware-debug": {
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
- The audit log records each caller as `token:<name>`. Calls naming different targets run in parallel; calls that
  name no target run one at a time, so name the target when several people share a server.
- **Everyone who can reach the endpoint acts with this server's account.** Tokens identify callers; they grant
  nothing on the platform. Run one endpoint per privilege level.
- **Several people or roles on one endpoint:** run `vmware-audit roles enable` once, then give each token a role (`vmware-audit token create NAME --role reader`, or a role in `roles.yaml` naming tools and targets; vmware-policy ≥ 1.24.0). A role limits what the token may call on this endpoint; it cannot grant more than the account has. See vmware-policy's README, "Roles for network callers".

**Offer only read tools, plus the writes you choose:**

```bash
vmware-debug mcp --expose read --allow-write close_case
# or: VMWARE_DEBUG_MCP_EXPOSE=read VMWARE_DEBUG_MCP_ALLOW_WRITE=close_case vmware-debug mcp
```

Tools not offered do not appear in the client's tool list. A bad value or an unknown write tool stops the server
(exit 2). This limits what clients are offered; it is not authorization, so the account itself should be
least-privilege.

Details: `skills/vmware-debug/references/setup-guide.md` ("Serving MCP over HTTPS", "Limiting which tools are offered").

<a id="readme-troubleshooting"></a>

## Troubleshooting

For installation issues, see the installation instructions on this page. Check CLI arguments with `--help` before operating. Include only a minimal, redacted example when reporting a problem.

<a id="readme-companion-skills"></a>

## Companion Skills

The VMware Skills family contains 14 MCP servers and the shared Policy library. Choose tools by responsibility: [vmware-skills](https://github.com/vmware-skills).

### Companion Skills

| Need | Skill |
|---|---|
| Incident correlation / root cause | **vmware-debug** (this project) |
| Centralized log search | vmware-log-insight (feed its `search_logs` results here) |
| vCenter events and alarms | vmware-monitor |
| Metrics / anomalies | vmware-aria |
| Executing a fix | vmware-aiops (single op) / vmware-pilot (multi-step, gated) |

<a id="readme-reference"></a>

## Reference

Release history: [RELEASE_NOTES.md](../../../RELEASE_NOTES.md).

Read-only self-test with your own model and agent host: [model-fit self-test](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

### Upgrading to 2.0

2.0 renames 13 of its 14 MCP tools so every name starts with a verb (e.g. `case_close` → `close_case`, `case_get` → `get_case`, `case_grade` → `grade_case`). The full old → new table is in
[RELEASE_NOTES.md](../../../RELEASE_NOTES.md#v200--mcp-tools-renamed-verb-first). Nothing else changes: same tools, parameters,
safety gates and CLI commands. If an agent prompt, script or `~/.vmware/rules.yaml` names a tool, update it — though deny
rules written with the old names keep working with vmware-policy ≥ 1.18.1 (`vmware-audit policy` lists any rule the
renames widened), and vmware-pilot ≥ 1.13 translates old names in saved workflows.
If an install older than 2.0 shares that `rules.yaml`, give it vmware-policy ≥ 1.18.2 too: it matches each rule
against both the old and the new name, so one file serves both.

<a id="readme-license"></a>

## License

MIT.
