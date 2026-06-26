---
name: text-to-carousel
description: Generate professional social media carousel images (Instagram, LinkedIn, TikTok, Xiaohongshu) from text content, articles, or URLs. Use when asked to create carousel, create slides, make social media graphics, convert article to carousel, generate carousel from text, text to carousel, or make Instagram/LinkedIn/TikTok carousel posts. Supports Chinese, English, Malay, and other languages. Outputs 1024x1024 PNG/JPG images.
---

# Text-to-Carousel

Generate professional carousel images from text content using Gemini image generation API.

## Requirements

- **Gemini API key** with billing enabled (check TOOLS.md or ask user)
- **Model**: `gemini-3-pro-image-preview` (REQUIRED for correct Chinese/CJK text rendering)
- **VPN**: May need US VPN if Gemini returns location errors

## Workflow

### 1. Gather Input

Determine carousel content from one of:
- Direct text/bullet points from user
- Article URL (fetch and extract key points)
- WordPress post (fetch via API)
- User-provided topic (generate content)

Collect:
- **Brand info**: name, colors, style (check TOOLS.md for known brands)
- **Product image**: URL or path (for CTA slide)
- **Slide count**: default 6 slides
- **Size**: default 1024x1024
- **Language**: detect from content

### 2. Plan Slide Structure

For health/product carousels, use this proven 6-slide structure:

| # | Type | Purpose |
|---|------|---------|
| 1 | Cover | Hook + brand + topic |
| 2 | Problem | Why reader should care |
| 3 | Solution | How product/topic solves it |
| 4 | Details | Key features, data, ingredients |
| 5 | Social Proof | Testimonials, results, evidence |
| 6 | CTA | Product image + buy/contact |

For other structures, see `references/prompt-patterns.md`.

### 3. Write Prompts

For each slide, write a Gemini prompt following these rules:

**Design prompt structure:**
```
Create a [SIZE] [STYLE_PRESET] Instagram slide for [BRAND].

LAYOUT:
- Background: [COLORS/GRADIENT]
- [ELEMENT DESCRIPTIONS WITH EXACT TEXT]
- "[SLIDE_NUM] / [TOTAL]" bottom right

CRITICAL: All Chinese/CJK text must be exactly as written above.
```

**Key rules:**
- Specify EXACT text to render — quote every Chinese character
- Include slide number (e.g., "01 / 06")
- Reference brand name and consistent color palette
- For CTA slide with product image: attach the image via `inlineData` in API call
- For style presets and templates, read `references/prompt-patterns.md`

### 4. Generate Images

Use `scripts/generate_carousel.py` or call Gemini API directly:

```python
import urllib.request, json, base64

API_KEY = "..."  # from TOOLS.md
MODEL = "gemini-3-pro-image-preview"  # REQUIRED for CJK text
url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

parts = [{"text": prompt}]
# For CTA slide with product image:
# parts.insert(0, {"inlineData": {"mimeType": "image/jpeg", "data": base64_image}})

payload = {
    "contents": [{"parts": parts}],
    "generationConfig": {"responseModalities": ["image", "text"]}
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
resp = urllib.request.urlopen(req, timeout=180)
result = json.loads(resp.read())
```

Add 5-second delay between slides to avoid rate limits.

### 5. Verify Output

After generation, verify each slide with vision model:
- Chinese/CJK text accuracy (character-level check)
- Design consistency across slides
- Product image visibility on CTA slide
- Brand elements present (logo, colors, slide numbers)

If text is garbled, regenerate that slide. Pro model rarely fails on Chinese but verify anyway.

## Model Selection Guide

| Model | Chinese Text | Design Quality | Speed | Use When |
|-------|-------------|---------------|-------|----------|
| `gemini-3-pro-image-preview` | ✅ Perfect | ✅ High | Slower | **Default choice** — CJK content |
| `gemini-2.5-flash-image` | ❌ Garbled | ✅ High | Fast | English-only content |
| `gemini-3.1-flash-image-preview` | ⚠️ Untested | ✅ High | Fast | Try for English content |

## Common Issues

| Problem | Solution |
|---------|----------|
| 429 quota exceeded | Check billing is linked to correct GCP project |
| Location not supported | Use US VPN |
| Chinese text garbled | Switch to `gemini-3-pro-image-preview` |
| Product image not matching | Attach actual product image via `inlineData` |
| Inconsistent design across slides | Include brand color hex codes and style description in every prompt |

## File Structure

```
text-to-carousel/
├── SKILL.md                          # This file
├── scripts/
│   └── generate_carousel.py          # Batch generation script (config-driven)
└── references/
    └── prompt-patterns.md            # Design presets, slide templates, tips
```
