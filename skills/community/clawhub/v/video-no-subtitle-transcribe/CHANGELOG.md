# Changelog

## [1.0.3] - 2026-08-22
### Changed
- Renamed the skill heading to “Video No-Subtitle Transcribe”.
- Added a browser download fallback through youtube.iiilab.com after all yt-dlp attempts fail; downloaded local files are then transcribed normally.

## [1.0.2] - 2026-08-15
### Changed
- Full English translation of all docs (README / SKILL.md / CHANGELOG)

## [1.0.1] - 2026-08-15
### Changed
- Removed crypto-specific examples from docs, replaced with generic ones (output format, typo notes)
- Fixed companion skill link: https://clawhub.ai/donnycui/skills/bilibili-youtube-watcher
- Generalized transcription speed description (0.5–1x realtime, 1-hour audio ~30–60 min)
- Limitations no longer name a specific commercial service (now "cloud transcription services")

## [1.0.0] - 2026-08-15
### Added
- Initial open-source release
- One-shot transcription script `scripts/transcribe_video.py`:
  - YouTube client fallback (tv_embedded → android → ios → default), bypasses 429/DRM/SABR
  - faster-whisper local transcription (CPU int8), timestamped transcript output
  - Auto model download + byte-size integrity check (ModelScope mirror)
  - Proxy support: `--proxy` arg / env vars / OpenClaw config fallback
  - Direct transcription of local audio/video files
- Complete pitfalls documentation (SKILL.md / README.md)
