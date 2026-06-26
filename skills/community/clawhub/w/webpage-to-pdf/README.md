# web-to-pdf

A skill that converts web pages — especially slide-based presentations — into multi-page PDFs using a headless browser.

## What it does

Captures any web page as a PDF by screenshotting each slide (or the full page) with Playwright, then assembling the PNGs into a PDF via Pillow. It auto-detects how the page navigates between slides:

| Navigation Model | Detection | Examples |
|------------------|-----------|---------|
| **reveal.js** | `.reveal` element + `Reveal` JS API | reveal.js decks |
| **Vertical scroll** | Page height > 1.5× viewport, multiple slide elements | Custom JS decks with stacked sections |
| **Keyboard** | Multiple slide elements, not scrollable | impress.js, deck.js, arrow-key decks |
| **Single page** | No slide structure detected | Regular web pages, articles |

## Installation

### As a skill

```bash
# Clone into your skills directory
git clone https://github.com/pearyj/web-to-pdf-skill.git ~/.claude/skills/web-to-pdf

# Install dependencies
cd ~/.claude/skills/web-to-pdf/scripts
npm install
npx playwright install chromium
pip install Pillow
```

### Via ClawHub

```bash
clawhub install web-to-pdf
```

## Usage

Once installed, Claude will automatically use this skill when you say things like:

- "Turn this into a PDF: https://example.com/slides"
- "Save this web page as PDF"
- "Export this presentation to PDF"

Or invoke it directly with `/web-to-pdf`.

### Standalone usage

```bash
node scripts/capture.mjs <url> <output.pdf> [options]
```

#### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--width N` | 1920 | Viewport width in pixels |
| `--height N` | 1080 | Viewport height in pixels |
| `--wait N` | 1000 | Milliseconds to wait per slide for animations |
| `--max-slides N` | 50 | Safety cap on number of slides |

## Prerequisites

- **Node.js** 18+
- **Python 3** with Pillow (`pip install Pillow`)
- **Playwright** (`npm install playwright && npx playwright install chromium`)

## License

MIT
