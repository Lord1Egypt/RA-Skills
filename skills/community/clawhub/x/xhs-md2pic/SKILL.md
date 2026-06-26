---
name: xhs-md2img
description: Convert Markdown text to beautiful Xiaohongshu (XHS) style card images with 5 themes, deterministic browser screenshot rules, auto-pagination, smart title extraction, and AI-generated decorative backgrounds.
metadata:
  clawdbot:
    emoji: "🎴"
    requires:
      env: [DASHSCOPE_API_KEY]
      anyBins: [python3, python]
    primaryEnv: DASHSCOPE_API_KEY
    permissions:
      network: true
      filesystem: true
---

# xhs-md2img

Convert Markdown text into Xiaohongshu (XHS) style multi-page card images with deterministic browser rendering and screenshot behavior.

## Overview

This skill renders Markdown content as publish-ready XHS card images and is designed to run reliably in browser screenshot services.

**Use cases:**
- Convert long-form content into XHS-ready multi-image posts
- Generate styled card images from Markdown articles
- Produce stable multi-page screenshots with consistent size and pagination

## Quick Start

Minimal input — just provide Markdown text:

```json
{
  "markdown": "## 5个提升效率的方法\n\n**1. 番茄工作法** — 25分钟专注 + 5分钟休息\n\n**2. 任务批处理** — 把相似的事情集中做\n\n> 效率不是做更多的事，而是用更少的时间做对的事。"
}
```

Default export is one 1125x1500 PNG card (`375x500` CSS px at `export_scale=3`).

## Input Parameters

See `templates/input-schema.json` for the full schema.

Core content/style params:
- `markdown` (required): Markdown content. Use `---` for manual page breaks.
- `title`, `author`, `description`: Cover metadata.
- `theme`: `default`, `monokai`, `nord`, `sakura`, `mint`.
- `font_family`: `sans-serif`, `serif`, `wenkai`.
- `padding`: `small`, `medium`, `large`.
- `show_cover`: Whether to show cover block.
- `bg_style`: `ai_art` or `none`.

Browser screenshot control params:
- `card_width` / `card_height`: Single card CSS size (default `375x500`).
- `export_scale`: Pixel ratio multiplier (default `3`).
- `viewport_width` / `viewport_height`: Browser viewport size for rendering stability.
- `page_gap`: Vertical gap between cards in DOM (default `20`).
- `pagination_mode`: `mixed` (default), `auto`, `manual_only`.
- `max_pages`: Hard limit to avoid runaway pagination.
- `show_page_number`: Whether to render `1 / N` indicator.
- `avoid_orphan_heading`: Keep headings with at least one following block.
- `last_page_compact`: Shrink last card when content is short.

## Deterministic Browser Screenshot Contract

Use these hard rules for consistent XHS-like output:

1. **Fixed card geometry**
- Card ratio must stay `3:4` (`375x500` base).
- Output pixel size must be `card_width * export_scale` by `card_height * export_scale`.
- Prefer `export_scale=3` for XHS quality (`1125x1500`).

2. **Stable browser context**
- Run headless browser with `deviceScaleFactor=export_scale`.
- Keep zoom at 100%; do not use browser print mode.
- Use explicit viewport (recommended `440x760` for default card).

3. **Render readiness gates (must pass before pagination/screenshot)**
- Wait for `document.fonts.ready`.
- Wait until `document.body[data-fonts-loaded="true"]` is present.
- Wait 2 consecutive animation frames with unchanged `.xhs-card` bounding boxes.

4. **Element-only screenshot**
- Screenshot each `.xhs-card` element, never full page + crop.
- Disable animations/transitions during capture.
- Export PNG only.

For implementation runbook and failure checks, read `references/browser-screenshot-spec.md`.

## Rendering Pipeline

### 1. Smart Format (LLM)

If input is plain text, reformat to Markdown without changing wording:
- Extract a short cover title (10-20 chars)
- Add structure (`##`, `**`, lists, quotes)
- Preserve all original symbols/emojis/hashtags verbatim

### 2. Markdown to HTML

Use `python-markdown` with extensions:
- `tables`, `fenced_code`, `codehilite`, `nl2br`, `sane_lists`, `smarty`, `attr_list`, `md_in_html`, `toc`
- Convert XHS hashtags (`#tag#`) into styled pills

### 3. HTML/CSS Card Construction

Use `templates/card-template.html` with fixed card dimensions and theme variables.

Card layers:
- `.xhs-card`: fixed-size card container
- `.bg-art`: optional low-opacity decorative image
- `.card-inner`: content layer above background

### 4. Pagination Rules (Critical)

Apply pagination in DOM, not PDF/print pagination.

Priority order:
1. Split by manual separators (`---`) first.
2. Within each segment, split by top-level block elements.
3. If `avoid_orphan_heading=true`, never place a heading as the last visible block on a page.
4. Keep list/table/code blocks intact when possible.
5. If a single block exceeds one page, split safely:
- list: split by `li`
- table: split by row groups
- code/pre: split by line groups
- paragraph: split by sentences as final fallback

Overflow rule:
- Page content area must satisfy `scrollHeight <= clientHeight`.
- Keep a bottom safety space (~16 CSS px) to avoid visual clipping.

### 5. Multi-Page Screenshot Output

For each page:
- Create one `.xhs-card` node
- Add optional page indicator `page / total_pages`
- Capture element screenshot in PNG
- Return pages ordered by index

Output shape:

```json
{
  "__type": "xhs_card_images",
  "title": "Extracted or provided title",
  "theme": "default",
  "total_pages": 3,
  "pages": [
    {
      "index": 0,
      "page": 1,
      "total_pages": 3,
      "width": 1125,
      "height": 1500,
      "size_bytes": 123456,
      "url": "https://...",
      "oss_uploaded": true
    }
  ]
}
```

If OSS is not configured, return `data_uri` for each page.

## XHS Visual Quality Checklist

Before returning images, verify:
- Exact size per page matches export formula
- No cropped text at bottom edge
- Heading/body spacing is consistent across pages
- Page number style is subtle (low opacity)
- Last page has no large empty area when `last_page_compact=true`

## Theme System

5 built-in themes are defined in `references/themes.md`.

| Theme | Background | Feel |
|-------|-----------|------|
| `default` | White `#ffffff` | Clean, professional |
| `monokai` | Dark `#272822` | Tech, developer-oriented |
| `nord` | Deep blue `#2e3440` | Nordic minimalist |
| `sakura` | Soft pink `#fff5f5` | Warm, feminine |
| `mint` | Light green `#f0faf4` | Fresh, natural |

## AI Background Generation

When `bg_style: "ai_art"`:
1. LLM generates an abstract decorative prompt from content/theme
2. Provider auto-select:
- Gemini first when `LLM_BASE_URL` is Google
- DashScope wanx fallback when available
3. Blend into card with low opacity (8-18% by theme)

Constraints:
- Decorative only (watercolor/bokeh/geometric/plant silhouettes)
- No text, no faces, no explicit objects

See `references/api-reference.md` for provider API details.

## Privacy & External Endpoints

Network calls may include:
- LLM API: format + title + bg prompt generation
- DashScope/Gemini: background image generation (prompt only)
- Alibaba Cloud OSS: optional output image upload

No raw user document is sent to image models; only abstract prompt text is used.
