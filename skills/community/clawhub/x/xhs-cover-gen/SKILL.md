---
name: xhs-cover
description: Generate Xiaohongshu (小红书) cover images with Chinese text overlays. Use when asked to create social media cover images, Xiaohongshu post images, or RED post covers. Supports split-screen comparisons, gradient backgrounds, and card layouts. Combines Pollinations.ai for AI base images with PIL for precise Chinese typography. Triggers on phrases like "小红书封面", "生成封面图", "make a cover image", "xhs cover", "xiaohongshu image".
---

# XHS Cover Generator

Generate publication-ready Xiaohongshu (小红书) cover images (1080×1440, 3:4 ratio) with Chinese text overlays.

## How It Works

1. **Base image**: Either AI-generated via Pollinations.ai (`--base-prompt`) or solid color background
2. **Text overlay**: Chinese text rendered with Noto Sans CJK font via PIL (auto-downloaded on first run)
3. **Output**: JPEG at 95% quality, ready to post

## Styles

| Style | Use Case | Example |
|-------|----------|---------|
| `split` | A vs B comparisons | PUA式AI vs 暖心AI |
| `gradient` | Single-topic posts | AI工具测评 |
| `card` | Clean/minimal posts | 效率技巧分享 |

## Usage

Run the generate script:

```bash
python3 scripts/generate.py \
  --title "主标题文字" \
  --subtitle "副标题" \
  --style split \
  --left-label "左侧标签" \
  --right-label "右侧标签" \
  --base-prompt "english prompt for AI base image" \
  --output cover.jpg
```

### Parameters

- `--title` (required): Main title text (Chinese OK)
- `--subtitle`: Secondary text line
- `--tagline`: Bottom tagline (split style only)
- `--style`: `split` | `gradient` | `card` (default: gradient)
- `--left-label` / `--right-label`: Labels for split style
- `--left-color` / `--right-color`: R,G,B colors (default: red/green)
- `--base-prompt`: English prompt for Pollinations.ai base image; if omitted, uses solid color
- `--width` / `--height`: Dimensions (default: 1080×1440)
- `--output`: Output path (default: cover.jpg)

### Examples

**Split comparison cover:**
```bash
python3 scripts/generate.py \
  --title "同一个问题，两种AI的回答" \
  --subtitle "差距有多大?" \
  --tagline "一招设置反PUA人设" \
  --style split \
  --left-label "PUA式AI" --right-label "暖心AI" \
  --base-prompt "cute flat illustration, split screen, left pink sad robot, right green happy robot, kawaii pastel" \
  --output pua-vs-warm.jpg
```

**Gradient tool review:**
```bash
python3 scripts/generate.py \
  --title "2026最强AI编程助手" \
  --subtitle "Cursor vs Copilot vs Windsurf" \
  --style gradient \
  --base-prompt "futuristic code editor interface, purple blue gradient, clean minimal" \
  --output coding-tools.jpg
```

**Card style tip:**
```bash
python3 scripts/generate.py \
  --title "用AI写周报只需30秒" \
  --subtitle "打工人效率神器" \
  --style card \
  --left-color "70,130,255" \
  --output weekly-report.jpg
```

## Requirements

- Python 3 with Pillow (`PIL`)
- `curl` for font download and Pollinations.ai
- Internet access (first run downloads ~17MB CJK font, cached in /tmp)

## Typical Workflow (for agents)

1. Determine the post topic and style
2. Craft an English prompt for the base image (descriptive, aesthetic keywords)
3. Run generate.py with Chinese title/subtitle
4. Send the resulting image to the user
