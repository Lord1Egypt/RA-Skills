# Smart Router

Intelligent multi-model router for [OpenClaw](https://github.com/openclaw/openclaw) — automatically selects the best AI model based on task type.

## Features

- 🧭 Auto-classification: vision, image gen, video gen, audio, reasoning, code, general chat
- ⚡ 35+ models across 7 categories
- 🎯 `@alias` shortcuts to call any model directly
- 🔄 Auto-fallback if a model fails
- 🔌 Works with any OpenAI-compatible API

## Install

```bash
clawhub install smart-router-pub
```

## Setup

Set your API provider credentials as environment variables:

```bash
export SMART_ROUTER_BASE_URL="https://your-api-provider.com/v1"
export SMART_ROUTER_API_KEY="your-api-key"
```

Any OpenAI-compatible API works (OpenAI, Azure, Together, OpenRouter, etc).

Then edit `models.json` to match the models your provider supports.

## Usage

Just talk to your OpenClaw agent normally. Smart Router kicks in automatically:

| You say | What happens |
|---------|-------------|
| Send an image + "what's this?" | → Vision model analyzes it |
| "Draw a cat in space" | → Image generation model |
| "Make a 10s video of waves" | → Video generation model |
| "Compose a jazz tune" | → Audio/music model |
| "Prove that √2 is irrational" | → Reasoning model |
| "Write a Python web scraper" | → Code model |
| "Translate this to French" | → General chat model |

### @ Shortcuts

Skip auto-classification and call a model directly:

```
@o3 Prove the Riemann hypothesis
@dalle A sunset over mountains
@sora A drone shot flying over Tokyo
@claude Review this code for bugs
@gpt52 Summarize this article
```

Run `@help` or check `SKILL.md` for the full alias table.

## Customization

Edit `models.json` to:
- Add/remove models
- Change defaults per category
- Point to a different API provider

Use `scripts/sync-models.sh` to discover all models available from your provider.

## Contact

Author: whatevername2023@proton.me

## License

MIT
