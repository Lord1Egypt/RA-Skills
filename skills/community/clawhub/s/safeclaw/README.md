# SafeClaw Skill

A security compliance checker skill for OpenClaw that performs non-invasive security assessments on MCP/LLM application configurations.

## Overview

SafeClaw analyzes configuration files for common security issues in MCP (Model Context Protocol) and LLM applications. It checks for:

- **Configuration & Secrets**: Hardcoded credentials, exposed API keys
- **Permissions**: File access controls, privilege settings
- **Network Exposure**: Open ports, CORS misconfigurations
- **Plugin Security**: Unverified MCP servers, untrusted sources
- **Logging & Audit**: Missing audit trails, insufficient logging
- **Version Information**: Outdated components, exposed version info
- **OpenClaw-specific**: Deployment isolation, firewall settings

## Usage

### Basic Check

```bash
/safeclaw --config ./path/to/config.json
```

### Auto-discovery

```bash
/safeclaw --auto
```

SafeClaw will search for configuration files in standard locations.

## Configuration File Formats

SafeClaw supports multiple configuration formats:

- **JSON**: `.json` files
- **YAML**: `.yaml` or `.yml` files
- **TOML**: `.toml` files

## Example Configuration

See `example-config.json` for a complete example or `templates/minimal-config.json` for a minimal starting point.

### Minimal Configuration

```json
{
  "server": {
    "host": "127.0.0.1",
    "port": 8080
  },
  "mcpServers": {},
  "auth": {
    "enabled": true
  }
}
```

## Understanding Results

SafeClaw uses three compliance levels:

| Level | Description | Action |
|-------|-------------|--------|
| ✅ 安全 (Safe) | No security concerns | None required |
| ⚠️ 注意 (Attention) | Issues that should be addressed | Review and fix when possible |
| 🚨 高危 (High Risk) | Critical security issues | Fix immediately |

## Exit Codes

When used in scripts or CI/CD:

- `0`: All checks passed
- `1`: Attention items found
- `2`: High-risk items found

## Requirements

- Python 3.12+
- uv package manager

## Files

```
skills/safeclaw/
├── SKILL.md              # Skill definition (invoked by OpenClaw)
├── README.md             # This file
├── example-config.json   # Full example configuration
└── templates/
    └── minimal-config.json  # Minimal template to get started
```

## Related

- [SafeClaw Main Documentation](../../README.md)
- [CLAUDE.md](../../CLAUDE.md) - Development guidelines
