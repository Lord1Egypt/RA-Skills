---
name: summarize-pdf
description: "PDF to Markdown converter - extract text, tables and formulas from PDF files to clean Markdown. Use when converting PDF documents, extracting PDF content, parsing PDF text, or summarizing PDF reports."
homepage: https://mineru.net
metadata: {"openclaw":{"emoji":"📄","requires":{"bins":["mineru-open-api"]},"install":[{"id":"npm","kind":"node","package":"mineru-open-api","bins":["mineru-open-api"],"label":"Install via npm"},{"id":"uv","kind":"uv","package":"mineru-open-api","bins":["mineru-open-api"],"label":"Install via uv"},{"id":"go","kind":"go","package":"github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api","bins":["mineru-open-api"],"label":"Install via go install","os":["darwin","linux"]}]}}
---

# Summarize PDF - Quick Content Extraction

Convert PDF files to clean Markdown using MinerU Open API. No API key required.

## Quick Start

```bash
# Summarize PDF - Quick Content Extraction
mineru-open-api flash-extract report.pdf

# Summarize PDF - Quick Content Extraction
mineru-open-api flash-extract https://cdn-mineru.openxlab.org.cn/demo/example.pdf

# Summarize PDF - Quick Content Extraction
mineru-open-api flash-extract report.pdf -o ./output/

# Summarize PDF - Quick Content Extraction
mineru-open-api flash-extract report.pdf --pages 1-10
```

## Language Rule

You MUST reply to the user in the SAME language they use. This is non-negotiable.

## Capabilities

- Extracts text, tables, and formulas from PDF
- Supports both local files and URLs directly
- Page range selection with `--pages`
- Language hint with `--language` (default: `ch`, use `en` for English)
- No API key, no signup, no authentication
- Max 10MB / 20 pages per document

## When to Use

- User asks to "read", "extract", "convert", or "parse" a PDF
- User shares a PDF file or PDF link and asks for its content
- User wants to summarize or analyze a PDF document
- User needs PDF content in Markdown format

## CLI Reference

Run `mineru-open-api flash-extract --help` for all available options.

## Data Flow

`flash-extract` sends the document to the MinerU API (mineru.net) for processing and returns Markdown. This is a stateless API call — no account, no persistent storage. MinerU is an open-source project by OpenDataLab (Shanghai AI Lab): https://github.com/opendatalab/MinerU

## Notes

- Output is Markdown only; images/tables/formulas may be replaced with placeholders
- For larger files (up to 200MB/600 pages) or precision extraction with full assets, use `mineru-open-api extract` (requires auth via `mineru-open-api auth`)
- If the CLI cannot be installed via npm/uv/go, download it from https://mineru.net/ecosystem?tab=cli
