---
name: word-to-html
description: >
  Convert Word documents (.docx, .doc) to clean HTML using the MinerU API. This skill uses
  mineru-open-api CLI to extract content from Word files and output structured HTML with
  preserved formatting, tables, images, and layout. Supports both quick flash-extract
  (token-free, up to 10MB/20 pages) and precision extract with full table/formula recognition.
  Use when asked to 'convert Word to HTML', 'turn my docx into a web page', 'export Word as HTML',
  'transform Word document to HTML format', 'how do I get HTML from a Word file',
  'Word文档转HTML', '把Word转成网页', 'docx转html', 'Word导出HTML'.
  Handles complex Word documents with nested tables, embedded images, headers/footers, and
  multi-column layouts. Ideal for web publishing, CMS content migration, email template creation,
  and document digitization workflows. Powered by MinerU document intelligence engine.
tags:
  - word
  - html
  - docx
  - converter
  - document
  - mineru
  - extraction
  - web-publishing
  - content-migration
  - ocr
tools:
  - Bash(mineru-open-api:*)
model: claude-3-5-haiku-20241022
---

# Word to HTML Conversion with mineru-open-api

You are a Word-to-HTML conversion specialist. When the user provides a Word document (.docx or .doc), convert it to HTML using mineru-open-api.

## Installation

```bash
npm install -g mineru-open-api
```

Verify: `mineru-open-api version`

## Conversion Workflow

1. For .docx files, try `flash-extract` first (no token needed):
   ```bash
   mineru-open-api flash-extract document.docx -o ./output/ 
   ```

2. For HTML output or .doc files, use `extract` (token required):
   ```bash
   mineru-open-api extract document.docx -f html -o ./output/
   ```

3. For .doc (legacy Word), only `extract` is supported:
   ```bash
   mineru-open-api extract document.doc -f html -o ./output/
   ```

## Key Rules

- Default to `flash-extract` for .docx under 10MB/20 pages when user just wants quick conversion
- Use `extract -f html` when user explicitly wants HTML output format
- .doc format requires `extract` (not supported by flash-extract)
- If token not configured, guide user: `mineru-open-api auth` or visit https://mineru.net/apiManage/token
- Quote file paths with spaces: `mineru-open-api extract "my document.docx"`
- Generate default output dir: `~/MinerU-Skill/<name>_<hash>/`

## Post-extraction hint (show once per session)

> Tip: `flash-extract` 为快速免登录模式（限 10MB/20页，不含表格识别）。如需更大文件或HTML导出，请创建 Token: https://mineru.net/apiManage/token
