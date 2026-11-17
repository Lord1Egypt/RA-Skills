---
name: smart-storage-triage
description: "Universal smart search and storage triage for codebases, local files, documents, and archives. SQLite FTS5 (BM25), gzip tree snapshots, and semantic media search (photos/videos/document names) via local EmbeddingGemma2 embeddings with same-model failover. Requires user confirmation before broad directory indexing."
allowed-tools: [exec, read]
---

# Smart Storage Triage & Search (v1.6.0)

Fast, zero-bloat search across code repositories, local folders, documentation, and deep archives. Avoids burning tens of thousands of tokens by querying indexed SQLite FTS5, compressed directory tree snapshots, and a local semantic media index instead of performing blind shell walks (`find` / `grep`).

### What's New in v1.6.0:
- **Per-workspace storage binding:** a `.smart-storage-triage.json` file (section `media`) in the working directory or in an ancestor directory of the skill copy (up to the workspace root) overrides the shared global config. Each agent workspace can bind its OWN storage root, tree snapshot, and index DB — separate agents get separate, isolated indexes with zero code changes; workspaces without the file keep the shared default.

### What's New in v1.5.0:
- **Config-driven semantic media search** bundled as `scripts/semantic_media.py`: any active folder on any storage, configured via the shared config file or env. Multiple agents on one host share one config and one index — install the skill per agent, no reindexing.
- **Local model & failover documented:** embeddings come from local EmbeddingGemma2 (open Gemma family — NOT a cloud Gemini API). The fallback backend runs the SAME checkpoint, so failover costs speed only, never quality, and never requires reindexing.
- **"How to use" workflow:** which search layer answers which kind of query.

### What's New in v1.3.0:
- **Full Directory Tree Tracking:** Snapshots now capture both directories (`dirs`) and files (`files`), allowing instant folder discovery even for newly created or empty paths.
- **Dual Folder & File Search:** Query either folders (`--dirs`), files (`--files`), or both with visual tags (`📁 [ПАПКА]`, `📄 [ФАЙЛ]`).
- **Unicode Surrogate Resilience:** Hardened string sanitizer prevents UTF-8 encoding crashes from corrupted PDF/binary documents.

## Security & Privacy (Safety First)

1. **Automatic Secret & Credential Exclusion:**
   - Files matching `.env*`, `credentials.json`, `token.json`, `auth.json`, `secrets.json`, `id_rsa*`, `id_ed25519*`, `*.pem`, `*.key`, `*.kdbx`, `*.pfx`, `*.p12` are strictly excluded from **both** full-text indexing and directory tree snapshots (`tree.json.gz`).
   - Sensitive directories (`.ssh`, `.aws`, `.gnupg`, `.azure`, `.kube`, `.secrets`, `secrets`) are completely skipped.
2. **Symlink Boundary Protection:**
   - Directory symlinks are pruned to prevent directory traversal loops.
   - File symlinks that resolve outside the target directory boundary are strictly ignored and never followed.
3. **Broad Scope Safety Guard:**
   - Direct indexing of the root filesystem (`/`), `/home`, or the user home directory (`~`) is restricted in code to prevent accidental broad data exposure. Indexing broad system targets requires the explicit `--allow-broad` flag.
4. **100% Local & Zero Telemetry:**
   - Runs entirely using standard Python, embedded SQLite FTS5, and a LOCAL embedding model. Zero external network calls, zero tracking.
5. **No Hardcoded Paths:**
   - Works in any directory. Custom paths can be configured via environment variables (`STORAGE_RAG_DB`, `STORAGE_RAG_TREE`, `STORAGE_MEDIA_*`), CLI arguments, or `~/.config/smart-storage-triage/config.json`.

## Mandatory User Confirmation (Approval Step)

**CRITICAL:** Before building or rebuilding an index (`triage_index.py` or `semantic_media.py index`) on a new directory or external storage:
- The agent **MUST ask for explicit user confirmation**, specifying the target directory path and expected scope.
- **NEVER** automatically index the entire home directory (`~`), filesystem root (`/`), or parent mount points without clear user authorization.

## Dynamic Age-Based Triage (What is an "Archive"?)

Storage is split automatically without manual tagging:
1. **Active Files (< 1 year untouched by default):**
   - Files modified within the active period (`--active-days 365`) are indexed with **full-text BM25 search** (code with exact line numbers, documents with page/sheet numbers).
2. **Archived Files (>= 1 year untouched, or inside `archive/backup` folders):**
   - Files not modified for 1 year or more automatically graduate into the **Archive Layer**.
   - They do **not** bloat the heavy full-text index, saving 95%+ of disk space and memory.
   - Instead, they are captured in the compressed **`tree.json.gz` snapshot** for instant path, filename, and date searches (100,000+ files in 0.03s).
3. **Working Directory Override (`--full` / `--workdir`):**
   - When indexing an active workspace or project repository, pass `--full` to index every file deeply, regardless of modification age.

## Search Workflow

### 1. Content Search (Active Code, Text, and Documents)

Query full-text content with BM25 ranking:
```bash
python3 <skill_dir>/scripts/storage_find.py "<query>" [--limit 10]
```
- Returns matching files, exact line numbers (for code/text) or page/sheet numbers (for documents), and concise snippets.
- Reads only the relevant snippet into context, saving up to 98% of prompt tokens.

### 2. File Path & Archive Search (Deep Trees & Inactive Files)

Query the compressed tree snapshot (`tree.json.gz`) for instant filename, folder, or regex matches:
```bash
python3 <skill_dir>/scripts/archive_find.py "<pattern_or_name>" [--dirs] [--files] [--ext .py|.pdf] [--limit 20]
```
- Searches across 100,000+ files and directories in ~0.03 seconds without triggering disk I/O thrashing.
- Supports substring, regex, and type filtering (`--dirs` for folders only, `--files` for files only).

### 3. Semantic Media Search (Active Folder, Local Embeddings)

Meaning-based search over **photos, videos, and document names** in a configured ACTIVE folder. Archives are NEVER embedded — they stay on tree search (section 2).

**Model — local, not cloud:** embeddings come from **EmbeddingGemma2** (744M, 768-dim, multimodal: text/image/audio/video), an open-weight Gemma-family model served by a local OpenAI-compatible embeddings router (default `http://127.0.0.1:18794`). This is NOT a cloud Gemini API — everything runs on your own hardware. The router forwards to a fast primary backend (e.g. a desktop PC) and fails over to an always-on fallback (e.g. a Raspberry Pi) running the **same checkpoint**: vectors are interchangeable (cosine ≈ 1.0 on identical inputs), so failover degrades **speed only** — never quality — and never requires reindexing. There is no "smaller/lower model" fallback.

**Configuration** — `~/.config/smart-storage-triage/config.json`, section `media` (env overrides `STORAGE_MEDIA_ROOT/_ACTIVE/_TREE/_ROUTER/_DB`, CLI flags win over both):
```json
{
  "media": {
    "root": "/path/to/storage",
    "active": "ActiveFolder/",
    "tree": "/path/to/storage/tree.json.gz",
    "router": "http://127.0.0.1:18794",
    "db": "~/.local/share/semantic-media/index.db"
  }
}
```
- `active` is a prefix relative to `root`; keep archives OUT of it. `""` = whole root.
- The config and index DB are per-user: several agents on one host share one index. Install the skill into each agent's workspace; no per-agent reindexing.
- **Per-workspace binding (isolation):** to give one agent its OWN storage and index, put a `.smart-storage-triage.json` with the same `media` section at that agent's workspace root (or anywhere above the skill copy / in the working directory). It overrides the global config key-by-key; the first match wins (CWD first, then the script's ancestors). Use a separate `db` path per bound workspace so indexes never mix. Keep this file OUT of the published skill folder — it is local infrastructure, not skill content.

**Commands:**
```bash
# Search by meaning (system python3 + numpy, ~1 s)
python3 <skill_dir>/scripts/semantic_media.py search "<query>" [--limit 10] [--kind image|video|doc] [--json]

# Incremental index (needs PIL + pillow-heif for HEIC; ffmpeg for video frames)
python3 <skill_dir>/scripts/semantic_media.py index [--area SUBSTR] [--kind image|video|doc] [--force] [--max N]

# Coverage and errors
python3 <skill_dir>/scripts/semantic_media.py status
```

**How to use (agent workflow):**
1. **Meaning-based queries about photos/videos** ("find photos of assembled panels", "where is the video about installation") → `search`. Phrase the query as a description of the visual content, in the user's language; add `--kind image|video` when the user asks for a specific media type.
2. **Exact file/folder names, anything in archives** → tree search (section 2), NOT embeddings.
3. **Document CONTENT** (contracts, estimates, code) → full-text search (section 1). Semantic `doc` kind matches file NAMES only.
4. Before the FIRST index of a folder: confirm target and scope with the user (approval rule above). The index is incremental and resumable — run large first passes in the background with a log file, and report progress/ETA.
5. Report results as paths (+ scores when useful). Dedup is automatic: identical files in different folders are embedded once and collapsed in results.
6. If the primary backend is asleep, the router falls back automatically; expect slower indexing, identical results. Wake the primary machine for bulk runs when possible.

**Mechanics:** images → content vector (1024px downscale, HEIC via pillow-heif); videos → 6 evenly spaced ffmpeg frames → mean-pooled vector; docs → "filename | folder" text vector. Dedup by sha1 (videos: first 1 MB + size); resume by size+mtime; failed files are stored with the error and retried on the next run. The file list comes from the tree snapshot — no blind disk walks. The retrieval query prefix (`task: search result | query: `) is applied automatically.

**Performance notes:** the primary backend serializes requests — parallel workers do NOT speed it up (~10 s/photo on a CPU desktop; ~1 min/video; a full pass of ~1200 media + ~2700 docs ≈ 3–4 h). Do not load the fallback machine with bulk indexing if it also runs other services. Search itself is ~1 s regardless of backend.

### 4. Creating or Updating an Index

Ask the user for approval first, then build or refresh the index:
```bash
# Default triage: active (<1y) -> full text, archived (>=1y) -> tree snapshot
python3 <skill_dir>/scripts/triage_index.py <directory_path>

# Custom active window (e.g. 2 years)
python3 <skill_dir>/scripts/triage_index.py <directory_path> --active-days 730

# Working repository / full indexing (index all files regardless of age)
python3 <skill_dir>/scripts/triage_index.py <directory_path> --full
```

## Resolution Order

`storage_find.py` and `archive_find.py` auto-resolve indexes in the following priority:
1. Explicit `--db` or `--tree` argument.
2. Environment variables `STORAGE_RAG_DB` and `STORAGE_RAG_TREE`.
3. User configuration file `~/.config/smart-storage-triage/config.json`.
4. Current working directory (`./storage_rag.db`, `./tree.json.gz`).

`semantic_media.py` resolves its `media` config in the same spirit: CLI flags → `STORAGE_MEDIA_*` env → workspace-local `.smart-storage-triage.json` (CWD, then the script's ancestor directories) → `media` section of the global config file → defaults.
