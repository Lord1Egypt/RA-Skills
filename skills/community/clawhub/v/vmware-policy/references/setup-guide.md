# VMware Policy -- Setup Guide

## Installation

### As a Dependency (Standard)

vmware-policy is automatically installed when you install any VMware skill:

```bash
uv tool install vmware-aiops       # installs vmware-policy as dependency
uv tool install vmware-monitor     # same
uv tool install vmware-nsx-mgmt   # same
```

### Standalone (For Audit Querying)

```bash
uv tool install vmware-policy==1.25.0
vmware-audit stats   # verify
```

### Development

```bash
git clone --branch v1.25.0 https://github.com/vmware-skills/VMware-Policy.git
cd VMware-Policy
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
pytest --cov=vmware_policy
```

## Configuration

### Audit Database

The audit database is created automatically at `~/.vmware/audit.db` on first use (`$OPS_HOME/audit.db` when `OPS_HOME` is set). No configuration needed.

```bash
# Verify the directory exists and is writable
mkdir -p ~/.vmware
chmod 700 ~/.vmware
```

### Policy Rules (Optional)

Policy rules are optional. Read/write authorization is the job of the vCenter/NSX account's RBAC; the policy engine only adds the operator's own deny rules and maintenance window on top. Which rules are in force depends on the rules file, and `vmware-audit policy` reports it:

| Source | When | What is permitted |
|--------|------|-------------------|
| `user` | `~/.vmware/rules.yaml` exists and loads | Whatever your rules allow |
| `packaged-default` | No `~/.vmware/rules.yaml` | The shipped baseline (`rules_default.yaml`), which has every rule commented out -- **nothing is denied**, all operations are allowed by policy. Audit logging still runs. |
| `user-unreadable` | Your file exists but will not load (YAML syntax error, not UTF-8) | **Nothing** -- every operation, reads included, is denied with a message naming the file, until it loads. The shipped baseline is never substituted for a broken user file. |
| `baseline-unreadable` | No user file, and the shipped baseline will not load | **Nothing** -- every operation is denied |

A user file replaces the baseline entirely; the two are never merged. Within a loaded rule set, a malformed `maintenance_window` blocks high/critical operations until it is fixed.

```bash
# Copy the default rules template
cp $(python -c "import vmware_policy; import os; print(os.path.join(os.path.dirname(vmware_policy.__file__), 'rules_default.yaml'))") ~/.vmware/rules.yaml

# Edit rules as needed
vi ~/.vmware/rules.yaml

# Confirm they loaded
vmware-audit policy
```

### Environment Variables

| Variable | Required | Description |
|----------|:--------:|-------------|
| `OPS_HOME` | No | Directory holding `audit.db`, `rules.yaml` and `undo.db` (default `~/.vmware`) |
| `VMWARE_POLICY_DISABLED` | No | Operator escape hatch -- `1` skips all policy evaluation (see below) |

### Policy Bypass (`VMWARE_POLICY_DISABLED=1`)

Read from the environment of the process running the skill -- the MCP host, or the shell running a skill CLI. When set to `1`:

- **Skipped**: every policy check -- deny rules, the maintenance window, and the fail-closed denial for an unreadable rules file.
- **Not skipped**: audit logging, parameter/result redaction, and `@vmware_tool`'s per-process call budget.
- **Recorded**: each bypassed check logs a warning with the operation, environment, risk level and parameter *names* (never values). Rows written by `@vmware_tool` and by CLI commands wrapped in `@guarded` both get a `_bypassed` status suffix (e.g. `ok_bypassed`, `error_bypassed`).

Treat it as a break-glass switch: restrict who can edit the MCP host's configuration or environment, and unset it once the rules file is fixed.

## Integration Into a New Skill

### 1. Add Dependency

In your skill's `pyproject.toml`:

```toml
dependencies = [
    "vmware-policy>=1.4.0",
    ...
]
```

### 2. Decorate All MCP Tools

```python
from vmware_policy import vmware_tool

@vmware_tool(risk_level="high", sensitive_params=["password"])
def my_tool(name: str, password: str) -> dict:
    ...
```

### 3. Sanitize API Responses

```python
from vmware_policy import sanitize

def list_items(api_client) -> list[dict]:
    raw = api_client.get_items()
    return [
        {"name": sanitize(item["name"]), "status": sanitize(item["status"])}
        for item in raw
    ]
```

### 4. Enforce Registration at Startup

```python
# In your MCP server startup
for tool in registered_tools:
    assert getattr(tool, "_is_vmware_tool", False), \
        f"{tool.__name__} not decorated with @vmware_tool"
```

## Security

### Audit Database Security

- Location: `~/.vmware/audit.db` (user home directory, or `$OPS_HOME`)
- Permissions: the engine sets the directory to `0700` and `audit.db` / `-wal` / `-shm` to `0600` on creation and rotation (best-effort -- verify on shared hosts)
- No network exposure -- SQLite is local-only
- WAL mode for concurrent write safety
- Best-effort: if the database cannot be written, the tool call still proceeds and a warning is logged

**Treat the audit database as sensitive.** Every row holds the skill, tool name, call parameters, the result (or error text and a traceback excerpt), status, duration, OS user, inferred agent, timestamp, and the self-attested `rationale` / `approved_by` fields (from `VMWARE_AUDIT_RATIONALE` / `VMWARE_AUDIT_APPROVED_BY`). Results can include inventory names, addresses and configuration. Rotated archives (`audit.YYYYMMDD-HHMMSS.db`, five kept) hold the same data. Restrict access to the directory and review an export before attaching it to a ticket.

### Rules File Security

- Location: `~/.vmware/rules.yaml`
- Contains only rule definitions, no credentials
- Readable by the user running the skill processes

### Credential Redaction in Audit Rows

Redaction applies to the audit copy only; the caller always receives the real value.

- **Parameters**: names listed in `sensitive_params` are replaced with `***`, including inside nested dicts and lists. Credential-named parameters (`password`, `token`, ...) are also redacted automatically, declared or not; declare any credential whose key name is not on that list.
- **Declared credential results**: a tool decorated with `sensitive_result=True` (e.g. one returning a kubeconfig or token) has its whole result stored as `"[redacted: return value declared sensitive]"`.
- **Credential-named result keys**: in every result, values under keys such as `password`, `token`, `secret`, `api_key`, `authorization`, `kubeconfig` are replaced -- the net for a tool that forgot to declare. A key matches when its whole name is one of those words, or when it *ends* in `_` plus a credential word (`vc_password`, `new_password`, `client_api_key`, `admin_token`); matching is case-insensitive with `-`/`_` folded. It is not a substring search: `token_count` and `secret_manager_url` stay readable because the credential word is not the tail.
- **Error text**: exceptions raised by `@vmware_tool` tools and `@guarded` CLI commands have credential-shaped text (`password=...`, `Authorization: Bearer ...`, URL userinfo, PEM private keys, JWTs) redacted before storage.

```python
# In audit.db, params column shows:
# {"name": "my-vm", "password": "***"}
```

### Data Sanitization

API response text that a skill passes through `sanitize()`:
- Control characters stripped: C0/C1 (newline, tab and carriage return kept) and Unicode format characters (zero-width, bidi overrides)
- Truncation: default 500 characters (configurable per call), applied after stripping
- Prevents prompt injection via crafted VM names or descriptions

## AI Platform Compatibility

vmware-policy is framework-agnostic. It works with any MCP client:

| Platform | Status | Agent Detection |
|----------|:------:|-----------------|
| Claude Code | Supported | `CLAUDE_SESSION_ID` / `CLAUDE_CODE` |
| OpenAI Codex | Supported | `CODEX_SESSION` |
| Ollama (local) | Supported | `OLLAMA_HOST` |
| DeerFlow | Supported | `DEERFLOW_SESSION` |
| Any MCP client | Supported | Logged as "unknown" agent |

## MCP Server Configuration

vmware-policy does not run as an MCP server itself and has no MCP client configuration -- `vmware-audit` is a plain CLI, not an MCP server, so do not register it in an `mcpServers` block. It is a Python library consumed by other VMware skill MCP servers. For MCP tool access, use the individual skill servers (vmware-aiops, vmware-nsx, etc.), which include vmware-policy as a dependency; `VMWARE_POLICY_DISABLED` and `OPS_HOME` take effect in *their* process environment.

## Troubleshooting

### Import Error: "No module named vmware_policy"

Ensure vmware-policy is installed in the same environment as your skill:

```bash
uv pip install vmware-policy==1.25.0
```

### "Permission denied" on audit.db

```bash
chmod 700 ~/.vmware
chmod 600 ~/.vmware/audit.db
```

### Rules file changes not taking effect

The PolicyEngine checks file mtime on each call. Verify:

```bash
vmware-audit policy           # rule source: user / packaged-default / *-unreadable
ls -la ~/.vmware/rules.yaml   # check mtime updated
python -c "import yaml; print(yaml.safe_load(open('$HOME/.vmware/rules.yaml', encoding='utf-8')))"  # validate YAML
```

`packaged-default` means the engine did not find your file (check `OPS_HOME`); `user-unreadable` means it found it, could not load it, and is denying every operation until it is fixed.

### PyYAML not installed

PyYAML is a declared dependency of vmware-policy, so a normal install always has it. If it is missing from the environment anyway, the PolicyEngine cannot be constructed and every `@vmware_tool` call fails with `ModuleNotFoundError` (recorded as `error` in the audit log) -- no operation is silently allowed. Reinstall the skill, or:

```bash
uv pip install pyyaml
```
