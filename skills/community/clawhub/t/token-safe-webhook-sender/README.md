# Webhook Token Security (Zero‑Exposure Edition)

Secure webhook token management using MGC Blackbox. Supports DingTalk, WeCom, Feishu, Telegram, Slack and more.

## What This Skill Does

This skill provides a pattern for managing webhook tokens securely:
- Store tokens encrypted in MGC Blackbox
- Retrieve at runtime without AI seeing plaintext
- Send notifications safely

## Prerequisites

- Python 3.10+
- pip install mgc-blackbox
- MGC service running

> **Important:** For AI agents, use **MCP tools**. CLI may have port conflicts.

## Quick Start

### 1. Install MGC

```bash
pip install mgc-blackbox
mgc
```

### 2. Prepare Token

Create `webhook_token.json` with your platform-specific token:

**For Slack:**
```json
{
  "webhook_url": "https://hooks.slack.com/services/xxx"
}
```

**For Telegram:**
```json
{
  "bot_token": "your_bot_token",
  "chat_id": "your_chat_id"
}
```

**For DingTalk:**
```json
{
  "access_token": "xxx",
  "secret": "xxx"
}
```

### 3. Store in MGC

> **Important:** Use **MCP tools** for AI agents. CLI may have port conflicts.

**Recommended (MCP):** Use `mgc_save` tool
**Alternative (CLI):**
```bash
mgc_save info_type=config info_owner=my_webhook < webhook_token.json
```

### 4. Use in Your Script

Your local script retrieves token from MGC, sends notification - all without exposing tokens to AI.

## Supported Platforms

- DingTalk
- WeCom (Enterprise WeChat)
- Feishu (Lark)
- Telegram
- Slack

## What's Inside

- Webhook token storage pattern
- Platform-specific configuration
- MGC API reference
- Conceptual sending code
- Security best practices

## Security

- Tokens never exposed to AI
- Encrypted storage via MGC
- Runtime token retrieval only
- No plaintext in logs

## Learn More

- GitHub: https://github.com/zkeviny/MGC-Blackbox
- Issues: https://github.com/zkeviny/MGC-Blackbox/issues
- Contact: mirgincipher@outlook.com

## License

MIT