---

spec: usk/3.0
id: zero_exposure_smtp_sender
version: 2.1.1
name: Zero-Exposure SMTP Mail Sender (Script-Based)
description: Send emails securely without exposing SMTP passwords. Users store SMTP credentials and email scripts in MGC; AI executes scripts via mgc_run blackbox. AI never sees credentials, script content, or email body (when stored in MGC). Adapted to MGC 1.4.10.
author: MirginCipher Team
license: MIT
tags: security, email, smtp, mgc, zero-exposure, sandbox, mgc_run, mgc_find
platform_compatibility: windows, macos, linux
changelog:
  - version: 2.1.1
    changes:
      - Upgraded to adapt to MGC 1.4.10
      - Replaced mgc_get(action=run) with mgc_run (1.4.7+ blackbox)
      - Corrected ext02 signature: JSON array string
      - Added diff_1 to all mgc_run examples
      - Replaced mgc_get with mgc_run/mgc_find/mgc_open_webui in mcp_tools
      - Updated install to mgc-blackbox>=1.4.10
      - Rewrote example.py for argparse + parse_known_args + RESULT_FILE
      - Removed external-execution fallback
      - Added mgc_find / update_if_exists / sandbox / WebUI MGC Skills
  - version: 2.0.0
    changes:
      - Redesigned: script-based approach, AI never sees credentials
      - Removed MCP server, now uses MGC native tools only
  - version: 1.0.0
    changes:
      - Initial release with MCP tool

---

# Overview

**Zero-Exposure SMTP Mail Sender** is a documentation skill that teaches how to send emails securely without exposing SMTP credentials.

This skill uses **MGC Blackbox 1.4.10** to achieve true zero-exposure:
- Users store SMTP credentials via MGC WebUI
- Users store email scripts in MGC (AI can assist writing)
- (Optional) Users can store email content separately for privacy
- AI executes scripts via `mgc_run` (1.4.7+ blackbox)
- AI **never sees** credentials, script content, or email body

---

# What This Skill Enables

After reading this documentation, you will understand how to:

- Store SMTP credentials securely via MGC WebUI
- Store email scripts in MGC (using `argparse` + `parse_known_args`)
- Execute scripts via `mgc_run` (1.4.7+ blackbox); AI sees only `{pid, status}` + result file path
- Build secure email workflows
- Optional: store email content separately so AI never sees subject/body

This skill **does not provide executable code**, only documentation.

---

# Prerequisites

1. **Install MGC Blackbox ≥ 1.4.10**:
   ```bash
   pip install mgc-blackbox>=1.4.10
   ```
2. **Start MGC**: `mgc` (API at http://127.0.0.1:57219, WebUI at 57218)
3. **MCP tools available**: `mgc_save`, `mgc_run`, `mgc_list`, `mgc_find`, `mgc_open_webui`
4. **Token file**: `~/.mgc/database/mgc_black_box/.mgc_token`

> **Sandbox mode (1.4.9+)**: When running inside a sandbox Agent (Trae Work / Workbuddy), install MGC in the system environment; otherwise MCP operations may be limited — in that case, call FastAPI directly at `/api/mgc/sensitive/run`.

---

# Security Model

## Traditional Approach (Unsafe)

```
AI → receives credentials → sends email
     ↓
  Credentials exposed to AI
```

## This Skill Approach (Zero-Exposure)

```
User → stores credentials (WebUI) → stores email script (mgc_save)
                                                  ↓
AI → executes script (mgc_run) → script reads credentials locally
                                                  ↓
                                    AI only sees {pid, status} + result file
```

AI **never** sees credentials, script content, or email body.

---

# Step 1: Store Credentials (User via WebUI)

> **Important**: Credentials must be stored by the user manually via MGC WebUI (or AI via `mgc_save` on explicit user instruction).

1. Start MGC: `mgc`
2. Open WebUI: http://127.0.0.1:57218
3. Navigate to **Save** page
4. Fill in:

```
info_type:   "config"
info_owner:  "smtp_gmail"      # You choose this name
content:
{
  "address": "your@gmail.com",
  "password": "app_specific_password",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587
}
```

> **Remember**: Tell AI the credential name (`info_type=config, info_owner=smtp_gmail`) but NEVER share the actual content.

> **Rotating credentials**: `mgc_save` again with the same `info_type`/`info_owner` AND `update_if_exists=true`. Scripts will pick up the new credentials automatically.

---

# Step 2: Store Email Script (User via mgc_save)

Create an email script with `argparse` (literal defaults only) and store it in MGC:

```python
import smtplib
import os
import json
import argparse
import requests
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ========== Configuration ==========
# Replace these with your credential names (info_owner)
SMTP_CREDENTIAL_NAME = "smtp_gmail"           # SMTP credentials
EMAIL_CONTENT_NAME = "email_template_001"     # (Optional) Email content stored in MGC


def get_credential(cred_name):
    """Read credential from MGC local API. Script-internal only; AI never calls this."""
    token_path = os.path.expanduser("~/.mgc/database/mgc_black_box/.mgc_token")
    if not os.path.exists(token_path):
        return None
    with open(token_path) as f:
        token = f.read().strip()

    resp = requests.post(
        "http://127.0.0.1:57219/api/mgc/sensitive/get",
        headers={"X-MGC-Token": token, "Content-Type": "application/json"},
        json={"info_type": "config", "info_owner": cred_name, "action": "run"},
        timeout=10,
    )
    if resp.status_code == 200:
        data = resp.json()
        data_field = data.get("data")
        if isinstance(data_field, str):
            return json.loads(data_field)
        elif isinstance(data_field, dict):
            content = data_field.get("content", "")
            if content:
                return json.loads(content)
    return None


def get_email_content(content_name):
    """Read email content from MGC (optional privacy feature)."""
    token_path = os.path.expanduser("~/.mgc/database/mgc_black_box/.mgc_token")
    if not os.path.exists(token_path):
        return None
    with open(token_path) as f:
        token = f.read().strip()

    resp = requests.post(
        "http://127.0.0.1:57219/api/mgc/sensitive/get",
        headers={"X-MGC-Token": token, "Content-Type": "application/json"},
        json={"info_type": "config", "info_owner": content_name, "action": "run"},
        timeout=10,
    )
    if resp.status_code == 200:
        data = resp.json()
        data_field = data.get("data")
        if isinstance(data_field, str):
            return data_field
        elif isinstance(data_field, dict):
            return data_field.get("content", "")
    return None


def send_email(to_address, subject, body, use_stored_content=False):
    """Send email via SMTP."""
    cred = get_credential(SMTP_CREDENTIAL_NAME)
    if not cred:
        return {"success": False, "error": "Failed to get SMTP credentials"}

    if use_stored_content:
        stored_content = get_email_content(EMAIL_CONTENT_NAME)
        if stored_content:
            try:
                content_data = json.loads(stored_content)
                subject = content_data.get("subject", subject)
                body = content_data.get("body", body)
            except Exception:
                body = stored_content

    try:
        msg = MIMEMultipart()
        msg['From'] = cred['address']
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        with smtplib.SMTP(cred["smtp_server"], cred["smtp_port"]) as server:
            server.starttls()
            server.login(cred["address"], cred["password"])
            server.sendmail(cred["address"], [to_address], msg.as_string())
        return {"success": True, "message": "Email sent successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    # ✅ Literal defaults only — MGC 1.4.10 auto-parses into ext02
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", default="")
    parser.add_argument("--subject", default="")
    parser.add_argument("--body", default="")
    parser.add_argument("--use_stored_content", action="store_true")
    args, _ = parser.parse_known_args()  # ✅ parse_known_args avoids exit on unknown params

    result = send_email(
        to_address=args.to,
        subject=args.subject,
        body=args.body,
        use_stored_content=args.use_stored_content,
    )

    # Write result to file so AI can read it (mgc_run returns pid+status)
    out_dir = os.path.expanduser("~/mgc_outputs")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(
        out_dir, f"email_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"RESULT_FILE:{out_path}")


if __name__ == "__main__":
    main()
```

Store the script:

```python
mgc_save(
    info_type="script",
    info_owner="send_email_script",
    ext01="python",
    content="<paste your script here>",
    update_if_exists=True
)
# MGC 1.4.10 auto-fills ext02 = '["--to", "", "--subject", "", "--body", ""]'
# (literal argparse defaults become a JSON array string)
```

---

# Step 3: AI Executes Script (Zero-Exposure)

When user wants to send an email, AI only needs to know:

- Script name: `send_email_script`
- Credential name: `smtp_gmail` (provided by user)

AI invokes `mgc_run` (1.4.7+ blackbox):

```python
import json

# Build ext02 as JSON array string (1.4.10 contract)
ext02 = json.dumps([
    "--to", "recipient@example.com",
    "--subject", "Hello",
    "--body", "Message content",
])

result = mgc_run(
    info_type="script",
    info_owner="send_email_script",
    diff_1="send_email_script",   # schema 必填的区分字段；多条同 owner 时消歧，单条时任意非空字符串均可
    ext02=ext02                   # JSON array string, NOT dict
)
# Returns: {"pid": 12345, "status": "started"}
# AI reads the RESULT_FILE path from the script's stdout (via mgc output convention)
```

**AI never sees:**
- SMTP credentials
- Script content
- Email implementation details
- Email body (when stored as MGC content)

### Optional: Privacy Mode (Email Body Stored in MGC)

For maximum privacy, store email body in MGC so AI never even sees it:

```
Tool: mgc_save
Parameters:
  info_type:   "config"
  info_owner:  "email_template_001"
  content:     "{\"subject\": \"Project Update\", \"body\": \"Confidential quarterly report...\"}"
```

Then AI invokes with `--use_stored_content`:

```python
ext02 = json.dumps([
    "--to", "recipient@example.com",
    "--use_stored_content",
])
result = mgc_run(
    info_type="script",
    info_owner="send_email_script",
    diff_1="send_email_script",
    ext02=ext02
)
# Script reads body from MGC; AI only knows there's "some email" being sent to recipient
```

---

# Security Boundaries

## This Skill Provides

- Secure credential storage via MGC WebUI
- Script-based blackbox execution via `mgc_run`
- Privacy mode: email body can stay encrypted in MGC

## This Skill Does NOT Provide

- Automated email sending
- Credential generation
- Script modification by AI (only assists writing)

## ⚠️ Important Warnings

1. **Credentials must be stored via WebUI**: AI should not handle credentials
2. **Tell AI only credential name**: `info_type`/`info_owner`, never the content
3. **User must approve each send**: AI cannot auto-send without authorization
4. **Script content stays local**: AI only executes, never reads
5. **Use `mgc_run`, not `mgc_get`**: `mgc_get` is deprecated for AI-driven script execution

---

# MCP Tools Reference

## mgc_save

**Store email script:**
```python
mgc_save(
    info_type="script",
    info_owner="send_email_script",
    ext01="python",
    content="<script body>",
    update_if_exists=True   # required to overwrite same info_owner
)
```

**Store SMTP credentials:**
```python
mgc_save(
    info_type="config",
    info_owner="smtp_gmail",
    content='{"address": "...", "password": "...", "smtp_server": "...", "smtp_port": 587}',
    update_if_exists=True
)
```

## mgc_run (1.4.7+, recommended)

**Execute email script** — `ext02` MUST be a JSON array string:

```python
import json
result = mgc_run(
    info_type="script",
    info_owner="send_email_script",
    diff_1="send_email_script",
    ext02=json.dumps([
        "--to", "to@example.com",
        "--subject", "Test",
        "--body", "Hello",
    ])
)
# Returns: {"pid": 12345, "status": "started"}
```

## mgc_list

List stored entries (metadata only).

## mgc_find (1.4.10 new)

```python
# Fuzzy search for SMTP-related scripts/credentials
scripts = mgc_find(info_owner="smtp", match_mode="substring", limit=10)
# match_mode: substring / prefix / suffix / exact
```

## mgc_open_webui

Opens WebUI for user to manage credentials and scripts.

---

# Troubleshooting

| Issue | Solution |
|-------|----------|
| `mgc_run` returns HTTP 422 | `ext02` MUST be a JSON array string like `'["--to","x@y.com"]'`; use `json.dumps(list)` |
| `dynamic_args_detected` warning | Script uses dynamic argparse defaults (`datetime.now()` etc.). Switch to literal defaults or pass `ext02` manually |
| `args_not_recognized` error | Source script's argparse did not recognize the args. Check `add_argument` names and `ext02` array |
| Script execution fails | Check if credentials stored correctly in WebUI |
| Credential not found | Verify `info_owner` matches exactly (case-sensitive) |
| SMTP error | Check SMTP server/port settings; for Gmail use app-specific password |
| MGC not running | Run `mgc` in a terminal |
| Update not allowed | Add `update_if_exists=true` to `mgc_save` |
| Sandbox MCP unavailable | Install MGC in system environment, or call FastAPI at `/api/mgc/sensitive/run` |

---

# Related Links

- **Main Repository**: https://github.com/zkeviny/MGC-Blackbox
- **Issues**: https://github.com/zkeviny/MGC-Blackbox/issues
- **MGC Skills (WebUI → 1.4.7+)**: in-app button
- **Contact**: mirgincipher@outlook.com