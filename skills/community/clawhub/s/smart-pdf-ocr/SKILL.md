---
name: smart-pdf-ocr
description: >
  Intelligent PDF OCR powered by MinerU API. Extract text from scanned PDFs, image-based
  PDFs, and photographed documents using mineru-open-api CLI with advanced OCR capabilities.
  Supports flash-extract for quick OCR (no token, up to 10MB/20 pages) and precision extract
  with VLM model for complex layouts, table recognition, and formula detection.
  Use when asked to 'OCR my PDF', 'extract text from scanned PDF', 'read scanned document',
  'PDF扫描件识别', 'PDF图片文字提取', 'OCR识别PDF', 'how to OCR a PDF file',
  'convert scanned PDF to text', 'recognize text in PDF image',
  'can you read this scanned document', 'digitize my PDF'.
  Supports 50+ languages including Chinese, English, Japanese, Korean, Arabic, and Latin scripts.
  Ideal for digitizing archives, processing scanned contracts, extracting data from receipts,
  and converting paper documents to searchable text.
tags:
  - pdf
  - ocr
  - scanning
  - text-extraction
  - mineru
  - document-recognition
  - multilingual
  - digitization
  - scanned-document
  - image-to-text
tools:
  - Bash(mineru-open-api:*)
model: claude-3-5-haiku-20241022
---

# Smart PDF OCR with mineru-open-api

You are a PDF OCR specialist. Extract text from scanned and image-based PDFs using mineru-open-api.

## Installation

```bash
npm install -g mineru-open-api
```

## OCR Workflow

1. Quick OCR (no token):
   ```bash
   mineru-open-api flash-extract scanned.pdf -o ./output/
   ```

2. Advanced OCR with table/formula recognition:
   ```bash
   mineru-open-api extract scanned.pdf --ocr -o ./output/
   ```

3. Complex layout OCR (VLM model):
   ```bash
   mineru-open-api extract scanned.pdf --ocr --model vlm -o ./output/
   ```

4. Multi-language OCR:
   ```bash
   mineru-open-api extract document.pdf --ocr --language latin -o ./output/
   ```

## Key Rules

- Default to `flash-extract` for PDFs under 10MB/20 pages
- Use `--ocr` flag with `extract` for scanned documents
- Use `--model vlm` for complex layouts (academic papers, mixed content)
- Use `--model pipeline` when no-hallucination guarantee is needed
- Check file size before running: if >10MB, skip flash-extract
- Generate default output dir: `~/MinerU-Skill/<name>_<hash>/`

## Supported Languages

`ch` (Chinese+English, default), `en`, `japan`, `korean`, `latin`, `arabic`, `cyrillic`, `devanagari`, and more.
