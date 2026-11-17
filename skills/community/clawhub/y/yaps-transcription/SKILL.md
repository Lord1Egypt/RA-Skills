---
name: yaps-transcription
description: "Turn an audio or video file into text with Yaps. Good for interviews, podcasts, and voice memos. New users: install Yaps and sign in."
---

# Yaps Transcription

Read [the runtime guide](references/runtime.md) before the first operation. It defines `<yaps>`, account readiness, local permissions, and file handling.

Required Yaps version: 2.3.124 or newer. Check installed command help for later capabilities.

Feature readiness: Subtitles/Whisper: inspect features list; install with features subtitles --enable only when the download is authorized.

## Workflow

Choose a new `.txt` destination beside the input, such as `Interview Transcript.txt`. Write a private temporary JSON request file containing `input` and `output`, both absolute paths. Run `node <skill-root>/runtime/run.mjs transcribe-file <request.json>`. Remove only that request file afterwards.

The helper uses Yaps's `srt generate` engine, stages its SRT in an owned temporary directory, and exports the returned plain transcript. It exclusively publishes a completed text file, refuses replacement, rejects blank speech, and removes the temporary SRT. It does not require Python.

Report the returned output path, engine, duration, and word count. Read transcript contents only for a requested review or downstream task. If structured processing fails, its coded error is the result; inspect the matching CLI command for recovery guidance without automatically launching a second long job.

## Boundaries

- Use the SRT vertical when timestamps are requested; use Meetings for speaker labels.
- Do not invent missing phrases or label a blank/partial decode as complete.
- No silent cloud transcription fallback.
