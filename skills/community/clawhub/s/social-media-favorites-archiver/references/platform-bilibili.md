# Bilibili

The adapter discovers collection IDs in the user's authenticated Bilibili page context, then delegates favorite-list extraction, BV/AV normalization, WBI handling, media format negotiation, multi-part videos, and native subtitle extraction to `yt-dlp`.

- Use only the dedicated Chrome profile configured for this application.
- Never copy cookies or browser databases into project files or CLI arguments.
- A QR, captcha, or device confirmation is a user-owned pause; do not bypass it.
- Native SRT data returned by `yt-dlp` is normalized with explicit human, AI, or unknown-platform provenance. When no usable subtitle exists, the item remains valid and schedules local ASR.
- Multi-part videos remain one canonical note with ordered part chapters.
- Private, deleted, or unavailable favorites retain safe metadata rather than disappearing silently.
- Real favorite content and signed media URLs belong only in ignored live-work paths, never fixtures or Git.

## Local ASR benchmark

Development-machine smoke benchmark on 2026-08-08:

- Backend/model: `mlx-whisper 0.4.3` / `mlx-community/whisper-tiny`
- Architecture: Apple Silicon `arm64`
- Input: 3.308-second synthetic Mandarin clip generated locally with the macOS Ting-Ting voice
- Warm-cache elapsed time: 3.028 seconds; real-time factor 0.915
- Result: speech outcome with one bounded timestamped segment
- Model cache: 141.9 MiB; generated input/intermediate disk use: 0.2 MiB

This is a compatibility smoke test, not a universal speed or accuracy claim. The tiny model and synthetic voice are less representative than real saved videos, and users may select a larger local model when accuracy matters. The lightweight Task 18 run completed a real native-subtitle item and inventoried real no-subtitle candidates, but did not heavy-process the live ASR fallback path; that gap remains explicit in the live verification report.
