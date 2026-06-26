---
name: zotero-vectorize
description: Build and maintain a cross-platform local Zotero semantic index using metadata embeddings and PDF full-text chunk embeddings. Use when the user asks to vectorize a Zotero library, create or refresh metadata_vectors.json or fulltext_vectors.json, check for new Zotero items missing from the vector store, incrementally update a Zotero semantic/RAG index, verify vector store counts and sizes, or reproduce this workflow on Windows, macOS, or Linux.
---

# Zotero Vectorize

Build and maintain a **local-first, cross-platform Zotero vector store** for semantic search and RAG over bibliographic metadata and PDF full text.

Keep `SKILL.md` focused on workflow. Read the reference files only when needed:

- `references/config.md` — paths, environment variables, output layout
- `references/data-format.md` — JSON schemas and file naming
- `references/windows.md` / `macos.md` / `linux.md` — platform-specific path defaults and notes
- `references/troubleshooting.md` — common failures and recovery

## Core rules

- Treat Zotero as **read-only input**. Never modify the user’s Zotero database or attachment storage.
- Prefer creating a **database snapshot** before reading.
- For incremental updates: **check first, report missing items, wait for user confirmation, then apply**.
- Before any update that rewrites store files: **back up first, then write**.
- Backup retention for this skill is fixed: keep only **the latest and previous backup** per file.
- Default output filenames are:
  - `metadata_vectors.json`
  - `fulltext_vectors.json`
  - `vector_store_metadata.json`

## Workflow decision tree

### 1) Detect or confirm paths

If the Zotero data directory, database path, or storage path is unknown:

1. Read `references/config.md`
2. Read the platform-specific reference (`windows.md`, `macos.md`, or `linux.md`)
3. Run:

```bash
python scripts/detect_zotero_paths.py
```

If the detected paths are wrong, ask the user to open Zotero and use **Show Data Directory**, then rerun with explicit `--data-dir`, `--db`, or `--storage-dir`.

### 2) Create a database snapshot

Before full builds or incremental checks, snapshot the Zotero database:

```bash
python scripts/snapshot_zotero_db.py --output-dir <store-dir>
```

If snapshotting fails because SQLite is locked, ask the user to close Zotero and retry.

### 3) Build the metadata vector store

Use this when the user asks to create or rebuild metadata embeddings for the Zotero library.

```bash
python scripts/build_metadata_vectors.py --output-dir <store-dir>
```

This writes `metadata_vectors.json` and refreshes `vector_store_metadata.json` + `README.md`.

### 4) Build the full-text vector store

Use this when the user asks to create or rebuild PDF full-text embeddings.

```bash
python scripts/build_fulltext_vectors.py --output-dir <store-dir>
```

This scans Zotero PDF attachments, extracts text, chunks it, embeds each chunk, and writes `fulltext_vectors.json`.

### 5) Check incremental updates

Use this when the user asks whether Zotero contains new items not yet added to the vector store.

```bash
python scripts/check_incremental_updates.py --output-dir <store-dir>
```

Report:

- total top-level Zotero items
- total PDF-parent items
- current metadata/fulltext vector counts
- missing metadata items
- missing fulltext items

Do **not** update the store yet.

### 6) Apply incremental updates

Only run this after the user confirms the update.

```bash
python scripts/apply_incremental_updates.py --output-dir <store-dir>
```

This script:

1. snapshots the DB
2. backs up store files
3. appends missing metadata/fulltext entries
4. keeps only the latest and previous backup per file
5. updates store metadata and README

Use `--item-id` to limit the update to specific items if the user wants a partial apply.

### 7) Verify the finished store

After any build or incremental update, verify counts and sizes:

```bash
python scripts/verify_vector_store.py --output-dir <store-dir>
```

Always report:

- metadata item count
- fulltext item count
- fulltext chunk count
- metadata file size
- fulltext file size

## Scripts

- `scripts/detect_zotero_paths.py` — resolve default/current Zotero paths
- `scripts/snapshot_zotero_db.py` — create a safe SQLite snapshot
- `scripts/build_metadata_vectors.py` — full rebuild of metadata vectors
- `scripts/build_fulltext_vectors.py` — full rebuild of PDF full-text vectors
- `scripts/check_incremental_updates.py` — compare Zotero against current vector store
- `scripts/apply_incremental_updates.py` — append missing items after user confirmation
- `scripts/backup_with_retention.py` — back up store files and retain only the latest two states
- `scripts/verify_vector_store.py` — report counts, sizes, and store metadata

## Output expectations

When using this skill successfully, return concise operational summaries such as:

- detected paths
- snapshot path used
- number of items/chunks written
- current file sizes
- whether any items are missing
- which itemIDs were appended during incremental update

## Escalation notes

Read `references/troubleshooting.md` when:

- SQLite snapshot fails
- HuggingFace/model download or local model loading fails
- PDFs are missing or unreadable
- full-text extraction is incomplete
- file paths differ from defaults on the current OS
