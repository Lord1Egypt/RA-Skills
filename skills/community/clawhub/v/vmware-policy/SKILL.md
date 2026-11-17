---
name: vmware-policy
description: >
  Unified audit logging, policy enforcement, and input sanitization for the entire VMware MCP skill family.
  Use when querying audit logs, managing policy rules, or when any VMware skill needs audit/policy infrastructure.
  Provides the @vmware_tool decorator that most skills in the family wrap their MCP tools in.
  Use when user asks to "show audit log", "check denied operations", "view policy rules", "audit stats", or "query audit trail".
  For VM lifecycle use vmware-aiops, for monitoring use vmware-monitor, for networking use vmware-nsx, for load balancing use vmware-avi.
installer:
  kind: uv
  package: vmware-policy
allowed-tools:
  - Bash
user-invocable: false
metadata: {"openclaw":{"requires":{"anyBins":["vmware-audit","uvx"]},"optional":{"env":["CLAUDE_SESSION_ID","OLLAMA_HOST"]},"homepage":"https://github.com/vmware-skills/VMware-Policy","emoji":"🛡️","os":["macos","linux"]}}
---

# VMware Policy

> Self-test: [guide](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware" and "vSphere" are trademarks of Broadcom. Source code is publicly auditable at [github.com/vmware-skills/VMware-Policy](https://github.com/vmware-skills/VMware-Policy) under the MIT license.

Unified audit logging, policy enforcement, and input sanitization -- the infrastructure layer for the entire VMware MCP skill family.

> **Infrastructure dependency**: Every other package in the VMware skill family depends on vmware-policy. It is auto-installed and provides the `@vmware_tool` decorator, `sanitize()`, and the shared audit database.
> **Family**: [vmware-aiops](https://github.com/vmware-skills/VMware-AIops) (VM lifecycle), [vmware-monitor](https://github.com/vmware-skills/VMware-Monitor) (read-only monitoring), [vmware-storage](https://github.com/vmware-skills/VMware-Storage) (iSCSI/vSAN), [vmware-vks](https://github.com/vmware-skills/VMware-VKS) (Tanzu Kubernetes), [vmware-nsx](https://github.com/vmware-skills/VMware-NSX) (NSX networking), [vmware-nsx-security](https://github.com/vmware-skills/VMware-NSX-Security) (DFW/firewall), [vmware-aria](https://github.com/vmware-skills/VMware-Aria) (metrics/alerts/capacity), [vmware-avi](https://github.com/vmware-skills/VMware-AVI) (AVI/ALB/AKO).
> | [vmware-pilot](../vmware-pilot/SKILL.md) (workflow orchestration)

## What This Skill Does

| Category | Components | Count |
|----------|-----------|:-----:|
| **Audit Logging** | AuditEngine (SQLite WAL), log rotation, agent detection | 3 |
| **Policy Engine** | deny rules, maintenance windows, hot-reload | 3 |
| **Sanitization** | `sanitize()` -- prompt injection defense, control char stripping | 1 |
| **Decorator** | `@vmware_tool` -- pre-check + execute + post-log + metadata | 1 |
| **CLI** | `vmware-audit log`, `export`, `stats`, `policy`, `undo-list`, `undo-show` | 6 |

## Quick Install

```bash
uv tool install vmware-policy==1.25.0
vmware-audit stats          # verify installation
```

> vmware-policy is automatically installed as a dependency of all VMware skills. Manual install is only needed for standalone audit querying.

## When to Use This Skill

- Query the unified audit trail across all VMware skills
- View denied operations and policy violations
- Check audit statistics (by skill, by status, by time range)
- Export audit logs as JSON for external analysis
- Configure deny rules or maintenance windows
- Integrate the `@vmware_tool` decorator into a new VMware skill

**This skill is auto-loaded as a dependency** -- you do not need to invoke it directly. It activates when:
- Any VMware skill tool function is called (via `@vmware_tool` decorator)
- User asks about audit logs, denied operations, or policy rules
- User runs `vmware-audit` CLI commands

## Related Skills -- Skill Routing

| User Intent | Recommended Skill |
|-------------|------------------|
| VM lifecycle, deployment, guest ops | **vmware-aiops** (`uv tool install vmware-aiops`) |
| Read-only monitoring, zero risk | **vmware-monitor** (`uv tool install vmware-monitor`) |
| Storage: iSCSI, vSAN, datastores | **vmware-storage** (`uv tool install vmware-storage`) |
| Tanzu Kubernetes (vSphere 8.x+) | **vmware-vks** (`uv tool install vmware-vks`) |
| NSX networking: segments, gateways, NAT | **vmware-nsx** (`uv tool install vmware-nsx-mgmt`) |
| NSX security: DFW rules, security groups | **vmware-nsx-security** (`uv tool install vmware-nsx-security`) |
| Aria Ops: metrics, alerts, capacity | **vmware-aria** (`uv tool install vmware-aria`) |
| Load balancer, AVI, ALB, AKO, Ingress | **vmware-avi** (`uv tool install vmware-avi`) |
| Multi-step workflows with approval | **vmware-pilot** |
| Audit log query, policy rules | **vmware-policy** -- this skill |

## Common Workflows

### Query Recent Audit Activity

1. View last 20 audit entries: `vmware-audit log --last 20`
2. Filter by skill: `vmware-audit log --skill nsx --last 50` (the `skill` column holds the short name: `nsx`, `aiops`, `nsx_security`, ...)
3. Check denied operations: `vmware-audit log --status denied --since 2026-03-28`
4. View aggregate stats: `vmware-audit stats --days 7`

### Set Up Policy Rules for Production

1. Copy default rules: `cp $(python -c "import vmware_policy; print(vmware_policy.__file__.replace('__init__.py','rules_default.yaml'))") ~/.vmware/rules.yaml` (the shipped baseline denies nothing -- every rule in it is commented out)
2. Edit `~/.vmware/rules.yaml` -- add deny rules for production:
   ```yaml
   deny:
     - name: no-delete-in-prod
       operations: ["delete_*", "remove_cluster_host"]
       environments: ["production"]
       reason: "Destructive operations blocked in production"
   maintenance_window:
     start: "22:00"
     end: "06:00"
   ```
3. Rules hot-reload automatically -- no restart needed
4. Confirm the rules loaded: `vmware-audit policy` prints the rule source; `vmware-audit policy --operation delete_vm --skill aiops --env production --risk critical` shows what happens to one call
5. Verify: `vmware-audit log --status denied` to see blocked operations

### Export Audit Logs for Compliance

1. Export all logs as JSON: `vmware-audit export --format json > audit-export.json`
2. Filter by skill: `vmware-audit export --skill aiops --since 2026-01-01`
3. Import into your SIEM or compliance tool

## Usage Mode

| Scenario | Recommended | Why |
|----------|:-----------:|-----|
| Query audit logs | **CLI** | `vmware-audit` provides rich table output |
| Integrate into a skill | **Python API** | `from vmware_policy import vmware_tool, sanitize` |
| Automated compliance export | **CLI** | `vmware-audit export --format json` pipes to any tool |

## CLI Quick Reference

```bash
# View recent audit entries
vmware-audit log --last 20
vmware-audit log --skill nsx --status denied
vmware-audit log --since 2026-03-28 --tool delete_segment

# Which rules are in force (user file, shipped baseline, or unreadable)
vmware-audit policy

# Export for compliance
vmware-audit export --format json > audit.json
vmware-audit export --skill aiops --since 2026-01-01

# Aggregate statistics
vmware-audit stats --days 7
vmware-audit stats --days 30
```

> Full CLI reference: see `references/cli-reference.md`

## Python API

```python
from vmware_policy import vmware_tool, sanitize

# Wrap every MCP tool function
@vmware_tool(risk_level="high", sensitive_params=["password"])
def delete_segment(name: str, env: str = "") -> dict:
    ...

# Sanitize untrusted API responses before returning to LLM
clean_text = sanitize(api_response_text, max_len=500)
```

## MCP Tools (0)

vmware-policy does not expose MCP tools. It is a Python library and CLI consumed by other VMware skills.

| Component | Type | Description |
|-----------|------|-------------|
| `@vmware_tool` | Decorator | Policy pre-check + audit row around each MCP tool of the skills that use it |
| `sanitize()` | Function | Prompt injection defense for API responses |
| `AuditEngine` | Class | SQLite WAL audit logger with rotation |
| `PolicyEngine` | Class | YAML rule evaluation with hot-reload |
| `vmware-audit` | CLI | Typer CLI for querying audit trail |
| `detect_agent()` | Function | Infers calling AI agent from env vars (see below) |

### Agent Detection (Transparency Note)

The `detect_agent()` function in `audit.py` checks the following environment variables to identify which AI agent is calling the tools. This is **read-only inspection** for audit logging purposes — no credentials are extracted or stored:

| Env Var | Detected Agent | Purpose |
|---------|---------------|---------|
| `CLAUDE_SESSION_ID` or `CLAUDE_CODE` | claude | Claude Code session |
| `CODEX_SESSION` | codex | OpenAI Codex session |
| `OLLAMA_HOST` | local | Local Ollama model |
| `DEERFLOW_SESSION` | deerflow | DeerFlow session |
| (none matched) | unknown | Unrecognized agent |

Only the *presence* of these variables is checked; their values are never read into the audit row, and no API-key variable is inspected. The `agent` column stores only the inferred name above.

## Policy Defaults and Failure Behavior

Read/write authorization belongs to the vCenter/NSX account's RBAC; this engine only applies the operator's own optional deny rules and maintenance window. `vmware-audit policy` reports which of four rule sources is in force:

| Source | When | What is permitted |
|--------|------|-------------------|
| `user` | `~/.vmware/rules.yaml` exists and loads | Whatever your rules allow |
| `packaged-default` | No `~/.vmware/rules.yaml` | The shipped baseline, which **denies nothing** -- every operation is allowed by policy |
| `user-unreadable` | Your file exists but will not load (bad YAML, not UTF-8) | **Nothing** -- every operation is denied until the file is fixed; it is never replaced by the baseline |
| `baseline-unreadable` | No user file and the shipped baseline will not load | **Nothing** -- every operation is denied |

A malformed `maintenance_window` blocks high/critical operations. PyYAML is a declared dependency; if it is missing, the engine cannot start and every decorated tool call fails with an error (audited as `error`) -- nothing is silently allowed. `~/.vmware` is `$OPS_HOME` when that variable is set.

**`VMWARE_POLICY_DISABLED=1` is an operator escape hatch.** Read from the environment of the process running the skill (the MCP host or the CLI shell), it skips *all* policy evaluation -- deny rules, maintenance window, and the fail-closed state above. It does not disable auditing: a warning naming the operation and parameter *names* is logged, and rows from both surfaces -- MCP tools (`@vmware_tool`) and CLI commands wrapped by `@guarded` -- are recorded with a `_bypassed` status suffix (`ok_bypassed`, `error_bypassed`). Restrict who can set environment variables for the MCP host process, and do not leave the variable set.

## Troubleshooting

### "Cannot initialize audit DB" warning
The audit database directory `~/.vmware/` must be writable. Create it manually: `mkdir -p ~/.vmware && chmod 700 ~/.vmware`.

### Policy rules not taking effect
Rules are loaded from `~/.vmware/rules.yaml` (`$OPS_HOME/rules.yaml` if set). Run `vmware-audit policy`: `packaged-default` means your file was not found, `user-unreadable` means it failed to load and every operation is being denied. The PolicyEngine hot-reloads on file change -- no restart needed.

### Audit log growing too large
The AuditEngine automatically rotates at 100MB, keeping the 5 most recent archives. For manual cleanup: `ls ~/.vmware/audit.*.db` to see archives.

### "PolicyDenied" exception in skill
A deny rule in `~/.vmware/rules.yaml` matched, a closed maintenance window blocked a high/critical operation, or (rule `rules_unreadable`) the rules file failed to load. Check `vmware-audit log --status denied` for the rule name and reason. Fix the rule or file rather than bypassing; `VMWARE_POLICY_DISABLED=1` removes all policy for that process (see Policy Defaults above).

### Decorator not detecting skill name
The `@vmware_tool` decorator infers the skill name from the module path (e.g., `vmware_aiops.ops.vm_lifecycle` -> `aiops`). If the module does not follow the `vmware_<skill>` convention, the skill is logged as "unknown".

### SQLite "database is locked" error
Multiple concurrent skill processes can write to the same audit.db via WAL mode. If locks persist beyond 5 seconds, check for zombie processes holding the database file.

## Setup

```bash
uv tool install vmware-policy==1.25.0
mkdir -p ~/.vmware
```

> vmware-policy is auto-installed as a dependency of all VMware skills. The `~/.vmware/` directory is created automatically on first audit write.

> Full setup guide, security details, and integration instructions: see `references/setup-guide.md`

## Security

- **Source Code**: [github.com/vmware-skills/VMware-Policy](https://github.com/vmware-skills/VMware-Policy)
- **Config File Contents**: `~/.vmware/rules.yaml` contains only rule definitions, no credentials
- **Webhook Data Scope**: N/A -- vmware-policy does not send data externally
- **TLS Verification**: N/A -- vmware-policy does not make network connections
- **Prompt Injection Protection**: `sanitize()` strips C0/C1 control characters and Unicode format characters (zero-width, bidi overrides), then truncates (default 500 chars)
- **Least Privilege**: Audit database is local-only (`~/.vmware/audit.db`), no network exposure; the directory is set to `0700` and the database files to `0600` (best-effort)
- **Audit data is sensitive**: each row records tool name, parameters, result, status, OS user, inferred agent, and timestamps. Parameters named in `sensitive_params` are stored as `***`; results from tools declaring `sensitive_result=True` are replaced wholesale; credential-named keys (`password`, `token`, `kubeconfig`, ...) are redacted automatically in both parameters and results, on the MCP and CLI surfaces alike, as is credential-shaped text in error messages. A credential under a key not on that list still needs `sensitive_params`. Treat `audit.db` and its rotated archives as confidential.
- **Best-effort audit**: if the database cannot be written, the call still proceeds and a warning is logged
- **Policy bypass**: `VMWARE_POLICY_DISABLED=1` disables policy checks, not auditing -- restrict who can set it (see Policy Defaults above)

## License

MIT -- [github.com/vmware-skills/VMware-Policy](https://github.com/vmware-skills/VMware-Policy)

## Current evidence boundary

CPU/memory change_limits are enforced at the updated AIops reconfiguration backend, including decreases, using actual VM state and changeVersion. Generic parameter checks cannot prove a resize percentage. Scope and required package versions: `references/capabilities.md`.
