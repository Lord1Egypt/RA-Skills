---
name: md-to-pdf
description: Use when converting markdown files to PDF with styling, code highlighting, and CJK support
---

# MD to PDF Conversion

## Overview

Converts markdown files to styled PDF documents using Node.js, marked, and puppeteer-core. Supports Chinese/CJK text, code syntax highlighting, tables, and images.

## When to Use

- User asks to convert a `.md` file to PDF
- Need to generate a printable document from markdown
- Creating offline documentation or reports
- Sharing formatted technical documents

## Prerequisites

- Node.js installed (v18+ recommended)
- Google Chrome or Microsoft Edge browser installed

## Quick Start

```bash
# Convert a markdown file to PDF
node convert.js input.md

# Specify output file
node convert.js input.md output.pdf

# Without page numbers
node convert.js input.md --no-page-numbers
```

## Installation

First-time setup in the target project directory:

```bash
mkdir -p .md-to-pdf-tool && cd .md-to-pdf-tool
npm init -y
npm install marked@4.3.0 puppeteer-core@19.11.1
```

Then copy the `convert.js` script from this skill's directory.

## Features

| Feature | Support |
|---------|---------|
| Headings (H1-H6) | Styled with hierarchy |
| Code blocks | Syntax highlighting via highlight.js |
| Tables | Bordered with zebra striping |
| Lists | Bulleted and numbered |
| Images | Embedded (relative paths resolved) |
| Links | Clickable in PDF |
| CJK/Chinese | Full support |
| Page numbers | Bottom center by default |

## Customization

Edit the CSS in `convert.js` to customize:

- **Font**: Change `font-family` in `body` style
- **Colors**: Modify `color` and `background` values
- **Margins**: Adjust `--marginTop`, `--marginBottom`, etc. in options
- **Code theme**: Change `pre` and `code` background colors

## Common Issues

| Issue | Solution |
|-------|----------|
| Browser not found | Set `CHROME_PATH` or `EDGE_PATH` environment variable |
| Permission denied | Use Edge instead of Chrome, or run with elevated permissions |
| ESM module errors | Use marked@4.3.0 and puppeteer-core@19.11.1 (CommonJS compatible) |
| Large file timeout | Increase timeout in `page.setContent()` options |

## Implementation

The conversion script uses:

1. **marked** - Parse markdown to HTML
2. **puppeteer-core** - Launch headless browser to render HTML
3. **Page.pdf()** - Generate PDF from rendered page

See `convert.js` in this skill directory for the complete implementation.
