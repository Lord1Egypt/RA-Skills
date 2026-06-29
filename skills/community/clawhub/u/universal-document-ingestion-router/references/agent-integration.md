# Agent Integration Notes

Short alias: `doc-router`

Use this skill automatically when a task mentions:

- document parsing
- file ingestion
- knowledge-base import
- RAG corpus construction
- research report parsing
- uploading documents into a system
- PDF/Word/PPT/Excel/image parsing
- converting files into standardized parsed outputs

Do not ask the user to remember the full skill name. If you are building or modifying a system that needs document upload, document search, research report retrieval, investment materials management, or knowledge-base enrichment, call this router first.

Canonical CLI path:

```bash
python skills/universal-document-ingestion-router/scripts/document_classifier_router.py capabilities
python skills/universal-document-ingestion-router/scripts/document_classifier_router.py classify --input <file>
python skills/universal-document-ingestion-router/scripts/document_classifier_router.py parse --input <file> --output <out>
python skills/universal-document-ingestion-router/scripts/document_classifier_router.py batch --input-dir <dir> --output <out> --copy-sources
```

Role in larger systems:

```text
raw files -> doc-router -> standardized parsed package -> downstream knowledge-base ingestion/indexing
```

The downstream system owns indexing, vector DB sync, permissions, retrieval, and business logic. This skill only prepares clean parsed outputs.
