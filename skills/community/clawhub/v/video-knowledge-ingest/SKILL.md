---
name: video-knowledge-ingest
description: Ingest and summarize cross-platform videos into a local knowledge base. Use when working with YouTube, Bilibili, Xiaohongshu, or local media/subtitle files and you need to fetch subtitles when available, fall back to yt-dlp download + ffmpeg + Whisper transcription when subtitles are missing, generate a text summary, and save transcript/summary/metadata into local files. Also use when packaging this workflow for sub-agents or debugging failures such as subtitle 429s, Bilibili share-link 403s, YouTube anti-bot issues, Xiaohongshu no-subtitle cases, missing ffmpeg/yt-dlp/Whisper dependencies, or summarize/codex auth problems.
---

# Video Knowledge Ingest

Use this skill as the default cross-platform video → transcript → summary → local-knowledge workflow.

## Quick start

1. Run the bundled entrypoint:
   - `skills/video-knowledge-ingest/scripts/video-ingest.sh "<url-or-local-file>"`
2. Read the JSON stdout for paths.
3. Send the summary back to the user from `summary.md`.
4. Keep the stored files in the local knowledge base; do not move them unless asked.

Default knowledge-base root:
- `/home/jason/.openclaw/workspace/knowledge/video-notes/`

## What this skill invokes

Core tools in the normal path:
- `yt-dlp` — resolve metadata, fetch subtitles, or download media
- `ffmpeg` / `ffprobe` — normalize audio before transcription
- bundled `scripts/whisper-gpu.sh` — local Whisper transcription using the workspace GPU venv
- `summarize --cli codex` — generate the final written summary
- local filesystem — persist transcript, summary, metadata, and index entries

Platform-specific notes:
- **YouTube**: prefer subtitles when available; fall back to media download + Whisper
- **Bilibili**: often falls back to Whisper; the script auto-normalizes `bilibili.com/...` to `www.bilibili.com/...` and strips `spm_` tracking params
- **Xiaohongshu**: usually no subtitles; expect media download + Whisper
- **Local subtitle/text files**: skip download and summarize directly
- **Local media files**: skip `yt-dlp`; go straight to Whisper

## Workflow

### 1. Normalize the source

- If the input is a URL, use the bundled normalizer.
- Keep YouTube timing parameters (`t`, `start`, `list`, `index`) but drop common tracking params.
- For Bilibili, force `www.bilibili.com` and remove `spm_*` query params.

### 2. Try subtitles first

- Run `yt-dlp` in subtitle-only mode.
- Prefer `zh.*` and `en.*` subtitles.
- Treat subtitle download as **best effort**.
- If any usable `.srt` / `.vtt` file lands, continue with that file even if another subtitle variant returned a non-zero exit code.

### 3. Fall back to media + Whisper

If no usable subtitles land:
- Download best audio/media with `yt-dlp`
- Transcribe with bundled `scripts/whisper-gpu.sh`
- If GPU transcription fails, the script falls back to CPU automatically

### 4. Summarize

- Summarize the resulting transcript with `summarize --cli codex --force-summary`
- Expect `codex` to be installed and logged in, or configure the summarize backend another way before use

### 5. Persist results

For each ingested item, keep these files:
- `source.url` or `source.path`
- `source.info.json`
- `downloads/` (when remote media/subtitles are fetched)
- `whisper/` (when Whisper was used)
- `transcript.txt`
- `summary.md`
- `record.json`
- global append-only index: `knowledge/video-notes/index.jsonl`

## Common commands

Remote URL:
```bash
skills/video-knowledge-ingest/scripts/video-ingest.sh "https://www.youtube.com/watch?v=..."
skills/video-knowledge-ingest/scripts/video-ingest.sh "https://bilibili.com/video/BV..."
skills/video-knowledge-ingest/scripts/video-ingest.sh "https://www.xiaohongshu.com/explore/..."
```

Local files:
```bash
skills/video-knowledge-ingest/scripts/video-ingest.sh /path/to/file.srt
skills/video-knowledge-ingest/scripts/video-ingest.sh /path/to/file.mp4
```

Custom output root:
```bash
skills/video-knowledge-ingest/scripts/video-ingest.sh "<source>" --kb-root /some/other/root
```

## When to read bundled references

Read `references/toolchain.md` when you need:
- dependency details
- exact file layout
- how each tool is used in the pipeline

Read `references/troubleshooting.md` when you hit:
- YouTube anti-bot / cookies issues
- Bilibili 403 on shared links
- subtitle 429 / partial subtitle failures
- Xiaohongshu subtitle absence
- summarize / codex auth failures
- Whisper venv, CUDA, ffmpeg, or yt-dlp problems

## Operating rules

- Prefer the bundled `scripts/video-ingest.sh` entrypoint over re-implementing the workflow.
- Do not skip the local knowledge-base write unless explicitly asked.
- When a run fails, inspect the generated directory before declaring total failure; partial artifacts often explain the real issue.
- If a platform provides subtitles, prefer them over Whisper.
- If subtitles are absent or unusable, fall back to media + Whisper automatically.
