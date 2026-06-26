# Seedream Reference

Source: [Volcengine Official Docs](https://www.volcengine.com/docs/82379/1541523) | [Seedream Tutorial](https://www.volcengine.com/docs/82379/1824121) (last verified: 2026-05-16, API doc updated 2026-05-11)

---

## 1. API endpoint

- Base URL: `https://ark.cn-beijing.volces.com/api/v3`
- Generate: `POST /images/generations`
- List models: `GET /models`
- Auth: `Authorization: Bearer <api_key>`
- Timeout: 300s (generation), 30s (model listing)

## 2. Complete parameter list

| Parameter | Required | Type | Default | Description |
|-----------|:--------:|------|---------|-------------|
| `model` | ✅ | string | — | Model ID (e.g. `doubao-seedream-5-0-260128`). Also supports Endpoint ID for advanced features. |
| `prompt` | ✅ | string | — | Text prompt, supports Chinese and English. Max ~300 Chinese chars / 600 English words. |
| `image` | | string/array | — | Reference image. String for single, array for multiple. URL or base64. Max 14 images. |
| `size` | | string | `2048x2048` | Preset (`1K`/`2K`/`3K`/`4K`) or pixel (`WIDTHxHEIGHT`). Two modes cannot be mixed. |
| `response_format` | | string | `url` | `url` (24h valid link) or `b64_json` (base64 encoded) |
| `output_format` | | string | `jpeg` | `jpeg` or `png` (**5.0-lite only**) |
| `watermark` | | bool | `true` | Add "AI生成" watermark to bottom-right |
| `sequential_image_generation` | | string | `disabled` | `auto` (group mode) or `disabled` (single image) |
| `sequential_image_generation_options` | | object | — | `{"max_images": N}` (1-15). Input images + generated images ≤ 15. |
| `tools` | | array of object | — | `[{"type": "web_search"}]` — **5.0-lite only**. Enables web search for real-time info. |
| `stream` | | bool | `false` | Enable streaming output |
| `optimize_prompt_options` | | object | — | `{"mode": "standard"}` (all models) or `{"mode": "fast"}` (4.0 only) |
| `guidance_scale` | | float | — | Text weight [1-10]. **Only for 3.0-t2i, NOT supported by 5.0-lite/4.5/4.0** |

### Parameter notes

- `image` format for base64: `data:image/<format>;base64,<data>` (format must be lowercase, e.g. `jpeg` not `JPG`)
- `size` mode 1 (preset): model picks aspect ratio from prompt context
- `size` mode 2 (pixel): must satisfy both total pixel range AND aspect ratio range
- `tools` is an array: `[{"type": "web_search"}]` — not a simple boolean. The script's `--web-search` flag auto-converts to this format.
- `optimize_prompt_options` is a nested object — the script's `--prompt-optimization` flag auto-converts to this format
- `sequential_image_generation_options.max_images`: total input + output ≤ 15

## 3. Model capabilities

| Feature | 5.0-lite | 4.5 | 4.0 |
|---------|----------|-----|-----|
| Model ID | `doubao-seedream-5-0-260128` | `doubao-seedream-4-5-251128` | `doubao-seedream-4-0-250828` |
| Alias | `doubao-seedream-5-0-lite-260128` | — | — |
| Text-to-image | ✅ | ✅ | ✅ |
| Text-to-group | ✅ | ✅ | ✅ |
| Single image-to-image | ✅ | ✅ | ✅ |
| Multi image-to-image | ✅ | ✅ | ✅ |
| Single image-to-group | ✅ | ✅ | ✅ |
| Multi image-to-group | ✅ | ✅ | ✅ |
| Streaming | ✅ | ✅ | ✅ |
| Web search (via `tools`) | ✅ | ❌ | ❌ |
| Preset sizes | 2K, 3K, 4K | 2K, 4K | 1K, 2K, 4K |
| Output formats | png, jpeg | jpeg | jpeg |
| Prompt optimization | standard | standard | standard, fast |
| Rate limit (IPM) | 500 | 500 | 500 |

## 4. Complete resolution table

### Preset sizes

| Preset | 1:1 | 4:3 | 3:4 | 16:9 | 9:16 | 3:2 | 2:3 | 21:9 |
|--------|-----|-----|-----|------|------|-----|-----|------|
| 1K | 1024×1024 | 1152×864 | 864×1152 | 1280×720 | 720×1280 | 1248×832 | 832×1248 | 1512×648 |
| 2K | 2048×2048 | 2304×1728 | 1728×2304 | 2848×1600 | 1600×2848 | 2496×1664 | 1664×2496 | 3136×1344 |
| 3K | 3072×3072 | 3456×2592 | 2592×3456 | 4096×2304 | 2304×4096 | 3744×2496 | 2496×3744 | 4704×2016 |
| 4K | 4096×4096 | 4704×3520 | 3520×4704 | 5504×3040 | 3040×5504 | 4992×3328 | 3328×4992 | 6240×2656 |

### Pixel format constraints

| Model | Min total pixels | Max total pixels | Aspect ratio range |
|-------|-----------------|-----------------|-------------------|
| 5.0-lite | 3,686,400 (≈2560×1440) | 16,777,216 (4096×4096) | [1/16, 16] |
| 4.5 | 3,686,400 (≈2560×1440) | 16,777,216 (4096×4096) | [1/16, 16] |
| 4.0 | 921,600 (≈1280×720) | 16,777,216 (4096×4096) | [1/16, 16] |

### Common pixel sizes

| Use case | Size | Pixels | Ratio |
|----------|------|--------|-------|
| Phone wallpaper (portrait) | 1080×1920 | 2,073,600 | 9:16 |
| Phone wallpaper (landscape) | 1920×1080 | 2,073,600 | 16:9 |
| Desktop wallpaper | 2560×1440 | 3,686,400 | 16:9 |
| 4K desktop | 3840×2160 | 8,294,400 | 16:9 |
| Instagram square | 1080×1080 | 1,166,400 | 1:1 |
| Instagram story | 1080×1920 | 2,073,600 | 9:16 |
| Product photo | 2048×2048 | 4,194,304 | 1:1 |

## 5. Input image specifications

### Supported formats

jpeg, png, webp, bmp, tiff, gif, heic, heif

### Constraints

| Constraint | Value |
|-----------|-------|
| Max file size | 30MB per image |
| Max total pixels | 36,000,000 (width × height, i.e. 6000×6000) |
| Aspect ratio range | [1/16, 16] |
| Min dimension | > 14px per side |
| Max images per request | 14 |
| Total (input + output) | ≤ 15 images |

### Base64 format

```
data:image/png;base64,iVBORw0KGgoAAAAN...
```

- Format must be lowercase: `jpeg`, `png`, `webp`
- Do NOT use `JPG` or `JPEG` — use `jpeg`

### Image URL requirements

- Must be publicly accessible
- HTTPS recommended
- No authentication required to fetch

## 6. Response format

### Non-streaming (default)

```json
{
  "model": "doubao-seedream-5-0-260128",
  "created": 1773654512,
  "data": [
    {
      "url": "https://...",
      "size": "2048x2048"
    }
  ],
  "usage": {
    "generated_images": 1,
    "output_tokens": 16384,
    "total_tokens": 16384
  }
}
```

When `response_format=b64_json`:
```json
{
  "data": [
    {
      "b64_json": "iVBORw0KGgoAAAAN..."
    }
  ]
}
```

### Error in group generation

When generating a group of images, if one image fails:
- **Audit failure (content review)**: Other images continue generating. Failed image returns an `error` object.
- **Internal server error (500)**: Remaining images are NOT generated.

```json
{
  "data": [
    { "url": "https://...", "size": "2048x2048" },
    { "error": { "code": "ContentReviewBlocked", "message": "..." } }
  ]
}
```

### Streaming

When `stream=true`, response is SSE (Server-Sent Events):
```
data: {"data":[{"url":"https://..."}]}
data: [DONE]
```

### Error response

```json
{
  "error": {
    "code": "InvalidArgument",
    "message": "Invalid parameter",
    "status": 400
  }
}
```

## 7. Web search behavior

- **Only available on 5.0-lite** (via `tools: [{type: "web_search"}]`)
- Model autonomously decides whether to search based on prompt content
- Adds latency (~1-5s depending on search complexity)
- Check `usage.tool_usage.web_search` in response to see if search was actually performed (0 = no search)
- Best for: weather, current events, trending topics, product info, real-time data
- Skip for: static content, artistic descriptions, abstract concepts

## 8. Sequential/group generation

### Behavior

- `sequential_image_generation: "auto"` enables group mode
- `sequential_image_generation_options.max_images` controls count (1-15)
- All generated images are content-related (same character, style, or theme)
- Input images + max_images ≤ 15

### Generation modes

| Mode | Input | Output | Config |
|------|-------|--------|--------|
| Text-to-image | prompt only | 1 image | `sequential: disabled` |
| Single image-to-image | 1 image + prompt | 1 image | `sequential: disabled` |
| Multi image-to-image | 2-14 images + prompt | 1 image | `sequential: disabled` |
| Text-to-group | prompt only | N images | `sequential: auto` |
| Single image-to-group | 1 image + prompt | N images | `sequential: auto` |
| Multi image-to-group | 2-14 images + prompt | N images | `sequential: auto` |

## 9. Prompt optimization

### API format

```json
{
  "optimize_prompt_options": {
    "mode": "standard"
  }
}
```

### Modes

| Mode | Quality | Speed | Supported models |
|------|---------|-------|-----------------|
| `standard` | Higher | ~1-2s added | 5.0-lite, 4.5, 4.0 |
| `fast` | Normal | Less overhead | 4.0 only |

### What it does

The model rewrites your prompt to be more detailed and effective before generating the image. Useful when:
- User's prompt is short or vague
- You want better quality without manual prompt engineering
- Prompt is in a language the model handles less well

## 10. Common error codes

| HTTP | Code | Meaning | Fix |
|------|------|---------|-----|
| 400 | InvalidArgument | Bad parameter | Check request body |
| 401 | Unauthenticated | Invalid/missing API key | Check key |
| 403 | PermissionDenied | Model not enabled | Enable in Volcengine console |
| 429 | ResourceExhausted | Rate limited | Wait, retry (500 IPM limit) |
| 500 | Internal | Server error | Retry |
| 503 | Unavailable | Service temporarily down | Retry with backoff |

## 11. Performance notes

- **Latency**: Single image ~2-5s (2K), ~5-10s (4K). Sequential: ~3s per additional image.
- **Prompt optimization**: Adds ~1-2s (standard) or ~0.5s (fast)
- **Web search**: Adds ~1-5s depending on search complexity
- **Streaming**: First token ~1-2s, then continuous delivery
- **Timeout**: Script uses 300s timeout for generation

## 12. Troubleshooting

| Problem | Likely cause | Solution |
|---------|-------------|----------|
| `WARNING: may not support size 'X'` | Preset not supported by model | Use different preset or pixel format |
| Empty output | Prompt too vague | Add more detail, use prompt optimization |
| Images look different from prompt | Prompt too long, model ignoring details | Shorten to <300 Chinese chars |
| `ERROR: No image data` | API returned unexpected response | Check API key, retry |
| Black/corrupted image | Base64 truncated | Use URL format instead |
| Generation very slow | Using 4K or sequential | Expected, or try lower resolution |
| Web search not working | Using non-5.0-lite model | Switch to `doubao-seedream-5-0-260128` |
