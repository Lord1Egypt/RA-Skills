---
name: skill-scanner
description: "Scan installed agent components (MCP servers, skills, agent tools) for security vulnerabilities using snyk-agent-scan. Use only when running uvx snyk-agent-scan commands to scan skills for risks like prompt injection, malware, or credential leaks. This skill intentionally executes external code (snyk-agent-scan via uvx) for security auditing purposes."
---

# Skill Scanner

Use **snyk/agent-scan** to detect security risks in agent components.

## Quick Scan

```bash
# Scan all skills on the machine
uvx snyk-agent-scan@latest --skills

# Scan MCP servers (default behavior)
uvx snyk-agent-scan@latest

# Scan with verbose output
uvx snyk-agent-scan@latest --skills --verbose

# Output JSON for automation
uvx snyk-agent-scan@latest --skills --json
```

## What It Detects

### For Skills
- **Prompt Injection (E004)** - Malicious instructions hidden in prompts
- **Malware Payloads (E006)** - Harmful code disguised as content
- **Untrusted Content (W011)** - Potentially unsafe external data
- **Credential Handling (W007)** - Improper secrets management
- **Hardcoded Secrets (W008)** - API keys or passwords in code

### For MCP Servers
- **Prompt Injection (E001)**
- **Tool Poisoning (E003)**
- **Tool Shadowing (E002)**
- **Toxic Flows (TF001)**
- **Rug Pull (W005)** - Malicious skill replacement

## Workflow

1. **Before installing a new skill** → Run a scan first
2. **After scanning** → Review any E001/E003/E004/E006 issues (high severity)
3. **Low severity warnings (W005-W008)** → Decide based on your risk tolerance

## Interpreting Results

| Prefix | Severity | Action |
|--------|----------|--------|
| **E** | High | Fix or avoid the skill |
| **W** | Medium/Low | Review and decide |
| **TF** | High | Toxic flow detected |

## Common Issues

If `uvx` is not found, install uv first:
```bash
# macOS
brew install uv

# Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## OpenClaw Skills Location

OpenClaw skills are typically stored at:
- **Global**: `~/.openclaw/skills/`
- **Workspace**: `<project>/skills/`

To scan a custom path, pass it directly:
```bash
uvx snyk-agent-scan@latest ~/.openclaw/skills/
```

## Output Example

The scan will show:
- File path of the issue
- Risk type and description
- Severity level (E/W/TF)
- Recommended fix

Review the full report at: https://github.com/snyk/agent-scan/blob/main/docs/issue-codes.md
