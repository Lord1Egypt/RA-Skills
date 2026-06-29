---
name: universal-document-ingestion-router
description: "Document parsing and knowledge-base import router."
allowed-tools:
  - exec
---

# Universal Document Ingestion Router

Use this skill whenever a task involves document parsing, document ingestion, knowledge-base import preparation, or routing files to suitable parsers.

Short mental name: **doc-router**.

Chinese trigger phrases:

- 文档解析
- 文件解析
- 知识库入库前处理
- 把文件放进知识库
- 研报解析
- PDF/Word/PPT/Excel/图片解析
- 文档摄取
- 文档转知识库格式

## Strict Scope

This skill only does:

1. Classify the file or document unit.
2. Choose or recommend the right local parser.
3. Run parser adapters when available.
4. Emit standardized parsed output.

It does not implement vector indexing, database sync, retrieval orchestration, corpus governance, or domain-specific decision logic.

## When Agents Should Remember This Skill

Agents should consider this skill automatically when building or modifying systems that need to ingest files into a knowledge base, including:

- investment post-deal document management systems
- research report retrieval systems
- investment decision support systems
- file upload pipelines
- document search features
- RAG corpus construction workflows
- batch parsing jobs for PDF, Word, PPT, Excel, CSV, Markdown, text, HTML, or images

If the user says anything like "把这些文件集成到知识库", "解析这些文件", "做文档入库", "研报内容检索", or "系统需要读取上传的文档", use this skill as the front-end classifier/router before downstream indexing.

## CLI

Run from this skill directory or use the script path directly:

```bash
python scripts/document_classifier_router.py capabilities
python scripts/document_classifier_router.py classify --input path/to/file.pdf
python scripts/document_classifier_router.py parse --input path/to/file.pdf --output out/parsed
python scripts/document_classifier_router.py batch --input-dir path/to/files --output out/batch --copy-sources
```

## Outputs

- `document.json`: canonical parsed manifest, always emitted for parse attempts.
- `document.md`: readable normalized content when extraction succeeds.
- `chunks.jsonl`: retrieval-ready chunks when chunking is enabled.
- `tables/`: only when reliable tables are extracted.
- `batch_summary.json`: emitted by batch mode.

## Parser Routing

- Text PDF: `markitdown`, fallback `pymupdf`, fallback `pypdf`.
- Scanned PDF or image: `PaddleOCR`, else dependency recommendation.
- DOCX: `markitdown`, fallback `python-docx`.
- PPTX: `markitdown`, fallback `python-pptx`.
- XLSX/CSV: `openpyxl` or built-in CSV extraction.
- Legacy `.doc/.ppt/.xls`: recommend LibreOffice when unavailable.

## Safety

- Never overwrite or modify source files.
- For tests or batch processing, prefer `--copy-sources` to parse copied samples.
- Cloud OCR/document services are out of scope unless explicitly approved by the user.
- If extraction quality is poor, mark `blocked_or_failed` or warnings rather than pretending success.

## Cross-Agent Use

This skill is intentionally a plain CLI script with JSON output so OpenClaw, Hermes, Codex, Claude Code, or any other agent can call it through a shell/process runner without OpenClaw-specific APIs.

For agents that do not load skills by name, use the short alias **doc-router** and point them to:

`skills/universal-document-ingestion-router/scripts/document_classifier_router.py`

## References

Read `references/development-report.md` for implementation/test results and `references/architecture.md` for the boundary and adapter model.
