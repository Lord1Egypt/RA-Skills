---
name: top-coding-models
description: Use when user wants benchmark rankings, pricing, token limits, or IDE compatibility info for top 20 agentic coding models. Supports OpenRouter, OpenAI, Anthropic, Google, DeepSeek, xAI, Meta, and other major LLM providers.
---

Get live rankings, pricing, and compatibility data for the top 20 agentic coding models — cross-referenced from BenchLM benchmark API and OpenRouter models API.

| Field      | Value                                           |
| ---------- | ----------------------------------------------- |
| Identifier | `top-coding-models`                             |
| Version    | 1.0.0                                           |
| Author     | Wai Yan                                         |
| Category   | tooling                                         |
| Installs   | 0                                               |
| Rating     | 0 / 5 (0 ratings)                               |
| License    | MIT                                             |

---

## Skill Overview

This skill fetches live data on the top 20 coding models from two authoritative sources:
1. **BenchLM AI Coding Leaderboard** — benchmark scores (SWE-bench Pro + LiveCodeBench 50/50 weighted)
2. **OpenRouter Models API** — live pricing, context windows, max output tokens

It outputs a structured markdown table with model rankings, costs, capabilities, and IDE compatibility info for agentic coding tools like Claude Code, Cursor, Windsurf, Cline, OpenCode, and more.

### Use this skill when

- User asks for "best coding models" or "top AI for coding"
- User wants benchmark scores vs pricing comparison
- User needs model compatibility info for a specific IDE (Claude Code, Cursor, Windsurf, etc.)
- User wants to compare costs between OpenAI, Anthropic, Google, DeepSeek models
- User asks for "free coding models" or "best budget model"
- User wantsSWE-bench or LiveCodeBench rankings
- User needs OpenRouter model IDs for API integration
- User wants tool-calling support info for agentic frameworks

### Do not use this skill when

- User wants general LLMs for chat (not coding-specific)
- User is asking about fine-tuned models not on BenchLM
- User wants image generation or multimodal models
- User is asking about local/self-hosted models (use ollama-skill instead)

### Core capabilities

- **Live Benchmark Data**: Fetches real-time rankings from BenchLM coding leaderboard
- **Cross-Referenced Pricing**: Pulls live token pricing from OpenRouter API
- **IDE Compatibility Matrix**: Lists which IDEs support each model via OpenRouter
- **Tool Calling Support**: Indicates which models support function calling
- **Cost-Performance Analysis**: Calculates best value (score per dollar)
- **Free Model Identification**: Lists available free-tier models

### Supported integration targets

- **Claude Code**: Via `ANTHROPIC_BASE_URL=https://openrouter.ai/api/v1`
- **OpenCode**: Provider: `openrouter` in config
- **Cursor**: Settings → Models → OpenAI-compatible
- **Windsurf**: Custom provider with OR base URL
- **Cline / Roo Code**: OpenAI Compatible provider
- **Aider**: `--openai-api-base` flag
- **Continue.dev**: Custom LLM provider

---

## Core Facts

| Source | API Endpoint | Update Frequency |
|--------|--------------|------------------|
| BenchLM | `https://benchlm.ai/api/data/leaderboard?category=coding` | Daily |
| OpenRouter | `https://openrouter.ai/api/v1/models` | Real-time |

| Benchmark | Weight | Description |
|-----------|--------|-------------|
| SWE-bench Pro | 50% | Real-world GitHub issue resolution |
| LiveCodeBench | 50% | Contamination-free competitive programming |

- **Top Provider by BenchLM**: Claude Mythos Preview (79.5% coding score)
- **Best Value**: Grok 4.1 (70.9% score at $0.70/1M tokens)
- **Free Models**: GLM-5 Reasoning, Qwen3.5 397B Reasoning (via OpenRouter)

---

## Quick Start

### 1. Run the Skill

The skill is located at:
```
~/.config/opencode/skills/top-coding-models/scripts/fetch_models.py
```

### 2. Basic Usage

```bash
python3 ~/.config/opencode/skills/top-coding-models/scripts/fetch_models.py
```

### 3. Get JSON Output (for automation)

```bash
python3 ~/.config/opencode/skills/top-coding-models/scripts/fetch_models.py --json
```

### 4. Customize Top N

```bash
python3 ~/.config/opencode/skills/top-coding-models/scripts/fetch_models.py --top=10
```

---

## Implementation Guide

### Decision Policy

**Choose Claude models when:**
- Maximum coding quality is priority
- Willing to pay premium for best benchmarks
- Need excellent tool calling for agentic workflows
- Context length > 200K tokens needed

**Choose OpenAI GPT-5.x models when:**
- Need reasoning + coding hybrid capabilities
- Want Codex-specific optimizations
- Balance quality and cost

**Choose Google Gemini models when:**
- Need largest context windows (1M+ tokens)
- Want multimodal capabilities
- Budget-conscious but need strong coding

**Choose xAI Grok models when:**
- Best value is priority (lowest cost per benchmark point)
- Need fast inference
- Can accept slightly lower coding scores

**Choose open-weight models (Qwen, GLM, DeepSeek) when:**
- Need free or very cheap inference
- Self-hosting or using OpenRouter free tier
- Willing to accept slightly lower benchmarks

### Implementation Workflow

1. **Fetch BenchLM rankings**: GET `https://benchlm.ai/api/data/leaderboard?category=coding`
2. **Fetch OpenRouter models**: GET `https://openrouter.ai/api/v1/models`
3. **Normalize names**: Match BenchLM model names to OpenRouter IDs
4. **Cross-reference pricing**: Map BenchLM pricing to OpenRouter live prices
5. **Calculate insights**: Best value, free models, budget picks
6. **Generate markdown**: Format as structured table with IDE compatibility

---

## Capability Details

### Live Data Fetching

The script fetches from two APIs every run to ensure fresh data.

```python
import urllib.request

BENCHMARKS_URL = "https://benchlm.ai/api/data/leaderboard?category=coding"
OPENROUTER_URL = "https://openrouter.ai/api/v1/models"

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "OpenCode-TopCodingModels/1.0"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())
```

**Rules:**
- Always fetch fresh data (no caching) to get latest rankings
- Handle API errors gracefully with user-friendly messages
- Timeout after 20 seconds to prevent hanging

### Model Name Matching

The script uses a fuzzy matching algorithm to link BenchLM model names to OpenRouter IDs.

```python
OR_ID_HINTS = {
    "claude opus 4.6": "anthropic/claude-opus-4.6",
    "gpt-5.3 codex": "openai/gpt-5.3-codex",
    "gemini 2.5 pro": "google/gemini-2.5-pro",
    # ... 50+ mappings
}
```

**Rules:**
- Use known hints first for exact matches
- Fall back to normalized substring matching
- Prefer longer matches over shorter ones

### Pricing Calculation

Prices are normalized to "per 1 million tokens" for easy comparison.

```python
inp_1m = float(pricing.get('prompt', 0)) * 1_000_000
out_1m = float(pricing.get('completion', 0)) * 1_000_000
```

**Rules:**
- Output prices in USD per 1M tokens
- Mark free models as "**Free**"
- Mark unknown prices as "N/A"

---

## Integration Patterns

### Pattern A: OpenRouter Unified API
Best for: Most agentic IDEs (Claude Code, Cursor, Windsurf)

```
Base URL: https://openrouter.ai/api/v1
Auth: Bearer <OPENROUTER_API_KEY>
Model ID: <from table above>
```

### Pattern B: Direct Provider API
Best for: When you have direct API keys (Anthropic, OpenAI, Google)

```
Use provider's native SDK with model-specific endpoints
```

### Pattern C: Local Proxy
Best for: Enterprise setups with custom routing

```
Route through proxy that selects provider based on model ID
```

---

## Best Practices

For selecting coding models, default to:

- **Premium quality**: Claude Opus 4.6 or Claude Sonnet 4.6 (Anthropic)
- **Best value**: Grok 4.1 (xAI) at $0.20/$0.50 per 1M tokens
- **Free tier**: Use `:free` suffix on OpenRouter (qwen3-coder:free, minimax-m2.5:free)
- **Long context**: Gemini 2.5 Pro/Flash (1M context)
- **Agentic tools**: Any model with Tools ✓ in the table

**Recommended abstractions:**
- `fetch_benchlm_rankings()` — Get benchmark scores
- `fetch_openrouter_pricing()` — Get live prices
- `cross_reference_models()` — Match and enrich data
- `format_markdown_table()` — Generate output

---

## Examples Reference

| Example | Description |
|---------|-------------|
| Default run | `python3 fetch_models.py` — Top 20 with full table |
| JSON output | `python3 fetch_models.py --json` — Machine-readable |
| Top 10 | `python3 fetch_models.py --top=10` — Focused list |

---

## Output Contract

When applying this skill, produce:

- Markdown table with 20 rows (or --top=N)
- Columns: Rank, Model, Provider, Type, Coding Score, Agentic Score, Input Price, Output Price, Context, Max Output, OpenRouter ID, Tools Support, Structured Outputs
- Key insights section with best value, free models, budget picks
- IDE compatibility matrix with setup instructions
- Python code snippet for OpenRouter API usage

---

## Anti-Patterns

Do not:
- Cache benchmark data (rankings change frequently)
- Trust BenchLM pricing alone (use OpenRouter for live prices)
- Ignore tool-calling support for agentic use cases
- Recommend models without checking OpenRouter availability
- Mix up input vs output pricing (they differ significantly)

---

## Definition of Done

The task is done when:
- Script successfully fetches from both APIs
- Table shows all 20 models with complete data
- At least 15 models have matched OpenRouter IDs
- Key insights section identifies best value and free models
- IDE compatibility matrix covers 5+ tools
- Python snippet is runnable with minimal changes

---

## MIT License

Copyright (c) 2026 Wai Yan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
