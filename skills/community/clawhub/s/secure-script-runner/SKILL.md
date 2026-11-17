---
spec: usk/3.0
id: secure_script_runner
version: 1.1.1
name: Secure Script Runner (Zero‑Exposure Sandbox)
description: Zero‑exposure script execution using MGC Blackbox. Store scripts encrypted, execute in blackbox, AI sees no plaintext. Supports MCP (mgc_run) / API / WebUI execution, internal credential calls, and script sealing. Includes MGC 1.4.9 temporary workaround guidelines. This skill only executes scripts with explicit user authorization and will never automatically execute any scripts.
author: MirginCipher Team
license: MIT
tags: security, script, zero-exposure, mgc, sandbox, execution, blackbox
platform_compatibility: windows, macos, linux
changelog:
  - version: 1.1.1
    changes:
      - Added MGC 1.4.9 temporary workaround section (parse_known_args / _strip_quotes / file output)
      - Added ext02 parameter format recommendations (forward-slash paths, T separator for spaces)
      - Provided complete script template
      - Noted that known issues will be fixed in a future release
  - version: 1.1.0
    changes:
      - Core flow upgrade: Uses mgc_run for blackbox script execution (no script exposure to AI)
      - Removed mgc_get(action="run") as recommended method
      - Added ext02 parameter passing specification
      - Adapted to MGC 1.4.9 sandbox mode
  - version: 1.0.1
    changes:
      - Security hardening update: added security warnings, permission boundaries, script source review checklist
      - Removed dangerous security claims
      - Added authorization requirements
  - version: 1.0.0
    changes:
      - Initial release with zero‑exposure script execution
---

# Overview

Secure Script Runner is a documentation skill that teaches how to execute scripts with **zero plaintext exposure** using MGC Blackbox.

This skill enables:
- Store scripts encrypted in local MGC
- **Execute scripts in blackbox** (AI sees results only, no stdout)
- Multiple execution modes: MCP (`mgc_run`, recommended), API, WebUI
- Scripts can call internal MGC credentials
- Script sealing for cross‑node delegation

This skill **only provides documentation**, but involves script execution, which requires manual human approval.

---

# What This Skill Enables

After reading this documentation, an AI agent will understand how to:

- Store scripts securely in MGC Blackbox
- Execute scripts via MCP (AI), API (script), or WebUI (human)
- Pass runtime parameters to scripts via `ext02`
- Call MGC internal credentials from scripts
- Seal scripts using node public key
- Build zero‑exposure workflows

---

# Prerequisites

1. **Install MGC Blackbox**: `pip install mgc-blackbox>=1.4.9`
2. **Start MGC service**: `mgc` (WebUI: http://127.0.0.1:57218, API: http://127.0.0.1:57219)
3. **MCP tools available**: `mgc_save`, `mgc_run`, `mgc_list`, `mgc_seal`, `mgc_open_webui`
4. **Token file**: `~/.mgc/database/mgc_black_box/.mgc_token`

> **Important:** For AI agents, use **MCP tools**. `mgc_run` is the preferred tool for executing scripts as it provides true zero‑exposure.

> **Sandbox mode (Trae Work / Workbuddy):** MGC 1.4.9 introduced sandbox mode. In this mode, scripts executed via `mgc_run` run in an isolated environment, further enhancing security. The AI can call `mgc_open_webui` to guide the user to view the status.

---

# Zero‑Exposure Execution

## Core Concept

```
Script (plaintext) → MGC Encryption → Encrypted Storage
                                              ↓
                              Blackbox Execution (MGC)
                                              ↓
                              AI receives result only
```

AI executes but **never sees script plaintext** or standard output.

---

## Three Execution Modes

| Mode | Interface | Use Case |
|------|-----------|----------|
| **MCP (Recommended)** | `mgc_run` | AI agents (blackbox, zero‑exposure) |
| **REST API** | `/api/mgc/sensitive/run` | System scripts |
| **WebUI** | http://127.0.0.1:57218 | Human operators |

> **Note:** `mgc_get(action="run")` is still available, but `mgc_run` is recommended as it is explicitly designed for execution and does not expose the process.

---

# Storing Scripts

## Step 1: Prepare Script

Store a script with execution metadata:

```python
# Via MCP tool
mgc_save(
    info_type="script",
    info_owner="my_script",
    ext01="python",           # Startup command (e.g., python, python3)
    ext02="",                 # Default runtime args (optional)
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

## Mode 1: Via MCP (AI) - Recommended

Execute using the `mgc_run` tool:

```python
# Basic execution
result = mgc_run(
    info_owner="my_script"
)

# Execution with parameters (via ext02)
import json
params = {"arg1": "value1", "arg2": "value2"}
result = mgc_run(
    info_owner="my_script",
    ext02=json.dumps(params)  # Must be a JSON string
)
# AI receives execution result only
```

> **ext02 Parameter Specification:**
> - `ext02` is used to pass runtime parameters to the script.
> - It **must** be converted to a JSON string using `json.dumps()`.
> - Failure to do so may cause MCP serialization errors (HTTP 422).
> - The script can read these parameters from environment variables or standard input.

## Mode 2: Via REST API (Script)

```bash
# Execute script
curl -X POST http://127.0.0.1:57219/api/mgc/sensitive/run \
  -H "Content-Type: application/json" \
  -H "X-MGC-Token: $(cat ~/.mgc/database/mgc_black_box/.mgc_token)" \
  -d '{
    "info_type": "script",
    "info_owner": "my_script",
    "ext02": "{\"arg1\": \"value1\"}"
  }'
```

## Mode 3: Via WebUI (Human)

1. Open WebUI: http://127.0.0.1:57218
2. Navigate to Skill page
3. Find your script
4. Click "Run" button

---

# ⚠️ MGC 1.4.9 Temporary Workaround (Script Execution Guidelines)

> **Important:** MGC 1.4.9 has known engineering defects in script execution that may cause scripts to silently fail or produce no output. Please strictly follow these scripting guidelines. The MGC team will fix these issues in a future release.

## Three Mandatory Scripting Rules

### Rule 1: Use `parse_known_args` instead of `parse_args`

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--output_dir')
parser.add_argument('--content')
parser.add_argument('--filename')

# ❌ Wrong: parse_args() exits on unknown parameters
# args = parser.parse_args()

# ✅ Correct: parse_known_args() ignores extra parameters
args, unknown = parser.parse_known_args()
```

### Rule 2: Manually Strip Quotes Added by MGC

```python
def _strip_quotes(v):
    """Remove quotes added by MGC's ext02 parameter passing"""
    if isinstance(v, str) and len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
        return v[1:-1]
    return v

# Apply to all fields that may contain paths or content
args.output_dir = _strip_quotes(args.output_dir)
args.content = _strip_quotes(args.content)
```

### Rule 3: Write to Files, Avoid Excessive print()

```python
# ❌ Wrong: print() output exceeding 4KB causes PIPE blocking
# print(f"Processing completed, result: {result}")

# ✅ Correct: Write results to a file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"Processing completed\n")
    f.write(f"Result: {result}\n")
```

## ext02 Parameter Format Recommendations

| Rule | Recommended | Avoid |
|------|-------------|-------|
| **Path separator** | ✅ Forward slash `/` (`D:/path`) | ❌ Backslash `\` (`D:\path`) |
| **Parameters with spaces** | ✅ Use `T` to separate (`2026-07-28T00:00:00`) | ❌ Use spaces directly |
| **Parameter structure** | ✅ `--key "value"` explicitly named | ❌ Positional arguments |

## Complete Script Template

```python
import argparse
import os
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='MGC Script Template')
    parser.add_argument('--content', default='Default content')
    parser.add_argument('--output_dir', default=os.path.expanduser("~/Desktop"))
    parser.add_argument('--filename', default=None)

    # Rule 1: Use parse_known_args
    args, unknown = parser.parse_known_args()

    # Rule 2: Strip quotes
    def _strip_quotes(v):
        if isinstance(v, str) and len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
            return v[1:-1]
        return v
    args.content = _strip_quotes(args.content)
    args.output_dir = _strip_quotes(args.output_dir)
    args.filename = _strip_quotes(args.filename)

    # Business logic
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    filename = args.filename or f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    output_file = os.path.join(args.output_dir, filename)

    # Rule 3: Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"content={args.content}\n")
        f.write(f"output_dir={args.output_dir}\n")

    # Return execution result (concise)
    print(f"SUCCESS:{output_file}")

if __name__ == "__main__":
    main()
```

> **Note:** These guidelines are temporary workarounds for MGC 1.4.9. The MGC team will fix `ext02` parameter parsing and `stdout` blocking issues in a future release, at which point these workarounds can be removed.

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

> **Note:** Credentials are retrieved locally, script executes in blackbox, AI never sees plaintext.

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

## mgc_save (Store Script)

**Arguments:**
```json
{
  "info_type": "script",
  "info_owner": "unique identifier",
  "ext01": "startup command (python, node, etc.)",
  "ext02": "default runtime arguments (optional)",
  "content": "script plaintext"
}
```

## mgc_run (Execute Script - Recommended)

**Arguments:**
```json
{
  "info_owner": "script identifier",
  "ext02": "runtime parameters (JSON string, optional)"
}
```

**Returns:** Script execution result

## mgc_list (List Scripts)

**Arguments:**
```json
{
  "info_type": "script"
}
```

**Returns:** List of scripts (no plaintext)

## mgc_seal (Seal Script)

**Arguments:**
```json
{
  "info_type": "script",
  "info_owner": "script identifier",
  "ext04": "target node RSA public key"
}
```

**Returns:** Sealed script (encrypted with target node key)

## mgc_open_webui (Open WebUI)

**Purpose:** Opens the MGC WebUI in the browser for user to view or manually operate.

---

# Security Notes

1. **Zero‑exposure**: Script executes in blackbox, AI receives result only (unless user actively exposes)
2. **Encrypted storage**: All scripts encrypted at rest
3. **No plaintext leakage**: AI default does not see script content or stdout
4. **Script sealing**: Cross‑node scripts stay encrypted

---

# ⚠️ Security Warnings

> **Please read the following warnings carefully**

1. **Do not execute untrusted scripts**: Only execute scripts from trusted sources
2. **AI cannot review script content**: AI cannot audit code security when executing scripts
3. **Scripts may access local credentials**: Scripts can call MGC credentials, ensure script purpose is verified
4. **User must manually confirm script source**: Must verify script provider and purpose before execution
5. **User must bear execution risk**: Execution results are user's responsibility
6. **Every execution requires manual approval**: AI will not execute automatically, explicit user authorization required

---

# Permission Boundaries

1. Scripts can only access local environment
2. Will not access remote resources (unless script itself contains remote calls)
3. Will not execute automatically
4. Will not call credentials automatically
5. All sensitive operations must be triggered by user

---

# Script Source Review Checklist

> **Before executing scripts, user must confirm the following:**

- [ ] Confirm script source is trusted
- [ ] Confirm script purpose is clear
- [ ] Confirm script will not access sensitive data (unless needed)
- [ ] Confirm script will not execute dangerous commands (e.g., disk format)
- [ ] User must manually approve execution

---

# Links

- **Main Repository**: https://github.com/zkeviny/MGC-Blackbox
- **Issues**: https://github.com/zkeviny/MGC-Blackbox/issues
- **Contact**: mirgincipher@outlook.com