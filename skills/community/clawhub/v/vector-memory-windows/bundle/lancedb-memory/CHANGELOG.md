# Changelog

All notable changes to `lancedb-memory` are documented in this file.

## v1.0.1 - Windows compatibility release

### Added

- Added cross-platform storage path strategy:
  - Windows default: `D:\clawtest\memory\lancedb`
  - Unix default: `~/.clawdbot/memory/lancedb`
- Added environment overrides:
  - `OPENCLAW_LANCEDB_PATH`
  - `CLAWTEST_ROOT` (Windows base root)
- Added `requirements.txt` for reproducible dependency install:
  - `lancedb`
  - `pandas`
  - `pyarrow`

### Changed

- Refactored `final_memory.py` into a stable cross-platform backend.
- Kept external API behavior unchanged:
  - `add_memory(content, metadata)`
  - `search_memories(query, limit)`
  - `get_all_memories()`
- Converted `simple_memory.py` and `working_memory.py` into compatibility wrappers to preserve old import paths.
- Simplified `clawdbot_memory.py` into an async provider adapter while preserving provider interface.
- Updated skill documentation for Windows-first usage and installation.

### Fixed

- Removed hardcoded macOS paths (`/Users/...`) that broke Windows usage.
- Removed fragile schema assumptions and improved table bootstrap handling.
- Avoided regex interpretation in text search by using literal substring matching.

### Compatibility

- OpenClaw/Clawdbot integration: compatible.
- OS support: Windows, macOS, Linux.
- Python: 3.9+ recommended.

### Migration Notes

- No API-breaking changes.
- Existing calls and integration points continue to work.
- Existing data can be retained; new installs use platform-aware defaults.
