> Detailed usage and architecture reference. [Quick overview](../../../README.md).

# VMware Policy

[![PyPI](https://img.shields.io/pypi/v/vmware-policy)](https://pypi.org/project/vmware-policy/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#readme-license)

English | [中文](detailed-guide-CN.md)

Maintainer: Wei Zhou · [zhouwei008@gmail.com](mailto:zhouwei008@gmail.com)

Community-maintained open-source project; not an official VMware or Broadcom product.

[Overview](#readme-overview) · [Quick Start](#readme-quick-start) · [Library Usage](#readme-library-usage) · [Capabilities and Workflows](#readme-capabilities-and-workflows) · [Safety and Audit](#readme-safety-and-audit) · [Troubleshooting](#readme-troubleshooting) · [Companion Skills](#readme-companion-skills) · [Reference](#readme-reference) · [License](#readme-license)

<a id="readme-overview"></a>

## Overview

Shared library; does not provide a standalone MCP server.

Unified audit logging, policy enforcement, and sanitization for the VMware MCP skill family.

<a id="readme-quick-start"></a>

## Quick Start

Requires Python `>=3.10` and `uv`.

```bash
uv tool install vmware-policy==1.26.0
vmware-audit --help
```

<details>
<summary>Installation and configuration details (including offline setup)</summary>

### Install

```bash
pip install vmware-policy==1.26.0
```


</details>

<a id="readme-library-usage"></a>

## Library Usage

Policy is a shared dependency of the VMware tools; do not create a standalone MCP marketplace entry for it.

### Usage

```python
from vmware_policy import vmware_tool

@vmware_tool(risk_level="high", sensitive_params=["password"])
def delete_segment(name: str, env: str = "") -> dict:
    ...
```

<a id="readme-capabilities-and-workflows"></a>

## Capabilities and Workflows

### Undo storage availability

A failed undo recording leaves the completed platform operation successful and prints a warning on stderr.
The store retries initialization on the next operation, so fixing its directory or disk does not require a
process restart. `vmware-audit undo-list` and `undo-show` report an unavailable store as an error rather than
showing it as empty. A returned `_undo_id` is the evidence that an inverse was actually recorded.

### Reporting a failure the tool *returns*

Most tools signal failure by raising, and `@vmware_tool` records that. A tool that
instead catches the exception and returns an error payload looks identical to a
successful call — and for a long time was recorded as one, which also meant undo
tokens were written for changes that never happened and the circuit breaker never
saw a failure.

Dict-shaped payloads are now detected automatically. Nothing to do if a tool
returns the family shape:

```python
return {"error": msg, "hint": "Run 'vmware-nsx doctor'."}   # audited as a failure
```

A tool whose return type cannot carry that marker — one handing back console text,
say — must say so explicitly:

```python
from vmware_policy import report_tool_failure

except Exception as exc:
    report_tool_failure(str(exc))
    return f"Error: {msg}"
```

Strings are deliberately not sniffed: skills that return console output can emit
text beginning with "Error:" as *data*, and marking those calls failed would be
the same misreport in the opposite direction.

### CLI

```bash
vmware-audit log --last 20
vmware-audit log --status denied --since 2026-03-28
vmware-audit stats --days 7
vmware-audit policy          # which rules are in force
```

The audit CLI requires positive bounds for `log --last`, `export --limit` and `undo-list --last`; zero or negative values are rejected before accessing the store.

### Components

| Component | Description |
|-----------|-------------|
| `@vmware_tool` | Decorator around a skill's MCP tools -- policy pre-check + execute + audit row |
| `AuditEngine` | Append-only SQLite (WAL) audit log; rotates at 100 MB, keeps 5 archives |
| `PolicyEngine` | YAML rules: deny rules and maintenance window, hot-reloaded on file change. `change_limits` bounds AIops VM CPU/memory reconfiguration using backend-read state. |
| `sanitize()` | Prompt-injection defense -- strips C0/C1 control and Unicode format characters, truncates (default 500 chars) |
| `vmware-audit` | Typer CLI -- query, export, statistics, rule status |

### Policy rules

Read/write authorization belongs to the vCenter/NSX account's RBAC. The policy
engine only adds the operator's own deny rules and maintenance window, from
`~/.vmware/rules.yaml` (`$OPS_HOME/rules.yaml` if set). `vmware-audit policy`
reports which source is in force:

| Source | When | What is permitted |
|--------|------|-------------------|
| `user` | Your rules file exists and loads | Whatever your rules allow |
| `packaged-default` | No rules file | The shipped baseline, which denies nothing -- all operations are allowed by policy |
| `user-unreadable` | Your file exists but will not load (YAML error, not UTF-8) | Nothing -- every operation is denied until it loads; the baseline is never substituted |
| `baseline-unreadable` | No user file and the shipped baseline will not load | Nothing -- every operation is denied |

PyYAML is a declared dependency; if it is missing, decorated tool calls fail
rather than run. Rules hot-reload on file change.

`VMWARE_POLICY_DISABLED=1` is an operator escape hatch: in the process that has
it set (the MCP host, or a CLI shell) every policy check is skipped, including
the unreadable-rules denial. Auditing continues -- each bypassed check logs a
warning, and rows from both surfaces -- `@vmware_tool` MCP calls and `@guarded`
CLI commands -- are recorded with a `_bypassed` status suffix (`ok_bypassed`,
`error_bypassed`). Restrict who can set the MCP host's environment.

Copy the default rules to `~/.vmware/rules.yaml` and customize them:

```yaml
# Deny rules -- block specific operations
deny:
  - name: no-delete-in-prod
    operations: ["delete_*", "remove_cluster_host"]
    environments: ["production"]
    reason: "Destructive operations are not allowed in production"

# Maintenance window -- high/critical operations allowed only inside the window
maintenance_window:
  start: "22:00"
  end: "06:00"

# AIops VM CPU/memory reconfiguration only: absolute percentage change
# from actual current sizing (increases and decreases). Requires updated AIops.
change_limits:
  max_cpu_change_pct: 20
  max_memory_change_pct: 50
```

Rule changes hot-reload; no service needs a restart.

### Tool exposure

Every skill's MCP server can offer a subset of its tools. `<cli> mcp --expose read` (or
`VMWARE_<SKILL>_MCP_EXPOSE=read`) keeps only tools annotated `readOnlyHint: true`; `--allow-write a,b`
(or `VMWARE_<SKILL>_MCP_ALLOW_WRITE`) keeps chosen write tools on top. A tool without the annotation counts as a
write. An unknown value, or a name that is not a write tool of that server, stops the server before it serves
(exit 2). Pre-2.0 tool names are accepted.

A launcher that imports a server object directly can use the same code instead of the SDK's private registry:

```python
from vmware_policy.exposure import restrict_tools

restrict_tools(mcp, skill="storage", expose="read", allow_write=["enable_iscsi"])
mcp.run(transport="streamable-http")
```

Inside a running event loop use `await arestrict_tools(...)`. The server object only needs the SDK's public
`list_tools()` and `remove_tool()`. `restrict_tools` does not read the environment; to honour
`VMWARE_<SKILL>_MCP_*` the way `<cli> mcp` does, pass `*settings("storage")` (or call `apply_or_exit`). If either
flag is given, the environment is ignored for both, so the two sources never mix.

A tool that runs other steps (a plan, workflow or batch tool) carries every write it can execute, including writes
the exposure hides.

This limits what clients are offered. It is not authorization: the account's permissions decide what a call may
change, and deny rules still apply to every exposed tool.

### Serving MCP over HTTPS

`vmware_policy.serve` runs a skill's MCP server on stdio (default), on HTTPS, or on loopback HTTP behind a
TLS-terminating reverse proxy. Both network transports require bearer tokens; nothing binds without one.

```bash
vmware-audit token create alice      # prints the token once; only its sha256 is stored (0600)
vmware-audit token list
vmware-audit token revoke alice      # running servers refuse it from the next request
```

- Tokens live in `$OPS_HOME/mcp-tokens` (default `~/.vmware`). Clients send `Authorization: Bearer <token>`.
- `https` needs `--cert`/`--key` (PEM) and `--public-name` for every host name clients use; requests for any other
  Host or Origin are refused (DNS-rebinding protection). `http` binds 127.0.0.1/::1/localhost only.
- Each audit row records the caller as `token:<name>` and the surface (`mcp-https`, `mcp-http-loopback`).
- Calls naming the same `target` run one at a time; calls naming different targets run in parallel; a call that
  names no target (the skill's default target, or a tool without a `target` parameter) runs alone. Waiting calls
  are served first come, first served, so neither kind can starve the other; to get parallelism, name the target.
  The runaway breaker is per caller. Skills that keep a session pool (below) lift these limits.
- A session can only be used by the token name that created it (the SDK enforces this). Revoking a token and
  creating a new one under the same name lets the new token continue the old sessions, so use a new name when a
  token leaks. Idle sessions expire after 30 minutes.
- Deny rules can name callers: `clients: ["intern-*"]` in `$OPS_HOME/rules.yaml` matches those token names only
  (stdio and CLI calls are not matched by such a rule).
- Before it binds, the server sends itself unauthenticated POST/GET/DELETE requests and refuses to start unless
  all three get 401.
- `GET`/`HEAD /healthz` answers `{"status": "ok"}` without a token, for a load balancer's health probe; it reveals
  nothing else and accepts any `Host`. Every other path requires the token.
- Each audit row records the caller's correlation id: the trace-id of a `traceparent` header, else `X-Request-ID`,
  else `X-Correlation-ID` (safe characters only, up to 128). `vmware-audit log --correlation-id ID` finds the rows
  for one platform request. The id is whatever the caller sends: it joins traces, it proves nothing.
- Tools that read or write files on this host (guest file transfer, OVA and spec files, kubeconfig output) never
  touch its configuration, tokens, audit log or TLS key. Over a network transport they are off entirely unless
  `VMWARE_MCP_FILE_ROOT` names a directory for them; then only paths inside it are allowed.
- **Every caller of an endpoint acts with that server's account.** Tokens identify callers; they authorize nothing
  at the platform. Run one endpoint per privilege level and per group of people who may see each other's work.

### Roles for network callers

Several people or agents can share one HTTPS endpoint with different jobs (vmware-policy ≥ 1.24.0, HLD §18).
A role limits which tools and targets a token may use **on that endpoint**. It narrows what the server's account
is used for; it cannot grant more than the account has, so the platform account stays the boundary.

```bash
vmware-audit roles enable                      # turn roles on; existing tokens become admin
vmware-audit token create ops-agent --role reader
vmware-audit token create storage-team --role storage-operator
vmware-audit token set-role ops-agent admin    # applies from its next request
vmware-audit token list --long                 # name, role, file
vmware-audit roles check                       # exit 1 if a role or token cannot be used
```

- **Built-in roles:** `reader` (tools that only read, every skill, every target) and `admin` (every tool the
  server offers). Custom roles live in `$OPS_HOME/roles.yaml` (owner-only, owned by the server's user). Every
  key is required and "all" is spelled `"*"`, so a file cut off mid-edit refuses a role instead of widening it:

  ```yaml
  roles:
    storage-operator:
      skills:
        storage:
          tools: read                    # read | "*"
          allow_write: [rescan_storage]  # write tools on top
          allow_escape: []               # tools that escape a role, named one by one
          targets: ["vc-prod-*"]         # target names (globs) for this skill, or "*"
        monitor: { tools: read, allow_write: [], allow_escape: [], targets: "*" }
      approve: none                      # vmware-pilot approvals: none | any | others
  ```

- **Opting in is one command.** Before `roles enable`, every token keeps working as `admin` and
  `token create --role` refuses. `roles enable` moves every token into
  `$OPS_HOME/mcp-tokens.v2` (as `admin`, or `--assign NAME=ROLE`) and leaves the old file empty. Servers on this
  host still running an older vmware-policy then refuse every request, so upgrade them in the same change.
  After it, `token create` needs `--role`. `$OPS_HOME/mcp-tokens.v2` must belong to the server's user, in a
  directory others cannot write.
- **What a role checks, on every call:** the tool, and the target it resolves to (the default target's real name
  when none is given). A tool that reads every target is refused unless the role's targets for that skill are
  `"*"`. A tool that runs other tools (an AIops plan, a batch, a TTL that deletes later) is allowed only if the
  role allows every tool it can run. A refused call is audited as `denied` with `rule=role:<name>` and counts
  toward the caller's runaway budget; every row carries the caller's role.
- **Escape tools** give their holder more than a role: credentials (`issue_*_kubeconfig`), code in a guest, raw
  API paths (Aria `get_api_path`), files on the server host while `VMWARE_MCP_FILE_ROOT` is set. `reader` never
  has them; a custom role gets one only by naming it under `allow_escape`. **A role holding an escape tool is
  equivalent to the account.**
- **`tools/list` is per caller**: a token is offered only what its role may call. Server instructions list target
  addresses to `admin` only. A role that cannot be used (a broken `roles.yaml`, an undefined role) is explained
  in the server's log, not to the caller.
- A skill that has not declared role metadata (an older release under this Policy) admits `admin` only.
- In a server on a network transport, a call that carries no authenticated caller is refused — from this
  release, whether or not roles are enabled.
- Deny rules can name roles: `roles: [reader]` in `rules.yaml`, next to `clients:`.
- vmware-pilot: `approve: none` cannot approve; `others` cannot approve a workflow its own token created, edited
  or confirmed as a draft.
- Token and role changes (`token create/revoke/set-role`, `roles enable`) are audit rows, and a server writes a
  `roles_reload` row (the file's SHA-256 and its roles) each time `roles.yaml` changes under it.
- `roles check` validates `roles.yaml` and the tokens. It cannot see each skill's tools, so a misspelled tool in
  `allow_write` or a composite whose reach the role does not cover shows up when a server refuses the call.
- **Roles separate people who reach the platform only through this endpoint.** Someone with the account's
  credentials, or an agent with its own shell and network path to vCenter, is outside them. For a team that must
  never write, a read-only account on its own endpoint is still the stronger answer.

### Session pools

A skill that connects to a platform can keep a small pool of sessions per target
(`vmware_policy.pool.SessionPool`, `VMWARE_MCP_POOL_SIZE`, default 2) and start its server with
`run_server(..., pooled=True)`. Over a network transport each call then holds its own session per target for its whole
body (tools return plain data, so nothing is read from the session after it), so calls on one target run side by side up to the pool size and calls that
name no target are not serialized. A call that already holds a session never waits for another target; if that
target's pool is busy it gets a temporary extra session, so multi-target calls cannot deadlock. A call that waits
longer than 300 s for a session gets an error naming the target. Each session is a login on the target. stdio and
the CLI keep one cached session per target, separate from the pooled ones.

### Access self-diagnosis

`vmware_policy.access.vsphere_access_info(si, target=, requirements=, tool=)` backs each vSphere skill's
`get_access_info` tool: the account the target uses, the privileges each tool needs (from the skill's
requirements table) and whether the current session holds them on the root folder
(`AuthorizationManager.HasPrivilegeOnEntities`, which needs only System.View). "Not granted at the root" is not
"no access": permissions on specific objects are not covered. A lookup that fails is `undetermined`, never granted.

### Risk levels

The level a tool declares is recorded in the audit row, can be matched by a
deny rule's `min_risk_level`, and decides whether a configured maintenance
window applies. It does not by itself gate execution.

| Level | Examples |
|-------|----------|
| `low` | list, get, info, status |
| `medium` | reconfigure, update |
| `high` | power off, migrate, snapshot revert |
| `critical` | delete VM, delete cluster |

<a id="readme-safety-and-audit"></a>

## Safety and Audit

### Security

- The audit database (`~/.vmware/audit.db`, local only, `0700` directory / `0600` files) records tool parameters, results, status, OS user and inferred agent -- treat it and its archives as sensitive.
- Parameters named in `sensitive_params` are stored as `***`; results from tools declaring `sensitive_result=True` are replaced; credential-named keys (`password`, `token`, `kubeconfig`, ...) in parameters and results, and credential-shaped text in error messages, are redacted on both the MCP and CLI surfaces. A credential under a key name not on that list must be declared in `sensitive_params`.
- `sanitize()` guards against prompt injection through API response text.
- Policy bypass (`VMWARE_POLICY_DISABLED=1`) skips policy checks, not auditing.

<a id="readme-troubleshooting"></a>

## Troubleshooting

For installation issues, see the installation instructions on this page. Check CLI arguments with `--help` before operating. Include only a minimal, redacted example when reporting a problem.

<a id="readme-companion-skills"></a>

## Companion Skills

The VMware Skills family contains 14 MCP servers and the shared Policy library. Choose tools by responsibility: [vmware-skills](https://github.com/vmware-skills).

### VMware Skill Family

| Skill | Scope | Install |
|-------|-------|---------|
| **vmware-aiops** | VM lifecycle + deployment + guest ops | `uv tool install vmware-aiops` |
| **vmware-monitor** | Read-only monitoring | `uv tool install vmware-monitor` |
| **vmware-storage** | Storage management (iSCSI + vSAN) | `uv tool install vmware-storage` |
| **vmware-vks** | Tanzu Kubernetes | `uv tool install vmware-vks` |
| **vmware-nsx** | NSX networking | `uv tool install vmware-nsx-mgmt` |
| **vmware-nsx-security** | NSX security (DFW + security groups) | `uv tool install vmware-nsx-security` |
| **vmware-aria** | Aria Ops metrics/alerts/capacity | `uv tool install vmware-aria` |
| **vmware-avi** | AVI/ALB load balancing | `uv tool install vmware-avi` |
| **vmware-harden** | Compliance baselines + drift detection | `uv tool install vmware-harden` |
| **vmware-vdi** | Horizon VDI operations | `uv tool install vmware-vdi` |
| **vmware-privateai** | Private AI GPU / model-serving ops | `uv tool install vmware-privateai` |
| **vmware-debug** | Incident correlation / root cause | `uv tool install vmware-debug` |
| **vmware-log-insight** | Centralized log search | `uv tool install vmware-log-insight` |
| **vmware-pilot** | Multi-step workflow orchestration | `uv tool install vmware-pilot` |
| **vmware-policy** | Audit + policy (this package) | `uv tool install vmware-policy==1.26.0` |

<a id="readme-reference"></a>

## Reference

Release history: [RELEASE_NOTES.md](../../../RELEASE_NOTES.md).

Read-only self-test with your own model and agent host: [model-fit self-test](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

### Architecture

```
AI Agent -> vmware-pilot (optional orchestration) -> @vmware_tool pre-check -> skill operation -> audit row -> ~/.vmware/audit.db
```

vmware-policy is a **mandatory dependency** of every VMware skill. It provides:

- **Audit logging**: calls to MCP tools wrapped by `@vmware_tool` are recorded in the unified database `~/.vmware/audit.db`
- **Policy engine**: deny rules and maintenance window, hot-reloaded without a restart (AIops VM reconfiguration limits use actual before-state)
- **Input sanitization**: all text from the vSphere/NSX/Aria APIs passes through `sanitize()`
- **AI agent detection**: records the caller from its environment: `claude`, `codex`, `deerflow`, `local` (an Ollama host) or `unknown`

### Development

```bash
git clone --branch v1.26.0 https://github.com/vmware-skills/VMware-Policy.git
cd VMware-Policy
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
pytest --cov=vmware_policy
```

<a id="readme-license"></a>

## License

MIT

### VM reconfiguration limits

Policy 1.25.0 and AIops 2.5.0 enforce the configured CPU/memory percentages at
the backend mutation boundary. For example, CPU 4 to 8 is a 100% change and is
refused under a 20% maximum; a 4 to 3 decrease is 25% and is also refused. The
exact boundary is allowed. Malformed/unknown limits, missing sizing or missing
`changeVersion` fail closed for the checked reconfiguration. The ConfigSpec is
bound to that version to reject concurrent changes. A caller-supplied percentage
is not trusted. Generic `check_allowed(params=...)` is surface authorization,
not this backend state check. Initial create/clone tasks, storage and other products are
outside this scope; post-deployment resizing through the backend is checked. Older AIops versions do not enforce these limits; upgrade
both packages before relying on them. Concurrent rejection has synthetic
contract coverage; positive appliance validation is still pending.

A post-deployment resize through the same backend is still checked. Its refusal
can leave a newly created VM at its original sizing; inspect the result before
retrying. The initial create/clone task itself is not a percentage-limit gate,
and no automatic cleanup or clone retry is introduced.
