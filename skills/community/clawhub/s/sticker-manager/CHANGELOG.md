# Changelog

## 0.3.0

### Added
- Generic animation-preservation rule for sticker collection
- Support for animated GIPHY page sources resolving to real GIF assets

### Changed
- `collect_stickers.py` now follows a generic animation-preservation rule: suffix → Content-Type → downloaded file validation
- animated-looking sources are no longer silently downgraded to static WEBP/PNG previews during collection

### Fixed
- animated GIPHY page sources now resolve to real GIF assets instead of static preview files
- collector now rejects static fallback downloads when the source looked animated

## 0.2.1

### Added
- Support for saving stickers from recent chat/media history
- Vision fallback planning and failure messaging
- Model-first semantic matching payload flow
- Bilingual user-facing script output
- Pytest coverage for core workflows
- Project license and public-repo preparation files

### Changed
- Clarified source discovery behavior in the English and Chinese READMEs and in `SKILL.md`

### Fixed
- `discover_sources.py` now keeps remote URL discovery lightweight by default and only verifies remote URLs when `--fetch-urls` is explicitly passed
- `discover_sources.py` no longer counts failed page fetches as successful discovered sources
- `batch_import.py` now reports duplicate counts consistently in both terminal summaries and JSON output

## 0.2.0

### Added
- **Batch import**: New `scripts/batch_import.py` for importing stickers from local directories with automatic deduplication, size filtering, and optional auto-tag plan generation
- **Source discovery**: New `scripts/discover_sources.py` for discovering sticker sources from URLs, local directories, and web pages (static scraping)
- **Auto-tag**: Extended `sticker_semantic.py` with `auto-tag` and `auto-tag-dir` commands for generating vision-based semantic tags
- **Context-aware recommendation**: Extended `sticker_semantic.py` with `context-recommend` command for chat history-based sticker suggestions
- Comprehensive test coverage for all new features:
  - `tests/test_batch_import.py`
  - `tests/test_auto_tag.py`
  - `tests/test_context_recommend.py`
  - `tests/test_e2e_workflow.py`

### Changed
- Updated README.md and README.zh-CN.md with documentation for new features
- Improved `suggest` command to return success when candidates are available for model matching

## 0.1.0

Initial public version of `sticker-manager` extracted from a working OpenClaw workflow.
