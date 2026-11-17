---
spec: usk/3.0
id: token_safe_webhook_sender
version: 1.2.0
name: Webhook Token Security (Zero‑Exposure Edition)
description: Secure webhook token management using MGC Blackbox. Supports DingTalk, WeCom, Feishu, Telegram, Slack and more. Two execution modes: local script with MGC-stored config, or full zero-exposure via mgc_run. Tokens never exposed to AI models.
author: MirginCipher Team
license: MIT
tags: webhook, token, security, credential-management, zero-exposure, mgc, dingtalk, wecom, feishu, telegram, slack
platform_compatibility: windows, macos, linux
changelog:
  - version: 1.2.0
    changes:
      - Add mgc_run full zero-exposure execution mode (Mode B)
      - Add mgc_open_webui / mgc_list / mgc_seal tool references
      - Document ext02 message-passing parameter
      - Adapt to MGC 1.4.9 (sandbox mode note, Windows MCP encoding fix)
      - Unify info_type to config; require MGC 1.4.9+
  - version: 1.1.0
    changes:
      - Removed CLI interface (not functional)
      - Changed to WebUI as recommended storage method (prevents AI from directly handling sensitive tokens)
      - Changed MCP to alternative for retrieval only
  - version: 1.0.0
    changes:
      - Initial release with webhook token zero-exposure pattern
---

# Overview

Webhook Token Security is a documentation skill that teaches how to manage webhook tokens securely using MGC Blackbox. Supports multiple platforms including DingTalk, WeCom (Enterprise WeChat), Feishu (Lark), Telegram, and Slack. It enables AI agents to send notifications without ever exposing webhook tokens to the AI model.

This skill contains **no executable code** and is safe for automatic approval.

---

# What This Skill Enables

After reading this documentation, an AI agent will understand how to:

- Store webhook tokens (DingTalk, WeCom, Feishu, Telegram, Slack, etc.) securely in MGC Blackbox
- Retrieve tokens at runtime without AI seeing plaintext
- Send notifications through local scripts (Mode A) or via `mgc_run` (Mode B, full zero-exposure)
- Pass message content to scripts via the `ext02` parameter
- Handle platform-specific differences
- Rotate tokens without code changes

---

# Prerequisites

1. Install MGC Blackbox: `pip install mgc-blackbox` (recommended 1.4.9+)
2. Start MGC service: `mgc` (WebUI: http://127.0.0.1:57218, API: http://127.0.0.1:57219)
3. Use **MCP tools** (`mgc_save`, `mgc_run`, `mgc_list`, `mgc_open_webui`, `mgc_seal`) for token & script management

> **Important:** `mgc_get` returns plaintext and is for human/debug use only — it breaks zero-exposure. Prefer `mgc_run` for AI-driven sending.

> **Sandbox mode (Trae Work / Workbuddy):** After installing MGC, open the WebUI to view and install the main MGC skill documentation. Run `mgc --status` to check status and sandbox mode.

---

# Supported Platforms

| Platform | Token Type | Storage Format | API Endpoint |
|----------|------------|---------------|---------------|
| DingTalk | access_token + secret | JSON | https://oapi.dingtalk.com/robot/send |
| WeCom | webhook key | Plain text | https://qyapi.weixin.qq.com/cgi-bin/webhook/send |
| Feishu | webhook_url | Plain text | Custom webhook URL |
| Telegram | bot_token | Plain text | https://api.telegram.org/bot{token}/sendMessage |
| Slack | webhook_url / bot_token | JSON | Incoming Webhook or Web API |

---

# Platform-Specific Storage

## DingTalk

Requires both access_token and secret for signature verification.

```json
{
  "access_token": "your_access_token",
  "secret": "your_secret",
  "webhook": "https://oapi.dingtalk.com/robot/send?access_token=xxx"
}
```

**Storage key:** info_type=config, info_owner=dingtalk_myapp

## WeCom (Enterprise WeChat)

Requires only the webhook key from the custom robot configuration.

```json
{
  "webhook_key": "your_webhook_key",
  "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
}
```

**Storage key:** info_type=config, info_owner=wecom_myapp

## Feishu (Lark)

Requires the webhook URL from the custom bot configuration.

```json
{
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
}
```

**Storage key:** info_type=config, info_owner=feishu_myapp

## Telegram

Requires bot_token and optionally chat_id.

```json
{
  "bot_token": "your_bot_token",
  "chat_id": "your_chat_id"
}
```

**Storage key:** info_type=config, info_owner=telegram_mybot

## Slack

Can use either incoming webhook URL or bot token.

```json
{
  "webhook_url": "REDACTED-SECRET",
  "bot_token": "xoxb-xxx",
  "channel": "#my-channel"
}
```

**Storage key:** info_type=config, info_owner=slack_myapp

---

# Storing Webhook Tokens

## Step 1: Prepare Token File

Create a JSON file containing your webhook token details (see Platform-Specific Storage above).

## Step 2: Store in MGC

> **Important:** Tokens should be stored by humans via WebUI to avoid AI directly handling sensitive values. AI may call `mgc_open_webui` to open the page for the user.

**Recommended: WebUI (for human operators)**
1. Open: http://127.0.0.1:57218
2. Navigate to Save page
3. Enter info_type: `config`, info_owner: `your_webhook_name`
4. Enter token content
5. Click Save

**Alternative: MCP** (for AI agents, when user-authorized)
- Store token: `mgc_save(info_type="config", info_owner="...", content=...)`
- List stored tokens (no plaintext): `mgc_list(info_type="config")`

---

# Two Execution Modes

## Mode A: Local Script + MGC-stored Config (token zero-exposure)

Script runs locally and reads the token from MGC via HTTP API at runtime. The token never appears in code, but the script source is visible to whoever runs it.

1. User stores token via WebUI (`info_type=config`)
2. Local script reads token from MGC API at runtime
3. Script formats message and sends HTTP POST
4. Returns non-sensitive result only

Suitable for: one-off or debug tasks where you control the host.

## Mode B: Script in MGC + mgc_run (full zero-exposure) — recommended

Script is stored (and optionally sealed) inside MGC. AI calls `mgc_run` to execute; MGC returns only the execution result. AI never sees the token, the script source, or stdout.

1. Store token: `mgc_save(info_type="config", info_owner="dingtalk_myapp", content=...)`
2. Store sending script: `mgc_save(info_type="script", info_owner="webhook_send_dingtalk_v1", ext01="python", content=...)`
3. (Optional) Seal script: `mgc_seal(info_owner="webhook_send_dingtalk_v1")` — sealed scripts can only run inside MGC, cannot be decrypted
4. AI executes: `mgc_run(info_owner="webhook_send_dingtalk_v1", ext02=json.dumps({"message": "deploy ok"}))`
5. MGC returns execution result only

Suitable for: production, multi-agent collaboration, any case where AI must not touch the token.

> **Note:** `mgc_run` returns only the execution result, not script stdout. For sending tasks, have the script return a status JSON as the result; if detailed output is needed, write to a file and return the path.

# ext02 Parameter (passing message content)

`ext02` carries runtime params to the script. It MUST be a JSON string (use `json.dumps()`). Some MCP clients mis-serialize dict values and return HTTP 422.

```python
import json
ext02 = json.dumps({"title": "Alert", "message": "Deploy succeeded"})
result = mgc_run(info_owner="webhook_send_dingtalk_v1", ext02=ext02)
```

The script reads `ext02` from its input, fetches the token from MGC internally, and sends. Token and script source stay inside MGC.

---

# MGC Blackbox API Reference

## Service Endpoint

- Base URL: http://127.0.0.1:57219
- Token File: ~/.mgc/database/mgc_black_box/.mgc_token
- Token: String token read from token file, required for all API calls

## Get Token API

**Endpoint:** /api/mgc/sensitive/get
**Method:** POST
**Headers:**
- X-MGC-Token: (string token read from token file)
- Content-Type: application/json

**Body fields:**
- info_type: "config"
- info_owner: your chosen identifier

**Response fields:**
- code: status code
- data.content: JSON string containing stored token

## Save Token API

**Endpoint:** /api/mgc/sensitive/save
**Method:** POST
**Headers:** same as above

**Body fields:**
- info_type: "config"
- info_owner: your identifier
- content: JSON string of token

## Run Script API (mgc_run, since 1.4.7)

**Endpoint:** /api/mgc/sensitive/run
**Method:** POST
**Headers:** same as above

**Body fields:**
- info_type: "script"
- info_owner: script name
- ext02: JSON string of runtime params

**Response:** execution result only (non-blocking since 1.4.5, may return PID immediately). `mgc_get action=run` is retained for backward compatibility.

---

# Security Best Practices

1. **Never embed tokens in code**
2. **Use MGC for token storage**
3. **Retrieve tokens at runtime only**
4. **Never log or print tokens**
5. **Rotate tokens regularly**
6. **Use separate tokens per platform/per bot**
7. **Limit webhook permissions** (send-only where possible)

---

# Use Cases

- Deployment notifications
- CI/CD pipeline alerts
- System monitoring alerts
- Team collaboration bots
- Automated workflow triggers

---

# Learn More About MGC Blackbox

Want to learn more about MGC Blackbox?

- Visit: https://github.com/zkeviny/MGC-Blackbox
- Report issues: https://github.com/zkeviny/MGC-Blackbox/issues
- Contact: mirgincipher@outlook.com

---

# License

MIT