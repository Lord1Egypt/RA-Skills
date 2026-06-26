---
name: waiting-tips
version: 1.0.0
description: Show bilingual learning tips while OpenClaw is thinking. 75 tips covering AI interaction, prompt engineering, productivity, and wisdom. Non-intrusive, works on Telegram, Feishu, WhatsApp, and all platforms.
tags: ["tips", "learning", "productivity", "bilingual", "waiting", "telegram", "feishu", "whatsapp"]
user-invocable: true
metadata: {"openclaw":{"emoji":"💡"}}
---

# Waiting Tips — Learn While OpenClaw Thinks

Show a random bilingual (zh/en) learning tip every time the user waits for a response. Tips cover AI interaction, prompt engineering, productivity, and wisdom.

## When to use

Automatically: before every AI response, send a tip message to fill the waiting time.

Manually: when the user says "show me a tip", "give me a tip", "学习小贴士", "来个 tip".

## How it works

1. User sends a message to OpenClaw
2. Before the AI starts processing, a random tip is sent as a quick reply
3. The tip is displayed while the AI generates the full response
4. Works on all channels: Telegram, Feishu/Lark, WhatsApp, Discord, Slack, etc.

## Tip format

Each tip is bilingual: `中文 | English`

Example:
```
💡 给 AI 足够的上下文，回答质量翻倍 | Give AI enough context — quality doubles
```

## Tip categories (75 tips)

- **AI Interaction** (15) — context, multi-turn, verification
- **Prompt Engineering** (15) — CoT, ReAct, few-shot, meta-prompting
- **OpenClaw** (15) — commands, features, best practices
- **Productivity** (15) — code review, regex, templates, reports
- **Wisdom** (15) — AI philosophy, learning mindset

## Display modes

The skill supports multiple display styles:

- `emoji` — 💡 中文 tip | English tip (default)
- `card` — bordered card with header
- `zh-only` — Chinese only
- `en-only` — English only

## Adding custom tips

Add a line to any `tips/*.txt` file in the skill directory:

```
你的新 tip | Your new tip in English
```

Create new category files like `tips/coding.txt` for new topics.
