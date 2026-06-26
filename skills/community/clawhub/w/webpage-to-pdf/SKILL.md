---
name: web-to-pdf
description: Convert a web page to PDF, especially web-based slide decks and presentations (reveal.js, impress.js, custom JS slideshows, scroll-based decks). Use when the user wants to save a website as PDF, capture slides to PDF, convert an online presentation to PDF, export a web deck, or screenshot a web page into a document. Also use when the user pastes a URL and says "turn this into a PDF", "save as PDF", "export this", or "make a PDF of this".
---

# Web to PDF

Capture any web page — especially slide-based presentations — as a multi-page PDF using a headless browser.

## How it works

A bundled Playwright script screenshots each slide (or the full page) as PNG, then assembles them into a PDF via Pillow. It auto-detects the navigation model:

| Model | Detection | Examples |
|-------|-----------|---------|
| **reveal.js** | `.reveal` element + `Reveal` JS API | reveal.js decks |
| **Vertical scroll** | Page height > 1.5× viewport, multiple slide elements | Custom JS slide decks with stacked sections |
| **Keyboard** | Multiple slide elements, not scrollable | impress.js, deck.js, arrow-key decks |
| **Single page** | No slide structure detected | Regular web pages, articles |

## Prerequisites

The script bundles its own `package.json`. On first use (or if `node_modules` is missing), install dependencies:

```bash
cd ${CLAUDE_SKILL_DIR}/scripts && npm install && npx playwright install chromium
```

Pillow (Python) is also required for PNG-to-PDF assembly:

```bash
pip install Pillow
```

## Usage

Run the capture script:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/capture.mjs <url> <output.pdf> [options]
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--width N` | 1920 | Viewport width in pixels |
| `--height N` | 1080 | Viewport height in pixels |
| `--wait N` | 1000 | Milliseconds to wait per slide for animations |
| `--max-slides N` | 50 | Safety cap on number of slides |

### Examples

```bash
# Presentation deck at 1080p
node ${CLAUDE_SKILL_DIR}/scripts/capture.mjs https://example.com/pitch output.pdf

# Narrow viewport for mobile-style capture
node ${CLAUDE_SKILL_DIR}/scripts/capture.mjs https://example.com/page doc.pdf --width 1280 --height 720

# Slow animations, give extra time
node ${CLAUDE_SKILL_DIR}/scripts/capture.mjs https://example.com/deck slides.pdf --wait 2000
```

## Workflow

1. Check that `playwright` and `Pillow` are installed; install if missing
2. Run the capture script with the user's URL and desired output path
3. Verify the output — check page count and spot-check a few pages by reading the PDF or individual screenshots
4. Report the result to the user (page count, file size, output path)

## Troubleshooting

- **Slides all identical**: The navigation detection may have picked the wrong model. Try adding `--wait 2000` for slower transitions, or check if the site requires interaction (cookie banners, login) before slides are accessible.
- **Missing content / animations not rendered**: Increase `--wait` to give JS more time to render.
- **Blank pages**: Some sites lazy-load content; the scroll-based capture handles this by scrolling to each slide. If keyboard navigation produces blanks, the site may actually be scroll-based.
- **Too few / too many pages**: Check `--max-slides` and verify the slide selector detected is correct by inspecting the script's console output.
