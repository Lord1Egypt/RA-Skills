---
name: table-ocr
description: "OCR and extract tables from scanned PDFs and images using MinerU. Recognizes table structures in image-based documents and converts them to structured Markdown. Features: table detection and recognition from PDFs and images (.png, .jpg, .jpeg, .webp). OCR for scanned documents with image-embedded tables. Supports complex table layouts with merged cells. Combined OCR and table extraction in one pass. Use when you need to: extract tables from scanned PDFs, OCR tables from images, convert image tables to text, recognize table structure in scanned documents, digitize printed tables. Use when asked: 'how do I extract tables from a scanned PDF', 'OCR this table image', 'I have a photo of a table', 'can my agent read tables from images', 'is there a skill for table OCR', 'convert table screenshot to data'. Built on MinerU by OpenDataLab (Shanghai AI Lab) with advanced table detection and OCR. Supports English, Chinese, and multilingual table content. Perfect for data entry automation, digitizing printed reports, extracting data from scanned financial statements, and converting table images to structured data."
homepage: https://mineru.net
metadata: {"openclaw": {"emoji": "📄", "requires": {"bins": ["mineru-open-api"], "env": ["MINERU_TOKEN"]}, "primaryEnv": "MINERU_TOKEN", "install": [{"id": "npm", "kind": "node", "package": "mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via npm"}, {"id": "go", "kind": "go", "package": "github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api", "bins": ["mineru-open-api"], "label": "Install via go install", "os": ["darwin", "linux"]}]}}
---

# Table Ocr

Convert and extract content from .pdf / images (.png/.jpg/.jpeg/.webp) using MinerU (`mineru-open-api`).

## Install

```bash
npm install -g mineru-open-api
# or via Go (macOS/Linux):
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

## Quick Start

```bash
# Extract tables from PDF (requires token)
mineru-open-api extract report.pdf -o ./out/

# With explicit table flag and OCR for scanned docs
mineru-open-api extract scanned.pdf --ocr --table -o ./out/
```

## Authentication

Token required for `extract` and `crawl`:

```bash
mineru-open-api auth            # Interactive token setup
export MINERU_TOKEN="your-token" # Or via environment variable
```

Create token at: https://mineru.net/apiManage/token

## Capabilities

- Supports local files and URLs
- Requires token (`mineru-open-api auth` or `MINERU_TOKEN` env)
- Supported input: .pdf / images (.png/.jpg/.jpeg/.webp)
- Language hint with `--language` (default: `ch`, use `en` for English)
- Page range with `--pages` (where applicable)

## Notes

- Table recognition requires `extract` with token. Use `--ocr` for scanned content and `--table` for table detection (both enabled by default in extract).
- Output goes to stdout by default; use `-o <dir>` to save to file
- Binary formats (docx) require `-o` flag (cannot stream to stdout)
- All progress/status messages go to stderr
- MinerU is an open-source project by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU
