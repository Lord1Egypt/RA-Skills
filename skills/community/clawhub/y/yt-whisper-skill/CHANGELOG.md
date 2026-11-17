# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/); versioning follows [SemVer](https://semver.org/).

## [2.0.2] - 2026-09-23

### Security
- Removed concrete local secrets-file paths from the shipped docs (`AGENTS.md`, `README.md`,
  `SKILL.md`). The "never commit tokens" guidance is now generic and names no host path.

## [2.0.1] - 2026-09-19

- Renamed the skill/repository to `yt-whisper-skill` (folder, GitHub repo, frontmatter `name`, symlinks and config).

## [2.0.0] - 2026-09-19

- Renamed the skill to `yt-whisper` and moved it into its own repository under `~/Repositories/`.
- Added `*_AISUMMARY.md`: a structured, implementation-oriented report built from a transcript.
- Added `*_AISEARCHPLAN.md`: a compact, deterministic research plan for any input file.
- Reworked `SKILL.md` (complete `description`, `{baseDir}` paths, expanded operating rules).
- Added repository scaffolding: `README`, `LICENSE` (MIT), `.gitignore`, `.env.template`, `CHANGELOG`, `AGENTS.md`.

## [1.0.0] - 2025-07-21

- Initial skill: YouTube audio download + Whisper transcription with category routing.
- Automatic JavaScript runtime resolution for `yt-dlp` (fixes `HTTP Error 403: Forbidden`).
- Installer for the local venv and PATH copy.
