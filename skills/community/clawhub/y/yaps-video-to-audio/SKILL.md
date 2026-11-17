---
name: yaps-video-to-audio
description: "Save the sound from a video as MP3, WAV, or M4A with Yaps. New users: install Yaps and sign in."
---

# Yaps Video to Audio

Read [the runtime guide](references/runtime.md) before the first operation. It defines `<yaps>`, account readiness, local permissions, and file handling.

Required Yaps version: 2.3.124 or newer. Check installed command help for later capabilities.

Feature readiness: Yaps media extraction and the installed FFmpeg dependency. Check media extract-audio help; no separate speech model is required.

## Workflow

Choose MP3 unless the user requests WAV or M4A. Use WAV for a requested lossless working copy feeding another audio workflow. Select a new `<source> Audio.<format>` path.

Run `<yaps> media extract-audio <video> --format <mp3|wav|m4a> --output <new-audio> --pretty`. Confirm the result exists, is non-empty, has a playable audio stream, and has the expected duration. Preserve the video and prior exports.

A video with no audio must return that condition rather than an empty success file. If media dependencies are missing, use the runner's specific guidance; install only when authorized. Do not replace this integration with ad-hoc conversion software silently.

## Boundaries

- No transcript, denoising, or scene editing is implied by extraction.
- Format conversion may re-encode; do not label MP3 as lossless.
- Do not extract unrelated tracks or change the source video.
