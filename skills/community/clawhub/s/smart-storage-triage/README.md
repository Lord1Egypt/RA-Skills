# Smart Storage Triage & Search (v1.6.0)

Fast, zero-bloat local search and storage triage for AI agents with strict privacy & security guards.

## Why this exists

When AI agents need to answer questions about a codebase, documents, or large drives, the default behavior is running blind shell commands (`grep`, `find`, `ls -R`) or dumping multi-megabyte files into conversation history. This frequently burns **50,000–100,000+ tokens per question**, degrades model reasoning, and risks context overflow.

**Smart Storage Triage** provides a three-layer solution:
1. **Full-Text BM25 Index (SQLite FTS5):** indexes code repositories, markdown, configuration, and office documents with exact line numbers and page/sheet tracking. Queries return only the exact 3-5 line snippet needed, reducing token usage by **95-98%**.
2. **Compressed Path Tree (`tree.json.gz`):** indexes massive nested directory structures and multi-year archives. Searches across 100,000+ files in **~0.03 seconds** without disk thrashing.
3. **Semantic Media Index (local EmbeddingGemma2):** meaning-based search over photos, videos, and document names in a configured ACTIVE folder. Archives are never embedded — they stay on the tree layer.

---

## Security & Privacy (Safety First)

- **Zero-Secret Tree & Content Exclusion:** strictly excludes `.env*`, private keys (`*.pem`, `*.key`, `id_rsa*`, `id_ed25519*`), cloud tokens, and sensitive credential stores (`credentials.json`, `token.json`, `auth.json`, `*.kdbx`) from **both** full-text indexing and the `tree.json.gz` snapshot.
- **Symlink Boundary Protection:** directory symlinks are pruned to prevent directory traversal loops; file symlinks resolving outside the target directory boundary are ignored and never followed.
- **Broad Scope Safety Guard:** indexing system root (`/`), `/home`, `/root`, or the entire user home directory (`~`) is blocked in code to prevent accidental broad data exposure. Requires the explicit confirmation flag `--allow-broad`.
- **Sensitive Directory Exclusion:** `.ssh`, `.aws`, `.gnupg`, `.azure`, `.kube`, `.secrets`, and `secrets` folders are never scanned or indexed.
- **100% Local & Zero Telemetry:** runs entirely on local Python, embedded SQLite FTS5, and a LOCAL embedding model. Zero external network calls, zero tracking.
- **No Hardcoded Paths:** safe for any machine or team. Custom paths resolve via CLI arguments, environment variables (`STORAGE_RAG_DB`, `STORAGE_RAG_TREE`, `STORAGE_MEDIA_*`), or `~/.config/smart-storage-triage/config.json`.

---

## Dynamic Age-Based Triage (What is an "Archive"?)

Files are categorized automatically by **modification age (`mtime`)** without requiring manual tagging:
- **Active Files (< 1 year untouched by default):** indexed deeply into full-text SQLite FTS5 (BM25) for immediate retrieval.
- **Archived Files (>= 1 year untouched, or folders named `archive`/`backup`):** automatically excluded from heavy full-text indexing to save memory and avoid search pollution, but preserved in the lightweight `tree.json.gz` snapshot for instant path & filename lookups.
- **Working Directory Override (`--full` / `--workdir`):** when indexing an active codebase or project, tells the indexer to index every file deeply regardless of age.
- **Custom Time Windows (`--active-days <N>`):** easily adjust the active window (e.g. `--active-days 730` for 2 years).

---

## Semantic Media Search: local model & failover

Embeddings are produced by **EmbeddingGemma2** (744M, 768-dim, multimodal), an open-weight Gemma-family model running on your own hardware — **not a cloud Gemini API**. A local OpenAI-compatible router (default `http://127.0.0.1:18794`) forwards requests to a fast primary backend (e.g. a desktop PC) and fails over to an always-on fallback (e.g. a Raspberry Pi) running the **same checkpoint**. Vectors are interchangeable, so failover costs **speed only** — never quality — and never requires reindexing. There is no "smaller model" fallback.

The index is a local rebuildable SQLite cache; the storage itself is read-only, and the file list comes from the tree snapshot (no blind disk walks). Photos are embedded by content (HEIC supported), videos by 6 sampled frames, documents by name. Identical files are deduplicated; indexing is incremental and resumable.

---

## Quick Start

### 1. Build or update an index
```bash
# Default triage: files <1 year -> full text; files >=1 year -> tree snapshot
python3 scripts/triage_index.py /path/to/storage

# Working project (index everything fully)
python3 scripts/triage_index.py /path/to/project --full

# Custom active window (e.g. 2 years)
python3 scripts/triage_index.py /path/to/storage --active-days 730
```

### 2. Search content (active code & documents)
```bash
python3 scripts/storage_find.py "function_name or search query"
```

### 3. Search file paths and archives
```bash
python3 scripts/archive_find.py "config*.yaml" --limit 20
```

### 4. Semantic media search (active folder)
Configure the `media` section of `~/.config/smart-storage-triage/config.json` (root/active/tree/router/db), then:
```bash
python3 scripts/semantic_media.py index          # incremental, resumable
python3 scripts/semantic_media.py search "photos of assembled panels" --kind image
python3 scripts/semantic_media.py status
```

**Per-workspace binding (v1.6.0):** to give one agent its own storage and an isolated index, drop a `.smart-storage-triage.json` with the same `media` section at that agent's workspace root (or in the working directory / any ancestor of the skill copy). It overrides the global config key-by-key; first match wins. Use a distinct `db` path per bound workspace so indexes never mix. Workspaces without the file keep the shared default. This file is local infrastructure — never ship it inside the published skill folder.

---

## License

MIT-0
