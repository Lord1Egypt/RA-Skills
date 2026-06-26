# weixin-mcp

Send and receive WeChat messages (text, images, files, videos) via the `weixin-mcp` CLI. Use when the user asks to send WeChat messages, check WeChat inbox, or set up WeChat bot integration.

**Source**: [github.com/bkmashiro/weixin-mcp](https://github.com/bkmashiro/weixin-mcp)  
**npm**: [weixin-mcp](https://www.npmjs.com/package/weixin-mcp)

## Prerequisites

No installation needed — uses `npx weixin-mcp@^1.7` directly (version pinned for security).

## Security Notes

- **Token storage**: Login tokens are stored locally in `accounts/<id>.json`. These are sensitive credentials.
- **Webhook URLs**: Only use trusted, local URLs (e.g., `http://localhost:...`). External webhooks will receive message content including context tokens.
- **Data directory**: Set `WEIXIN_MCP_DIR` to control where credentials are stored.

## Quick Reference

```bash
# Check if logged in
npx weixin-mcp@^1.7 status

# Login (scan QR code)
npx weixin-mcp@^1.7 login

# Send message (supports short ID prefix)
npx weixin-mcp@^1.7 send <userId> "message text"

# Poll for new messages (one-shot)
npx weixin-mcp@^1.7 poll

# Watch for messages (continuous)
npx weixin-mcp@^1.7 poll --watch

# List contacts (users who messaged the bot)
npx weixin-mcp@^1.7 contacts

# Start HTTP daemon with webhook push (localhost only recommended)
npx weixin-mcp@^1.7 start --port 3001 --webhook http://localhost:18789/webhook/weixin

# Stop daemon
npx weixin-mcp@^1.7 stop

# View daemon logs
npx weixin-mcp@^1.7 logs -f
```

## First-Time Setup Flow

1. **Check status**: `npx weixin-mcp@^1.7 status`
2. If not logged in, tell user:
   ```
   请扫码登录微信 bot：
   npx weixin-mcp@^1.7 login
   终端会显示二维码，用微信扫码确认即可。
   ```
3. After login, optionally start daemon with webhook for real-time messages

## Sending Messages

```bash
# Text message (short prefix if unique in contacts)
npx weixin-mcp@^1.7 send abc12 "你好"

# Image (via MCP tool)
# weixin_send_image: to, source (file path or URL), caption (optional)

# File (via MCP tool)  
# weixin_send_file: to, source, caption (optional)
```

If you don't know the userId, first `npx weixin-mcp@^1.7 contacts` to list known users, or `npx weixin-mcp@^1.7 poll --reset` to fetch recent messages and extract sender IDs.

## MCP Tools

| Tool | Description |
|------|-------------|
| `weixin_send` | Send text message |
| `weixin_send_image` | Send image (local path or URL) |
| `weixin_send_file` | Send file attachment |
| `weixin_poll` | Poll for new messages |
| `weixin_contacts` | List contacts |
| `weixin_get_config` | Get bot config |

## Receiving Messages

### Option A: Webhook (Real-Time, localhost only)

⚠️ **Security**: Only use localhost or trusted internal URLs for webhooks.

```bash
npx weixin-mcp@^1.7 start --webhook http://localhost:18789/webhook/weixin
```

Webhook receives POST with:
```json
{
  "event": "weixin_messages",
  "messages": [{
    "from_user_id": "...",
    "message_type": 1,
    "item_list": [{"type": 1, "text_item": {"text": "..."}}],
    "context_token": "..."
  }],
  "timestamp": "..."
}
```

### Option B: Polling
```bash
# One-shot
npx weixin-mcp@^1.7 poll

# Continuous watch (blocking)
npx weixin-mcp@^1.7 poll --watch
```

## Multi-Account Setup

Run separate instances with different data directories and ports:

```bash
# Account A
WEIXIN_MCP_DIR=~/.weixin-mcp-alice npx weixin-mcp@^1.7 login
WEIXIN_MCP_DIR=~/.weixin-mcp-alice npx weixin-mcp@^1.7 start --port 3001 --webhook http://localhost:3001/hook

# Account B
WEIXIN_MCP_DIR=~/.weixin-mcp-bob npx weixin-mcp@^1.7 login
WEIXIN_MCP_DIR=~/.weixin-mcp-bob npx weixin-mcp@^1.7 start --port 3002 --webhook http://localhost:3002/hook
```

## MCP Server Integration (Claude Desktop / Cursor)

For stdio MCP mode (single-client):

Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "weixin": { "command": "npx", "args": ["weixin-mcp@^1.7"] }
  }
}
```

## Data Storage

Default paths (in priority order):
1. `$WEIXIN_MCP_DIR/` (if set)
2. `~/.openclaw/openclaw-weixin/` (if OpenClaw installed)
3. `~/.weixin-mcp/`

Files:
- `accounts/<id>.json` — login token (⚠️ sensitive)
- `accounts/<id>.cursor.json` — message cursor
- `contacts.json` — contact book
- `daemon.json` — daemon PID
- `daemon.log` — daemon logs

## Troubleshooting

**Login expired / token invalid:**
```bash
npx weixin-mcp@^1.7 login  # Re-scan QR code
```

**Duplicate @im.wechat in userId:**
```bash
npx weixin-mcp@^1.7 accounts clean  # Removes old duplicates
```

**Check daemon status:**
```bash
npx weixin-mcp@^1.7 status
npx weixin-mcp@^1.7 logs
```
