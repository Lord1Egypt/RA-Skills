# QoderWork-PPT

Generate QoderWork-style presentations with AI. Describe your topic and get an editable `.pptx` file — automatically structured, styled, and ready to present.

## Features

- **14 professional templates** — cover, contents, section divider, left-text-right-image, 1/2/3/4-column cards, data highlight, quote, timeline, full-image statement, comparison, and thank-you
- **Smart template matching** — AI selects the best layout for each page based on content structure
- **High-fidelity export** — HTML → PPTX conversion preserves backgrounds, rounded corners, fonts, and colors
- **Lucide icon support** — use any [Lucide](https://lucide.dev) icon via `lucide:<icon-name>` syntax
- **AI image generation** — automatically generates or searches for contextual images
- **Resumable pipeline** — checkpoint recovery lets you re-run only the steps that changed

## Installation

```bash
# Clone or download this skill into your agent's skill directory
# For Cursor:
cp -r skills/qoderwork-ppt ~/.cursor/skills/QoderWork-amazing-ppt

# Install dependencies
cd ~/.cursor/skills/QoderWork-amazing-ppt && npm install
```

## Usage

Tell your AI agent:

> "Generate a QoderWork-style PPT about [your topic]"

The agent will follow the skill's 5-step pipeline:

1. **Generate content** → `output/content.md`
2. **Match templates** → `output/slides.json`
3. **Fill HTML templates** → `output/filled/*.html`
4. **Convert to PPTX** → `output/presentation.pptx`
5. **Deliver** the final file

## Templates

| # | Template | Layout |
|---|----------|--------|
| 01 | Cover | Title + subtitle + description on green background |
| 02 | Contents | Chapter list with accent bar |
| 03 | Section Divider | Chapter number + title + decorative image |
| 04 | Left Text, Right Image | 3 text blocks + large image |
| 05 | One Column | 2 side-by-side text cards |
| 06 | Two Columns | 2 icon + text cards |
| 07 | Three Columns | 3 icon + text cards |
| 08 | Four Columns | 2×2 icon + text cards |
| 09 | Data Highlight | 3 large numbers on dark background |
| 10 | Quote | Large quote text on dark background |
| 11 | Timeline | 3-step process flow with green connectors |
| 12 | Full Image | Full-bleed background image with text overlay |
| 13 | Comparison | Side-by-side two-column contrast (green vs gray) |
| 14 | Thank You | Bold thank-you with description |

## Requirements

- Node.js 18+
- npm dependencies: `jsdom`, `puppeteer`, `dom-to-pptx`

## License

MIT
