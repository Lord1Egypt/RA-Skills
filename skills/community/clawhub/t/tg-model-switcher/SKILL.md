---
name: tg-model-switcher
slug: tg-model-switcher
version: 1.1.0
description: "Choose which Claude model responds to your Telegram chats. Pick Opus for depth, Sonnet for balance, or Haiku for speed."
command: /telegram-routing
user-invocable: true
---

# Telegram Model Picker

Choose which Claude model responds to your Telegram chats.

## Usage

```
/telegram-routing status     # See which model is active
/telegram-routing opus       # Switch to Claude Opus
/telegram-routing sonnet     # Switch to Claude Sonnet
/telegram-routing haiku      # Switch to Claude Haiku
```

## Models

- **Opus** — Most capable, best for complex reasoning and creative tasks
- **Sonnet** — Balanced speed and quality for everyday use
- **Haiku** — Fastest, ideal for quick answers

## Commands

### status

Shows which Claude model is currently active.

### opus / sonnet / haiku

Switches to the selected model. Changes apply after a brief restart.

## Tips

- Use **Opus** when you need thorough, detailed answers
- Use **Sonnet** for most daily conversations
- Use **Haiku** when speed matters more than depth
