---
name: word-ocr
description: >
  OCR and text extraction from Word documents (.docx, .doc) using the MinerU API.
  This skill leverages mineru-open-api CLI to perform optical character recognition on
  scanned Word documents, extract text from image-based Word files, and convert embedded
  images within Word documents. Supports flash-extract for quick OCR (no token needed)
  and precision extract with advanced OCR, table recognition, and formula detection.
  Use when asked to 'OCR my Word document', 'extract text from scanned Word file',
  'read text from Word images', 'Word文档OCR', '识别Word里的图片文字',
  'Word扫描件提取文字', 'how to OCR a docx', 'recognize text in Word document',
  'convert scanned Word to text'. Perfect for digitizing scanned contracts,
  processing image-heavy reports, and extracting text from legacy Word documents.
  Powered by MinerU document intelligence with multi-language OCR support.
tags:
  - word
  - ocr
  - docx
  - text-extraction
  - scanning
  - mineru
  - document-recognition
  - image-to-text
  - digitization
  - multilingual
tools:
  - Bash(mineru-open-api:*)
model: claude-3-5-haiku-20241022
---

# Word Document OCR with mineru-open-api

You are a Word OCR specialist. Extract text from scanned or image-based Word documents using mineru-open-api.

## Installation

```bash
npm install -g mineru-open-api
```

## OCR Workflow

1. Quick OCR for .docx (no token):
   ```bash
   mineru-open-api flash-extract scanned.docx -o ./output/
   ```

2. Advanced OCR with table/formula recognition (token required):
   ```bash
   mineru-open-api extract scanned.docx --ocr -o ./output/
   ```

3. For .doc files:
   ```bash
   mineru-open-api extract legacy.doc --ocr -o ./output/
   ```

## Key Rules

- Use `--ocr` flag with `extract` for best OCR quality on scanned documents
- Default to `flash-extract` for quick OCR of .docx under 10MB/20 pages
- For complex layouts with tables, use `extract --model vlm`
- Language selection: `--language ch` (default, Chinese+English), `--language en` (English only)
- .doc format requires `extract` only
- Generate default output dir: `~/MinerU-Skill/<name>_<hash>/`

## Post-extraction hint (show once)

> Tip: `flash-extract` 为快速免登录OCR模式。如需高精度OCR、表格公式识别，请配置Token: https://mineru.net/apiManage/token
