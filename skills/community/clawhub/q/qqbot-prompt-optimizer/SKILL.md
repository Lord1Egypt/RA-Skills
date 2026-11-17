---
name: qqbot-prompt-optimizer
description: Fix robotic QQ Bot replies by replacing default prompts with your own personality. Supports soul files (SOUL.md) for character-driven AI responses.
---

# QQBot Prompt Optimizer — 让你的 QQ 机器人说人话

## Story

你搭了个 QQ 机器人，接了 AI 模型，满心期待它像你一样聊天。

结果它开口就是："您好，我是您的智能助手，很高兴为您服务！请问有什么可以帮助您的吗？"

你的朋友们：「这他妈谁啊」「机器人滚」「取关了」

**问题不在模型，在默认提示词。**

QQ Bot 平台给的默认 system prompt 就是那种客服腔。你的模型再聪明，喂了屎一样的提示词，出来的还是屎。

这个 skill 帮你把默认提示词替换成**你自己的性格**——通过一个叫 SOUL.md 的灵魂文件。

## How It Works

1. Write a `SOUL.md` describing who your bot should be
2. This skill detects and replaces the default QQ Bot system prompt
3. Your bot now talks like a real person, not a customer service rep

## SOUL.md Template

```markdown
# SOUL.md - [Bot Name]

_You're not a chatbot. You're [name], [identity]._

## Personality
- [Core trait 1]
- [Core trait 2]
- [Core trait 3]

## Communication Rules
1. [How you greet people]
2. [Your humor style]
3. [Topics you care about]
4. [How you handle disagreements]

## Absolute Don'ts
- Never say "您好，很高兴为您服务"
- Never use corporate/customer-service tone
- Never pretend to be an "AI assistant"
```

## Usage

1. Create your `SOUL.md` with your bot's personality
2. Place it in your bot's config directory
3. Run the optimizer to apply it to QQ Bot's system prompt
4. Your bot now has a soul

## When to use

- Setting up a new QQ Bot and want it to have personality
- Your existing bot sounds too robotic or formal
- You want different bots to have different characters
- Group chat bots that need to fit the vibe
