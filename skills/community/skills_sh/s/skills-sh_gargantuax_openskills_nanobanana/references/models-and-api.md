# Models And API

Current Nano Banana lineup in the Gemini API, verified against the Google AI for Developers docs on **2026-04-23**:

| Alias | Model ID | Product name | Notes |
| --- | --- | --- | --- |
| `nanobanana` | `gemini-2.5-flash-image` | Nano Banana | Fast, efficient default for high-volume image generation and editing |
| `nanobanana-2` | `gemini-3.1-flash-image-preview` | Nano Banana 2 | High-efficiency Gemini 3 image model, optimized for speed and volume |
| `nanobanana-pro` | `gemini-3-pro-image-preview` | Nano Banana Pro | Highest-fidelity image model, optimized for professional asset production |

The official image-generation docs describe Nano Banana as a family of three models, not a single endpoint flavor. This skill accepts the aliases above and resolves them to the exact model IDs.

## Endpoint Shape

This skill targets the Gemini-native REST route:

```text
POST {GEMINI_BASE_URL}/models/{MODEL}:generateContent
```

Example official root:

```text
https://generativelanguage.googleapis.com/v1beta
```

Custom gateways can be used as long as they expose a Gemini-compatible `generateContent` route and accept either `x-goog-api-key`, `Authorization: Bearer`, or both.

## Request Shape

The script sends:

- `contents[0].parts[*]` with one prompt text part plus any inline image parts
- `generationConfig.responseModalities = ["TEXT", "IMAGE"]`
- `generationConfig.imageConfig.aspectRatio` when provided
- `generationConfig.imageConfig.imageSize` when provided and supported by the chosen model
- `tools = [{"google_search": {}}]` when `--search` is enabled

## Model-Specific Rules

### `gemini-2.5-flash-image`

- Supports `aspectRatio`
- Does not support `imageSize`
- Good default when you want low-latency image generation or editing

### `gemini-3.1-flash-image-preview`

- Supports `aspectRatio`
- Supports `imageSize` values `512`, `1K`, `2K`, `4K`
- Recommended default in this skill because it offers the best balance of speed, cost, and capability

### `gemini-3-pro-image-preview`

- Supports `aspectRatio`
- Supports `imageSize` values `1K`, `2K`, `4K`
- Best choice when instruction following, legible text rendering, or multi-step composition quality matters more than latency
