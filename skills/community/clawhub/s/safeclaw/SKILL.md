---
name: safeclaw
description: Security compliance checker for MCP/LLM applications. Performs non-invasive security assessments on configuration files.
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: [uv, python3]
      env: []
      config: []
    os: [darwin, linux]
---

# SafeClaw Security Checker

Perform security compliance checks on MCP/LLM application configurations.

## Usage

When the user invokes this skill, run security checks on their configuration.

### Basic Command

```bash
cd {baseDir}/../../ && uv run python main.py check --config "<config_path>" --format json
```

### Arguments

- `config_path`: Path to the configuration file to check (JSON/YAML/TOML)
- If no path provided, use `--auto` to auto-discover config:
  ```bash
  cd {baseDir}/../../ && uv run python main.py check --auto --format json
  ```

## Execution Flow

1. **Determine config path**:
   - If user provides a path, use it
   - If user wants auto-discovery, use `--auto`
   - If unsure, ask the user

2. **Run the check**:
   ```bash
   cd {baseDir}/../../ && uv run python main.py check --config "<path>" --format json
   ```

3. **Parse JSON output**: The output has this structure:
   ```json
   {
     "summary": {
       "overall_status": "安全|注意|高危",
       "total": 10,
       "passed": 7,
       "failed": 3,
       "by_level": {"safe": 7, "attention": 2, "high_risk": 1}
     },
     "failed_results": [
       {
         "name": "检查项名称",
         "category": "安全类别",
         "level": "高危|注意",
         "message": "问题描述",
         "risk_description": "风险说明",
         "remediation": "整改建议",
         "fix_commands": ["command to fix"]
       }
     ]
   }
   ```

4. **Report findings**:
   - Show summary: X passed, Y attention items, Z high-risk
   - List high-risk items FIRST with remediation steps
   - List attention items with suggestions
   - If all passed, congratulate the user

## Exit Codes

- `0`: All checks passed (safe)
- `1`: Attention items found
- `2`: High-risk items found

## Example Config

Use `{baseDir}/example-config.json` as a reference template for users who need a starting point.

## Categories Checked

| Category | Description |
|----------|-------------|
| 配置与密钥 | Secrets in config, hardcoded credentials |
| 权限 | File permissions, access controls |
| 网络暴露 | Network bindings, CORS, exposed ports |
| 插件安全 | MCP server security, plugin sources |
| 日志与审计 | Logging configuration, audit trails |
| 版本信息 | Version exposure, update status |
| OpenClaw安全 | OpenClaw-specific deployment security |

## Example Invocation

User: "/safeclaw check my config at ./config/mcp.json"

Response:
1. Run: `cd {baseDir}/../../ && uv run python main.py check --config "./config/mcp.json" --format json`
2. Parse results and present findings in a clear, actionable format

## Tips

- Always use `--format json` for machine-readable output
- The skill runs from the skill directory, so use `{baseDir}/../../` to reach project root
- If the config file doesn't exist, suggest using the template at `{baseDir}/templates/minimal-config.json`
