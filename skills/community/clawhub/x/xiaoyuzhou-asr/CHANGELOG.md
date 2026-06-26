# Changelog

## v2.0.0 (2026-05-05)

Major feature release with significant improvements across all areas.

### New Features

- **Interactive login** (`--login`): phone number → verification code → save tokens to config file
- **Batch transcription** (`--pid + --count`): transcribe N most recent episodes of a podcast
- **Output formats** (`--format markdown|srt|txt`): SRT subtitles with segment-aware timestamps
- **Podcast discovery** (`--podcast-info`): search podcasts and display PID, subscriptions, episode count
- **Episode listing** (`--list-episodes`): browse recent episodes before batch transcription
- **Environment check** (`--check-env`): validate all dependencies (ffmpeg, xyz API, token, ASR, model)
- **Config file** (`~/.xiaoyuzhou-asr.json`): persistent token and path settings
- **Version flag** (`--version`)

### Improvements

- Custom exception hierarchy (TranscriptionError/ApiError/TokenExpiredError/DependencyError/AudioError)
- Auto-detect ASR binary and model paths with env var override
- Download retry (3 attempts) for network resilience
- Batch mode checkpoint/resume (skips already-transcribed episodes)
- SRT timestamps use actual segment durations with character-proportional timing
- Transcription progress percentage display
- Cross-platform safe filename generation (sanitize_filename)
- Settings resolved from CLI arg > env var > config file
- Auto token refresh on 401

### Infrastructure

- 36 unit tests (pytest)
- GitHub Actions CI (Python 3.10-3.13)
- mypy type checking (zero errors)
- pyproject.toml for standard Python packaging

## v1.0.0 (2026-05-01)

Initial release.
