---
name: 企业微信对话配置
description: Set up WeCom (企业微信) as a chat channel for OpenClaw using the official Tencent plugin with WebSocket long-polling. Use when user wants to connect WeCom bot, configure 企业微信 channel, or mentions wecom/企微 integration. Triggers on "企业微信", "企微", "wecom", "WeCom bot", "配置企微".
---

# WeCom Channel Setup

Connect OpenClaw to WeCom (企业微信) via the official Tencent WebSocket plugin.

## Prerequisites

- OpenClaw >= 2026.2.13
- A WeCom AI Bot created at [WeCom Open Platform](https://open.work.weixin.qq.com)
- Bot **API mode**: 长连接 (WebSocket long-polling, no domain/IP required)
- Bot ID and Secret from the bot management page

> 📖 Full WeCom AI Bot docs: https://open.work.weixin.qq.com/help?doc_id=21657

## Setup Steps

### 1. Install the plugin

```bash
openclaw plugins install @wecom/wecom-openclaw-plugin
```

Wait for installation to complete. A security warning about "Environment variable access combined with network send" is expected — the plugin needs the bot secret to establish WebSocket connections.

### 2. Configure the channel

Edit `~/.openclaw/openclaw.json`. Add `wecom` under `channels`:

```json
{
  "channels": {
    "wecom": {
      "enabled": true,
      "botId": "<YOUR_BOT_ID>",
      "secret": "<YOUR_BOT_SECRET>",
      "dmPolicy": "open",
      "allowFrom": ["*"],
      "groupPolicy": "open"
    }
  }
}
```

Also ensure the plugin is allowed and enabled under `plugins`:

```json
{
  "plugins": {
    "allow": ["wecom-openclaw-plugin"],
    "entries": {
      "wecom-openclaw-plugin": {
        "enabled": true
      }
    }
  }
}
```

### 3. Verify the model configuration

The WeCom channel uses the global default model (`agents.defaults.model.primary`). Confirm it points to a provider with sufficient credits:

```bash
openclaw models status
```

If the default model's provider has no balance, update the primary:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "<provider>/<model>"
      }
    }
  }
}
```

### 4. Restart the gateway

```bash
openclaw gateway restart
```

If the restart exits with code 1 or produces no output (common on Windows), verify health manually:

```powershell
# PowerShell
Invoke-WebRequest -Uri http://localhost:<port>/health -UseBasicParsing | Select-Object -ExpandProperty Content
# Expected: {"ok":true,"status":"live"}
```

### 5. Test

Send a message to the bot in WeCom. It should reply within a few seconds.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `billing error — API key has run out of credits` | Default model provider has no balance | Change `agents.defaults.model.primary` to a funded provider, restart gateway |
| `doctor warning: allowFrom` | `dmPolicy: "open"` requires `allowFrom: ["*"]` | Add `"allowFrom": ["*"]` to wecom config |
| Bot connects but no reply | Gateway cached old config | Full stop + start: `openclaw gateway stop`, wait 5s, `openclaw gateway start` |
| Windows CLI outputs nothing | PowerShell encoding issue | Use `--plain` flag or check health via HTTP directly |

## Access Control Options

| Setting | Values | Default | Notes |
|---|---|---|---|
| `dmPolicy` | `pairing` / `open` / `allowlist` / `disabled` | `open` | Controls who can DM the bot |
| `allowFrom` | Array of user IDs or `["*"]` | `[]` | Required when `dmPolicy` is `open` |
| `groupPolicy` | `open` / `allowlist` / `disabled` | `open` | Controls group chat access |
| `groupAllowFrom` | Array of group IDs | `[]` | Used with `groupPolicy: "allowlist"` |
| `sendThinkingMessage` | `true` / `false` | `true` | Show "thinking…" placeholder while processing |

### Restrict to specific users (DM)

```json
{
  "channels": {
    "wecom": {
      "dmPolicy": "allowlist",
      "allowFrom": ["user_id_1", "user_id_2"]
    }
  }
}
```

### Restrict to specific groups

```json
{
  "channels": {
    "wecom": {
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["group_id_1"]
    }
  }
}
```
