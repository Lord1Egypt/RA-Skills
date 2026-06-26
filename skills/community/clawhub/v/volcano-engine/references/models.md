# Volcengine Models Reference

Complete list of available models on Volcano Engine platform.
**Last updated from API**: 2026-04-25

## General Models (volcengine provider)

Endpoint: `https://ark.cn-beijing.volces.com/api/v3`

### LLM Models (Text Generation)

| Model ID | Name | Output | Context | Function Calling | Notes |
|----------|------|--------|---------|-----------------|-------|
| `doubao-1-5-pro-32k-250115` | Doubao 1.5 Pro 32K | 12,288 | 131,072 | ✅ | Balanced flagship |
| `doubao-1-5-lite-32k-250115` | Doubao 1.5 Lite 32K | 12,288 | 32,768 | ✅ | Lightweight, lower cost |
| `doubao-1-5-pro-32k-character-250715` | Doubao 1.5 Pro Char | 12,288 | 32,768 | ✅ | Character-optimized variant |
| `doubao-seed-character-251128` | Doubao Seed Character | 32,768 | 131,072 | ❌ | Role-play optimized |
| `doubao-seed-translation-250915` | Doubao Seed Translation | 3,072 | 4,096 | ❌ | Translation only |
| `glm-4-7-251222` | GLM 4.7 | 131,072 | 204,800 | ✅ | Zhipu AI, strong Chinese |
| `deepseek-v3-2-251201` | DeepSeek V3.2 | 32,768 | 131,072 | ✅ | Cost-effective |

### VLM Models (Multimodal: Text + Image + Video → Text)

| Model ID | Name | Output | Context | Function Calling | Input |
|----------|------|--------|---------|-----------------|-------|
| `doubao-seed-2-0-pro-260215` | Doubao Seed 2.0 Pro | 131,072 | 262,144 | ✅ | text, image, video |
| `doubao-seed-2-0-lite-260215` | Doubao Seed 2.0 Lite | 131,072 | 262,144 | ✅ | text, image, video |
| `doubao-seed-2-0-mini-260215` | Doubao Seed 2.0 Mini | 131,072 | 262,144 | ✅ | text, image, video |
| `doubao-seed-2-0-code-preview-260215` | Doubao Seed 2.0 Code | 131,072 | 262,144 | ✅ | text, image, video |
| `doubao-seed-1-8-251228` | Doubao Seed 1.8 | 131,072 | 262,144 | ❌ | text, image, video |
| `doubao-seed-1-6-250615` | Doubao Seed 1.6 | 131,072 | 262,144 | ❌ | text, image, video |
| `doubao-seed-1-6-251015` | Doubao Seed 1.6 (newer) | 131,072 | 262,144 | ❌ | text, image, video |
| `doubao-seed-1-6-flash-250615` | Doubao Seed 1.6 Flash | 131,072 | 262,144 | ❌ | text, image, video |
| `doubao-seed-1-6-flash-250828` | Doubao Seed 1.6 Flash (newer) | 131,072 | 262,144 | ❌ | text, image, video |
| `doubao-seed-1-6-vision-250815` | Doubao Seed 1.6 Vision | 131,072 | 262,144 | ❌ | text, image, video |
| `doubao-seed-code-preview-251028` | Doubao Seed Code Preview | 131,072 | 262,144 | ❌ | text, image, video |
| `doubao-1-5-vision-pro-32k-250115` | Doubao 1.5 Vision Pro 32K | 12,288 | 131,072 | ❌ | text, image |

### Video Generation Models

| Model ID | Name | Input | Description |
|----------|------|-------|-------------|
| `doubao-seedance-2-0-260128` | Seedance 2.0 | text, image, video, audio | Latest video generation |
| `doubao-seedance-2-0-fast-260128` | Seedance 2.0 Fast | text, image, video, audio | Faster generation |
| `doubao-seedance-1-5-pro-251215` | Seedance 1.5 Pro | text, image | Previous gen pro |
| `doubao-seedance-1-0-pro-250528` | Seedance 1.0 Pro | text, first_frame, first_last_frame | Initial release |
| `doubao-seedance-1-0-pro-fast-251015` | Seedance 1.0 Pro Fast | text, image | Fast generation |

### Image Generation Models

| Model ID | Name | Description |
|----------|------|-------------|
| `doubao-seedream-5-0-260128` | Seedream 5.0 | Latest image generation |
| `doubao-seedream-4-5-251128` | Seedream 4.5 | |
| `doubao-seedream-4-0-250828` | Seedream 4.0 | |

### 3D Generation Models

| Model ID | Name | Input |
|----------|------|-------|
| `doubao-seed3d-2-0-260328` | Seed3D 2.0 | image |
| `hyper3d-gen2-260112` | Hyper3D Gen2 | image, text |
| `hitem3d-2-0-251223` | HiTem3D 2.0 | image |

### Third-Party Models

| Model ID | Name | Type |
|----------|------|------|
| `qwen3-32b-20250429` | Qwen 3 32B | LLM (text-only) |
| `qwen3-14b-20250429` | Qwen 3 14B | LLM (text-only) |
| `qwen3-8b-20250429` | Qwen 3 8B | LLM (text-only) |
| `qwen3-0-6b-20250429` | Qwen 3 0.6B | LLM (text-only) |
| `qwen2-5-72b-20240919` | Qwen 2.5 72B | LLM (text-only) |
| `glm-4-5-air-20250728` | GLM 4.5 Air | LLM (text-only) |

### Embedding & Router

| Model ID | Name | Type | Input |
|----------|------|------|-------|
| `doubao-embedding-vision-250615` | Doubao Embedding Vision | Text/Image Embedding | text, image |
| `doubao-embedding-vision-251215` | Doubao Embedding Vision (newer) | Text/Image Embedding | text, image |
| `doubao-smart-router-250928` | Doubao Smart Router | Model Router | text |

## Deprecated / Shutdown Models

The following models are **no longer available** or in **retirement**:

- `doubao-lite-4k-240328` / `doubao-lite-32k-240428` / `doubao-lite-128k-240428` (Shutdown)
- `doubao-pro-4k-240515` / `doubao-pro-32k-240615` / `doubao-pro-128k-240515` (Shutdown)
- `doubao-pro-32k-240828` / `doubao-pro-32k-241215` (Retiring)
- `doubao-1-5-pro-256k-250115` (Shutdown)
- `doubao-1-5-pro-32k-character-250228` (Retiring)
- `doubao-1.5-vision-lite-250315` (Retiring)
- `doubao-1.5-vision-pro-250328` (Retiring)
- `doubao-1-5-thinking-pro-250415` (Retiring)
- `doubao-vision-pro-32k-241028` / `doubao-vision-lite-32k-241015` (Shutdown)
- `deepseek-v3-241226` (Shutdown) / `deepseek-v3-250324` (Retiring)
- `deepseek-r1-250120` / `deepseek-r1-distill-qwen-7b-250120` / `deepseek-r1-distill-qwen-32b-250120` (Shutdown)
- `kimi-k2-250711` (Shutdown) / `kimi-k2-250905` (Retiring) / `kimi-k2-thinking-251104` (Retiring)
- `wan2-1-14b-i2v-250225` / `wan2-1-14b-t2v-250225` (Shutdown)
- `doubao-seaweed-241128` (Shutdown)
- `doubao-seedance-1-0-lite-*` (Retiring)

## Model Selection Guide

### By Use Case

| Task | Recommended | Alternative | Why |
|------|-------------|-------------|-----|
| **General Chat** | `doubao-1-5-pro-32k-250115` | `doubao-seed-2-0-lite-260215` | Balanced, reliable |
| **Code Generation** | `doubao-seed-2-0-code-preview-260215` | `doubao-seed-2-0-pro-260215` | Code-optimized |
| **Multi-modal (image/video)** | `doubao-seed-2-0-pro-260215` | `doubao-seed-2-0-lite-260215` | Best vision support |
| **Chinese Content** | `glm-4-7-251222` | `doubao-seed-2-0-pro-260215` | Native Chinese |
| **Cost-sensitive** | `doubao-1-5-lite-32k-250115` | `doubao-seed-2-0-mini-260215` | Lower cost |
| **Long Context** | `doubao-seed-2-0-pro-260215` | `glm-4-7-251222` | 262K context |
| **Role-play** | `doubao-seed-character-251128` | `doubao-seed-2-0-pro-260215` | Character-optimized |

### By Context Window

| Context | Model |
|---------|-------|
| **≤32K** | `doubao-1-5-lite-32k-250115`, `doubao-1-5-pro-32k-character-250715` |
| **≤128K** | `doubao-1-5-pro-32k-250115`, `doubao-seed-character-251128`, `deepseek-v3-2-251201` |
| **≤200K** | `glm-4-7-251222` |
| **≤262K** | `doubao-seed-2-0-*` (all variants), `doubao-seed-1-6/1-8` |

## Seed 2.0 Series Details

All Seed 2.0 models support:
- **Context window**: 262,144 (256K)
- **Max output**: 131,072 (128K)
- **Max reasoning tokens**: 131,072 (128K)
- **Multimodal input**: text, image, video
- **Function calling**: ✅ (except code-preview lacks explicit fc)

### Variant Comparison

| Variant | Speed | Quality | Best For |
|---------|-------|---------|----------|
| **Pro** | Slower | Highest | Complex reasoning, creative tasks |
| **Lite** | Fast | Good | Daily chat, quick responses |
| **Mini** | Fastest | Adequate | Cost-sensitive, high-volume |
| **Code Preview** | Medium | High (code) | Code generation and review |

## API Parameters

All models support standard OpenAI-compatible parameters:

```json
{
  "model": "doubao-seed-2-0-pro-260215",
  "messages": [...],
  "temperature": 0.7,
  "top_p": 0.9,
  "max_tokens": 2048,
  "stream": false
}
```

### Recommended Settings

| Task | Temperature | Max Tokens |
|------|-------------|------------|
| Creative writing | 0.8-1.0 | 1024-4096 |
| Code generation | 0.2-0.5 | 2048-8192 |
| Analysis | 0.3-0.7 | 512-2048 |
| Translation | 0.1-0.3 | Same as input |

## Rate Limits

Check current rate limits in the [Volcano Engine Console](https://console.volcengine.com/ark). Limits depend on subscription plan.

---

*Last API sync: 2026-04-25*
*Source: Volcano Engine List Models API*
