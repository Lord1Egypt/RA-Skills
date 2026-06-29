# Architecture

## Boundary

The router is not a knowledge base. It prepares standardized parsed output for a downstream knowledge-base system.

Responsibilities:

- classify input files
- detect parser capabilities
- choose a parser route
- recommend missing dependencies
- emit standardized parse artifacts

Non-responsibilities:

- vector indexing
- full-text search management
- database sync
- corpus governance
- investment or domain decision logic

## Classifier Signals

The classifier combines cheap signals:

- extension, MIME type, and size
- PDF text density and image block count
- sample text readability and garbled ratio
- Office/spreadsheet extension and parser availability
- image vs text-native routing

## Dependency Profiles

Minimal:

- markitdown
- pymupdf
- pypdf
- pandas
- openpyxl

Research report:

- minimal
- PaddleOCR
- pdfplumber
- Pillow

Office full:

- minimal
- python-docx
- python-pptx
- LibreOffice headless for legacy formats

## Standard Artifacts

- `document.json`: canonical manifest and provenance
- `document.md`: readable normalized text
- `chunks.jsonl`: retrieval-friendly chunks
- `tables/`: reliable table exports only
- `batch_summary.json`: batch results

## Cross-Agent Contract

The CLI is the contract. Agents should call:

```bash
python scripts/document_classifier_router.py classify --input <file>
python scripts/document_classifier_router.py parse --input <file> --output <dir>
python scripts/document_classifier_router.py batch --input-dir <dir> --output <dir> --copy-sources
```

Every command prints JSON to stdout and writes deterministic artifacts under the requested output directory.
