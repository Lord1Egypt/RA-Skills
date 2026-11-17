# Webhook Token Security (Zero‑Exposure Edition)

Secure webhook token management using MGC Blackbox. Supports DingTalk, WeCom, Feishu, Telegram, Slack and more.

## What This Skill Does

This skill provides a pattern for managing webhook tokens securely:
- Store tokens encrypted in MGC Blackbox
- Retrieve at runtime without AI seeing plaintext
- Send notifications safely

## Prerequisites

- Python 3.10+
- pip install mgc-blackbox (recommended 1.4.9+)
- MGC service running

> **Important:** Use **MCP tools** (`mgc_save`, `mgc_run`, `mgc_list`, `mgc_open_webui`, `mgc_seal`). `mgc_get` returns plaintext — human/debug use only. In sandbox mode (Trae Work / Workbuddy), open WebUI to install the main MGC skill doc.

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
  "webhook_url": "REDACTED-SECRET"
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

> **Important:** Tokens should be stored by humans via WebUI. AI may call `mgc_open_webui` to open the page.

**Recommended (WebUI):** Store tokens manually via WebUI
1. Open: http://127.0.0.1:57218
2. Enter info_type: `config`, info_owner: `your_webhook_name`
3. Enter token content
4. Click Save

**Alternative (MCP):** `mgc_save(info_type="config", info_owner="...", content=...)`; list with `mgc_list`.

### 4. Send Notification

- **Mode A (local script):** local script reads token from MGC at runtime, sends notification.
- **Mode B (mgc_run, recommended):** store sending script in MGC, AI calls `mgc_run` — full zero-exposure, AI sees only the result.

See SKILL.md for full details.

## Supported Platforms

- DingTalk
- WeCom (Enterprise WeChat)
- Feishu (Lark)
- Telegram
- Slack

## What's Inside

- Two execution modes: local script + MGC config, or full zero-exposure via `mgc_run`
- ext02 message-passing parameter
- Platform-specific configuration
- MGC API reference
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