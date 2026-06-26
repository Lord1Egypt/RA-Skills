---
name: video-to-srt
description: Generate timecoded SRT subtitles from local video or audio files. Use when a user wants a local low-cost subtitle workflow, asks to transcribe local media into SRT with timestamps, or needs subtitle files that can be imported into editing tools.
---

# Video to SRT

## Workflow

1. Create a new top-level task folder for the request in the workspace.
2. Locate the user's local media file and confirm the language choice only if it is unclear.
3. Run `scripts/run_local_subtitles.sh` from this skill folder.
4. Default to `--language zh` and `--model small`. Switch to `--language auto` for mixed language audio. Switch to `--model medium` only when the user wants better accuracy and accepts slower runtime.
5. Inspect the generated `.srt` file by checking the first and last few cues before handing it off.
6. Return the subtitle path and mention that editors which accept `SRT`, including Jianying desktop, can import it.

## Stable Defaults

- Keep dependency installation inside a local virtual environment created by `scripts/run_local_subtitles.sh`.
- Keep caches local to the skill folder. This avoids macOS cache permission issues.
- Keep `HF_HUB_DISABLE_XET=1` enabled. This avoids a common Hugging Face Xet download failure.
- Prefer `SRT`. It is the simplest subtitle format for broad editor compatibility.
- Override `VENV_DIR`, `HF_HOME`, or `XDG_CACHE_HOME` only when reusing an existing environment or model cache is helpful.

## Commands

Use the wrapper script for the normal path:

```bash
scripts/run_local_subtitles.sh "/absolute/path/to/video.mp4" --output-dir "/absolute/path/to/task/output" --copy-next-to-input
```

Use these common variants:

```bash
scripts/run_local_subtitles.sh "/absolute/path/to/video.mp4" --language auto --output-dir "/absolute/path/to/task/output" --copy-next-to-input
scripts/run_local_subtitles.sh "/absolute/path/to/video.mp4" --model medium --output-dir "/absolute/path/to/task/output" --copy-next-to-input
```

## Validation

- If the wrapper needs to install packages or download a model, request permission when required by the environment.
- Confirm that the final `.srt` exists.
- Preview the first and last cues with `sed -n '1,24p'` and `tail -n 24`.
- If the user wants a faster import workflow, keep a copy beside the source media with `--copy-next-to-input`.

## Resources

- `scripts/run_local_subtitles.sh`: create or reuse a local virtual environment, install dependencies, configure stable cache paths, and run transcription.
- `scripts/transcribe_to_srt.py`: transcribe media and write timecoded SRT output.
- `scripts/requirements.txt`: minimal dependency list for the workflow.
