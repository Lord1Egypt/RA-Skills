---
name: push-server-py
description: Send notifications to WeCom (企业微信) users via OpenAPI push service(https://github.com/qingzhou-dev/push-server). Supports TEXT, MARKDOWN, TEXT_CARD, and NEWS message types.
metadata: { "openclaw": { "emoji": "📨", "requires": { "bins": ["python3"], "env": ["QYWX_PUSH_API_KEY", "QYWX_PUSH_URL"] }, "primaryEnv": "QYWX_PUSH_API_KEY" } }
---
# Push-Server WeCom Notification

Send notifications to WeCom (企业微信) users via the [Push Server](https://github.com/qingzhou-dev/push-server) OpenAPI.
This skill is designed for push notifications powered by [Push Server](https://github.com/qingzhou-dev/push-server). It can also be adapted for other webhook notification services by modifying  `notify.py` .

Supports TEXT, MARKDOWN, TEXT_CARD, and NEWS message types.

## Acknowledgements
The current version was collaboratively refined with AI assistance. Special thanks to:

- [OpenClaw](https://github.com/openclaw/openclaw) — the agent framework that powers this skill
- [Qwen](https://chat.qwen.ai/) — AI coding assistant

## Configuration

Two environment variables are required. Set them in `openclaw.json`:

```json
"skills": {
  "entries": {
    "push-server-py": {
      "apiKey": "your-api-key-here",
      "env": {
        "QYWX_PUSH_URL": "https://push.wechat.com"
      }
    }
  }
}
```

- `apiKey` → automatically injected as `QYWX_PUSH_API_KEY` (via primaryEnv)
- `env.QYWX_PUSH_URL` → the base URL of the push service

## Usage

```bash
python3 {baseDir}/notify.py '<JSON>'
```

## Environment Variables

| Variable          | Required | Source                         | Description                                  |
| ----------------- | -------- | ------------------------------ | -------------------------------------------- |
| QYWX_PUSH_API_KEY | yes      | `skills.entries.*.apiKey`      | API Key for authentication (`X-API-Key`)     |
| QYWX_PUSH_URL     | yes      | `skills.entries.*.env`         | Base URL of the push service                 |

## Request Parameters

| Param       | Type      | Required              | Default      | Description                                          |
| ----------- | --------- | --------------------- | ------------ | ---------------------------------------------------- |
| toUser      | str       | yes                   | -            | Target user(s), pipe-separated, e.g. `"user1|user2"` |
| msgType     | str       | no                    | TEXT         | `TEXT` / `MARKDOWN` / `TEXT_CARD` / `NEWS`           |
| content     | str       | yes (TEXT / MARKDOWN) | -            | Message content                                      |
| title       | str       | TEXT_CARD only        | -            | Card title                                           |
| description | str       | TEXT_CARD only        | -            | Card description                                     |
| url         | str       | TEXT_CARD only        | -            | Card link URL                                        |
| btnText     | str       | TEXT_CARD only        | View Details | Card button text                                     |
| articles    | list[obj] | NEWS only             | -            | List of article objects (see below)                  |

## Article Object (NEWS)

| Param       | Type | Required | Description         |
| ----------- | ---- | -------- | ------------------- |
| title       | str  | yes      | Article title       |
| url         | str  | yes      | Article link        |
| description | str  | no       | Article description |
| picUrl      | str  | no       | Article cover image |

## Examples

```bash
# Send TEXT notification
python3 {baseDir}/notify.py '{"toUser":"user1","content":"System is running normally.","msgType":"TEXT"}'

# Send MARKDOWN notification
python3 {baseDir}/notify.py '{
  "toUser": "user1|user2",
  "msgType": "MARKDOWN",
  "content": "## 🚨 Alert\n\n> CPU usage exceeds **90%**"
}'

# Send TEXT_CARD notification
python3 {baseDir}/notify.py '{
  "toUser": "user1|user2",
  "msgType": "TEXT_CARD",
  "title": "Weekly Report Ready",
  "description": "Click to view this week report.",
  "url": "https://example.com/reports/weekly",
  "btnText": "View Report"
}'

# Send NEWS notification
python3 {baseDir}/notify.py '{
  "toUser": "user1|user2",
  "msgType": "NEWS",
  "articles": [{
    "title": "March Monthly Report",
    "url": "https://example.com/reports/202503",
    "description": "March report is ready for review.",
    "picUrl": "https://example.com/reports/202503/cover.jpg"
  }]
}'
```

## Message Type Reference

| `msgType`   | Required Fields                 | Description              |
| ----------- | ------------------------------- | ------------------------ |
| `TEXT`      | `content`                       | Plain text message       |
| `MARKDOWN`  | `content`                       | Markdown rich text       |
| `TEXT_CARD` | `title`, `description`, `url`   | Card message with button |
| `NEWS`      | `articles`                      | News / articles          |

## Success Response

```json
{
  "success": true,
  "message": "ok",
  "errCode": 0
}
```

## Error Response

```json
{
  "success": false,
  "message": "Send failed: API error: invalid api key (errCode: 401)",
  "errCode": 401
}
```

## Current Status

Fully functional.
