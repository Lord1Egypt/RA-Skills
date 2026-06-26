---
name: web-render-screenshot
description: >-
  Generate ultra-high-resolution screenshots from HTML content using Playwright.
  Default 4x device scale factor produces crisp, pixel-perfect output ideal for
  UI mockups, dashboards, data visualizations, infographics, website previews,
  and any content requiring accurate text rendering. Use when: (1) user wants a
  website/webpage screenshot or mockup image, (2) content has text, numbers,
  tables, charts that must be legible, (3) user wants a UI design rendered as an
  image, (4) HTML Canvas or data-driven visuals need to be exported as PNG/JPEG.
  Triggers: "website screenshot", "网页截图", "网站首页图", "UI mockup image",
  "dashboard image", "数据可视化图片", "render HTML to image". Prefer this over
  AI image generation (stable-image-ultra) when the content has structured text,
  data, or UI elements. AI image generation cannot produce readable text.
---

# Web Render Screenshot

Generate ultra-high-resolution PNG/JPEG images from HTML content via Playwright headless Chromium.

## When to Use

| Scenario | Use This Skill | Use AI Image Gen Instead |
|----------|---------------|------------------------|
| Website UI / mockup | ✅ | ❌ |
| Dashboard / data viz | ✅ | ❌ |
| Text-heavy infographic | ✅ | ❌ |
| Weather/finance/news page | ✅ | ❌ |
| Artistic illustration | ❌ | ✅ |
| Photorealistic scene | ❌ | ✅ |

**Rule**: If it has text that must be readable → use this skill.

## Quick Start

### Step 1: Create the HTML

Write a self-contained HTML file with inline CSS. Guidelines:

- Use system fonts or Google Fonts CDN for Chinese support: `"PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif`
- All styles inline (no external CSS files)
- Design for the target viewport (default: 1920×1080)
- Use emoji for icons when appropriate (universally supported)
- Ensure `overflow: hidden` on body if single-viewport capture is desired

### Step 2: Take the Screenshot

Use the bundled script:

```bash
python3 scripts/screenshot.py <input.html> [output.png] [options]
```

Or inline Python when the script cannot be invoked directly:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(
        viewport={"width": 1920, "height": 1080},
        device_scale_factor=4,  # 4x ultra-high res (default)
    )
    page.goto("file:///path/to/input.html", wait_until="networkidle")
    page.wait_for_timeout(1000)
    page.screenshot(path="output.png", full_page=True)
    browser.close()
```

### Step 3: Deliver

Output `MEDIA:<path>` for inline delivery, or use `openclaw message send` with `--force-document` for Telegram to avoid compression.

## Default Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `device_scale_factor` | **4** | Ultra-high resolution (4x). Output = viewport × 4 |
| `viewport.width` | 1920 | CSS pixel width |
| `viewport.height` | 1080 | CSS pixel height |
| `full_page` | true | Capture entire scrollable content |
| `wait` | 1000ms | Wait after page load for rendering |
| `format` | png | Lossless output (use jpeg for smaller files) |

### Resolution Reference

| Scale | Output for 1920×1080 viewport | File Size (typical) | Use Case |
|-------|-------------------------------|--------------------:|----------|
| 1x | 1920×1080 | ~100KB | Draft / preview |
| 2x | 3840×2160 | ~1-2MB | Standard high-res |
| 3x | 5760×3240 | ~3-5MB | High-quality print |
| **4x** | **7680×4320** | **5-8MB** | **Ultra-high (default)** |

## Script Options

```
python3 scripts/screenshot.py <html> [output] [options]

Arguments:
  html              HTML file path or URL
  output            Output file path (default: <input-stem>.png)

Options:
  --scale N         Device scale factor (default: 4)
  --width N         Viewport width (default: 1920)
  --height N        Viewport height (default: 1080)
  --full-page       Capture full page (default)
  --no-full-page    Capture viewport only
  --wait N          Wait time in ms (default: 1000)
  --format FORMAT   png or jpeg (default: png)
  --quality N       JPEG quality 0-100 (default: 92)
```

## HTML Design Tips

1. **Glassmorphism**: `backdrop-filter: blur(20px); background: rgba(255,255,255,0.12);`
2. **Gradient backgrounds**: `background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);`
3. **Card shadows**: `box-shadow: 0 8px 32px rgba(0,0,0,0.1);`
4. **Chinese fonts**: Always include fallback chain for cross-platform rendering
5. **Emoji icons**: Use emoji for weather/status/category icons — they render at any scale
6. **Grid layout**: CSS Grid for complex dashboards; Flexbox for simpler layouts

## File Size Management

If the output PNG is too large for delivery (e.g., >5MB for Telegram):

```python
from PIL import Image
img = Image.open("output.png")
img.save("output.jpg", "JPEG", quality=92, optimize=True)  # Usually 5-10x smaller
```

Or use `--format jpeg --quality 92` with the screenshot script.
