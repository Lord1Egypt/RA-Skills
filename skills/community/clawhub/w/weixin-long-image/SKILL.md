---
name: weixin-long-image
description: >-
  Turn Weixin/Wechat replies into readable image cards by rendering HTML into long PNG screenshots. Use when a Weixin direct-chat reply would exceed 150 Chinese characters, when the user asks for a card, a beautiful visual, or a poster-like output, or when the content benefits from HTML-based rendering such as charts, tables, curves, timelines, relation diagrams, comparison layouts, dashboards, or mixed text-image presentation. First write HTML, then render it into an image.
---

# Weixin Long Image

Use this skill to turn rich HTML layouts into long PNGs for Weixin delivery.

## Core Rule

In Weixin direct chats, if the reply body for the user would exceed 150 Chinese characters, treat this as a hard rule: prefer this skill over a long plain-text message.

## When To Use

Use this skill when any of these is true:

- The Weixin reply would be long and hard to read as plain chat text.
- The user asks for a card, poster, beautiful layout, or visually polished output.
- The content needs HTML rendering power, such as:
  - charts
  - tables
  - timelines
  - curves / trend visuals
  - relation diagrams
  - dashboards
  - mixed text + image layouts
- You want stable final presentation rather than chat-native formatting.

## Default Visual Standard

Unless the user explicitly wants a poster/card/dashboard style, default to a **WeChat public-article layout**, not a centered floating card.

## Night Rule

In Asia/Shanghai time, if the image is being prepared at **22:00 or later**, default to a **dark-mode article template** to reduce eye strain, unless the user explicitly asks for a light theme.

### Default article layout

- Use a plain white page background.
- Keep only moderate side margins for readability.
- Do **not** wrap the whole article in a large rounded card with heavy shadow.
- Prefer continuous reading flow, like a WeChat public account article.
- Use readable typography, generous line height, and responsive images.

### Default dark article layout after 22:00

- Use a dark page background with softened contrast.
- Keep the same article flow and margins as the daytime template.
- Avoid excessive glow, neon accents, or dashboard-style visuals unless explicitly requested.
- Preserve readability first: muted metadata, bright headings, comfortable code blocks, and responsive images.

### Use card style only when appropriate

Reserve card/poster/dashboard styling for cases like:

- cover cards
- poster-like announcements
- KPI / dashboard views
- side-by-side comparison blocks
- highly visual share cards

For ordinary long articles, analysis notes, translated writeups, and image-heavy explanations, prefer article layout.

## Reusable Templates

Use `assets/wechat-article-template.html` as the default starting point for daytime article-style pages.
Use `assets/wechat-article-template-dark.html` as the default starting point for article-style pages prepared at or after 22:00 Asia/Shanghai.

They provide:

- WeChat-like article spacing
- narrower side margins
- no outer card shell
- responsive images
- readable tables
- wrapped code blocks
- simple note/tip blocks
- matched light/dark article styles

## Workflow

1. Write a complete HTML document first.
2. For article-like content, choose the template by time:
   - before 22:00 Asia/Shanghai → `assets/wechat-article-template.html`
   - at or after 22:00 Asia/Shanghai → `assets/wechat-article-template-dark.html`
3. Render the HTML with `scripts/render_long_image.py`.
4. Send the PNG with the `message` tool using an absolute local path.
5. After the `message` send succeeds, immediately delete temporary render artifacts (`.png` and temporary `.html`) unless the user explicitly asked to keep them.
6. In Weixin direct chats, use `message` for any progress update; do not rely on multi-part assistant text arriving in order.

## Quick Start

```bash
python3 scripts/render_long_image.py \
  --input /absolute/path/to/page.html \
  --png-out /absolute/path/to/output.png
```

You may also pass raw HTML via `--input` or stdin.

## Input Rules

- The script accepts complete HTML only.
- `--input` can be a file path or inline HTML.
- If `--input` is omitted, read HTML from stdin.
- `--html-out` is optional.
  - If provided, persist the rendered HTML there.
  - If omitted and `--input` is an existing HTML file, reuse that file.
  - If omitted and the source is inline HTML or stdin, create a temporary HTML file and auto-delete it after rendering.
- If the source content starts as text, convert it into HTML first.

## Rendering Guidance

- Build for phone reading first.
- For long-form articles, prefer article layout over card layout.
- For tables, charts, diagrams, and mixed media, define layout explicitly in CSS instead of relying on browser defaults.
- If images are embedded in the HTML, make them responsive with `max-width: 100%` unless overflow is intentional.
- Use absolute output paths so the PNG can be delivered reliably.
- If the content is sensitive, write outputs inside the workspace or `/tmp`, send the PNG, then remove temporary files if appropriate.

## Sending

Use `message` with the generated PNG path.

- `action=send`
- `channel=openclaw-weixin`
- `media=/absolute/path/to/output.png`
- `message=一句很短的说明`

### Post-send cleanup

For temporary outputs, once `message` reports success, delete the local render artifacts immediately.

Typical cleanup:

```bash
rm -f /absolute/path/to/output.png /absolute/path/to/output.html
```

Rules:

- Prefer writing temporary outputs under `/tmp`.
- Delete the PNG after a successful send unless the user asked to keep the file.
- Delete the HTML too when it is only an intermediate artifact.
- If `render_long_image.py` used inline HTML or stdin without `--html-out`, the script already auto-deletes its temporary HTML file; you still need to delete the PNG after send.

After a user-visible `message` send, reply with `NO_REPLY` to avoid duplicates.

## Troubleshooting

- If Playwright cannot launch Chromium, verify the local Playwright browser runtime is installed.
- If the screenshot looks clipped, increase `--width` or fix the HTML/CSS layout first.
- If the result is too tall, split the content into multiple HTML pages and render multiple images.
- If the content is short and visually simple, skip this skill and reply normally.

## Assets

- `assets/wechat-article-template.html`: Default daytime HTML template for WeChat-article-style long images.
- `assets/wechat-article-template-dark.html`: Default night-mode HTML template for WeChat-article-style long images after 22:00 Asia/Shanghai.

## Script

- `scripts/render_long_image.py`: Render complete HTML into a long PNG screenshot.
