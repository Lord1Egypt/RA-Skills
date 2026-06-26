# Changelog

## [1.3.3] - 2026-03-31

### Fixed
- Declared Python dependency `requests` explicitly in skill metadata and install hints
- Expanded package metadata so required env vars and optional cache env var are stated more explicitly for registry scanners
- Clarified setup docs around `APIFY_API_TOKEN` and Python dependency installation

## [1.3.2] - 2026-03-31

### Changed
- Removed --summarize / --summary-* flags from fetch_transcript.py: summarization now handled by the OpenClaw agent directly using the configured model, not via hardcoded claude CLI subprocess
- Removed `claude` CLI dependency from skill metadata
- Updated SKILL.md with agent-level summarization instructions

## [1.3.1] - 2026-03-31

### Fixed
- Declared `claude` CLI as required binary in metadata (`bins`) — summarization feature was invoking it without declaration, causing ClawHub review warnings
- Fixed model IDs in summarize function: removed `anthropic/` provider prefix (Claude CLI only accepts short IDs like `claude-haiku-4-5`)
- Updated skill description to mention optional AI summarization feature

## [1.3.0] - 2026-03-31

### Added
- Added `--summarize` / `-s` to generate transcript summaries with the Claude CLI.
- Added `--summary-model`, `--summary-style`, and `--summary-lang` flags for summary customization.
- Cached summaries in each transcript cache file under the `summaries` key and reused cached summaries when available.
- Added JSON output support for summaries via a top-level `summary` field.

## [1.1.3] - 2026-03-03

### Changed
- Improved auth/cache docs and synced metadata cleanup changes.


## [1.1.2] - 2026-02-11

### 🆕 Local Caching

- **FREE Repeat Requests:** Transcripts are cached locally — no API cost for re-fetching!
- **Cache Location:** `.cache/` in skill directory (configurable via `YT_TRANSCRIPT_CACHE_DIR`)
- **Cache Management:**
  - `--cache-stats` — View cache statistics
  - `--no-cache` — Bypass cache, fetch fresh
  - `--clear-cache` — Delete all cached transcripts

### 🆕 Batch Mode

- **Multiple Videos:** Process a list of URLs in one command
- **Usage:** `--batch urls.txt` where file contains one URL per line
- **Output:** Shows progress, cached vs fetched count, total cost estimate

### Changed

- **APIFY Auth:** Uses Bearer header instead of query string (more secure)
- **Cache Key:** Based on video ID for simple lookups

### Usage Examples

```bash
# Batch processing
python3 scripts/fetch_transcript.py --batch urls.txt

# View cache stats
python3 scripts/fetch_transcript.py --cache-stats

# Clear cache
python3 scripts/fetch_transcript.py --clear-cache

# Skip cache
python3 scripts/fetch_transcript.py "URL" --no-cache
```

## [1.0.7] - 2026-02-04

- Privacy cleanup: removed hardcoded paths and personal info from docs
