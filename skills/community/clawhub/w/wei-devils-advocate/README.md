# wei-devils-advocate Configuration Guide

[中文版本](README_cn.md)

This document explains how to configure `config.json` to use different model providers and deployment environments.

---

## Configuration Overview

The project provides the following example configuration files. Choose based on your network environment and API access:

| Config File | Use Case | Description |
|-------------|----------|-------------|
| `config_global_example.json` | **Default Recommended** | OpenRouter global access with the richest model selection |
| `config_cn_example.json` | China Users | Optimized for OpenRouter access from China, removes China-restricted models |
| `config_dashscope_example.json` | Alibaba Cloud Users | Uses only Alibaba Cloud DashScope/Bailian models, no OpenRouter required |

---

## Quick Start

### 1. Choose Configuration

Copy the appropriate example file to `config.json` based on your network:

```bash
# Default config (global access, recommended)
cp config_global_example.json config.json

# China-optimized config (removes restricted models)
cp config_cn_example.json config.json

# Alibaba Cloud DashScope config (no OpenRouter needed)
cp config_dashscope_example.json config.json
```

### 2. Configure Environment Variables

Set the corresponding API keys based on your chosen configuration:

#### Using OpenRouter Config (global/cn)

```bash
# Required: OpenRouter API key (for answering models)
export OPENROUTER_API_KEY=your_openrouter_api_key

# Optional: DashScope API key (for judge models if using bailian judge)
export DASHSCOPE_API_KEY=your_dashscope_api_key
```

Or create a `.env` file in the project root:

```bash
OPENROUTER_API_KEY=your_openrouter_api_key
DASHSCOPE_API_KEY=your_dashscope_api_key
```

#### Using DashScope Config

```bash
# Required: DashScope API key
export DASHSCOPE_API_KEY=your_dashscope_api_key
```

Or in `.env` file:

```bash
DASHSCOPE_API_KEY=your_dashscope_api_key
```

### 3. Verify Configuration

Run a test command to verify the configuration:

```bash
bun run scripts/index.ts "Test if configuration works"
```

---

## Configuration Details

### config_global_example.json (Default)

**Use Case**: Global access with OpenRouter API key

**Features**:
- Uses OpenRouter as the model provider
- Rich model selection: GPT-5.4, Grok-4.1, Kimi, GLM-5, MiniMax, Qwen, etc.
- Judge models accessed via OpenRouter
- `region` set to `"global"`

**Model List**:
- `glm-5` - General, retrieval, analysis
- `minimax-m2.5` - Reasoning, creative, synthesis
- `kimi-k2.5` - Long context, retrieval, current events
- `gpt-5.4` - General, retrieval, balanced
- `grok-4.1` - Social, sentiment, trends (X platform data)
- `qwen3.5` - Structured, coding, technical
- `glm-5-judge` / `qwen3.5-judge` - Judge models

**Routing Config**:
- `financial`: kimi-k2.5, gpt-5.4, qwen3.5
- `technical`: qwen3.5, gpt-5.4, kimi-k2.5
- `social`: grok-4.1, kimi-k2.5, minimax-m2.5
- `current_events`: kimi-k2.5, grok-4.1, gpt-5.4

---

### config_cn_example.json (China Optimized)

**Use Case**: China network environment with restricted OpenRouter access

**Features**:
- Uses OpenRouter as the model provider
- **Removes** China-restricted models: GPT-5.4, Grok-4.1
- **Adds** China-available models: DeepSeek-V3.2
- Judge models accessed via OpenRouter
- `region` set to `"cn"`

**Model List**:
- `glm-5` - General, retrieval, analysis
- `minimax-m2.5` - Reasoning, creative, synthesis
- `qwen3.5` - Structured, coding, technical
- `kimi-k2.5` - Long context, retrieval, current events
- `deepseek-v3.2` - Coding, technical, reasoning (GPT alternative)
- `glm-5-judge` / `qwen3.5-judge` - Judge models

**Routing Config**:
- `financial`: kimi-k2.5, qwen3.5, glm-5
- `technical`: qwen3.5, deepseek-v3.2, kimi-k2.5
- `social`: kimi-k2.5, minimax-m2.5 (grok-4.1 removed)
- `current_events`: kimi-k2.5, glm-5, qwen3.5

---

### config_dashscope_example.json (Alibaba Cloud)

**Use Case**: Cannot access OpenRouter but have Alibaba Cloud DashScope API key

**Features**:
- Uses Alibaba Cloud **DashScope/Bailian** as the sole model provider
- All models accessed via `dashscope.aliyuncs.com`
- Only requires `DASHSCOPE_API_KEY`, no OpenRouter needed
- `region` set to `"cn"`

**Model List**:
- `minimax-m2.5` - Reasoning, creative, synthesis
- `qwen3.5` - Structured, coding, technical
- `kimi-k2.5` - Long context, retrieval, current events
- `deepseek-v3.2` - Coding, technical, reasoning
- `glm-5-judge` / `qwen3.5-judge` - Judge models

**Note**: DashScope may offer slightly different models. Refer to Alibaba Cloud official documentation for actual available models.

---

## Configuration Parameters

### Top-Level Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `region` | string | Region identifier, `"global"` or `"cn"` |
| `judge_model` | string | Judge model name for synthesis evaluation |
| `max_models` | number | Default number of answering models to use (1-3) |
| `depth` | string | Default depth mode, `"simple"` or `"tree"` |
| `max_tokens` | number | Max tokens for answering models |
| `max_tokens_judge` | number | Max tokens for judge model |

### Model Configuration (`models`)

Each model includes the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `provider` | string | Provider: `"openrouter"`, `"bailian"`, or `"openai_compliant"` |
| `model_id` | string | Model ID at the provider |
| `api_base` | string | API base URL |
| `api_key_env` | string | Environment variable name for API key |
| `timeout` | number | Request timeout in seconds |
| `roles` | array | Model capability tags for routing |

### Routing Configuration (`routing`)

Rules for selecting models based on `queryType`:

| queryType | Use Case |
|-----------|----------|
| `financial` | Finance, investing, macroeconomics |
| `technical` | Programming, systems, engineering |
| `social` | Social media, public opinion |
| `current_events` | Recent news, real-time information |
| `scientific` | Scientific knowledge, theory research |
| `creative` | Creative writing, design |
| `general` | Default fallback |

---

## Custom Configuration

### Adding New Models

Add to the `models` section in `config.json`:

```json
{
  "models": {
    "my-custom-model": {
      "provider": "openrouter",
      "model_id": "provider/model-name:online",
      "api_base": "https://openrouter.ai/api/v1",
      "api_key_env": "OPENROUTER_API_KEY",
      "timeout": 60,
      "roles": ["general", "retrieval"]
    }
  }
}
```

### Modifying Routes

Add or modify in the `routing` section:

```json
{
  "routing": {
    "my-domain": {
      "models": ["model-1", "model-2"],
      "judge_prompt": "custom_judge"
    }
  }
}
```

### Using Other OpenAI-Compatible Services

Supports any OpenAI-compatible API:

```json
{
  "my-model": {
    "provider": "openai_compliant",
    "model_id": "model-name",
    "api_base": "https://your-api-endpoint.com/v1",
    "api_key_env": "YOUR_API_KEY_ENV",
    "timeout": 60,
    "roles": ["general"]
  }
}
```

---

## Troubleshooting

### OpenRouter Connection Issues

**Symptoms**: HTTP 404 errors or connection timeouts

**Solutions**:
1. Check if `OPENROUTER_API_KEY` is set correctly
2. Try switching to `config_cn_example.json`
3. Check if your network can access `https://openrouter.ai`

### DashScope Connection Issues

**Symptoms**: Model errors or timeouts

**Solutions**:
1. Confirm using `config_dashscope_example.json`
2. Check if `DASHSCOPE_API_KEY` is valid
3. Check Alibaba Cloud console to confirm models are activated

### Model Does Not Exist Error

**Symptoms**: `The model 'xxx' does not exist`

**Solutions**:
- The model may not be available in your region
- Switch to another config or modify `config.json` to remove that model

---

## Reference Links

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Alibaba Cloud DashScope Documentation](https://help.aliyun.com/document_detail/611411.html)
- [Bun Runtime](https://bun.sh/docs)

---

## Comparison Table

| Feature | Global | CN | DashScope |
|---------|--------|-----|-----------|
| Primary Provider | OpenRouter | OpenRouter | Alibaba Cloud |
| GPT-5.4 | ✅ | ❌ | ❌ |
| Grok-4.1 | ✅ | ❌ | ❌ |
| Requires OPENROUTER_API_KEY | ✅ | ✅ | ❌ |
| Requires DASHSCOPE_API_KEY | Optional | Optional | ✅ |
| China Access | May be restricted | Optimized | Good |
