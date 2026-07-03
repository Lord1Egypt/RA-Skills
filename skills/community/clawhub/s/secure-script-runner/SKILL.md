---
spec: usk/3.0
id: secure_script_runner
version: 1.0.0
name: Secure Script Runner (Zero‑Exposure Sandbox)
description: Zero‑exposure script execution using MGC Blackbox. Store scripts encrypted, execute locally, AI never sees plaintext. Supports MCP/API/WebUI execution, internal credential calls, and script sealing.
author: MirginCipher Team
license: MIT
tags: security, script, zero-exposure, mgc, sandbox, execution
platform_compatibility: windows, macos, linux
changelog:
  - version: 1.0.0
    changes:
      - Initial release with zero‑exposure script execution
---

# Overview

Secure Script Runner is a documentation skill that teaches how to execute scripts with **zero plaintext exposure** using MGC Blackbox.

This skill enables:
- Store scripts encrypted in local MGC
- Execute scripts locally (AI sees results only)
- Three execution modes: MCP, API, WebUI
- Scripts can call internal MGC credentials
- Script sealing for cross‑node delegation

This skill contains **no executable code** and is safe for automatic approval.

---

# What This Skill Enables

After reading this documentation, an AI agent will understand how to:

- Store scripts securely in MGC Blackbox
- Execute scripts via MCP (AI), API (script), or WebUI (human)
- Call MGC internal credentials from scripts
- Seal scripts using node public key
- Build zero‑exposure workflows

---

# Prerequisites

1. **Install MGC Blackbox**: `pip install mgc-blackbox`
2. **Start MGC service**: `mgc` (runs at http://127.0.0.1:57219)
3. **MCP tools available**: Use `mgc_save`, `mgc_get`, `mgc_seal`
4. **Token file**: `~/.mgc/database/mgc_black_box/.mgc_token`

> **Important:** For AI agents, use **MCP tools**. CLI may have port conflicts in some environments.

---

# Zero‑Exposure Execution

## Core Concept

```
Script (plaintext) → MGC Encryption → Encrypted Storage
                                              ↓
                              Local Execution (MGC)
                                              ↓
                              AI receives result only
```

AI executes but **never sees script plaintext**.

---

## Three Execution Modes

| Mode | Interface | Use Case |
|------|-----------|----------|
| **MCP** | mgc_get | AI agents |
| **REST API** | /api/mgc/sensitive/get | System scripts |
| **WebUI** | http://127.0.0.1:57218 | Human operators |

---

# Storing Scripts

## Step 1: Prepare Script

Store a script with execution metadata:

```python
# Via MCP tool
mgc_save(
    info_type="script",
    info_owner="my_script",
    ext01="python",           # Startup command
    ext02="script.py arg1",  # Default runtime args
    content="print('Hello from zero‑exposure!')"
)
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| info_type | Yes | Must be "script" |
| info_owner | Yes | Unique script identifier |
| ext01 | Yes | Startup command (python, node, etc.) |
| ext02 | No | Default runtime arguments |
| content | Yes | Script plaintext (encrypted at rest) |

---

# Executing Scripts

## Mode 1: Via MCP (AI)

```python
# Execute via MCP tool
result = mgc_get(
    info_type="script",
    info_owner="my_script",
    action="run"
)
# AI receives execution result only
```

## Mode 2: Via REST API (Script)

```bash
curl -X POST http://127.0.0.1:57219/api/mgc/sensitive/get \
  -H "Content-Type: application/json" \
  -H "X-MGC-Token: $(cat ~/.mgc/database/mgc_black_box/.mgc_token)" \
  -d '{
    "info_type": "script",
    "info_owner": "my_script",
    "action": "run"
  }'
```

## Mode 3: Via WebUI (Human)

1. Open WebUI: http://127.0.0.1:57218
2. Navigate to Get page
3. Find your script
4. Click "Run" button

---

# Calling MGC Credentials

Scripts can call MGC internal credentials using the internal API:

```python
# Example: Call MGC credential from script
import urllib.request
import json

def get_mgc_credential(info_type, info_owner):
    data = json.dumps({
        "info_type": info_type,
        "info_owner": info_owner
    }).encode("utf-8")

    req = urllib.request.Request(
        "http://127.0.0.1:57219/api/mgc/sensitive/get",
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-MGC-Token": open("/path/to/token").read()
        },
        method="POST"
    )

    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())["data"]
```

> **Note:** Credentials are retrieved locally, script executes locally, AI never sees plaintext.

---

# Script Sealing (Advanced)

For cross‑node delegation, scripts can be sealed using the node's public key:

## Step 1: Get Node Public Key

```python
# Via MCP tool
node_pub = mgc_get(
    info_type="__NODE_PUB__",
    info_owner="__NODE_PUB__"
)
```

## Step 2: Seal Script

```python
# Via MCP tool
sealed = mgc_seal(
    info_type="script",
    info_owner="my_script",
    ext04=node_pub  # Target node public key
)
```

## Step 3: Store Sealed Script

```python
# Store sealed version
mgc_save(
    info_type="script",
    info_owner="my_script_sealed",
    ext01="python",
    content=sealed
)
```

Sealed scripts are encrypted and can only be executed by the target node.

---

# MCP Tools Reference

## mgc_save

**Arguments:**
```json
{
  "info_type": "script",
  "info_owner": "unique identifier",
  "ext01": "startup command (python, node, etc.)",
  "ext02": "default runtime arguments",
  "content": "script plaintext"
}
```

## mgc_get

**Arguments:**
```json
{
  "info_type": "script",
  "info_owner": "script identifier",
  "action": "get | run"
}
```

**Returns:** Script content or execution result

## mgc_seal

**Arguments:**
```json
{
  "info_type": "script",
  "info_owner": "script identifier",
  "ext04": "target node RSA public key"
}
```

**Returns:** Sealed script (encrypted with target node key)

---

# Security Notes

1. **Zero‑exposure**: Script executes locally, AI receives result only
2. **Encrypted storage**: All scripts encrypted at rest
3. **No plaintext leakage**: AI never sees script content
4. **Script sealing**: Cross‑node scripts stay encrypted

---

# Links

- **Main Repository**: https://github.com/zkeviny/MGC-Blackbox
- **Issues**: https://github.com/zkeviny/MGC-Blackbox/issues
- **Contact**: mirgincipher@outlook.com