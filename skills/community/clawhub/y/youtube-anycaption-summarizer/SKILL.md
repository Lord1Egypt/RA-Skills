---
name: youtube-anycaption-summarizer
description: "Turn YouTube videos into dependable markdown transcripts and polished summaries — even when caption coverage is messy. This skill works with manual closed captions (CC), auto-generated subtitles, or no usable subtitles at all by using subtitle-first extraction with local Whisper fallback. Supports private/restricted videos via cookies, batch processing, transcript cleanup, language backfill, source-language or user-selected summary language, and end-to-end completion reporting. Ideal for YouTube research, technical walkthroughs, founder content, tutorials, private/internal uploads, and batch video summarization workflows."
metadata: {"openclaw":{"homepage":"https://github.com/arthurli202602-commits/youtube-anycaption-summarizer","requires":{"bins":["yt-dlp","ffmpeg","whisper-cli","python3"]},"install":[{"id":"brew-yt-dlp","kind":"brew","formula":"yt-dlp","bins":["yt-dlp"],"label":"Install yt-dlp (brew)"},{"id":"brew-ffmpeg","kind":"brew","formula":"ffmpeg","bins":["ffmpeg"],"label":"Install ffmpeg (brew)"},{"id":"brew-whisper-cpp","kind":"brew","formula":"whisper-cpp","bins":["whisper-cli"],"label":"Install whisper.cpp CLI (brew)"}]}}
---

# YouTube AnyCaption Summarizer

**The YouTube summarizer that still works when captions are broken, missing, or inconsistent.**

Outputs: raw markdown transcript + polished markdown summary + session-ready result block.

Unlike caption-only tools, this skill still works when subtitles are missing by falling back to local Whisper transcription.

Generate a raw transcript markdown file and a polished summary markdown file from one or more YouTube videos.

This skill is self-contained. It does not require any other YouTube summarizer skill or prior workflow context.

## Best for

- founder videos, operator walkthroughs, and technical explainers
- long tutorial videos that need transcript + implementation summary
- private/internal YouTube uploads that may require cookies
- mixed-caption environments where some videos have CC, some only have auto-captions, and some have no usable subtitles
- batch research workflows where many YouTube links need standardized markdown outputs
- users who want reliable markdown artifacts, not just a one-off chat summary

## Why choose this over simpler transcript skills?

- manual CC first, auto-captions second, local Whisper fallback last
- keeps working when subtitle coverage is weak or missing
- supports private/restricted YouTube videos via cookies
- returns durable markdown artifacts, not just chat text
- supports batch processing and session-ready completion reporting

## Install dependencies

For a fresh macOS setup, new users should be able to copy-paste the following exactly:

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

What this does:
- installs `yt-dlp`, `ffmpeg`, and `whisper-cli`
- creates the default models directory used by this skill if it does not already exist: `~/.openclaw/workspace`
- downloads the default Whisper model file only if it is missing
- avoids touching `~/.openclaw/openclaw.json` or any other OpenClaw config file
- does not delete, replace, or overwrite other files in your existing workspace folder
- verifies that the required binaries and model file are present

If you want to store models elsewhere, pass `--models-dir /path/to/models` when running the workflow.

## Example requests

- “Summarize this YouTube video into markdown.”
- “Generate a transcript and polished summary for this YouTube link.”
- “Process this private YouTube video with my browser cookies.”
- “Batch summarize these YouTube links and give me transcript + summary files.”
- “Use subtitles when available, otherwise transcribe locally.”
- “Create a Chinese summary from this English YouTube video.”

## Quick start

### Single video

```bash
python3 scripts/run_youtube_workflow.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

This creates a dedicated per-video folder, writes the raw transcript markdown, creates the summary placeholder markdown, and prints JSON describing the outputs plus the exact follow-up commands/prompts needed to finish the summary step.

Important: the workflow script alone is not the finished deliverable. The current OpenClaw session must still:
1. infer/backfill the language if the workflow left it as `unknown`
2. overwrite the placeholder `Summary.md` with a real polished summary
3. run `scripts/complete_youtube_summary.py` to validate/finalize the result

### Force simplified Chinese summary

```bash
python3 scripts/run_youtube_workflow.py "https://www.youtube.com/watch?v=VIDEO_ID" \
  --summary-language zh-CN
```

### Restricted video with cookies

```bash
python3 scripts/run_youtube_workflow.py "https://www.youtube.com/watch?v=VIDEO_ID" \
  --cookies /path/to/cookies.txt
```

or

```bash
python3 scripts/run_youtube_workflow.py "https://www.youtube.com/watch?v=VIDEO_ID" \
  --cookies-from-browser chrome
```

### Batch / queue mode

See `references/batch-input-format.md`.

Safe invocation rule for batch mode:
- if you have exactly one URL, use `run_youtube_workflow.py <url>`
- if you have more than one URL, first create a plain-text batch file with one URL per line, then pass only `--batch-file` to the batch runner
- do not pass multiple positional URLs directly to `run_youtube_batch_end_to_end.py`

Recommended end-to-end batch mode:

```bash
cat > ./youtube-urls.txt <<'EOF'
https://www.youtube.com/watch?v=VIDEO_ID_1
https://www.youtube.com/watch?v=VIDEO_ID_2
EOF
python3 scripts/run_youtube_batch_end_to_end.py --batch-file ./youtube-urls.txt
```

When launched from an OpenClaw session, the batch orchestrator can now post best-effort milestone updates back into that same launching session automatically. It only forwards high-signal events like started, summary ready, failed, and batch complete.

Low-level extraction-only batch mode still exists:

```bash
python3 scripts/run_youtube_workflow.py --batch-file ./youtube-urls.txt
```

## Why this skill stands out

This skill is designed to keep working across the messy reality of YouTube:
- if a video has **manual closed captions (CC)**, use them first
- if it only has **auto-generated subtitles**, use those next
- if it has **no usable subtitles at all**, fall back to **local Whisper transcription**

That makes it materially more reliable than caption-only workflows. It works well for caption-rich videos, caption-poor videos, and private/internal uploads where subtitle coverage is inconsistent.

For multi-video requests, prefer the end-to-end batch orchestrator so each video is processed to completion when possible, failures do not block the whole batch, failed items are retried up to 3 times, and the final batch result includes both successful outputs and failed-video reasons. For stability, multi-video requests should always be converted into a batch file first and then run via `run_youtube_batch_end_to_end.py --batch-file ...`.

Core capabilities:
- fetch YouTube metadata first and derive safe output paths
- support single-video mode and batch / queue mode
- handle manual CC, auto-generated subtitles, or no subtitles via subtitle-first extraction with local Whisper fallback
- support restricted/private videos via cookies or browser-cookie extraction
- normalize noisy transcript text before summarization
- create a placeholder summary file, overwrite it with the final summary, and finalize end-to-end timing
- clean up only known intermediates created by the workflow unless explicitly told otherwise

## What this skill produces

For each video, create exactly one dedicated output folder containing these final deliverables:
- `SANITIZED_VIDEO_NAME_transcript_raw.md`
- `SANITIZED_VIDEO_NAME_Summary.md`

By default, delete only the known intermediate media, subtitle, and WAV files created by the workflow. Do not wipe unrelated files that may already exist in the per-video folder.

## Required local tools

Verify these tools exist before running the workflow:
- `yt-dlp`
- `ffmpeg`
- `whisper-cli`
- `python3`

The workflow also requires a supported Whisper ggml model file in the configured models directory.

## Bundled scripts

Use these scripts directly:
- `scripts/run_youtube_workflow.py` — main deterministic workflow for metadata, download/subtitles, transcription, placeholder summary creation, cleanup, and workflow metadata emission
- `scripts/run_youtube_batch_end_to_end.py` — recommended batch orchestrator for multiple URLs; processes videos sequentially to completion when possible, retries failed items up to 3 times, and returns final success/failure results including failed-video reasons and successful-item `end_to_end_total_seconds`
- `scripts/backfill_detected_language.py` — update `transcript_raw.md`, `Summary.md`, and workflow metadata after the current session LLM decides the major transcript language
- `scripts/complete_youtube_summary.py` — validate that `Summary.md` is no longer a placeholder, optionally backfill language, compute the final end-to-end timing report for one item, and emit a session-ready result block
- `scripts/normalize_transcript_text.py` — convert raw timestamped transcript text into cleaner summary input without modifying the raw transcript file
- `scripts/finalize_youtube_summary.py` — lower-level timing helper used by the completion flow
- `scripts/prepare_video_paths.py` — derive sanitized folder and output file paths from a title and video ID

Useful references:
- `references/detailed-workflow.md` — full operational workflow, completion rules, batch guidance, naming rules, and practical notes
- `references/summary-template.md` — required structure and writing rules for the final `Summary.md`
- `references/session-output-template.md` — required user-facing output format to return to the current OpenClaw session after completion
- `references/batch-input-format.md` — input format for queue / batch processing

## Defaults

- Default parent output folder: `~/Downloads`
- Default whisper model: `ggml-medium`
- Supported whisper models: `ggml-base`, `ggml-small`, `ggml-medium`
- Default media mode: audio-only
- Default transcript language: auto-detect if transcription is needed
- Default summary language: `source`
- Raw transcript keeps timestamps

## Public workflow overview

At a high level, the skill does this:
1. fetch metadata first and create safe output paths
2. try manual subtitles, then auto-captions, then local Whisper fallback
3. write `SANITIZED_VIDEO_NAME_transcript_raw.md`
4. create `SANITIZED_VIDEO_NAME_Summary.md` as a placeholder
5. have the current OpenClaw session overwrite the placeholder with a real summary
6. run `scripts/complete_youtube_summary.py` to validate completion, backfill language if needed, and emit a session-ready result block

## What counts as completion

For a normal end-to-end request, completion means all of the following are true:
1. the workflow script succeeded
2. if language was initially `unknown`, the language was backfilled into both markdown files
3. the placeholder summary file was overwritten with a real summary
4. `scripts/complete_youtube_summary.py` was run successfully
5. the user received the resulting output paths and timing/result status

If the workflow script succeeded but the summary/completion step did not happen yet, describe the state as partial/in-progress rather than complete.

## When to read the deeper references

Read these as needed:
- `references/detailed-workflow.md` when you need the full implementation contract, batch guidance, naming rules, cleanup rules, timing flow, or debugging details
- `references/summary-template.md` before writing the final polished `Summary.md`
- `references/session-output-template.md` before returning the final user-facing per-video result block
- `references/batch-input-format.md` when handling `--batch-file`
- `references/batch-end-to-end-behavior.md` when handling multi-video end-to-end completion with retry and final success/failure reporting

## Practical public promise

This skill is optimized for dependable end-to-end output, not just quick transcript extraction:
- raw transcript markdown
- polished summary markdown
- session-ready completion report
