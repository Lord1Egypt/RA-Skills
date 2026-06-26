# Configuration

## Required inputs

The skill needs four paths:

- Zotero data directory
- Zotero SQLite database
- Zotero attachment storage directory
- Vector store output directory

## Environment variables

Use these when you want persistent configuration without repeating CLI flags:

- `ZOTERO_DATA_DIR`
- `ZOTERO_DB`
- `ZOTERO_STORAGE`
- `ZOTERO_VECTORS_DIR`

Scripts also accept explicit flags:

- `--data-dir`
- `--db`
- `--storage-dir`
- `--output-dir`

Flags override environment variables.

## Output layout

Default output directory: `<cwd>/zotero-vectors`

Files:

- `metadata_vectors.json`
- `fulltext_vectors.json`
- `vector_store_metadata.json`
- `README.md`
- `snapshots/` (SQLite snapshots)
- `*.bak_YYYYMMDD_HHMMSS` backups

## Embedding defaults

- Model: `paraphrase-multilingual-MiniLM-L12-v2`
- Metadata batch size: `50`
- Fulltext batch size: `32`
- Chunk size: `800` words
- Chunk overlap: `100` words

## Dependency expectations

Python packages:

- `sentence-transformers`
- `torch`
- `PyMuPDF`
- `numpy`

Install in a virtual environment when possible.
