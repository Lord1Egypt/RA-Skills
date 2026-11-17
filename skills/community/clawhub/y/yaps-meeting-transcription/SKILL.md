---
name: yaps-meeting-transcription
description: "Make a meeting transcript with speaker labels in Yaps. Correct it, export it, or ask questions. New users: install Yaps and sign in."
---

# Yaps Meeting Transcription

Read [the runtime guide](references/runtime.md) before the first operation. It defines `<yaps>`, account readiness, local permissions, and file handling.

Required Yaps version: 2.3.124 or newer. Check installed command help for later capabilities.

Feature readiness: Meeting/Sherpa; optional MOSS on supported Apple Silicon systems. Inspect features and group help before selecting an engine. Recaps also need the local chat model.

## Workflow

Write a private temporary JSON request with an absolute `input`, optional `title`, `engine` (default `auto`), and optional integer `speakers` from 1 to 20. Run `node <skill-root>/runtime/run.mjs meeting-file <request.json>`. Remove only the request file. The helper extracts a temporary WAV for recognized video types through Yaps, then creates the durable meeting project; Yaps retains its own project audio.

Use `auto` by default. Use `sherpa` for cross-platform execution or a supplied speaker count. Use `moss` only when installed and supported on Apple Silicon; it detects speakers itself and cannot take a speaker-count hint. Treat the returned engine and reason as authoritative. A project with no transcript segments is not a successful meeting.

Inspect `<yaps> meeting show <id>` and `meeting speakers <id>` before editing. Use stable segment IDs with `meeting correct <id> --segment <id> --text-file <file>` or `meeting assign <id> --segment <id> --speaker <number>`. Roster numbers are 1-based. Use `rename-speaker` for a name correction; use `merge-speakers <id> --speakers 3,4 --into 2` only after the user identifies the same participant. Never infer identity from voice alone. Export using `meeting export <id> --output <new.md>`.

For requested recaps, use `meeting summarize <id>` and then `meeting chapters <id>`. Reuse a recap unless regeneration is requested or its transcript/template changed. For a grounded question, use `meeting ask <question> --meeting <id> --scope meeting`; `--scope all` requires an explicit cross-meeting request. Preserve returned source citations. Never edit project JSON directly.

## Boundaries

- No joining calls or starting live recording on the user's behalf.
- Speaker labels are diarization labels until the user supplies identities.
- Recaps are generated interpretations, not verbatim transcript. Preserve project audio and existing exports.
