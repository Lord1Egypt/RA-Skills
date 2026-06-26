---
name: seedream-volcengine
description: Generate or edit images with Volcengine Seedream (Doubao). Use for image creation requests incl. text-to-image, image-to-image, multi-reference fusion, sequential/group generation, PNG output, prompt optimization, web search, streaming. Supports Seedream 5.0-lite / 4.5 / 4.0.
---

# Seedream Image Generation

Generate and edit images via Volcengine Doubao-Seedream API using `{baseDir}/scripts/generate_image.py`.

This skill wraps the Volcengine Ark Image Generation API. It supports text-to-image, image editing, multi-reference fusion, sequential/group generation, PNG output, prompt optimization, web search, and streaming output. Works with Seedream 5.0-lite (default), 4.5, and 4.0 models.

## Quick start

```bash
# Text to image (simplest form)
uv run {baseDir}/scripts/generate_image.py --prompt "一只赛博朋克风格的猫"

# Image editing (with reference image)
uv run {baseDir}/scripts/generate_image.py --prompt "变为水墨画风格" --image "https://example.com/photo.jpg"

# Multi-reference fusion
uv run {baseDir}/scripts/generate_image.py --prompt "融合风格" --image "https://a.jpg" --image "https://b.jpg"

# Group/sequential generation
uv run {baseDir}/scripts/generate_image.py --prompt "四格漫画" --sequential --max-images 4

# List available models
uv run {baseDir}/scripts/generate_image.py --list-models
```

## API key

Set `VOLC_API_KEY` env var or pass `--api-key`. Never hardcode keys in scripts.

```bash
export VOLC_API_KEY="your-key"
# or
--api-key your-key
```

## Models

Default model: `doubao-seedream-5-0-260128` (5.0-lite). Override with `--model`.

### Model comparison

| Feature | 5.0-lite | 4.5 | 4.0 |
|---------|----------|-----|-----|
| Model ID | `doubao-seedream-5-0-260128` | `doubao-seedream-4-5-251128` | `doubao-seedream-4-0-250828` |
| Alias | `doubao-seedream-5-0-lite-260128` | — | — |
| Preset sizes | 2K, 3K, 4K | 2K, 4K | 1K, 2K, 4K |
| Output formats | png, jpeg | jpeg only | jpeg only |
| Prompt optimization | standard | standard | standard, fast |
| Streaming | ✅ | ✅ | ✅ |
| Web search | ✅ (only model) | ❌ | ❌ |
| Rate limit | 500 IPM | 500 IPM | 500 IPM |

### When to choose which model

- **5.0-lite (default)** — Best overall quality. Only model supporting PNG output, 3K resolution, and web search. Use for most tasks.
- **4.5** — High quality, slightly different style. Good alternative to 5.0-lite.
- **4.0** — Supports `--prompt-optimization fast` for quicker results. Good for rapid iteration. Also supports 1K for smaller/faster generation.

## Size and resolution

Two ways to specify size (cannot mix):

**Method 1 — Preset** (recommended for most cases):
```bash
--size 2K    # 2048x2048 (default)
--size 3K    # 3072x3072 (5.0-lite only)
--size 4K    # 4096x4096 (all models)
--size 1K    # 1024x1024 (4.0 only)
```

**Method 2 — Pixel format** (for custom aspect ratios):
```bash
--size 3840x2160    # 16:9 widescreen
--size 1080x1920    # 9:16 portrait
--size 1200x1200    # custom square
```

### Resolution table (preset sizes × aspect ratios)

When using preset sizes, the model picks the best aspect ratio based on your prompt. For precise control, use pixel format.

| Preset | 1:1 | 4:3 | 3:4 | 16:9 | 9:16 | 3:2 | 2:3 | 21:9 |
|--------|-----|-----|-----|------|------|-----|-----|------|
| 1K | 1024×1024 | 1152×864 | 864×1152 | 1280×720 | 720×1280 | 1248×832 | 832×1248 | 1512×648 |
| 2K | 2048×2048 | 2304×1728 | 1728×2304 | 2848×1600 | 1600×2848 | 2496×1664 | 1664×2496 | 3136×1344 |
| 3K | 3072×3072 | 3456×2592 | 2592×3456 | 4096×2304 | 2304×4096 | 3744×2496 | 2496×3744 | 4704×2016 |
| 4K | 4096×4096 | 4704×3520 | 3520×4704 | 5504×3040 | 3040×5504 | 4992×3328 | 3328×4992 | 6240×2656 |

### Pixel format constraints

- **5.0-lite**: total pixels ∈ [3,686,400 ~ 16,777,216], aspect ratio ∈ [1/16 ~ 16]
- **4.5**: total pixels ∈ [3,686,400 ~ 16,777,216], aspect ratio ∈ [1/16 ~ 16]
- **4.0**: total pixels ∈ [921,600 ~ 16,777,216], aspect ratio ∈ [1/16 ~ 16]

Examples:
- ✅ `3840x2160` → 8,294,400 pixels, ratio 1.78 → valid for all models
- ✅ `2160x3840` → same pixels, ratio 0.56 → valid for all models
- ❌ `1500x1500` → 2,250,000 pixels < 3,686,400 minimum → invalid for 5.0-lite/4.5

## Flags reference

### Required

- `--prompt` — Text description for image generation. Supports Chinese and English. Recommended under 300 Chinese characters or 600 English words.

### Model and size

- `--model` — Model ID (default: `doubao-seedream-5-0-260128`)
- `--size` — Preset (`1K`/`2K`/`3K`/`4K`) or pixel (`WIDTHxHEIGHT`, default: `2K`)

### Image input

- `--image` — Reference image URL or base64. Repeat for multiple images (max 14 total). Used for image editing and multi-reference fusion.

Supported input formats: jpeg, png, webp, bmp, tiff, gif, heic, heif.
Constraints: max 30MB per image, max 60MP (width×height), aspect ratio [1/16, 16].

### Output control

- `--output-format` — `jpeg` (default) or `png` (5.0-lite only)
- `--response-format` — `url` (default, 24h valid) or `b64_json` (base64 encoded)
- `--watermark` / `--no-watermark` — Enable/disable "AI生成" watermark (default: enabled)

### Generation mode

- `--sequential` — Enable group/sequential generation (multiple related images)
- `--max-images` — Number of images in sequential mode (1-15, default: 1)
- `--stream` — Enable streaming output (get results as generated)
- `--web-search` — Enable web search for real-time info (**5.0-lite only**). Uses `tools: [{type: "web_search"}]` API parameter.

### Prompt enhancement

- `--prompt-optimization` — `standard` (all models) or `fast` (4.0 only). Rewrites prompt for better results.

### Utilities

- `--list-models` — List available Seedream models and their capabilities
- `--api-key` — Volcengine API key (or set `VOLC_API_KEY` env)

## Use cases with complete examples

### 1. Text to image (basic)

```bash
uv run {baseDir}/scripts/generate_image.py --prompt "充满活力的特写肖像，模特眼神犀利，头戴雕塑感帽子，色彩拼接丰富，Vogue杂志封面美学"
```

### 2. Text to image (with specific size)

```bash
# 4K landscape
uv run {baseDir}/scripts/generate_image.py --prompt "壮丽的山川日出，金色阳光穿过云层" --size 4K

# Custom widescreen
uv run {baseDir}/scripts/generate_image.py --prompt "赛博朋克城市夜景" --size 3840x2160

# Portrait for phone wallpaper
uv run {baseDir}/scripts/generate_image.py --prompt "极简抽象艺术" --size 1080x1920
```

### 3. Image editing (single reference)

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "保持模特姿势和构图不变，将服装材质从银色金属改为完全透明的清水" \
  --image "https://example.com/original.jpg"
```

### 4. Multi-reference fusion

```bash
# Combine 2 images
uv run {baseDir}/scripts/generate_image.py \
  --prompt "将图1的服装换为图2的服装" \
  --image "https://example.com/person.jpg" \
  --image "https://example.com/clothing.jpg"

# Combine 3+ images
uv run {baseDir}/scripts/generate_image.py \
  --prompt "融合这三张图的风格特征，生成统一视觉" \
  --image "https://example.com/1.jpg" \
  --image "https://example.com/2.jpg" \
  --image "https://example.com/3.jpg"
```

### 5. Sequential/group generation

```bash
# Generate 4 related images
uv run {baseDir}/scripts/generate_image.py \
  --prompt "生成一组电影级科幻写实风的4张影视分镜" \
  --sequential --max-images 4

# With reference image
uv run {baseDir}/scripts/generate_image.py \
  --prompt "参考这张图，生成同角色在早晨、中午、晚上的连续画面" \
  --image "https://example.com/character.jpg" \
  --sequential --max-images 3
```

### 6. PNG output

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "高清产品图，白色背景，专业摄影灯光" \
  --output-format png
```

### 7. Prompt optimization

```bash
# Standard mode (higher quality, all models)
uv run {baseDir}/scripts/generate_image.py \
  --prompt "一只猫" \
  --prompt-optimization standard

# Fast mode (quicker, 4.0 only)
uv run {baseDir}/scripts/generate_image.py \
  --prompt "一只猫" \
  --model doubao-seedream-4-0-250828 \
  --prompt-optimization fast
```

### 8. Web search (real-time info, 5.0-lite only)

```bash
# Weather forecast image
uv run {baseDir}/scripts/generate_image.py \
  --prompt "制作一张上海未来5日的天气预报图，扁平化插画风格" \
  --web-search

# Current events
uv run {baseDir}/scripts/generate_image.py \
  --prompt "2026年最流行的时尚趋势海报" \
  --web-search
```

### 9. No watermark (commercial use)

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "产品宣传图，专业商业摄影" \
  --no-watermark
```

## Prompt writing tips

- **Language**: Supports Chinese and English. English tends to produce slightly better results for complex scenes, but Chinese works well too.
- **Length**: Under 300 Chinese characters or 600 English words recommended. Too long → model may ignore some details.
- **Specificity**: Be specific. "赛博朋克风格的猫，霓虹灯光，雨夜街道，4K，电影感" > "一只猫"
- **Style keywords**: Append style terms for control:
  - 水墨画风格 (ink painting)
  - 油画风格 (oil painting)
  - 写实摄影 (photorealistic)
  - 扁平化插画 (flat illustration)
  - 电影感 (cinematic)
  - 杂志封面 (magazine cover)
- **Structure**: For complex scenes, describe subject → composition → style → lighting → quality

## Output interpretation

Script stdout contains exactly one of:

- `MEDIA_URL: <url>` — Image download link. **Valid for 24 hours.** Use markdown: `![description](url)`
- `MEDIA_B64: <base64>` — Base64 encoded image data (when `--response-format b64_json`)
- `ERROR: <msg>` — Error occurred. Check message for details.

## Error handling

| Error | Cause | Fix |
|-------|-------|-----|
| `API key required` | No key provided | Set `VOLC_API_KEY` env or pass `--api-key` |
| `API request failed: 401` | Invalid API key | Check key at Volcengine console |
| `API request failed: 429` | Rate limited (500 IPM) | Wait and retry |
| `No image data in response` | API error | Check prompt/params, retry |
| `WARNING: may not support` | Model+size/format mismatch | Check model capabilities table above |

## Workflow

1. Parse user's image request to determine: text-to-image, editing, fusion, or sequential
2. Choose appropriate model (default: 5.0-lite unless specific need)
3. Determine size: use preset for general, pixel format for specific aspect ratio
4. Build and run the command with appropriate flags
5. Parse stdout for `MEDIA_URL:` or `MEDIA_B64:`
6. Display to user as markdown image or file
7. If URL, remind user it expires in 24h if they need to save it

## Input image requirements

- **Formats**: jpeg, png, webp, bmp, tiff, gif, heic, heif
- **Max size**: 30MB per image
- **Max pixels**: 60,000,000 (width × height)
- **Aspect ratio**: [1/16, 16]
- **Min dimension**: > 14px per side
- **Max images**: 14 per request
- **Total**: input images + output images ≤ 15

## Rate limits

All models: 500 images per minute (IPM). Plan batch operations accordingly.

## Full reference

For detailed API parameter docs, see [references/REFERENCE.md](references/REFERENCE.md).
