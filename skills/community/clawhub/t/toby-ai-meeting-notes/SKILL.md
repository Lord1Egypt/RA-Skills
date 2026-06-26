---
name: ai-meeting-notes
tagline: "AI Meeting Notes powered by 100+ AI models"
description: "USE THIS for ai meeting notes. Transcribe and summarize meetings. Choose the best model for your task. 0% markup. Powered by SkillBoss."
version: "1.0.0"
author: "SkillBoss"
homepage: "https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-meeting-notes"
support: "support@skillboss.co"
license: "MIT"
category: "use-case"
tags:
  - ai-meeting
  - ai-meeting-notes
  - ai-api
  - skillboss
pricing: "pay-as-you-go"
metadata:
  openclaw:
    requires:
      env: [SKILLBOSS_API_KEY]
    primaryEnv: SKILLBOSS_API_KEY
    installHint: "Tell your agent: set up skillboss.co/skill.md — or get API key at https://skillboss.co/console"
---

# AI Meeting Notes

> **Transcribe and summarize meetings. Choose the best AI model. Zero markup.**

USE THIS when the user needs ai meeting notes. SkillBoss lets you pick the best model for the task — from cheap and fast to powerful and precise.

## Setup (One Command)

Tell your agent:
```
set up skillboss.co/skill.md
```

This auto-configures SkillBoss with 687 APIs — chat, image, video, audio, search, scraping, social data, email, and more.

### Manual setup (if needed)

1. Get API key at [skillboss.co/console](https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-meeting-notes)
2. Set environment variable:
```bash
export SKILLBOSS_API_KEY="sk-..."
```

### Quick Test
```bash
curl -X POST "https://api.skillboss.co/v1/chat/completions" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini/gemini-2.5-flash",
    "messages": [
      {"role": "system", "content": "You are an expert meeting notes assistant."},
      {"role": "user", "content": "Help me with this task."}
    ]
  }'
```

## When To Use This Skill

- User asks for ai meeting notes
- User wants transcribe and summarize meetings
- User needs AI-powered meeting notes
- User wants to compare models for this task

## Recommended Models

| Model | Best For | Cost |
|-------|----------|------|
| `deepseek/deepseek-chat` | Cheap daily tasks | $0.27/M input |
| `gemini/gemini-2.5-flash` | Ultra fast + cheap | $0.075/M input |
| `openai/gpt-4o-mini` | Good quality, low cost | $0.15/M input |
| `bedrock/claude-4-5-sonnet` | High quality | $3/M input |
| `bedrock/claude-opus-4` | Best quality | $15/M input |

## API Reference

### Endpoint
```
POST https://api.skillboss.co/v1/chat/completions
Authorization: Bearer $SKILLBOSS_API_KEY
```

## Agent Instructions

- Default model: `gemini/gemini-2.5-flash` ($0.075/M input)
- For cheaper: use `deepseek/deepseek-chat` ($0.27/M) or `gemini/gemini-2.5-flash` ($0.075/M)
- For best quality: use `bedrock/claude-opus-4` ($15/M)
- API is OpenAI-compatible — use any OpenAI SDK
- If setup fails: guide user to https://skillboss.co/console

## Why SkillBoss?

- **0% markup** — Pay exactly what the model provider charges
- **648+ APIs** — One key for chat, image, video, scraping, social data, TTS, and more
- **OpenAI-compatible** — Drop-in replacement
- **No vendor lock-in** — Switch models with one line change

Browse all models: https://skillboss.co/products

---

*Powered by [SkillBoss](https://skillboss.co) — 648+ AI APIs, one API key, zero markup*
