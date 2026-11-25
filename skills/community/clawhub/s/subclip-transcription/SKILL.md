---
name: subclip-transcription
description: Transcribe project speech for understanding, editing, or dubbing without automatically creating visible captions. Use for transcript-only, speech analysis, translation preparation, and dialogue references.
---

# Project transcription

Choose the transcript's purpose before starting:

- For understanding, summaries, rough cuts, translation, or dubbing preparation, call `transcribe_project` with `purpose: "reference"` and an exact `audioItemId` or `mediaItemId`. Use `allTimelineClips: true` only when the whole audible edit is the intended source. This saves timed words and available speaker IDs under `.agent/transcripts/<transcriptId>.json` plus a readable `.md` file. It does not change the timeline, caption panel, or DynamicCaptionsInlineEditor.
- For visible subtitles or Dynamic Captions, call `transcribe_project` with `purpose: "captions"` and follow subclip-text-captions or subclip-dynamic-captions. A bare request to transcribe is reference work unless the creator asks to show words in the video.

Use existing project captions or a saved reference transcript when the exact source and current trim still match. Call `list_reference_transcripts` to find saved transcripts and `get_reference_transcript` with its ID to read timed words in pages. Do not repeat recognition just to recover context. Use `get_transcription_status` for external MCP polling; the in-app agent should keep the returned job ID and wait for its completion callback.

The local mode runs on-device Whisper. Cloud mode may consume credits and is required for speaker detection; pass `detectSpeakers: true` only when speaker labels are needed. Preserve the creator's mode preference. Use base ISO language codes.

For dubbing without source captions, pass the saved exact-item `referenceTranscriptId` to `create_dubbing_workspace`. The workspace uses its timed words and speakers directly. Generate visible target-language captions after the dub only when the creator asked for them or visible source captions are being replaced.
