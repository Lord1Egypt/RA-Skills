# VMware Policy -- Capabilities

Detailed reference for all components provided by vmware-policy.

## @vmware_tool Decorator

The wrapper that VMware skills put around their MCP tool functions: policy pre-check before, one audit row after.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `risk_level` | str | `"low"` | Risk classification: `low`, `medium`, `high`, `critical` |
| `idempotent` | bool | `False` | Whether the operation can be safely retried on failure |
| `timeout_seconds` | int | `300` | Maximum execution time before warning |
| `sensitive_params` | list[str] | `None` | Parameter names whose values are stored as `***` in audit rows (e.g., `["password"]`). Credential-named parameters (`password`, `token`, ...) are also redacted automatically; declare any credential whose key name is not on that list. |
| `sensitive_result` | bool | `False` | The return value *is* a credential (kubeconfig, token). The audit row stores `"[redacted: return value declared sensitive]"`; the caller still gets the real value. |
| `undo` | callable | `None` | `(params, result)` returning an inverse descriptor dict (or `None`),, recorded to `~/.vmware/undo.db` on success. Recording only -- nothing is executed. |

### Execution Flow

```
@vmware_tool invocation
  1. Redact sensitive_params for logging
  2. Detect calling AI agent (Claude, Codex, local, DeerFlow)
  3. Policy pre-check (deny rules, maintenance window, unreadable-rules denial;
     skipped entirely when VMWARE_POLICY_DISABLED=1)
     - If denied -> recorded as "denied", raise PolicyDenied
  4. Per-process call budget / runaway guard -> "budget_exceeded"
  5. Execute the wrapped function
  6. Post-log audit record to ~/.vmware/audit.db (in a finally block, best-effort)
     - Result: replaced if sensitive_result; credential-named keys redacted;
       raised exceptions stored with credential-shaped text redacted
     - Records: timestamp, skill, tool, params, result, status,
       duration_ms, agent, user, risk_level, rationale, approved_by
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
| `_sensitive_result` | bool | Whether the result is redacted from the audit row |

### Registration Enforcement

```python
# In MCP server startup -- verify all tools are decorated
for tool in tools:
    assert getattr(tool, "_is_vmware_tool", False), \
        f"{tool.__name__} missing @vmware_tool"
```

## PolicyEngine

Rule-based access control with YAML hot-reload. It applies only the operator's own rules; read/write authorization is the vCenter/NSX account's RBAC.

### Rule Sources

`active_rules_source()` (shown by `vmware-audit policy`) returns one of:

| Source | When | What is permitted |
|--------|------|-------------------|
| `user` | `~/.vmware/rules.yaml` exists and loads | Whatever the rules allow |
| `packaged-default` | No user file | The shipped `rules_default.yaml`, whose rules are all commented out -- nothing is denied |
| `user-unreadable` | User file exists but fails to load (YAML error, not UTF-8) | Nothing: every operation is denied (rule `rules_unreadable`) until the file loads. The baseline is not substituted. |
| `baseline-unreadable` | No user file and the baseline fails to load | Nothing: every operation is denied |

A user file replaces the baseline; they are never merged. An empty loaded rule set allows everything. PyYAML is a declared dependency; without it the engine cannot be constructed and decorated calls fail rather than run.

### Rule Types

| Rule Type | Scope | Effect |
|-----------|-------|--------|
| **deny** | Block specific operations | Operation rejected with reason |
| **maintenance_window** | Time-based restriction (UTC) | High/critical ops blocked outside window; a malformed window blocks them always |
| **change_limits** | AIops VM CPU/memory reconfiguration | Backend checks absolute percentage changes against current sizing and binds changeVersion |

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

change_limits:                  # Policy 1.25.0 + AIops 2.5.0 backend required
  max_cpu_change_pct: <number>  # finite, nonnegative; increases and decreases
  max_memory_change_pct: <number> # same, from current memory MB
```

### Rule Evaluation Order

1. Deny rules -- if any match, operation is blocked
2. Maintenance window -- high/critical ops restricted to window hours
3. Default -- allow

After surface authorization, the AIops backend checks configured limits using actual VM state before ReconfigVM_Task. Missing required state/version or malformed limits refuse the change. Other operations/products are outside this scope; caller-supplied percentages are not authoritative.

### Hot-Reload

The PolicyEngine checks the rules file mtime on every `check_allowed()` call. If the file has changed, rules are re-read automatically. No service restart needed.

### Policy Bypass

`VMWARE_POLICY_DISABLED=1`, read from the environment of the process running the skill, makes `check_allowed()` return allowed (rule `policy_disabled`) before any rule is evaluated -- including the fail-closed denial for unreadable rules. It is an operator escape hatch; restrict who can set the MCP host's environment.

It does not disable auditing or redaction. Each bypassed check logs a warning with the operation and parameter names (not values). Rows from both surfaces -- `@vmware_tool` MCP calls and `@guarded` CLI commands -- carry a `_bypassed` status suffix (`ok_bypassed`, `error_bypassed`).

## AuditEngine

Append-only audit logger backed by SQLite WAL.

### Database Schema

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Auto-increment primary key |
| `ts` | TEXT | ISO 8601 timestamp (UTC) |
| `skill` | TEXT | Skill name (e.g., `aiops`, `nsx`) |
| `tool` | TEXT | Tool function name |
| `params` | TEXT | JSON -- call parameters, with `sensitive_params` values stored as `***` |
| `result` | TEXT | JSON -- operation result (or error text + traceback excerpt), after credential redaction |
| `status` | TEXT | `ok`, `dry_run` (completed with `dry_run=True` — nothing changed), `denied`, `error` (raised; returned `{"error": …}` or `outcome: "failed"`; non-zero `SystemExit` / Typer exit; `report_tool_failure`), `budget_exceeded`, `rejected` (CLI: confirmation declined), `interrupted` (Ctrl+C or a cancelled MCP call — the remote operation may still be running), or `<status>_bypassed` |
| `duration_ms` | INTEGER | Execution time in milliseconds |
| `agent` | TEXT | Detected AI agent |
| `workflow_id` | TEXT | Workflow ID from vmware-pilot |
| `user` | TEXT | OS username |
| `risk_level` | TEXT | Declared risk level |
| `rationale` | TEXT | Self-attested, from `VMWARE_AUDIT_RATIONALE` (not an authorization) |
| `approved_by` | TEXT | Self-attested, from `VMWARE_AUDIT_APPROVED_BY` (not an authorization) |
| `risk_tier` | TEXT | Legacy column from the removed approval tiers; written empty |

**The database is sensitive.** Parameters and results can carry inventory names, addresses and configuration, and a credential under a key name the automatic redaction does not know must be declared in `sensitive_params`. The engine sets the directory to `0700` and the database files to `0600` (best-effort); treat `audit.db` and its archives as confidential. Writes are best-effort -- if the database cannot be written, the call proceeds and a warning is logged.

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
| Codex | `CODEX_SESSION` env var |
| Local (Ollama) | `OLLAMA_HOST` env var |
| DeerFlow | `DEERFLOW_SESSION` env var |
| Unknown | No matching env vars |

Only the presence of these variables is checked, and only the inferred name is stored. No API-key variable is inspected.

### Thread Safety

SQLite WAL mode allows multiple concurrent writers. The `busy_timeout` is set to 5 seconds to handle lock contention from parallel skill processes.

## sanitize()

Prompt injection defense for untrusted API responses.

### Signature

```python
def sanitize(text: str | None, max_len: int = 500) -> str:
    """Strip control and Unicode format characters, then truncate."""
```

### What It Removes

- C0 control characters: `\x00`-`\x08`, `\x0b`, `\x0c`, `\x0e`-`\x1f`
- C1 control characters: `\x7f`-`\x9f`
- Unicode format characters (category Cf): zero-width spaces/joiners, bidi overrides
- Preserves: newline (`\n`), tab (`\t`), carriage return (`\r`)
- Truncates to `max_len` *after* stripping; `None` becomes `""`

### When to Use

All text from vSphere, NSX, and Aria API responses must pass through `sanitize()` before being returned to the LLM. This prevents prompt injection via crafted VM names, descriptions, or annotation fields.

```python
from vmware_policy import sanitize

vm_name = sanitize(api_response["name"])
vm_notes = sanitize(api_response.get("annotation", ""), max_len=200)
```

## Risk Levels

Each operation is classified by risk level. The level is recorded in the audit
row, can be matched by a `deny` rule's `min_risk_level`, and decides whether a
configured `maintenance_window` applies (high/critical only); it does not by
itself gate execution.

| Level | Examples |
|-------|---------|
| `low` | list, get, info, status |
| `medium` | reconfigure, update settings |
| `high` | power off, migrate, snapshot revert |
| `critical` | delete VM, delete cluster, delete security policy |

## Maintenance safety boundary

CPU/memory change_limits are enforced at the updated AIops reconfiguration backend, including decreases, using actual VM state and changeVersion. Generic parameter checks cannot prove a resize percentage. Scope and required package versions: `references/capabilities.md`.

Post-deployment resizing through the same backend is checked too; refusal can leave the created VM at its original size. Inspect the result before retrying. No automatic cleanup or clone replay is performed.
