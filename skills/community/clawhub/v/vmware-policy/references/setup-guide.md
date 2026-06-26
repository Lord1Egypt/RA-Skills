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
uv tool install vmware-policy
vmware-audit stats   # verify
```

### Development

```bash
git clone https://github.com/zw008/VMware-Policy.git
cd VMware-Policy
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
pytest --cov=vmware_policy
```

## Configuration

### Audit Database

The audit database is created automatically at `~/.vmware/audit.db` on first use. No configuration needed.

```bash
# Verify the directory exists and is writable
mkdir -p ~/.vmware
chmod 700 ~/.vmware
```

### Policy Rules (Optional)

Policy rules are optional. Without `~/.vmware/rules.yaml`, all operations are allowed (audit logging still active).

```bash
# Copy the default rules template
cp $(python -c "import vmware_policy; import os; print(os.path.join(os.path.dirname(vmware_policy.__file__), 'rules_default.yaml'))") ~/.vmware/rules.yaml

# Edit rules as needed
vi ~/.vmware/rules.yaml
```

### Environment Variables

| Variable | Required | Description |
|----------|:--------:|-------------|
| `VMWARE_POLICY_DISABLED` | No | Set to `1` to bypass policy checks (still logged) |

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

- Location: `~/.vmware/audit.db` (user home directory)
- Permissions: inherited from `~/.vmware/` directory (recommend `chmod 700`)
- No network exposure -- SQLite is local-only
- WAL mode for concurrent write safety

### Rules File Security

- Location: `~/.vmware/rules.yaml`
- Contains only rule definitions, no credentials
- Readable by the user running the skill processes

### Sensitive Parameter Redaction

Parameters listed in `sensitive_params` are replaced with `***` in audit logs:

```python
# In audit.db, params column shows:
# {"name": "my-vm", "password": "***"}
```

### Data Sanitization

All API response text passes through `sanitize()`:
- Truncation: default 500 characters (configurable per call)
- Control character stripping: C0/C1 characters removed
- Prevents prompt injection via crafted VM names or descriptions

## AI Platform Compatibility

vmware-policy is framework-agnostic. It works with any MCP client:

| Platform | Status | Agent Detection |
|----------|:------:|-----------------|
| Claude Code | Supported | `CLAUDE_SESSION_ID` / `CLAUDE_CODE` |
| OpenAI Codex | Supported | `OPENAI_API_KEY` / `CODEX_SESSION` |
| Ollama (local) | Supported | `OLLAMA_HOST` |
| DeerFlow | Supported | `DEERFLOW_SESSION` |
| Any MCP client | Supported | Logged as "unknown" agent |

## MCP Server Configuration

vmware-policy does not run as an MCP server itself. It is a Python library consumed by other VMware skill MCP servers. The `vmware-audit` CLI is the user-facing interface.

```json
{
  "mcpServers": {
    "vmware-policy": {
      "command": "uvx",
      "args": ["--from", "vmware-policy", "vmware-audit"],
      "env": {}
    }
  }
}
```

> Note: This configuration exposes the `vmware-audit` CLI, not an MCP server. For MCP tool access, use the individual skill servers (vmware-aiops, vmware-nsx, etc.) which include vmware-policy as a dependency.

## Troubleshooting

### Import Error: "No module named vmware_policy"

Ensure vmware-policy is installed in the same environment as your skill:

```bash
uv pip install vmware-policy
```

### "Permission denied" on audit.db

```bash
chmod 700 ~/.vmware
chmod 600 ~/.vmware/audit.db
```

### Rules file changes not taking effect

The PolicyEngine checks file mtime on each call. Verify:

```bash
ls -la ~/.vmware/rules.yaml   # check mtime updated
python -c "import yaml; print(yaml.safe_load(open('$HOME/.vmware/rules.yaml')))"  # validate YAML
```

### PyYAML not installed

Policy rules require PyYAML. If not present, the PolicyEngine silently allows all operations (audit logging still works):

```bash
uv pip install pyyaml
```
