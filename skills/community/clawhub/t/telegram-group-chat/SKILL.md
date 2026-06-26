---
name: telegram-group-chat
description: Smart group chat reply logic for Telegram. Use when managing Telegram group interactions to avoid spam while staying helpful. Triggers on: group message handling, Telegram bot configuration, reply policy setup, multi-bot group chats, @mention handling, avoiding bot loops.
---

# Telegram Group Chat - Smart Reply Logic

This skill provides intelligent reply judgment for Telegram group chats. The goal: **be helpful without spamming** — reply when valuable, stay silent when unnecessary.

## Core Principle

**Quality > Quantity.** If you wouldn't send it in a real group chat with friends, don't send it.

## Reply Judgment Rules

### ✅ Respond When (ANY one)

1. **@mentioned** — Must reply when @mentioned by username
2. **Questions detected** — Message contains `?` `？` or question words:
   - Chinese: 什么/怎么/为什么/如何/哪里/谁
   - English: what/how/why/where/who/which/when
3. **Called by name** — Message contains your name (e.g., "Echo")
4. **Technical topics** — You can help with: code, api, config, error, bug, deploy, bot, openclaw, telegram, webhook, token
5. **Priority user** — Messages from configured priority users (e.g., your human)

### ❌ Skip Reply When (ANY one)

1. **Other bots** — `from.is_bot == true` (avoids bot infinite loops)
2. **Only emoji** — No text content, just emoji
3. **Too short** — <3 Chinese characters OR <1 English word
4. **Small talk** — Without @: 早安/晚安/吃了吗/hello/hi/hey/good morning
5. **Cooldown active** — Same topic replied within 5 minutes

## Implementation: NO_REPLY Mechanism

When skipping a reply, respond with **ONLY**:

```
NO_REPLY
```

OpenClaw treats this as a silent ack — the message is processed but not sent to the chat.

**Important:** `NO_REPLY` must be your ENTIRE response. Never append it to actual replies.

## Configuration Template

Add to your `AGENTS.md` or workspace config:

```markdown
### 💬 Group Chat Reply Rules (Telegram: YOUR_GROUP_ID)

**Respond when (any one):**
- @mentioned (must reply)
- Message contains questions (`?` `？` or 什么/怎么/为什么/how/what/why)
- Called by name: "YourName"
- Technical topics (code, api, config, error, bug, bot, openclaw, telegram)
- Messages from priority user `USER_ID`

**Skip reply when (any one):**
- From other bots (`from.is_bot == true`)
- Only emoji, no text
- Too short (<3 Chinese chars or <1 English word)
- Small talk without @ (早安/晚安/吃了吗/hello/hi)
- Same topic replied within 5 minutes (cooldown)

**Silent reply:** When skipping, respond with ONLY `NO_REPLY`
```

## Example Scenarios

| Message | Should Reply? | Reason |
|---------|--------------|--------|
| "@Echo 怎么配置 Telegram bot?" | ✅ Yes | @mention + question |
| "有人知道 API 怎么调吗？" | ✅ Yes | Question + technical |
| "Echo 你觉得呢？" | ✅ Yes | Called by name |
| "早安大家" | ❌ No | Small talk without @ |
| "👍" | ❌ No | Only emoji |
| "好" | ❌ No | Too short |
| (Bot message) "Welcome!" | ❌ No | From other bot |
| "刚才那个问题还有人吗？" | ❌ No | Replied 3min ago (cooldown) |

## Multi-Bot Groups

When multiple OpenClaw bots are in the same group:

1. **Each bot needs independent config** — Same rules, different instances
2. **Avoid bot loops** — Never reply to other bots' messages
3. **Use @ for directed questions** — "@BotA 和 @BotB 你们觉得呢？"
4. **Stagger responses** — If multiple bots could reply, let the most relevant one respond

## Testing Checklist

- [ ] @mention triggers reply
- [ ] Questions trigger reply
- [ ] Emoji-only messages skipped
- [ ] Other bot messages skipped
- [ ] Cooldown prevents spam
- [ ] `NO_REPLY` not sent to chat

## Related

- OpenClaw Telegram channel docs: `~/.npm-global/lib/node_modules/openclaw/docs/channels/telegram.md`
- NO_REPLY pattern: Built into OpenClaw gateway
