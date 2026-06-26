---
name: scan-to-markdown
description: "OCR document extraction - extract text from scanned documents, photos, and images using OCR. Use when reading scanned PDFs, photographed pages, handwritten notes, or any document that needs optical character recognition."
homepage: https://mineru.net
metadata: {"openclaw":{"emoji":"🔍","requires":{"bins":["mineru-open-api"]},"install":[{"id":"npm","kind":"node","package":"mineru-open-api","bins":["mineru-open-api"],"label":"Install via npm"},{"id":"uv","kind":"uv","package":"mineru-open-api","bins":["mineru-open-api"],"label":"Install via uv"},{"id":"go","kind":"go","package":"github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api","bins":["mineru-open-api"],"label":"Install via go install","os":["darwin","linux"]}]}}
---

# Scan to Markdown - OCR for Scanned Docs

Extract text from scanned documents and images using OCR via MinerU Open API. No API key required.

## Quick Start

```bash
# Scan to Markdown - OCR for Scanned Docs
mineru-open-api flash-extract scanned.pdf

# Scan to Markdown - OCR for Scanned Docs
mineru-open-api flash-extract page-photo.jpg

# Scan to Markdown - OCR for Scanned Docs
mineru-open-api flash-extract https://example.com/scanned.pdf

# Scan to Markdown - OCR for Scanned Docs
mineru-open-api flash-extract scanned.pdf --language en

# Scan to Markdown - OCR for Scanned Docs
mineru-open-api flash-extract scanned.pdf -o ./output/
```

## Language Rule

You MUST reply to the user in the SAME language they use. This is non-negotiable.

## Capabilities

- OCR for scanned PDFs, photographed documents, images
- Supports PDF, PNG, JPG, WebP, BMP, TIFF
- Supports both local files and URLs directly
- Language hint with `--language` (default: `ch`, use `en` for English)
- No API key, no signup, no authentication
- Max 10MB / 20 pages per document

## When to Use

- User asks to "OCR" a document or image
- User has a scanned PDF that needs text extraction
- User shares a photo of a page and wants the text
- User mentions "scan", "handwriting", or "recognize text"

## CLI Reference

Run `mineru-open-api flash-extract --help` for all available options.

## Data Privacy

- `flash-extract` uploads the document to MinerU's cloud API for processing and returns the result. No account or API key is required.
- Documents are processed in real-time and are not stored after extraction.
- For details, see https://mineru.net

## Notes

- Best results with clear, high-resolution scans
- For higher precision OCR with full layout preservation, use `mineru-open-api extract --ocr` (requires auth via `mineru-open-api auth`)
- If the CLI cannot be installed via npm/uv/go, download it from https://mineru.net/ecosystem?tab=cli
