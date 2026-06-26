# PDF to Markdown Converter

Convert PDF documents to clean, structured Markdown using IBM Docling AI with high-accuracy table and image extraction.

## Features

- **Text extraction** with formatting preservation (headers, bold, italic, lists)
- **Table extraction** using IBM's TableFormer AI model (~93.6% accuracy)
- **Image extraction** to cache directory with paths in output
- **Aggressive caching** - extract once, reuse forever

## Installation

```bash
cd ~/.claude/skills/pdf-to-markdown
uv venv .venv
uv pip install --python .venv/bin/python pymupdf docling docling-core
```

## Usage

```bash
# Basic conversion (outputs to document.md)
.venv/bin/python scripts/pdf_to_md.py document.pdf

# Custom output path
.venv/bin/python scripts/pdf_to_md.py document.pdf output.md
```

## Options

| Option | Description |
|--------|-------------|
| `--no-progress` | Disable progress indicator |
| `--clear-cache` | Clear cache for this PDF and re-extract |
| `--clear-all-cache` | Clear entire cache |
| `--cache-stats` | Show cache statistics |

## Project Structure

```
scripts/
  pdf_to_md.py    # Main CLI tool
  extractor.py    # PDF extraction using Docling
```

## Cache

PDFs are cached in `~/.cache/pdf-to-markdown/`. Cache is invalidated when:
- Source PDF is modified
- Extractor version changes
- Explicitly cleared with `--clear-cache`

## License

MIT
