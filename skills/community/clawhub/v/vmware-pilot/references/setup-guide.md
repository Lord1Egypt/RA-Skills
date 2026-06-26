# Setup Guide — vmware-pilot

## Prerequisites

- Python 3.10+
- `vmware-policy` package (auto-installed as dependency)
- At least one companion skill installed (aiops, monitor, nsx, etc.) for workflows to delegate to

## Installation

### Via uv (Recommended)

```bash
uv tool install vmware-pilot
```

### Via pip

```bash
pip install vmware-pilot

# China mainland mirror
pip install vmware-pilot -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Verify Installation

```bash
# Start the MCP server (exits immediately if all imports succeed)
uvx --from vmware-pilot vmware-pilot-mcp
```

---

## MCP Configuration

### Claude Code

Add to your Claude Code MCP config:

```json
{
  "mcpServers": {
    "vmware-pilot": {
      "command": "uvx",
      "args": ["--from", "vmware-pilot", "vmware-pilot-mcp"]
    }
  }
}
```

### Cursor / VS Code Copilot

```json
{
  "mcpServers": {
    "vmware-pilot": {
      "command": "uvx",
      "args": ["--from", "vmware-pilot", "vmware-pilot-mcp"]
    }
  }
}
```

### Goose

```yaml
extensions:
  vmware-pilot:
    name: vmware-pilot
    type: stdio
    cmd: uvx
    args:
      - --from
      - vmware-pilot
      - vmware-pilot-mcp
```

---

## Configuration

Pilot itself requires **no vCenter/NSX/AVI credentials**. It is a pure orchestrator that delegates all infrastructure calls to companion skills.

### Workflow Database

Workflows are persisted to `~/.vmware/workflows.db` (SQLite, WAL mode). Created automatically on first use.

### Custom Templates Directory

```bash
mkdir -p ~/.vmware/workflows
```

Drop YAML workflow templates here. Hot-reloaded without server restart.

### Policy Rules (Optional)

vmware-policy rules at `~/.vmware/rules.yaml` apply to all pilot operations:

```yaml
# Example: deny destructive operations outside maintenance window
rules:
  - name: maintenance_window
    match:
      risk_level: [high, critical]
    deny_unless:
      time_range: "02:00-06:00"
      timezone: "Asia/Shanghai"
```

### Audit Database

All tool calls are logged to `~/.vmware/audit.db` via vmware-policy. View with:

```bash
vmware-audit log --last 20
vmware-audit log --status denied
```

---

## Companion Skills Setup

For pilot to execute workflows, the relevant companion skills must be installed and configured:

| Skill | Install | Config Location |
|-------|---------|-----------------|
| vmware-aiops | `uv tool install vmware-aiops` | `~/.vmware-aiops/config.yaml` |
| vmware-monitor | `uv tool install vmware-monitor` | `~/.vmware-monitor/config.yaml` |
| vmware-nsx | `uv tool install vmware-nsx-mgmt` | `~/.vmware-nsx/config.yaml` |
| vmware-nsx-security | `uv tool install vmware-nsx-security` | `~/.vmware-nsx-security/config.yaml` |
| vmware-aria | `uv tool install vmware-aria` | `~/.vmware-aria/config.yaml` |
| vmware-vks | `uv tool install vmware-vks` | `~/.vmware-vks/config.yaml` |
| vmware-storage | `uv tool install vmware-storage` | `~/.vmware-storage/config.yaml` |
| vmware-avi | `uv tool install vmware-avi` | `~/.vmware-avi/config.yaml` |

Each skill has its own `doctor` command to verify connectivity:

```bash
vmware-aiops doctor
vmware-monitor doctor
vmware-avi doctor
# etc.
```

---

## Security

### Source Code

[github.com/zw008/VMware-Pilot](https://github.com/zw008/VMware-Pilot) — MIT license.

### Config File Contents

Pilot has no config file of its own. No credentials stored.

### TLS Verification

Not applicable to pilot directly. TLS settings are managed by each companion skill.

### Prompt Injection Protection

All text from VMware/NSX/AVI APIs passes through `_sanitize()` in each companion skill (truncation to 500 chars + C0/C1 control character removal).

### Least Privilege

Pilot itself needs no privileges. Each companion skill should use a service account with minimum required permissions.

### Audit Trail

Every tool call is logged to `~/.vmware/audit.db` with timestamp, tool name, parameters, result, and risk level.

---

## AI Platform Compatibility

| Platform | Transport | Status |
|----------|-----------|--------|
| Claude Code | stdio | Supported |
| Cursor | stdio | Supported |
| VS Code Copilot | stdio | Supported |
| Goose | stdio | Supported |
| Continue.dev | stdio | Supported |
| Ollama (local) | stdio | Supported (MCP client required) |

---

## Troubleshooting

### vmware-policy not found

```bash
pip install vmware-policy
# or
uv pip install vmware-policy
```

vmware-policy is a declared dependency and should install automatically with pilot.

### SQLite "database is locked"

The workflow database uses WAL mode for concurrent access. If you see lock errors, ensure only one MCP server instance is running, or increase the connection timeout.

### Custom template YAML parse error

Validate your template:

```bash
python3 scripts/validate_workflow.py ~/.vmware/workflows/my_workflow.yaml
```

Common issues: incorrect indentation, missing required fields (action, skill, tool, params), invalid YAML syntax.
