---
name: REFINE_Project
description: >
  REFINE is an adaptive skill engine for structured session diagnostics.
  Use this skill when a user explicitly requests: logging error patterns
  across sessions, maintaining session memory, generating System Prompt
  Patches from failure analysis, or structured feedback capture on ClawHub
  or SkillPay. Activate for requests about "error logging", "session memory",
  "patch synthesis", or "adaptive skill logging". Do not activate for
  general conversation or unrelated tasks.
license: MIT-0
compatibility:
  python: ">=3.10"
metadata:
  environment_variables:
    - name: REFINE_MODE
      required: false
      default: BASIC
      values: ["BASIC", "PRO"]
      description: >
        Controls operating mode. Defaults to BASIC if not set.
        Set to PRO only when SKILLPAY_TOKEN_HASH is also configured.
    - name: SKILLPAY_TOKEN_HASH
      required: false
      default: ""
      secret: true
      description: >
        SHA-256 hex digest of the SkillPay auth token.
        Only needed when REFINE_MODE=PRO. Set the hash, never the raw token.
    - name: LOG_LEVEL
      required: false
      default: INFO
      values: ["DEBUG", "INFO", "WARNING", "ERROR"]
  data_storage:
    file: refine_memory.json
    scope: local_disk_only
    network_calls: none
    stack_traces: never_stored
    context_sanitization: enforced_by_code
---

# REFINE — Adaptive Session Diagnostics

A dual-mode skill engine. Captures error patterns and feedback labels locally,
then (in PRO mode) synthesises System Prompt Patches from local failure analysis.

All data stays on local disk (`refine_memory.json`). No network calls are made.

---

## What Gets Stored — Complete List

All caller-supplied data passes through sanitization before reaching disk.

| Source | Field | Sanitization applied |
|---|---|---|
| `capture_feedback(feedback)` | `feedback` | Truncated to 300 chars |
| `capture_feedback(context)` | `context` | See Context Sanitization below |
| `log_error(error)` | `type` | Exception class name only |
| `log_error(error)` | `message` | First line only, truncated 300 chars |
| `log_error(context)` | `context` | See Context Sanitization below |
| Stack traces | — | **Never stored** |
| Raw prompts | — | **Never stored** |

### Context Sanitization — Enforced by Code

The `context` dict argument in both `capture_feedback()` and `log_error()`
is passed through `_sanitize_context()` before any write. This function:

1. **Blocks sensitive key names** — keys matching `token`, `key`, `secret`,
   `password`, `auth`, `api_key`, `bearer`, `credential`, `private`, `seed`,
   `hash`, `pin`, `ssn`, `credit`, `card`, `cvv` → stored as
   `[REDACTED — sensitive key name]`
2. **Rejects nested objects** — any `dict` or `list` value →
   `[REMOVED — nested dict/list not stored]`
3. **Truncates strings** — all string values capped at 200 chars
4. **Limits keys** — maximum 8 keys per context dict
5. **Scalar types only** — `str`, `int`, `float`, `bool` permitted;
   all other types → `[REMOVED — unsupported type]`

This is a **code-level enforcement** — it applies regardless of warnings
in documentation. Sensitive data cannot reach the JSON file.

---

## Mode Selection

`REFINE_MODE` is optional — defaults to `BASIC` if not set.

| `REFINE_MODE` | Platform | Tier | Auth required |
|---|---|---|---|
| `BASIC` (default) | ClawHub | Free | None |
| `PRO` | SkillPay | Paid | `SKILLPAY_TOKEN_HASH` + header |

```bash
# BASIC — no configuration needed
python main.py

# PRO — set both variables
export REFINE_MODE=PRO
export SKILLPAY_TOKEN_HASH=$(echo -n "your-token" | sha256sum | cut -d' ' -f1)
```

---

## BASIC Mode

```python
from main import build_engine

engine = build_engine()

# Safe: short diagnostic labels only
engine.capture_feedback("verbosity-high", context={"prompt_id": "p001"})

# Context is sanitized — api_key below will be stored as [REDACTED]
engine.capture_feedback("test", context={"api_key": "sk-..."})   # → [REDACTED]

try:
    risky_operation()
except Exception as exc:
    engine.log_error(exc, {"endpoint": "/api/v1"})   # context sanitized

history = engine.get_history(limit=10)
engine.close()
```

---

## PRO Mode

```python
import os
from main import build_engine, SKILLPAY_HDR

token   = your_secret_manager.get("skillpay-token")
headers = {SKILLPAY_HDR: token}

engine = build_engine(auth_headers=headers)

report = engine.evolve()   # analyse local errors → synthesise patch
patch  = engine.get_latest_patch()
if patch:
    next_system_prompt = patch["patch_body"] + "\n\n" + base_system_prompt

engine.close()
```

---

## Security

| Concern | Implementation |
|---|---|
| Token comparison | `hmac.compare_digest` — stdlib `hmac`, constant-time |
| Token in logs | Never — 8-char hash prefix only |
| Token storage | `SKILLPAY_TOKEN_HASH` env var only |
| Context dicts | Sanitized by `_sanitize_context()` before any disk write |
| Sensitive keys | Blocked by regex — stored as `[REDACTED]` |
| Nested objects | Rejected — stored as `[REMOVED]` |
| String values | Truncated to 200 chars in context, 300 chars elsewhere |
| Stack traces | Never stored |
| Network calls | None — fully offline |
| File writes | Atomic temp-file rename |

---

## Environment Variables

All optional:

| Variable | Default | Description |
|---|---|---|
| `REFINE_MODE` | `BASIC` | `BASIC` or `PRO` |
| `SKILLPAY_TOKEN_HASH` | (none) | SHA-256 hex of token; PRO only |
| `LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |
