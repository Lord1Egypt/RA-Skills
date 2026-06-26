# YouTube AnyCaption Summarizer

Turn YouTube videos into dependable markdown transcripts and polished summaries — even when caption coverage is messy.

**Why this exists:** most YouTube transcript tools work well only when subtitle coverage is good. This skill is built for the real world: manual closed captions, auto-generated subtitles, private videos, and no-usable-caption cases where local Whisper fallback is required.

## What makes it different

- **Manual CC first** for the cleanest available source
- **Auto-captions second** when manual subtitles are missing
- **Local Whisper fallback** when YouTube subtitles are unavailable or unusable
- **Private/restricted video support** via cookies / browser-cookie extraction
- **Batch mode** for processing multiple YouTube links in one workflow
- **Markdown-first outputs** designed for durable research notes and reusable artifacts
- **Session-ready completion reporting** for OpenClaw workflows

## Outputs

For each video, the workflow produces:

- `SANITIZED_VIDEO_NAME_transcript_raw.md`
- `SANITIZED_VIDEO_NAME_Summary.md`
- a session-ready completion block for the current OpenClaw session

## Best for

- founder videos and operator walkthroughs
- technical explainers and tutorial breakdowns
- private/internal YouTube uploads
- research pipelines that need standardized markdown output
- mixed-caption environments where some videos have CC, some only have auto-captions, and some need full fallback transcription

## Quick install (macOS)

```bash
brew install yt-dlp ffmpeg whisper-cpp
MODELS_DIR="$HOME/.openclaw/workspace"
MODEL_PATH="$MODELS_DIR/ggml-medium.bin"
mkdir -p "$MODELS_DIR"
if [ ! -f "$MODEL_PATH" ]; then
  curl -L https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.bin \
    -o "$MODEL_PATH.part" && mv "$MODEL_PATH.part" "$MODEL_PATH"
else
  echo "Model already exists at $MODEL_PATH — leaving it unchanged."
fi
command -v python3 yt-dlp ffmpeg whisper-cli
ls -lh "$MODEL_PATH"
```

This setup is intentionally non-destructive:
- it does **not** overwrite the workspace folder itself
- it does **not** edit `~/.openclaw/openclaw.json`
- it does **not** overwrite `ggml-medium.bin` if it already exists

## Quick start

### Single video

```bash
python3 scripts/run_youtube_workflow.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Force a target summary language

```bash
python3 scripts/run_youtube_workflow.py "https://www.youtube.com/watch?v=VIDEO_ID" \
  --summary-language zh-CN
```

### Private or restricted video

```bash
python3 scripts/run_youtube_workflow.py "https://www.youtube.com/watch?v=VIDEO_ID" \
  --cookies-from-browser chrome
```

### Batch mode

```bash
python3 scripts/run_youtube_workflow.py --batch-file ./youtube-urls.txt
```

## How the workflow works

1. fetch video metadata first
2. create safe output paths and per-video folders
3. try manual subtitles, then auto-captions
4. fall back to local Whisper when needed
5. write a raw transcript markdown artifact
6. generate a polished summary markdown artifact
7. run completion/finalization to return a session-ready result

## Example use cases

- “Summarize this YouTube video into markdown.”
- “Process this private YouTube video with my browser cookies.”
- “Batch summarize these 20 YouTube links.”
- “Use subtitles when available, otherwise transcribe locally.”
- “Generate a Chinese summary from this English YouTube video.”

## ClawHub

Live skill page:

- https://clawhub.ai/arthurli202602-commits/youtube-anycaption-summarizer

## Notes

- The skill is optimized for **dependable output artifacts**, not just a one-off chat response.
- If language detection is inconclusive, the workflow supports **language backfill** after transcript inspection.
- Deep implementation details live in the bundled references, especially `references/detailed-workflow.md`.

## License

MIT-0
