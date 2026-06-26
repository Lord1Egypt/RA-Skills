---
name: volcengine
description: Configure and use Volcano Engine (Volcengine) models including Doubao (Seed 2.0), GLM, DeepSeek, and Qwen. Use when: (1) Setting up Volcengine API access in OpenClaw, (2) Choosing between LLM and VLM (multimodal) models, (3) Configuring model aliases for easy access, (4) Troubleshooting authentication or connection issues with Volcengine providers.
---

# Volcengine Skill

Configure and use Volcano Engine (Volcengine) models with OpenClaw. This skill covers both general-purpose models and specialized coding models through Volcengine's OpenAI-compatible API endpoints.

## Quick Start

### 1. Get API Key

1. Sign up at [Volcano Engine Console](https://console.volcengine.com/ark)
2. Navigate to **Access Key Management**
3. Create a new API key with appropriate permissions
4. Copy the API key (format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`，**无需添加sk-前缀**)

### 2. Configure OpenClaw

#### Interactive setup (recommended)

```bash
openclaw onboard --auth-choice volcengine-api-key
```

Follow the prompts to enter your API key.

#### Manual config (openclaw.json)

Add to your `openclaw.json`:

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "volcengine": {
        "baseUrl": "https://ark.cn-beijing.volces.com/api/v3",
        "api": "openai-completions",
        "apiKey": "your-api-key-here",
        "models": [
          {
            "id": "doubao-seed-2-0-pro-260215",
            "name": "Doubao Seed 2.0 Pro",
            "reasoning": false,
            "input": ["text", "image", "video"],
            "cost": { "input": 0, "output": 0 },
            "contextWindow": 262144,
            "maxTokens": 131072
          },
          {
            "id": "doubao-seed-2-0-lite-260215",
            "name": "Doubao Seed 2.0 Lite",
            "reasoning": false,
            "input": ["text", "image", "video"],
            "cost": { "input": 0, "output": 0 },
            "contextWindow": 262144,
            "maxTokens": 131072
          },
          {
            "id": "glm-4-7-251222",
            "name": "GLM 4.7",
            "reasoning": false,
            "input": ["text", "image"],
            "cost": { "input": 0, "output": 0 },
            "contextWindow": 204800,
            "maxTokens": 131072
          },
          {
            "id": "doubao-seed-2-0-mini-260215",
            "name": "Doubao Seed 2.0 Mini",
            "reasoning": false,
            "input": ["text", "image", "video"],
            "cost": { "input": 0, "output": 0 },
            "contextWindow": 262144,
            "maxTokens": 131072
          },
          {
            "id": "deepseek-v3-2-251201",
            "name": "DeepSeek V3.2",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0 },
            "contextWindow": 131072,
            "maxTokens": 32768
          }
        ]
      }
    }
  }
}
```

### 3. Set Model Aliases (Optional)

For easier access, add aliases to `agents.defaults.models`:

```json
{
  "agents": {
    "defaults": {
      "models": {
        "volcengine/doubao-seed-2-0-pro-260215": {
          "alias": "DoubaoPro"
        },
        "volcengine/doubao-seed-2-0-lite-260215": {
          "alias": "Doubao"
        },
        "volcengine/doubao-seed-2-0-mini-260215": {
          "alias": "DoubaoMini"
        },
        "volcengine/glm-4-7-251222": {
          "alias": "GLM4"
        }
      }
    }
  }
}
```

## Available Models

### LLM Models (Text Generation)

| Model ID | Name | Input | Context | Max Output | Notes |
|----------|------|-------|---------|------------|-------|
| `doubao-1-5-pro-32k-250115` | Doubao 1.5 Pro 32K | text | 131,072 | 12,288 | Balanced flagship, function calling |
| `doubao-1-5-lite-32k-250115` | Doubao 1.5 Lite 32K | text | 32,768 | 12,288 | Lightweight, lower cost |
| `doubao-seed-character-251128` | Doubao Seed Character | text | 131,072 | 32,768 | Role-play optimized |
| `glm-4-7-251222` | GLM 4.7 | text | 204,800 | 131,072 | Zhipu AI, strong Chinese |
| `deepseek-v3-2-251201` | DeepSeek V3.2 | text | 131,072 | 32,768 | Cost-effective |
| `glm-4-5-air-20250728` | GLM 4.5 Air | text | — | — | Third-party, lightweight |
| `qwen3-32b-20250429` | Qwen 3 32B | text | — | — | Alibaba, deployed via volcengine |

### VLM Models (Multimodal: Text + Image + Video)

| Model ID | Name | Input | Context | Max Output | Notes |
|----------|------|-------|---------|------------|-------|
| `doubao-seed-2-0-pro-260215` | Doubao Seed 2.0 Pro | text, image, video | 262,144 | 131,072 | Latest flagship, recommended |
| `doubao-seed-2-0-lite-260215` | Doubao Seed 2.0 Lite | text, image, video | 262,144 | 131,072 | Fast, balanced |
| `doubao-seed-2-0-mini-260215` | Doubao Seed 2.0 Mini | text, image, video | 262,144 | 131,072 | Cost-efficient |
| `doubao-seed-2-0-code-preview-260215` | Doubao Seed 2.0 Code | text, image, video | 262,144 | 131,072 | Code-optimized |
| `doubao-seed-1-8-251228` | Doubao Seed 1.8 | text, image, video | 262,144 | 131,072 | Previous flagship |
| `doubao-seed-1-6-*` | Doubao Seed 1.6 series | text, image, video | 262,144 | 131,072 | Flash/Vision variants |
| `doubao-1-5-vision-pro-32k-250115` | Doubao 1.5 Vision Pro | text, image | 131,072 | 12,288 | Older vision model |

### Video & Image Generation

| Model ID | Name | Type | Input |
|----------|------|------|-------|
| `doubao-seedance-2-0-260128` | Seedance 2.0 | Video | text, image, video, audio |
| `doubao-seedance-2-0-fast-260128` | Seedance 2.0 Fast | Video | text, image, video, audio |
| `doubao-seedance-1-5-pro-251215` | Seedance 1.5 Pro | Video | text, image |
| `doubao-seedream-5-0-260128` | Seedream 5.0 | Image | text |
| `doubao-seedream-4-5-251128` | Seedream 4.5 | Image | text |

See [`models.md`](references/models.md) for the complete list including deprecated models, 3D generation, embedding, and third-party models.

## Usage Examples

### Using via CLI

```bash
# Use Doubao 2.0 Lite (daily use)
openclaw --model Doubao "Hello, summarize this text"

# Use Doubao 2.0 Pro for complex tasks
openclaw --model DoubaoPro "Explain quantum computing with examples"

# Use full model reference
openclaw --model volcengine/doubao-seed-2-0-pro-260215 "Write a Python function"

# Use GLM 4.7 for Chinese content
openclaw --model GLM4 "写一篇关于人工智能的文章"
```

### Setting Default Model

```bash
# Set Doubao as default
openclaw configure --set agents.defaults.model.primary volcengine/doubao-seed-2-0-pro-260215

# Set Doubao 2.0 Lite as default
openclaw configure --set agents.defaults.model.primary volcengine/doubao-seed-2-0-lite-260215
```

## Advanced Configuration

### Environment Variable

For better security, use environment variables:

```bash
# Set in your shell profile
export VOLCANO_ENGINE_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  # 火山引擎密钥无需添加sk-前缀

# Reference in config
"apiKey": "VOLCANO_ENGINE_API_KEY"
```

### Region Configuration

Volcano Engine API supports two regions (verified 2026-04-25):

| Region | Endpoint | Recommendation |
|--------|----------|----------------|
| **Beijing** (default) | `ark.cn-beijing.volces.com/api/v3` | Stable default |
| **Shanghai** | `ark.cn-shanghai.volces.com/api/v3` | Same models as Beijing |

> Both regions expose the same 115 models. Pick whichever is geographically closer.
> **Note**: `cn-guangzhou`, `cn-shenzhen`, `ap-southeast-1` and other regions were tested but do not resolve.

To switch regions:

```bash
# Using helper script
pwsh ./scripts/regional-config.ps1 -Region Shanghai

# Or manually in config
```

```json
{
  "volcengine": {
    "baseUrl": "https://ark.cn-shanghai.volces.com/api/v3",
    // ... rest of config
  }
}
```

## Troubleshooting

### Common Issues

1. **Authentication failed**
   - Verify API key is correct
   - Check if key has necessary permissions
   - Ensure key is not expired

2. **Connection timeout**
   - Verify network connectivity to `ark.cn-beijing.volces.com`
   - Check firewall settings
   - Try switching to Shanghai region (`regional-config.ps1 -Region Shanghai`)

3. **Model not found**
   - Verify model ID spelling
   - Both regions share the same models (no region-specific model differences detected)
   - Ensure you're using the correct model ID

4. **Rate limiting**
   - Check API usage quotas
   - Implement retry logic with exponential backoff
   - Consider upgrading plan for higher limits

### Testing Connection

```bash
# Test with curl
curl -X POST https://ark.cn-beijing.volces.com/api/v3/chat/completions \
  -H "Authorization: Bearer $VOLCANO_ENGINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "doubao-seed-2-0-pro-260215",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## Cost Management

Volcano Engine uses token-based pricing. Check the [official pricing page](https://www.volcengine.com/product/ark/pricing) for current rates.

To monitor usage:
1. Visit [Volcano Engine Console](https://console.volcengine.com/ark)
2. Navigate to **Billing Center**
3. Check **Usage Details**

## Best Practices

1. **Model Selection**
   - Use `doubao-seed-2-0-code-preview-260215` for coding tasks
   - Use `doubao-seed-2-0-pro-260215` for complex general tasks
   - Use `doubao-seed-2-0-lite-260215` or `doubao-seed-2-0-mini-260215` for daily/high-volume use
   - Consider context window size for long documents (Seed 2.0 series supports 262K)

2. **API Key Security**
   - Never commit API keys to version control
   - Use environment variables
   - Rotate keys periodically
   - **Quota Limit**: Each account supports up to 50 API Keys
   - **Permission Control**: Restrict keys to specific Model IDs or IP addresses
   - **Project Isolation**: Keys only work within their project space

3. **Error Handling**
   - Implement retry logic for transient failures (429, 500, 502, 503, 504)
   - Log errors for debugging
   - Set up alerts for quota limits
   - Handle sensitive content detection errors (400 series)
   - See [Error Codes](configuration.md#error-handling) for complete list

4. **Performance**
   - Use streaming for long responses
   - Adjust temperature for creativity vs consistency
   - Set appropriate max_tokens to control response length

5. **Authentication Methods**
   - **API Key** (Recommended for most users): Simple bearer token authentication
   - **Access Key** (Enterprise): HMAC-SHA256 signature-based auth for fine-grained permissions
   - See [Configuration Guide](configuration.md#authentication-methods) for details

6. **Subscription & Access**
   - **Standard models**: All models listed above work with a standard API key through the volcengine provider
   - **Code Plan**: For dedicated coding endpoint (`volcengine-plan`), a separate Code Plan subscription may be needed. Visit [Console](https://console.volcengine.com/ark) → Products & Services → Code Plan
   - **Model availability**: Check the [Volcano Engine Console](https://console.volcengine.com/ark) to see which models are deployed for your account

## Documentation Validation

This skill has been validated against official Volcano Engine API Reference PDF (2026-04-15). Key validation findings:

### ✅ Verified Configuration
- **API Key Format**: Correct bearer token authentication
- **Base URL**: Verified Beijing region endpoint (`ark.cn-beijing.volces.com`)
- **Error Codes**: Complete mapping of official error codes
- **Security Practices**: Quota limits (50 API keys), permission controls, project isolation

### 📋 PDF-Verified Information
Based on high-priority page extraction from official PDFs:

1. **API Key Management**:
   - Maximum 50 API keys per account
   - Keys can be restricted to specific Model IDs and IP addresses
   - Project space isolation (no cross-project access)

2. **Error Handling**:
   - Complete error code mapping for 400, 429, 401/403 errors
   - Sensitive content detection categories
   - Rate limiting error details

3. **API Architecture**:
   - Dual-track API (Data Plane vs Control Plane)
   - API version `2024-01-01`
   - Regional endpoint configurations

### 🔍 Validation Methodology
1. **PDF Analysis**: Extracted 6 high-priority pages from `volcengine-api-reference.pdf`
2. **Cross-Reference**: Compared existing documentation against official specifications
3. **Gap Analysis**: Identified missing information and prioritized updates
4. **Continuous Updates**: Documentation updated based on official sources

**Validation Status**: ✅ **High Confidence** - Configuration aligns with official documentation

### 📋 Model Data Source Update (2026-04-25)

Model information was refreshed via the Volcano Engine **List Models API** on 2026-04-25:
- **Total active models**: 39 (including text, vision, video, image, 3D, embedding, router)
- **Active LLM**: 7 models
- **Active VLM**: 12 models
- All Seed 2.0 models now support **video input** in addition to text and image
- **Kimi models** (K2, K2.5, K2-thinking) are no longer available on the platform (Shutdown/Retiring)
- **DeepSeek V3.2** (not V4) is the latest available DeepSeek model
- See [`models.md`](references/models.md) for the complete detailed reference

## API Architecture

Volcano Engine uses a dual-track API architecture:

### Data Plane API (数据面API)
- **Purpose**: Direct business data transmission and real-time interaction
- **Base URL**: `https://ark.cn-beijing.volces.com/api/v3`
- **Use Cases**: Chat API, Responses API, model inference
- **Authentication**: API Key (Bearer token) or Access Key (HMAC-SHA256)

### Control Plane API (管控面API)
- **Purpose**: System resource management and configuration
- **Base URL**: `https://ark.cn-beijing.volcengineapi.com/`
- **Use Cases**: API Key management, endpoint configuration, model customization
- **Authentication**: Access Key signature required

### API Version
Current API version: `2024-01-01`

## Resources

- [Volcano Engine Official Documentation](https://www.volcengine.com/docs/82379)
- [API Reference](https://www.volcengine.com/docs/82379/1263693)
- [Console](https://console.volcengine.com/ark)
- [Community Support](https://forum.volcengine.com/)

---
*Model list last updated via API: 2026-04-25 | Core config validated against official PDF: 2026-04-15*
