# 🤖 xAI / Grok Skill for OpenClaw

Chat with xAI's [Grok](https://x.ai) models. Text, vision, and real-time X/Twitter search.

## What it does

- **Chat with Grok** - text conversations with Grok-3, Grok-3-mini, Grok-3-fast
- **Vision** - analyze images with Grok's vision model
- **Search X** - real-time Twitter search with citations via x_search tool
- **Model selection** - pick the right model for the job

## Quick start

### Install the skill

```bash
git clone https://github.com/mvanhorn/clawdbot-skill-xai.git ~/.openclaw/skills/xai
```

### Set up your API key

Get a key from [console.x.ai](https://console.x.ai), then:

```bash
export XAI_API_KEY="xai-YOUR-KEY"
```

### Example chat usage

- "Ask Grok what it thinks about AI safety"
- "Use Grok to analyze this image"
- "Search X for what people are saying about Remotion"
- "What Grok models are available?"

## Available models

| Model | Best for |
|-------|----------|
| `grok-3` | Complex tasks, reasoning |
| `grok-3-mini` | Fast, efficient responses |
| `grok-3-fast` | Speed-optimized |
| `grok-2-vision-1212` | Image understanding |

## CLI usage

```bash
node scripts/chat.js "What is the meaning of life?"
node scripts/chat.js --model grok-3-mini "Quick question"
node scripts/chat.js --image /path/to/image.jpg "What's in this?"
node scripts/search-x.js "AI news" --days 7
node scripts/models.js
```

## How it works

Wraps the xAI API (`https://api.x.ai`). Chat uses the standard completions endpoint. X search uses the Responses API with the `x_search` tool for real tweets with citations.

- API docs: https://docs.x.ai/api

## License

MIT
