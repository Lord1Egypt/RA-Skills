---
spec: usk/3.0
id: token_safe_webhook_sender
version: 1.1.0
name: Webhook Token Security (Zero‑Exposure Edition)
description: Secure webhook token management using MGC Blackbox. Supports DingTalk, WeCom, Feishu, Telegram, Slack and more. Store webhook tokens locally in encrypted form, retrieve at runtime without exposing to AI models.
author: MirginCipher Team
license: MIT
tags: webhook, token, security, credential-management, zero-exposure, mgc, dingtalk, wecom, feishu, telegram, slack
platform_compatibility: windows, macos, linux
changelog:
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
- Send notifications through local scripts
- Handle platform-specific differences
- Rotate tokens without code changes

---

# Prerequisites

1. Install MGC Blackbox: `pip install mgc-blackbox`(recommended 1.4.6+)
2. Start MGC service: `mgc` (runs at http://127.0.0.1:57219)
3. Use **MCP tools** (`mgc_save`, `mgc_get`) for token management

> **Important:** For AI agents, use **MCP tools**. CLI may have port conflicts in some environments.

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
  "webhook_url": "https://hooks.slack.com/services/xxx",
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

> **Important:** Use **MCP tools** for AI agents. CLI may have port conflicts in some environments.

**Recommended: WebUI (for human operators)**
> **Note:** According to user feedback, webhook tokens should be stored by humans via WebUI to avoid AI directly handling sensitive tokens through MCP.

Store via WebUI:
1. Open: http://127.0.0.1:57218
2. Navigate to Save page
3. Enter info_type: "webhook", info_owner: "your_webhook_name"
4. Enter token content
5. Click Save

**Alternative: MCP Interface** (for AI agents)
- Use `mgc_get` MCP tool to retrieve tokens
- Use `mgc_save` MCP tool if needed

---

# Webhook Token Pattern (Conceptual)

## Local Script Pattern

A secure webhook script follows this pattern:

1. **Retrieve token from MGC** (not visible to AI)
2. **Format message** (platform-specific)
3. **Send request** (HTTP POST)
4. **Return result** (non-sensitive data only)

The script must never print or expose webhook tokens.

## Conceptual Code Structure

```
function send_webhook(message):
    token = retrieve_from_mgc("my_webhook")
    payload = format_message(message, token)
    response = http_post(token["webhook_url"], payload)
    return response
```

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