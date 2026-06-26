# Changelog

## [1.0.6] - 2026-03-24

### Fixed
- Remove trailing comma in `plugin.json` that caused JSON parse error during installation

## [1.0.5] - 2026-03-24

### Fixed
- Remove `dependencies` field from `plugin.json` — `youtube-transcript-api` is a Python package managed by `uv` at runtime, not a Claude plugin dependency

## [1.0.3] - 2026-03-24

### Fixed
- Replace bash-specific path resolution with a pure Python one-liner for full cross-platform support (Linux, macOS, Windows)

## [1.0.2] - 2026-03-24

### Fixed
- Fix script path resolution: look up `fetch_transcript.py` in the plugin cache first, then fall back to `~/.claude/skills/`, so the skill works after installing via `/plugin install` without requiring a manual file copy

## [1.0.0] - 2026-03-23

### Added
- Initial release
- Fetch YouTube video transcripts via `youtube-transcript-api`
- Structured summary generation (Overview, Key Points, Notable Quotes)
- Multi-language support with `--lang` flag
- Automatic language fallback when preferred language is unavailable
- Support for multiple YouTube URL formats (watch, shorts, embed, youtu.be, bare ID)
- Optional save to Markdown file
