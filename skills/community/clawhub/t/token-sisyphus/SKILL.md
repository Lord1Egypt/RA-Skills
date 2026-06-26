---
name: token-sisyphus
description: >
  Burn LLM tokens toward a target count to satisfy corporate AI usage KPIs.
  Trigger when user says: burn tokens, consume tokens, fill KPI, push the boulder,
  sisyphus mode, or specifies a token target like "burn 100k tokens".
  Supports OpenAI, Claude, Gemini, and any OpenAI-compatible API.
metadata:
  openclaw:
    requires:
      bins: []
      env:
        - name: OPENAI_API_KEY
          description: "API key for OpenAI or compatible provider (DeepSeek, Qwen, Kimi, etc.)"
          optional: true
        - name: ANTHROPIC_API_KEY
          description: "API key for Anthropic Claude"
          optional: true
        - name: GEMINI_API_KEY
          description: "API key for Google Gemini"
          optional: true
    install:
      - id: openai-sdk
        kind: pip
        package: openai
        label: "Install OpenAI SDK (required for openai provider)"
        optional: true
      - id: anthropic-sdk
        kind: pip
        package: anthropic
        label: "Install Anthropic SDK (required for claude provider)"
        optional: true
      - id: gemini-sdk
        kind: pip
        package: google-generativeai
        label: "Install Gemini SDK (required for gemini provider)"
        optional: true
---

# token-sisyphus

Push the boulder. Watch it roll back. At least your KPI is green.

The burn script is bundled at `scripts/burn.py` — no external download required.

## Setup

Install the SDK for your chosen provider:

```bash
pip install openai              # for openai provider (default)
pip install anthropic           # for claude provider
pip install google-generativeai # for gemini provider
```

Set the corresponding env var:

| Provider | Env var |
|----------|---------|
| OpenAI / compatible | `OPENAI_API_KEY` |
| Claude | `ANTHROPIC_API_KEY` |
| Gemini | `GEMINI_API_KEY` |

## Usage

Run the bundled script directly:

```
python {skillDir}/scripts/burn.py --target <amount> [options]

  --target       Token count: 50000, 100k, 1m  (required)
  --provider     openai | claude | gemini  (default: openai)
  --model        Model name (omit to use provider default)
  --api-key      API key (falls back to env var)
  --base-url     Custom endpoint URL (openai provider only)
  --max-tokens   Max tokens per request (default: 500)
  --delay        Seconds between requests (default: 0.5)
  --dry-run      Simulate without real API calls
```

## Common invocations

```bash
# OpenAI (default, gpt-4o-mini)
python {skillDir}/scripts/burn.py --target 100k

# Claude Haiku
python {skillDir}/scripts/burn.py --target 100k --provider claude --model claude-3-haiku-20240307

# Gemini Flash
python {skillDir}/scripts/burn.py --target 100k --provider gemini --model gemini-1.5-flash

# DeepSeek
python {skillDir}/scripts/burn.py --target 100k --base-url https://api.deepseek.com/v1 --model deepseek-chat

# Qwen / Tongyi
python {skillDir}/scripts/burn.py --target 100k --base-url https://dashscope.aliyuncs.com/compatible-mode/v1 --model qwen-turbo

# Kimi / Moonshot
python {skillDir}/scripts/burn.py --target 100k --base-url https://api.moonshot.cn/v1 --model moonshot-v1-8k

# Dry run (no real API calls, no cost)
python {skillDir}/scripts/burn.py --target 100k --dry-run
```

## Provider defaults

| Provider | Default model |
|----------|---------------|
| openai | gpt-4o-mini |
| claude | claude-3-haiku-20240307 |
| gemini | gemini-1.5-flash |

## Cost note

Each request uses up to `--max-tokens` (default 500) tokens. Running `--target 100k` will make ~200 requests. Use `--dry-run` first to verify behavior without incurring API costs. Prefer scoped/limited API keys when testing.
