---
name: video-no-subtitle-transcribe
displayName: Video No-Subtitle Transcribe
slug: video-no-subtitle-transcribe
description: Fallback transcription for videos without subtitles. When a video (YouTube/Bilibili, etc.) has no subtitles, subtitle endpoints are disabled or fail, download audio with yt-dlp and transcribe locally with faster-whisper, outputting a full timestamped transcript. Triggers: no subtitles, transcribe video, subtitles disabled, whisper transcription, extract speech.
version: 1.0.4
---

# Video No-Subtitle Transcribe

When subtitle-based approaches (e.g. bilibili-youtube-watcher) fail — video has no CC/auto-generated subtitles, or the subtitle endpoint is disabled by YouTube ("Subtitles are disabled for this video") — use this skill: **download audio → local speech recognition → timestamped transcript**.

## Use Cases
- YouTube/Bilibili videos without subtitles (creator disabled CC or auto-generated captions)
- Subtitle endpoints rate-limited/disabled by YouTube
- Any yt-dlp-supported site, or local audio/video files

## Prerequisites
- `yt-dlp` (pip install yt-dlp or brew install yt-dlp)
- `faster-whisper` (pip install faster-whisper)
- `ffmpeg` (system package)
- whisper small model: `~/.local/share/whisper-small/model.bin` (auto-downloaded from ModelScope if missing, ~483MB)

## Usage

```bash
python3 {baseDir}/scripts/transcribe_video.py "<URL>" --lang zh --out /tmp/transcript.txt
```

Arguments:
- `--lang`: language code, `zh` for Chinese, `en` for English (default zh)
- `--out`: output file path (default transcript.txt)
- `--proxy`: proxy URL, e.g. `http://127.0.0.1:7890` (default: env vars HTTPS_PROXY/HTTP_PROXY, then OpenClaw config)

Output format: one line per segment, `[start-end seconds] text`, e.g. `[2.0-4.0] Hello everyone, welcome to today's session`

## Workflow (full pipeline)
1. User provides a video link → first try the subtitle path (bilibili-youtube-watcher)
2. Subtitle path fails (no subs / disabled / fetch error) → use this skill
3. Download audio with this script (yt-dlp client fallbacks run automatically).
4. **If every yt-dlp download attempt fails**, use the browser fallback below to obtain an audio/video file, then run this script again with that local file path.
5. After transcription, read the output transcript → understand content by timeline → structured summary for the user

## Browser download fallback (only after yt-dlp fails)

Use this only when the script reports `[dl] FAILED`; do not send a video link to a third-party downloader before trying the local yt-dlp path.

1. Open `https://youtube.iiilab.com/` in the browser.
2. Paste the **YouTube** video URL into the site, start its parse/download flow, and select the best available audio format (preferred) or a video file.
3. Download the resulting file to a local path. If the site requests login, a CAPTCHA, payment, permissions, or any acknowledgement that data will be sent to a third party, stop and ask the user before proceeding.
4. Transcribe the downloaded local file; no yt-dlp download is needed:

```bash
python3 {baseDir}/scripts/transcribe_video.py "<LOCAL_AUDIO_OR_VIDEO_FILE>" --lang zh --out /tmp/transcript.txt
```

**Privacy note:** This fallback submits the source URL to `youtube.iiilab.com`, a third-party service. Tell the user before using it for private, unlisted, sensitive, or client-owned videos. Do not use it for non-YouTube URLs; report the yt-dlp failure instead.

## Pitfalls (must follow)

1. **YouTube's default client gets 429/bot-checked** ("Sign in to confirm you're not a bot") → try audio clients in order: `tv_embedded` (most reliable, bypasses DRM/SABR experiments, verified) → `android` → `ios` → default. The Android client may hit the SABR-only experiment (formats without URLs) — normal, just try the next client.

2. **Use the ModelScope CN mirror for model download** (~1MB/s): `https://modelscope.cn/models/Systran/faster-whisper-small/resolve/master/model.bin`. Don't use HuggingFace direct (very slow from China via proxy, ~90KB/s), and don't use the hf-mirror endpoint (its xet protocol silently corrupts files).

3. **Verify model integrity**: the intact file is exactly 483546902 bytes. If it doesn't match, delete and re-download; if whisper errors with `File model.bin is incomplete: failed to read a buffer...` the file is corrupt. Don't use a fixed size as the "done" signal — let the request finish naturally and verify the byte count.

4. **Proxy**: YouTube requires a proxy (mainland China); ModelScope direct access needs no proxy. Proxy priority: `--proxy` argument > env vars > OpenClaw config.

5. **Transcription params**: `WhisperModel(dir, device='cpu', compute_type='int8')` + `transcribe(audio, language=lang, vad_filter=True)`. Speed is roughly 0.5–1x realtime (1-hour audio takes ~30–60 min). Be patient, don't kill the process early.

6. **Homophone typos** (e.g. 在/再, 做/作 confusion) are normal for whisper small — restore by context when summarizing.

## Limitations
- Transcription quality depends on audio clarity; fast speech/noise cause errors
- Slower than cloud transcription services (minutes vs seconds), but **completely free, runs locally, no privacy leakage**

## License
MIT
