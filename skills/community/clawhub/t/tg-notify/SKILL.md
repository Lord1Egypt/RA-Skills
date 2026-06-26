---
name: tg-notify
description: Send Telegram notifications to team members by Telegram user ID. Use when you need to notify a specific person or multiple people via Telegram (e.g. alerts, reminders, task updates). Trigger phrases: "notify", "send telegram message", "alert [name] via telegram", "ping [person] on telegram", "отправь уведомление", "уведоми".
metadata: {"clawdbot":{"emoji":"📨","requires":{"bins":["curl","node"]}}}
---

# Telegram Notify Skill

Send messages to any Telegram user by chat ID using the OpenClaw bot.

## Bot Token

Read dynamically from `openclaw.json` — never hardcode:

```bash
BOT_TOKEN=$(node -e "const c=require(process.env.HOME+'/.openclaw/openclaw.json');console.log(c.channels.telegram.botToken)")
```

## Send a Message

```bash
BOT_TOKEN=$(node -e "const c=require(process.env.HOME+'/.openclaw/openclaw.json');console.log(c.channels.telegram.botToken)")

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "<TELEGRAM_USER_ID>",
    "text": "<MESSAGE>",
    "parse_mode": "HTML"
  }'
```

## Send to Multiple Recipients

```bash
BOT_TOKEN=$(node -e "const c=require(process.env.HOME+'/.openclaw/openclaw.json');console.log(c.channels.telegram.botToken)")

for CHAT_ID in 111111111 222222222; do
  curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -H "Content-Type: application/json" \
    -d "{\"chat_id\": \"${CHAT_ID}\", \"text\": \"<MESSAGE>\", \"parse_mode\": \"HTML\"}"
done
```

## Known Team Members

| Name    | Telegram ID |
|---------|-------------|
| Islam   | 6330057147  |

Add others to `USER.md` as they interact with the bot.

## Notes

- `parse_mode: HTML` supports `<b>bold</b>`, `<i>italic</i>`, `<code>code</code>`
- Bot can only message users who have previously started a chat with the bot
- Check response `ok: true` to confirm delivery; handle errors gracefully
- Token is always read from `~/.openclaw/openclaw.json` at runtime — never stored in this file
