---
name: yaps-srt-generator
description: "Make a timed SRT subtitle file from audio or video with Yaps. New users: install Yaps and sign in."
---

# Yaps Subtitle Generator

Read [the runtime guide](references/runtime.md) before the first operation. It defines `<yaps>`, account readiness, local permissions, and file handling.

Required Yaps version: 2.3.124 or newer. Check installed command help for later capabilities.

Feature readiness: Subtitles/Whisper, enabled through features subtitles --enable after an authorized model download.

## Workflow

Choose a new absolute `<source> Subtitles.srt` path. Write a private request JSON object with `input` and `output` absolute paths. Run `node "<skill-root>/runtime/run.mjs" srt-file <request.json>`. Remove only that temporary request file afterward. This adapter generates into owned temporary storage, checks numbered cues and ordered positive timings, then atomically publishes without replacing an existing destination, including one created during inference. Do not use raw `srt generate --output` for delivery: the installed CLI can overwrite an existing file.

Confirm the output is non-empty and inspect its actual content. Check first, middle, and final cues against the source when review is requested; timestamps alone do not prove words are correct. Return the subtitle file with engine, duration, and word count from Yaps. Report silence or coded failures accurately.

## Boundaries

- This creates sidecar subtitles, not burned-in captions.
- Do not renumber or shift timings while translating unless the user asks for retiming.
- No empty subtitle file presented as success.
