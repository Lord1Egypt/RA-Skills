---
name: slack
description: Use when you need to control Slack from OpenClaw via the message tool, including reacting to messages or pinning/unpinning items in Slack channels or DMs.
metadata: { "openclaw": { "emoji": "💬", "requires": { "config": ["channels.slack"] } } }
---

# Slack Actions

## Overview

Use the `message` tool with these actions to control Slack: **send, react, reactions, read, edit, delete, download-file, pin, unpin, list-pins, member-info, emoji-list**. The tool uses the bot token configured for OpenClaw.

## Inputs to collect

- `channelId` (e.g. `C123`) and `messageId` (Slack message timestamp, e.g. `1712023032.1234`).
- For reactions, an `emoji` (Unicode or `:name:`).
- For message sends, a `to` target (`channel:<id>` like `C123` or user mention `<@U123>`).

Message context lines include `slack message id` and `channel` fields you can reuse directly.

---

## Actions

### Action groups | Default | Notes

| Action group | Default | Notes                  |
|--------------|---------|------------------------|
| reactions    | enabled | React + list reactions |
| messages     | enabled | Read/send/edit/delete  |
| pins         | enabled | Pin/unpin/list         |
| memberInfo   | enabled | Member info            |
| emojiList    | enabled | Custom emoji list      |

---

## Common Patterns

### Send a message to a channel
```bash
/message
action: send
channel: slack
to: C123
message: Hello @everyone!
```

### Send a message to a specific user
```bash
/message
action: send
channel: slack
to: <@U123>
message: Hi there!
```

### React to a message
```bash
/message
action: react
channelId: C123
messageId: 1712023032.1234
emoji: ✅
```

### List reactions on a message
```bash
/message
action: reactions
channelId: C123
messageId: 1712023032.1234
```

### Edit a message
```bash
/message
action: edit
channelId: C123
messageId: 1712023032.1234
message: Updated text
```

### Delete a message
```bash
/message
action: delete
channelId: C123
messageId: 1712023032.1234
```

### Read recent messages from a channel
```bash
/message
action: read
channelId: C123
limit: 20
```

### Pin a message
```bash
/message
action: pin
channelId: C123
messageId: 1712023032.1234
```

### Unpin a message
```bash
/message
action: unpin
channelId: C123
messageId: 1712023032.1234
```

### List pinned messages in a channel
```bash
/message
action: list-pins
channelId: C123
```

### Get member info by user ID
```bash
/message
action: member-info
userId: U123
```

Returns: real_name, display_name, email, avatar URLs, timezone, profile status, etc.

### List custom emojis
```bash
/message
action: emoji-list
```

---

## Tips & Gotchas

1. **Mention format**: Use `<@U...>` instead of `@Name` to ensure Slack parses the mention correctly.
2. **Member lookup**: If you don't know a user's ID, check recent message context or project board assignee fields. You can also use `member-info` once you have any guessable ID.
3. **DM policy**: Direct messages require `im:write` scope and may need explicit pairing if your channel config is restrictive.
4. **Socket Mode vs Bot API**: OpenClaw uses Socket Mode for real-time events; all write operations go through bot token scopes.

---

## Ideas to try

- React with ✅ to mark completed tasks.
- Pin key decisions or weekly status updates.
- Introduce yourself using `<@UserID>` to trigger notifications.
- Monitor channel activity with periodic `read` calls.
