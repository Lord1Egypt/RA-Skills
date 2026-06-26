# Toolchain Reference

## Pipeline overview

The bundled entrypoint is:
- `skills/video-knowledge-ingest/scripts/video-ingest.sh`

It calls:
- `scripts/video_ingest.py` inside this skill
- `yt-dlp`
- `ffmpeg` / `ffprobe`
- bundled `scripts/whisper-gpu.sh`
- `summarize --cli codex`

## Dependency checklist

Required runtime tools:
- `yt-dlp`
- `ffmpeg`
- `ffprobe`
- `summarize`
- `codex`

Required local environment for Whisper:
- workspace venv: `/home/jason/.openclaw/workspace/.venv-whisper-gpu`
- bundled wrapper: `skills/video-knowledge-ingest/scripts/whisper-gpu.sh`
- bundled transcriber: `skills/video-knowledge-ingest/scripts/whisper_gpu_transcribe.py`

## Default storage layout

```text
knowledge/video-notes/
  index.jsonl
  YYYY-MM-DD/
    <platform>-<id>-<slug>/
      source.url | source.path
      source.info.json
      downloads/
      whisper/
      transcript.txt
      summary.md
      record.json
```

## Transcript source meanings

Typical `record.json` values:
- `subtitles:source.zh.vtt`
- `subtitles:source.en.srt`
- `whisper-gpu`
- `whisper-cpu`
- `text:<filename>`

Interpretation:
- `subtitles:*` => subtitle-first path succeeded
- `whisper-gpu` => remote/local media was transcribed on GPU
- `whisper-cpu` => GPU failed; CPU fallback succeeded
- `text:*` => local text/markdown input was summarized directly

## Platform expectations

### YouTube
- Usually best when subtitles exist
- May hit anti-bot / login barriers on some IPs
- If subtitles fail or are absent, media download + Whisper is the fallback

### Bilibili
- Shared links often need normalization to `www.bilibili.com`
- May not expose subtitles cleanly to `yt-dlp`
- Whisper fallback is common

### Xiaohongshu
- Metadata and download can work through `yt-dlp`
- Subtitles are often unavailable
- Expect Whisper fallback frequently

## Summary backend

The script currently uses:
- `summarize --cli codex --force-summary`

So the environment must satisfy both:
- `summarize` installed and working
- `codex` installed and logged in

If the environment changes later, update only the summarize call in `scripts/video_ingest.py`; keep the rest of the workflow intact.
