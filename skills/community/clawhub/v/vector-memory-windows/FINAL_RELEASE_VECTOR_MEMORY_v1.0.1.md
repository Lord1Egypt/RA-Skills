# Vector Memory (Windows) - Final Release Document

## 1) Release Identity

- Product: `vector-memory` (Windows-ready OpenClaw edition)
- Release version: `v1.0.1`
- Release date: `2026-03-08`
- Release type: `Full feature bundle` (3 skills)

## 2) Upload Artifact

- File to upload: `dist/clawhub-upload/vector-memory-windows.zip`
- Absolute path: `D:\clawtest\dist\clawhub-upload\vector-memory-windows.zip`
- Verified size: `24131 bytes`

## 3) Included Skills (Complete Bundle)

1. `lancedb-memory` - semantic storage/retrieval backend
2. `git-notes-memory` - branch-aware decision/context memory with git notes
3. `memory-hygiene` - memory cleanup and maintenance guidance

## 4) What Changed in This Release

### Cross-platform compatibility (focus: Windows)

- Removed hardcoded macOS paths (`/Users/...`) from memory runtime code.
- Added platform-aware default storage path:
  - Windows: `D:\clawtest\memory\lancedb`
  - Unix-like: `~/.clawdbot/memory/lancedb`
- Added env override support:
  - `OPENCLAW_LANCEDB_PATH`
  - `CLAWTEST_ROOT`

### Stability and backward compatibility

- Preserved existing API behavior for memory operations:
  - `add_memory(...)`
  - `search_memories(...)`
  - `get_all_memories()`
- Kept compatibility import paths via wrapper modules in `lancedb-memory`.
- Maintained async provider interface for OpenClaw integration.

### Safety and documentation

- Updated `git-notes-memory` bootstrap behavior to avoid persistent local git config mutation.
- Added Windows command guidance in skill docs.
- Added dependency manifest for `lancedb-memory`:
  - `requirements.txt` (`lancedb`, `pandas`, `pyarrow`)

## 5) Runtime Requirements

- Python `3.9+` (validated on Python `3.12`)
- Git installed and available in `PATH`
- For `lancedb-memory`: install dependencies

```bash
pip install -r lancedb-memory/requirements.txt
```

## 6) Validation Status

Validated in local Windows workspace:

- `lancedb-memory/final_memory.py`:
  - add memory: pass
  - search memory: pass
  - list memories: pass
- `git-notes-memory/memory.py -p . sync --start`: pass
- Zip structure and artifact integrity: pass

## 7) ClawHub Listing Copy (Ready to Paste)

### Title

`Vector Memory (Windows) for OpenClaw`

### Short Description

`Windows-ready full memory stack for OpenClaw: LanceDB semantic memory + git-notes persistent decision memory + memory hygiene workflow.`

### Detailed Description

`This full-feature bundle brings production-ready memory to OpenClaw on Windows while remaining compatible with macOS/Linux. It includes semantic memory storage and retrieval, branch-aware long-term decision memory, and practical memory governance guidance. Existing integration APIs are preserved to minimize migration risk.`

### Highlights

- Windows-first path compatibility
- Full feature bundle (3 skills)
- Backward-compatible memory APIs
- Safer git bootstrap behavior
- Ready-to-use release package

## 8) Known Notes

- `memory-hygiene` provides guidance and command examples; behavior depends on your OpenClaw runtime command availability.
- If your runtime uses a custom memory directory, set `OPENCLAW_LANCEDB_PATH` explicitly.

## 9) Additional Artifacts

- Bundle release notes:
  - `dist/clawhub-upload/RELEASE_NOTES_vector-memory-windows_v1.0.1.md`
- Single-skill package:
  - `dist/clawhub-upload/lancedb-memory-windows.zip`
- Single-skill release notes:
  - `dist/clawhub-upload/RELEASE_NOTES_lancedb-memory_v1.0.1.md`
