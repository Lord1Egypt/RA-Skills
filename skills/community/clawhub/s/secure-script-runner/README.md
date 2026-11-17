# Secure Script Runner (Zero‑Exposure Sandbox)

A documentation skill for **zero‑exposure script execution** using MGC Blackbox.

> **This skill only executes scripts with explicit user authorization and will never automatically execute any scripts.**

## What This Skill Is

Secure Script Runner teaches how to:
- Store scripts encrypted in MGC Blackbox
- Execute scripts locally (AI sees results only)
- Use three execution modes: MCP, API, WebUI
- Call MGC internal credentials from scripts
- Seal scripts for cross‑node delegation

## Prerequisites

- Python 3.10+
- Install: `pip install mgc-blackbox`
- Start MGC: `mgc` (runs at http://127.0.0.1:57219)

## Quick Start

### 1. Store a Script

```python
# Via MCP tool
mgc_save(
    info_type="script",
    info_owner="my_script",
    ext01="python",
    content="print('Hello from zero‑exposure!')"
)
```

### 2. Execute via MCP (AI)

```python
result = mgc_get(
    info_type="script",
    info_owner="my_script",
    action="run"
)
# AI receives execution result only
```

### 3. Execute via WebUI (Human)

1. Open: http://127.0.0.1:57218
2. Find your script
3. Click "Run"

## Three Execution Modes

| Mode | Interface | Use Case |
|------|-----------|----------|
| MCP | mgc_get | AI agents |
| REST API | /api/mgc/sensitive/get | System scripts |
| WebUI | http://127.0.0.1:57218 | Human operators |

## ⚠️ Security Warnings

> **Please read the following warnings carefully**

1. **Do not execute untrusted scripts**: Only execute scripts from trusted sources
2. **AI cannot review script content**: AI cannot audit code security when executing scripts
3. **Scripts may access local credentials**: Scripts can call MGC credentials, ensure script purpose is verified
4. **User must manually confirm script source**: Must verify script provider and purpose before execution
5. **User must bear execution risk**: Execution results are user's responsibility
6. **Every execution requires manual approval**: AI will not execute automatically, explicit user authorization required

## Permission Boundaries

- Scripts can only access local environment
- Will not access remote resources (unless script itself contains remote calls)
- Will not execute automatically
- Will not call credentials automatically
- All sensitive operations must be triggered by user

## Script Source Review Checklist

> **Before executing scripts, user must confirm the following:**

- [ ] Confirm script source is trusted
- [ ] Confirm script purpose is clear
- [ ] Confirm script will not access sensitive data (unless needed)
- [ ] Confirm script will not execute dangerous commands (e.g., disk format)
- [ ] User must manually approve execution

## MCP Tools

| Tool | Description |
|------|-------------|
| mgc_save | Store scripts encrypted |
| mgc_get | Retrieve or execute scripts |
| mgc_seal | Seal script for delegation |
| mgc_list | List stored scripts |
| mgc_open_webui | Open WebUI |

## Supported Platforms

- Windows
- macOS
- Linux

## Links

- **Main Repo**: https://github.com/zkeviny/MGC-Blackbox
- **Issues**: https://github.com/zkeviny/MGC-Blackbox/issues
- **Contact**: mirgincipher@outlook.com