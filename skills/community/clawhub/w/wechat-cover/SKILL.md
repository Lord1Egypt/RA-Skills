---
name: wechat-cover
description: Generate WeChat official account cover images with proper 2.35:1 aspect ratio. Supports OpenAI DALL-E and Gemini image generation with customizable styles.
---

# WeChat Cover Image Generator

Generate professional cover images for WeChat official account articles with multi-provider support (OpenAI DALL-E or Gemini).

## What Makes a Good WeChat Cover?

- **Aspect ratio**: 2.35:1 (wide cinematic format)
- **Time-prefixed filename**: Use `YYYY-MM-DD-wechat-cover-title.png` format.
- **No text**: WeChat overlays the article title
- **Visual focus**: One clear focal point, not cluttered
- **Clean & bright**: Modern aesthetic suitable for WeChat subscription feeds

## Usage

**Basic generation (OpenAI by default):**
```bash
uv run skills/wechat-cover/scripts/generate.py \
  --title "Your Article Title" \
  --topic "AI tools"
```

**With Gemini provider:**
```bash
uv run skills/wechat-cover/scripts/generate.py \
  --title "Your Article Title" \
  --topic "AI tools" \
  --provider gemini
```

**With custom base URL (OpenAI-compatible proxy):**
```bash
export OPENAI_BASE_URL="https://your-proxy.com/v1"
export OPENAI_API_KEY="sk-..."

uv run skills/wechat-cover/scripts/generate.py \
  --title "Your Article Title" \
  --topic "AI tools" \
  --provider openai
```

## Parameters

| Parameter       | Required | Description                                              |
| ---------------| -------- | -------------------------------------------------------- |
| `--title`      | Yes      | Article title (used to understand context)               |
| `--topic`      | Yes      | Topic/category (e.g., "technology", "AI")              |
| `--provider`   | No       | `openai` (default) or `gemini`                         |
| `--base-url`   | No       | OpenAI-compatible base URL (env: OPENAI_BASE_URL)        |
| `--model`      | No       | Model name override                                      |
| `--style`      | No       | Style variant: default, tech, business, lifestyle, creative |
| `--filename`   | No       | Output filename (auto-generated if omitted)               |
| `--resolution` | No       | 1K/2K/4K (default: 2K)                                |
| `--output-dir` | No       | Output directory (default: current directory)             |
| `--api-key`    | No       | API key (settings.json > env var)                        |

## Configuration File (settings.json)

```json
{
  "openai": {
    "api_key": "sk-...",
    "base_url": "https://your-proxy.com/v1",
    "model": "dall-e-3"
  },
  "gemini": {
    "api_key": "your-gemini-key",
    "model": "gemini-3-pro-image-preview"
  },
  "default_provider": "openai",
  "default_resolution": "2K",
  "default_style": "default"
}
```

**OpenAI-compatible proxies** (e.g. palebluedot, new-api) that use `/v1/chat/completions` for image generation are auto-detected and supported. Set `base_url` and `model` accordingly.

**Priority order:** CLI argument > settings.json > environment variable

## Style Variants

All styles follow Anthropic's Claude design language — clean, bright, and restrained:

| Variant   | Description                                              |
|-----------|----------------------------------------------------------|
| `default` | Warm minimalist: cream, beige, coral, sage. Organic shapes, soft lighting, generous whitespace |
| `tech`    | Cool modern: off-white, slate blue, lavender, cyan. Geometric lines, glass morphism, grid composition |
| `business`| Professional: warm white, navy, charcoal, amber. Architectural lines, natural light, clear hierarchy |
| `lifestyle`| Warm organic: cream, blush, sage, golden. Natural textures, golden-hour light, handcrafted feel |
| `creative`| Refined bold: white, coral red, teal, gold. Abstract geometric, asymmetric, paper-cut aesthetic |

## Environment Variables

| Variable           | Provider  | Description                              |
|-------------------|-----------|------------------------------------------|
| `OPENAI_API_KEY`  | openai    | OpenAI API key                           |
| `OPENAI_BASE_URL` | openai    | OpenAI-compatible proxy URL (optional)    |
| `GEMINI_API_KEY`  | gemini    | Gemini API key                           |

## Resolution Guide

| Resolution | Dimensions (OpenAI) | Dimensions (Gemini) | Use Case        |
|------------|---------------------|---------------------|-----------------|
| `1K`       | 1024×1024           | 1024×1024           | Preview/thumbnail |
| `2K`       | 1792×1024           | 2048×2048           | Standard cover   |
| `4K`       | 1792×1024           | 4096×4096           | High quality     |

## Examples

**Tech article with OpenAI:**
```bash
uv run skills/wechat-cover/scripts/generate.py \
  --title "2024年最值得学习的编程语言" \
  --topic "technology" \
  --style tech \
  --resolution 2K
```

**Business article with Gemini:**
```bash
uv run skills/wechat-cover/scripts/generate.py \
  --title "职场沟通技巧" \
  --topic "business" \
  --style business \
  --provider gemini
```

**Lifestyle article:**
```bash
uv run skills/wechat-cover/scripts/generate.py \
  --title "周末去哪儿：杭州小众咖啡馆推荐" \
  --topic "lifestyle" \
  --style lifestyle \
  --output-dir ./covers
```

## Output

- Auto-cropped and resized to **900×383** (2.35:1 WeChat cover format)
- Saves to specified directory (default: current directory)
- Filename format: `YYYY-MM-DD-wechat-cover-{title-slug}.png`
- Format: PNG for best quality

## Requirements

- `uv` installed for Python script execution
- `Pillow` (`pip install Pillow`) for image cropping/resizing
- **For OpenAI provider**: OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- **For Gemini provider**: Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
