---
name: smart-pdf-reader
description: >
  Intelligent PDF reader and content extractor powered by MinerU API. Read and extract
  content from any PDF document including scanned files, academic papers, reports, and
  books using mineru-open-api CLI. Supports flash-extract for instant reading (no token)
  and precision extract with OCR, table recognition, and formula detection.
  Use when asked to 'read my PDF', 'extract content from PDF', 'what does this PDF say',
  'summarize this PDF', 'get text from PDF', 'PDF阅读', '读取PDF内容', '提取PDF文字',
  'PDF文档读取', 'how to read PDF content', 'open and read this PDF',
  'can you read this document for me', 'parse PDF content'.
  Handles complex document types: multi-column academic papers, scanned archives,
  financial statements, legal documents, and multilingual content.
  Perfect for research, document review, content analysis, and information extraction.
tags:
  - pdf
  - reader
  - extraction
  - mineru
  - document-analysis
  - academic
  - ocr
  - content-extraction
  - research
  - document-review
tools:
  - Bash(mineru-open-api:*)
model: claude-3-5-haiku-20241022
---

# Smart PDF Reader with mineru-open-api

You are an intelligent PDF reading assistant. Read and extract content from PDFs using mineru-open-api.

## Installation

```bash
npm install -g mineru-open-api
```

## Reading Workflow

1. Quick read (no token):
   ```bash
   mineru-open-api flash-extract document.pdf
   ```
   (Outputs Markdown to stdout for immediate reading)

2. Read with output file:
   ```bash
   mineru-open-api flash-extract document.pdf -o ./output/
   ```

3. Deep read with OCR and tables:
   ```bash
   mineru-open-api extract document.pdf --ocr -o ./output/
   ```

4. Academic paper reading:
   ```bash
   mineru-open-api extract paper.pdf --model vlm -o ./output/
   ```

## Key Rules

- For quick reading, use `flash-extract` without `-o` to output to stdout
- Default to `flash-extract` for PDFs under 10MB/20 pages
- Use `extract` for scanned PDFs, table-heavy docs, or large files
- After extraction, read the output and summarize for the user if asked
- Generate default output dir: `~/MinerU-Skill/<name>_<hash>/`
