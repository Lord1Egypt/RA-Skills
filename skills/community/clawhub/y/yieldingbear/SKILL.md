---
name: yieldingbear
description: Use Yielding Bear's unified LLM API for cost arbitrage and intelligent routing. Use when cutting AI costs, routing LLM requests, comparing model pricing, or setting up an OpenClaw agent to use multiple LLM providers. YB routes every request to the cheapest capable model automatically — saving 60-80% vs direct API calls.
allowed-tools:
  - Bash
  - Read
  - Write
metadata:
  author: Yielding Bear
  version: "1.0.0"
---

# Yielding Bear — Unified LLM Routing API

Yielding Bear provides a single unified API that routes every LLM request to the cheapest capable model across 16+ providers — saving 60-80% vs calling OpenAI, Anthropic, or Google directly.

## Setup (First Time Only)

1. **Get an API key** at https://yieldingbear.com/api

2. **Set environment variable:**
   ```bash
   export YIELDINGBEAR_API_KEY="yb_live_your_key_here"
   ```

3. **Save to your shell profile** (optional):
   ```bash
   echo 'export YIELDINGBEAR_API_KEY="yb_live_your_key_here"' >> ~/.zshrc
   source ~/.zshrc
   ```

## Quick Start — OpenClaw Agents

### Method 1: Direct API calls

```bash
curl -X POST https://api.yieldingbear.com/v1/chat/completions \
  -H "Authorization: Bearer $YIELDINGBEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto",
    "messages": [{"role": "user", "content": "Summarize this email: ..."}],
    "max_tokens": 500
  }'
```

### Method 2: OpenAI-compatible drop-in replacement

```python
from openai import OpenAI

client = OpenAI(
    api_key="yb_live_your_key",
    base_url="https://api.yieldingbear.com/v1"
)
# Same SDK. Same code. 60-80% less cost.
```

## Model Routing

| Task Type | Routes To | Cost/1M |
|-----------|-----------|---------|
| Summaries, classification | Llama 3.1 8B | $0.04 |
| Email drafting, formatting | DeepSeek V3 | $0.07 |
| General chat, code | GPT-4o-mini | $0.15 |
| Complex reasoning | YB Sentinel 70B | $0.06 |
| Fast completions | Gemini 2.0 Flash | $0.10 |

Override routing:
```json
{ "model": "claude-3.5-haiku", "routing": { "capabilities": ["reasoning"] } }
```

## OpenClaw Agent Integration

### For OpenClaw sub-agents

Set in environment before spawning:
```bash
export YIELDINGBEAR_API_KEY="yb_live_..."
```

The agent uses YB automatically when calling OpenAI-compatible endpoints.

### For custom tools and scripts

```bash
RESULT=$(curl -s -X POST "https://api.yieldingbear.com/v1/chat/completions" \
  -H "Authorization: Bearer $YIELDINGBEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto","messages":[{"role":"user","content":"Analyze: $1"}]}')
echo "$RESULT"
```

## Cost Comparison

| Task | Direct OpenAI | Via YB | Savings |
|------|-------------|--------|---------|
| 1M simple summaries | $150 | $40 | 73% |
| 1M email drafts | $300 | $60 | 80% |
| 1M chat completions | $500 | $150 | 70% |
| 1M reasoning tasks | $3,000 | $300 | 90% |

## Key Links

- **API Docs**: https://yieldingbear.com/developers
- **Yields page**: https://yieldingbear.com/yields
- **How it works**: https://yieldingbear.com/how-it-works
- **Dashboard**: https://yieldingbear.com/dashboard
- **Get API key**: https://yieldingbear.com/api
