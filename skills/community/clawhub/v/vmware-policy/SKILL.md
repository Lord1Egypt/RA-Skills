---
name: vmware-policy
description: >
  Unified audit logging, policy enforcement, and input sanitization for the entire VMware MCP skill family.
  Use when querying audit logs, managing policy rules, or when any VMware skill needs audit/policy infrastructure.
  Provides the @vmware_tool decorator that wraps all 156+ MCP tools across 8 skills.
  Use when user asks to "show audit log", "check denied operations", "view policy rules", "audit stats", or "query audit trail".
  For VM lifecycle use vmware-aiops, for monitoring use vmware-monitor, for networking use vmware-nsx, for load balancing use vmware-avi.
installer:
  kind: uv
  package: vmware-policy
allowed-tools:
  - Bash
user-invocable: false
metadata: {"openclaw":{"requires":{"bins":["vmware-audit"],"config":["~/.vmware/rules.yaml"]},"optional":{"env":["CLAUDE_SESSION_ID","OLLAMA_HOST"]},"homepage":"https://github.com/zw008/VMware-Policy","emoji":"🛡️","os":["macos","linux"]}}
---

# VMware Policy

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware" and "vSphere" are trademarks of Broadcom. Source code is publicly auditable at [github.com/zw008/VMware-Policy](https://github.com/zw008/VMware-Policy) under the MIT license.

Unified audit logging, policy enforcement, and input sanitization -- the infrastructure layer for the entire VMware MCP skill family.

> **Infrastructure dependency**: All 8 VMware skills depend on vmware-policy. It is auto-installed and provides the `@vmware_tool` decorator, `sanitize()`, and the shared audit database.
> **Family**: [vmware-aiops](https://github.com/zw008/VMware-AIops) (VM lifecycle), [vmware-monitor](https://github.com/zw008/VMware-Monitor) (read-only monitoring), [vmware-storage](https://github.com/zw008/VMware-Storage) (iSCSI/vSAN), [vmware-vks](https://github.com/zw008/VMware-VKS) (Tanzu Kubernetes), [vmware-nsx](https://github.com/zw008/VMware-NSX) (NSX networking), [vmware-nsx-security](https://github.com/zw008/VMware-NSX-Security) (DFW/firewall), [vmware-aria](https://github.com/zw008/VMware-Aria) (metrics/alerts/capacity), [vmware-avi](https://github.com/zw008/VMware-AVI) (AVI/ALB/AKO).
> | [vmware-pilot](../vmware-pilot/SKILL.md) (workflow orchestration)

## What This Skill Does

| Category | Components | Count |
|----------|-----------|:-----:|
| **Audit Logging** | AuditEngine (SQLite WAL), log rotation, agent detection | 3 |
| **Policy Engine** | deny rules, maintenance windows, hot-reload | 3 |
| **Sanitization** | `sanitize()` -- prompt injection defense, control char stripping | 1 |
| **Decorator** | `@vmware_tool` -- pre-check + execute + post-log + metadata | 1 |
| **CLI** | `vmware-audit log`, `vmware-audit export`, `vmware-audit stats` | 3 |

## Quick Install

```bash
uv tool install vmware-policy
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
2. Filter by skill: `vmware-audit log --skill vmware-nsx --last 50`
3. Check denied operations: `vmware-audit log --status denied --since 2026-03-28`
4. View aggregate stats: `vmware-audit stats --days 7`

### Set Up Policy Rules for Production

1. Copy default rules: `cp $(python -c "import vmware_policy; print(vmware_policy.__file__.replace('__init__.py','rules_default.yaml'))") ~/.vmware/rules.yaml`
2. Edit `~/.vmware/rules.yaml` -- add deny rules for production:
   ```yaml
   deny:
     - name: no-delete-in-prod
       operations: ["delete_*", "cluster_delete"]
       environments: ["production"]
       reason: "Destructive operations blocked in production"
   maintenance_window:
     start: "22:00"
     end: "06:00"
   ```
3. Rules hot-reload automatically -- no restart needed
4. Verify: `vmware-audit log --status denied` to see blocked operations

### Export Audit Logs for Compliance

1. Export all logs as JSON: `vmware-audit export --format json > audit-export.json`
2. Filter by skill: `vmware-audit export --skill vmware-aiops --since 2026-01-01`
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
vmware-audit log --skill vmware-nsx --status denied
vmware-audit log --since 2026-03-28 --tool delete_segment

# Export for compliance
vmware-audit export --format json > audit.json
vmware-audit export --skill vmware-aiops --since 2026-01-01

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
| `@vmware_tool` | Decorator | Wraps all 156+ MCP tools across 8 skills |
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
| `OPENAI_API_KEY` or `CODEX_SESSION` | codex | OpenAI Codex session |
| `OLLAMA_HOST` | local | Local Ollama model |
| `DEERFLOW_SESSION` | deerflow | DeerFlow session |
| (none matched) | unknown | Unrecognized agent |

The detected agent name is stored in the `agent` column of `~/.vmware/audit.db` for audit trail purposes only. No API keys or tokens are logged.

## Troubleshooting

### "Cannot initialize audit DB" warning
The audit database directory `~/.vmware/` must be writable. Create it manually: `mkdir -p ~/.vmware && chmod 700 ~/.vmware`.

### Policy rules not taking effect
Rules are loaded from `~/.vmware/rules.yaml`. Verify the file exists and contains valid YAML. The PolicyEngine hot-reloads on file change -- no restart needed.

### Audit log growing too large
The AuditEngine automatically rotates at 100MB, keeping the 5 most recent archives. For manual cleanup: `ls ~/.vmware/audit.*.db` to see archives.

### "PolicyDenied" exception in skill
This means a deny rule in `~/.vmware/rules.yaml` matched the operation. Check `vmware-audit log --status denied` to see the rule name and reason. To temporarily bypass: `VMWARE_POLICY_DISABLED=1` (still logged as bypassed).

### Decorator not detecting skill name
The `@vmware_tool` decorator infers the skill name from the module path (e.g., `vmware_aiops.ops.vm_lifecycle` -> `aiops`). If the module does not follow the `vmware_<skill>` convention, the skill is logged as "unknown".

### SQLite "database is locked" error
Multiple concurrent skill processes can write to the same audit.db via WAL mode. If locks persist beyond 5 seconds, check for zombie processes holding the database file.

## Setup

```bash
uv tool install vmware-policy
mkdir -p ~/.vmware
```

> vmware-policy is auto-installed as a dependency of all VMware skills. The `~/.vmware/` directory is created automatically on first audit write.

> Full setup guide, security details, and integration instructions: see `references/setup-guide.md`

## Security

- **Source Code**: [github.com/zw008/VMware-Policy](https://github.com/zw008/VMware-Policy)
- **Config File Contents**: `~/.vmware/rules.yaml` contains only rule definitions, no credentials
- **Webhook Data Scope**: N/A -- vmware-policy does not send data externally
- **TLS Verification**: N/A -- vmware-policy does not make network connections
- **Prompt Injection Protection**: `sanitize()` truncates to 500 chars and strips C0/C1 control characters
- **Least Privilege**: Audit database is local-only (`~/.vmware/audit.db`), no network exposure

## License

MIT -- [github.com/zw008/VMware-Policy](https://github.com/zw008/VMware-Policy)
