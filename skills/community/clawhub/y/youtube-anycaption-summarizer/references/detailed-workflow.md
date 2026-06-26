# Detailed Workflow Reference

Use this reference when you need the full end-to-end operational contract for the skill, especially for batch runs, post-processing, or implementation/debugging work.

## Dependency setup for new users

For a fresh macOS setup, install and verify the default dependency stack with:

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

This setup flow:
- does not overwrite the workspace directory itself
- does not edit `~/.openclaw/openclaw.json` or other OpenClaw config files
- does not overwrite `ggml-medium.bin` if it already exists
- only creates the model file when it is missing

Default assumptions used by the skill after that:
- `python3`, `yt-dlp`, `ffmpeg`, and `whisper-cli` are on `PATH`
- the default model is `ggml-medium`
- the default models directory is `~/.openclaw/workspace`
- the default model file path is `~/.openclaw/workspace/ggml-medium.bin`

If you store model files elsewhere, use `--models-dir /path/to/models`.

## 1. Collect inputs

Accept either:
- one YouTube URL, or
- `--batch-file` with one YouTube URL per line

Invocation rule:
- if there is exactly one URL, run `scripts/run_youtube_workflow.py <url>`
- if there is more than one URL, first create a batch file, then run the batch script with `--batch-file`
- do not pass multiple positional URLs directly to `scripts/run_youtube_batch_end_to_end.py`

Optional flags:
- `--parent`
- `--model`
- `--models-dir`
- `--language`
- `--summary-language`
- `--full-video`
- `--dry-run`
- `--subtitle-first` or `--no-subtitle-first`
- `--cookies`
- `--cookies-from-browser`
- `--retries`
- `--retry-backoff`
- `--keep-intermediates`
- `--continue-on-error`

Important interpretations:
- `--language auto` means detect transcription language when Whisper is used.
- `--summary-language source` means write the summary in the same language as the apparent source/transcript language when possible.
- `--full-video` keeps video download mode instead of audio-only download mode.
- `--dry-run` fetches metadata and planned output paths without downloading media or transcribing.
- `--keep-intermediates` preserves temporary files for debugging.

## 2. Fetch metadata first

Fetch video metadata before downloading media.
- use the original title inside markdown content
- use a filesystem-safe sanitized title for the folder name and filename prefix

Use `scripts/prepare_video_paths.py` when you only need safe naming logic.

## 3. Create a dedicated subfolder per video

Create:

```text
PARENT_DIR/SANITIZED_VIDEO_NAME/
```

If the sanitized folder already exists for another video, append `__VIDEO_ID`.
If it matches the same video ID, overwrite the outputs in place.

## 4. Subtitle-first fallback

Try subtitles before audio transcription.

Order:
1. manual subtitles if available
2. automatic captions if available
3. local transcription fallback with `whisper-cli`

If a subtitle track is usable:
- convert it into timestamped transcript text
- keep only clean timestamps in the raw transcript line prefix, for example `[00:00:02.070 --> 00:00:06.950]`
- merge rolling subtitle chunks when the previous chunk end timestamp falls within the next chunk range
- deduplicate continued words/phrases across merged chunks
- save the cleaned result into the raw transcript markdown
- skip the local audio transcription path

If subtitles are missing or unusable:
- download media
- convert to WAV
- transcribe with `whisper-cli`

## 5. Retry / backoff for `yt-dlp`

All `yt-dlp` operations should use the built-in retry wrapper.
Use `--retries` and `--retry-backoff` when the user wants to tune behavior.

## 6. Cookies support for restricted videos

When a video is age-restricted, login-gated, or otherwise blocked, support:
- `--cookies /path/to/cookies.txt`
- `--cookies-from-browser BROWSER_NAME`

Do not invent cookies. Use only what the user explicitly provides or what `yt-dlp` can safely read from the named browser.

## 7. Save the raw transcript markdown

Save the raw transcript as:

```text
SANITIZED_VIDEO_NAME_transcript_raw.md
```

The raw transcript keeps timestamps.
It should include:
- 视频标题 / Video Title
- 来源 / Source
- Video ID
- Whisper model used
- detected language (`unknown` at first if deterministic detection is inconclusive, then backfilled by the current session LLM after transcript inspection)
- transcript body
- workflow metadata JSON

The workflow metadata JSON is important because the completion/finalization flow uses it to compute end-to-end timing later.

## 8. Normalize transcript text before summarization

Use `scripts/normalize_transcript_text.py` to produce a cleaner summary input without modifying the raw transcript file.

Example:

```bash
python3 scripts/normalize_transcript_text.py /path/to/raw_transcript.md
```

Use that cleaned output when the transcript is noisy, repetitive, or too hard to summarize directly from the raw timestamped text.

## 9. Create and then overwrite the summary placeholder

The workflow script creates:

```text
SANITIZED_VIDEO_NAME_Summary.md
```

as a placeholder so cleanup can still leave only the two required markdown files.

Then the current OpenClaw session model should overwrite that placeholder with the final polished summary in the same task. Do not stop after the workflow script if the user asked for the completed result.

Important:
- treat the workflow script output as an intermediate handoff, not the finished deliverable
- if the workflow leaves language as `unknown`, inspect the transcript and decide the main transcript language yourself
- overwrite the placeholder summary before reporting completion
- the final `Summary.md` must not contain placeholder status text
- after writing the final summary, run `scripts/complete_youtube_summary.py`; pass `--language LANGUAGE_TAG` when language was initially `unknown`
- include the completion/finalizer result when reporting success/failure to the user

Use the requested summary language:
- if `summary-language=source`, match the source language
- otherwise, write the summary in the user-requested language

Use the structure in `references/summary-template.md`.

### Quality bar for `Step-by-Step Execution / Deployment Details`
- make it the most operationally useful section in the document
- capture the workflow in real execution order
- include setup, config, auth, model/tool choices, commands, files, outputs, validation, and deployment/operational considerations whenever the transcript supports them
- write it so a beginner could realistically follow the same strategy or reproduce the same deployment/process from the summary
- if a required implementation detail is missing from the transcript, call that out explicitly instead of hand-waving or fabricating it

## 10. Cleanup

After the workflow script finishes, keep the final deliverables:
- `SANITIZED_VIDEO_NAME_transcript_raw.md`
- `SANITIZED_VIDEO_NAME_Summary.md`

Delete only known intermediates created by the current workflow run, such as:
- downloaded subtitle files
- downloaded media files
- generated WAV files

Do not delete unrelated files that happen to exist in the same folder. If `--keep-intermediates` was explicitly requested, preserve those known intermediates as well.

## 11. End-to-end timing

`run_youtube_workflow.py` reports deterministic timing for:
- metadata fetch
- subtitle fetch, if used
- media download, if used
- WAV conversion, if used
- language detection, if used
- transcription, if used
- transcript cleanup
- cleanup
- script total so far

To capture **true end-to-end timing including summary generation**, do this:
1. record a summary start timestamp immediately before the LLM writes the final summary
2. overwrite the summary placeholder with the final summary
3. run:

```bash
python3 scripts/complete_youtube_summary.py RAW_TRANSCRIPT_PATH SUMMARY_PATH --summary-start-epoch EPOCH_SECONDS
```

If language was initially unknown, include:

```bash
--language LANGUAGE_TAG
```

This returns:
- deterministic total seconds
- summary generation seconds
- end-to-end total seconds
- final detected language
- whether post-processing is complete
- a session-ready result block when run with `--format session`

## What counts as completion

Do not report success immediately after `run_youtube_workflow.py` finishes unless the user only asked for preparation.

For a normal end-to-end request, completion means all of the following are true:
1. the workflow script succeeded
2. if language was initially `unknown`, the language was backfilled into both markdown files
3. the placeholder summary file was overwritten with a real summary
4. `scripts/complete_youtube_summary.py` was run successfully
5. the user received the resulting output paths and timing/result status

If the workflow script succeeded but the summary/finalization step did not happen yet, describe the state as partial/in-progress rather than complete.

## Batch / queue mode guidance

Batch mode processes URLs sequentially.
When handling more than one URL, create a plain-text batch file first and invoke the batch orchestrator with `--batch-file`.
For each item it will:
- fetch metadata
- try subtitles first
- fall back to transcription if needed
- create the raw transcript markdown
- create the summary placeholder markdown
- clean intermediates

After deterministic processing, do **mandatory post-processing sequentially for every item**:
1. inspect the raw transcript
2. if language is `unknown`, infer the main transcript language and remember the language tag
3. overwrite the placeholder summary with a real polished summary that follows `references/summary-template.md`
4. run `scripts/complete_youtube_summary.py` for that item
5. collect the JSON completion report for that item
6. run the same completion script with `--format session` or reuse the `session_report` field from the JSON output
7. send the resulting per-video block back to the current OpenClaw session using the format in `references/session-output-template.md`

Do not report batch success until every item has a completion report showing the summary is no longer a placeholder and post-processing is complete, and the user-facing result blocks are ready.

## Naming rules

Apply these rules strictly:
- all files use prefix `SANITIZED_VIDEO_NAME`
- raw transcript filename suffix: `_transcript_raw.md`
- polished summary filename suffix: `_Summary.md`
- all video-specific files live in the same dedicated subfolder
- only the two markdown files remain after cleanup unless the user explicitly keeps intermediates

## Return results to the current session

After a video is fully processed, return a user-facing result block to the current OpenClaw session.

Preferred method:
- run `scripts/complete_youtube_summary.py ... --format session`
- paste that exact block into the current session

For batch mode:
- generate one block per video
- keep the original processing order
- separate blocks with a blank line

The required format is defined in `references/session-output-template.md`.

## Practical notes

- Prefer audio-only unless the user explicitly wants the full video.
- Verify `yt-dlp`, `ffmpeg`, and `whisper-cli` exist before running.
- Verify the requested ggml model file exists before fallback transcription.
- Use subtitle-first mode by default because it is often faster and sometimes more accurate.
- Market this capability clearly: the skill works well for videos with manual CC, videos with only auto-generated subtitles, and videos with no usable subtitles.
- If subtitles are absent or unusable, fall back cleanly to Whisper without treating that as a workflow failure.
- Use the transcript normalization helper before summarizing when the raw transcript is messy or when rolling captions create repeated phrases.
- When language auto-detection is inconclusive, record `unknown` rather than pretending the language is known.
- `--cookies-from-browser` may require local browser/keychain access and can hang or fail in locked-down/headless environments; prefer explicit cookie files when reliability matters.
- Private/login-gated video access should be validated with a real test video before blaming the rest of the pipeline.
- If the transcript is tiny or low-information, write a correspondingly small, honest summary instead of inventing detail.
- If the transcript is too large, summarize in chunks and then synthesize the final summary.
