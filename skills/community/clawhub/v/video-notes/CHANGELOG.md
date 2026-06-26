# Changelog

## [1.1.0] - 2026-05-27

### Added
- Bilibili support: extract subtitles from B站 videos (including `ai-zh` format), with automatic cookie-based authentication
- Chinese keyframe scoring: added Chinese heuristic rules covering domain terms like "第X部分/外观/续航/底盘/续航", fixing zero-score issue on Chinese videos

### Fixed
- Language matching now strictly enforced: notes UI language always matches the user's request language, not the video language (e.g. English video + Chinese request → Chinese notes)

### Changed
- `SKILL.md`: upgraded Language matching from soft guideline to mandatory rule with explicit examples

## [1.0.0] - 2026-05-21

### Added
- `extract_subtitles.py`: Downloads and deduplicates YouTube auto-generated subtitles via yt-dlp, outputs clean JSON with timestamps
- `capture_keyframes.py`: Identifies key moments using heuristic scoring, downloads only relevant video sections, extracts frames with ffmpeg, outputs base64-encoded JPEG images
- `assets/note-template.html`: Self-contained HTML template with dark theme, sidebar navigation, scroll-spy, SVG diagram components, keyframe gallery (auto-hides if empty), subtitle search viewer
- `SKILL.md`: Full workflow documentation covering subtitle extraction, keyframe capture, executive summary writing, HTML generation, and quality guidelines
