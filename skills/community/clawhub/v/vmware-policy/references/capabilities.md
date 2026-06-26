# VMware Policy -- Capabilities

Detailed reference for all components provided by vmware-policy.

## @vmware_tool Decorator

The mandatory wrapper for all VMware MCP tool functions across the entire skill family.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `risk_level` | str | `"low"` | Risk classification: `low`, `medium`, `high`, `critical` |
| `idempotent` | bool | `False` | Whether the operation can be safely retried on failure |
| `timeout_seconds` | int | `300` | Maximum execution time before warning |
| `sensitive_params` | list[str] | `None` | Parameter names to redact in audit logs (e.g., `["password"]`) |

### Execution Flow

```
@vmware_tool invocation
  1. Redact sensitive parameters for logging
  2. Detect calling AI agent (Claude, Codex, local, DeerFlow)
  3. Policy pre-check (deny rules, maintenance window)
     - If denied -> log as "denied", raise PolicyDenied
  4. Execute the wrapped function
  5. Post-log audit record to ~/.vmware/audit.db
     - Records: timestamp, skill, tool, params, result, status,
       duration_ms, agent, workflow_id, user, risk_level
```

### Usage Patterns

```python
# Minimal (defaults: low risk, not idempotent, 300s timeout)
@vmware_tool
def list_segments() -> list[dict]:
    ...

# Full options
@vmware_tool(
    risk_level="critical",
    idempotent=False,
    timeout_seconds=600,
    sensitive_params=["password", "secret_key"],
)
def delete_vm(name: str, password: str, env: str = "") -> dict:
    ...
```

### Metadata Attached to Wrapped Functions

After decoration, these attributes are available for introspection:

| Attribute | Type | Description |
|-----------|------|-------------|
| `_is_vmware_tool` | bool | Always `True` -- used for registration enforcement |
| `_risk_level` | str | Declared risk level |
| `_idempotent` | bool | Idempotency flag |
| `_timeout_seconds` | int | Timeout value |
| `_sensitive_params` | list[str] | List of redacted parameter names |

### Registration Enforcement

```python
# In MCP server startup -- verify all tools are decorated
for tool in tools:
    assert getattr(tool, "_is_vmware_tool", False), \
        f"{tool.__name__} missing @vmware_tool"
```

## PolicyEngine

Rule-based access control with YAML hot-reload.

### Rule Types

| Rule Type | Scope | Effect |
|-----------|-------|--------|
| **deny** | Block specific operations | Operation rejected with reason |
| **maintenance_window** | Time-based restriction | High/critical ops blocked outside window |
| **change_limits** | Parameter thresholds | Reserved -- not enforced (logs a warning if configured) |

### Rules YAML Schema

```yaml
# ~/.vmware/rules.yaml

deny:
  - name: <rule-name>           # Human-readable identifier
    operations: ["<pattern>"]   # Glob patterns (e.g., "delete_*")
    environments: ["<env>"]     # Target environments (e.g., "production")
    min_risk_level: <level>     # Minimum risk level to match
    reason: "<message>"         # Denial message shown to user

maintenance_window:
  start: "HH:MM"               # Window start (24h format)
  end: "HH:MM"                 # Window end (wraps midnight)

change_limits:                  # Reserved -- not enforced; configuring these
  max_cpu_change_pct: <int>     # only emits a "NOT enforced" warning (the
  max_memory_change_pct: <int>  # engine has no before-state to compute deltas)
```

### Rule Evaluation Order

1. Deny rules -- if any match, operation is blocked
2. Maintenance window -- high/critical ops restricted to window hours
3. Default -- allow

(change_limits is reserved and not enforced -- see the Rule Types table.)

### Hot-Reload

The PolicyEngine checks the rules file mtime on every `check_allowed()` call. If the file has changed, rules are re-read automatically. No service restart needed.

### Policy Bypass

Set `VMWARE_POLICY_DISABLED=1` to bypass all policy checks. Operations are still logged with status `ok_bypassed` for audit trail completeness.

## AuditEngine

Append-only audit logger backed by SQLite WAL.

### Database Schema

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Auto-increment primary key |
| `ts` | TEXT | ISO 8601 timestamp (UTC) |
| `skill` | TEXT | Skill name (e.g., `aiops`, `nsx`) |
| `tool` | TEXT | Tool function name |
| `params` | TEXT | JSON -- sanitized parameters |
| `result` | TEXT | JSON -- operation result |
| `status` | TEXT | `ok`, `denied`, `error`, `ok_bypassed` |
| `duration_ms` | INTEGER | Execution time in milliseconds |
| `agent` | TEXT | Detected AI agent |
| `workflow_id` | TEXT | Workflow ID from vmware-pilot |
| `user` | TEXT | OS username |
| `risk_level` | TEXT | Declared risk level |

### Rotation Policy

- **Threshold**: 100 MB
- **Archives kept**: 5 most recent
- **Archive naming**: `audit.YYYYMMDD-HHMMSS.db`
- **Location**: `~/.vmware/`

### Agent Detection

The audit engine auto-detects the calling AI agent:

| Agent | Detection Method |
|-------|-----------------|
| Claude | `CLAUDE_SESSION_ID` or `CLAUDE_CODE` env var |
| Codex | `OPENAI_API_KEY` or `CODEX_SESSION` env var |
| Local (Ollama) | `OLLAMA_HOST` env var |
| DeerFlow | `DEERFLOW_SESSION` env var |
| Unknown | No matching env vars |

### Thread Safety

SQLite WAL mode allows multiple concurrent writers. The `busy_timeout` is set to 5 seconds to handle lock contention from parallel skill processes.

## sanitize()

Prompt injection defense for untrusted API responses.

### Signature

```python
def sanitize(text: str, max_len: int = 500) -> str:
    """Strip C0/C1 control characters (except newline/tab) and truncate."""
```

### What It Removes

- C0 control characters: `\x00`-`\x08`, `\x0b`, `\x0c`, `\x0e`-`\x1f`
- C1 control characters: `\x7f`-`\x9f`
- Preserves: newline (`\n`), tab (`\t`), carriage return (`\r`)

### When to Use

All text from vSphere, NSX, and Aria API responses must pass through `sanitize()` before being returned to the LLM. This prevents prompt injection via crafted VM names, descriptions, or annotation fields.

```python
from vmware_policy import sanitize

vm_name = sanitize(api_response["name"])
vm_notes = sanitize(api_response.get("annotation", ""), max_len=200)
```

## Risk Levels

| Level | Confirmation Required | Examples |
|-------|:---------------------:|---------|
| `low` | No | list, get, info, status |
| `medium` | No | reconfigure, update settings |
| `high` | Yes | power off, migrate, snapshot revert |
| `critical` | Yes + production approval | delete VM, delete cluster, delete security policy |
