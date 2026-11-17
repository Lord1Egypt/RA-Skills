# Zero-Exposure SMTP Mail Sender

Send emails securely without exposing SMTP passwords using MGC Blackbox 1.4.10.

> **This skill only executes scripts with explicit user authorization.**

---

## What's New in v2.1.1

- **Upgraded to MGC 1.4.10**: install `mgc-blackbox>=1.4.10`
- **`mgc_run` blackbox execution** (1.4.7+) replaces `mgc_get(action="run")`
- **`ext02` contract**: MUST be a JSON array string (not dict-style JSON object)
- **`diff_1` required** in all `mgc_run` calls (schema-required differentiation field)
- **`update_if_exists=true`** for credential/script rotation
- **`mgc_find` fuzzy search** (1.4.10) for locating scripts/credentials
- **Privacy mode enhanced**: AI can send emails without ever seeing the body
- **`argparse` + `parse_known_args`** in `example.py` (1.4.10 ext02 auto-parse)

---

## What This Skill Does

This is a documentation skill that teaches how to send emails securely:

1. **User stores SMTP credentials** via MGC WebUI (AI never sees)
2. **User stores email script** via WebUI or `mgc_save` (AI can assist)
3. **(Optional) User stores email content** via WebUI for full privacy
4. **AI executes script** via `mgc_run` (AI only sees `{pid, status}` + result file)

---

## Prerequisites

- Python 3.10+
- `pip install mgc-blackbox>=1.4.10`
- MGC service running: `mgc` (API at http://127.0.0.1:57219, WebUI at 57218)

---

## Quick Start

### Step 1: Store Credentials (via WebUI)

Open http://127.0.0.1:57218 and save:

```
info_type: "config"
info_owner: "smtp_gmail"
content: {"address": "you@gmail.com", "password": "...", "smtp_server": "smtp.gmail.com", "smtp_port": 587}
```

### Step 2: Store Email Script (via mgc_save)

```python
mgc_save(
    info_type="script",
    info_owner="send_email",
    ext01="python",
    content="<paste example.py here>",
    update_if_exists=True
)
# MGC 1.4.10 auto-fills ext02 from argparse literal defaults
```

### Step 3: AI Sends Email (via mgc_run)

```python
import json
result = mgc_run(
    info_type="script",
    info_owner="send_email",
    diff_1="send_email",
    ext02=json.dumps([
        "--to", "to@example.com",
        "--subject", "Test",
        "--body", "Hello",
    ])
)
# Returns: {"pid": 12345, "status": "started"}
```

---

## Security

- AI never sees SMTP credentials
- AI never sees script content
- AI never sees email body when stored in MGC (privacy mode)
- AI can assist with script writing (user stores it)
- User must approve each send
- Strict 1.4.10 contracts enforced (JSON array ext02, diff_1 required, update_if_exists for overwrite)

---

## MCP Tools

| Tool | Purpose |
|------|---------|
| `mgc_save` | Store credentials / scripts (`update_if_exists=true` to overwrite) |
| `mgc_run` | Blackbox script execution (1.4.7+, ext02 = JSON array string, diff_1 required) |
| `mgc_list` | List stored entries (exact match) |
| `mgc_find` | Fuzzy search by `info_owner` (1.4.10 new) |
| `mgc_open_webui` | Open WebUI for user to manage entries |

> ❌ AI must NOT call `mgc_get` — deprecated for AI-driven script execution.

---

## Sandbox Mode (1.4.9+)

If running inside a sandbox Agent (Trae Work / Workbuddy), install MGC in the system environment; otherwise MCP operations may be limited. In that case, call FastAPI directly at `/api/mgc/sensitive/run`.

---

## License

MIT