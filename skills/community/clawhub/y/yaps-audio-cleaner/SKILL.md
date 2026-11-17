---
name: yaps-audio-cleaner
description: "Reduce noise, hiss, and static in a speech recording with Yaps. Save a separate clean file. New users: install Yaps and sign in."
---

# Yaps Audio Cleaner

Read [the runtime guide](references/runtime.md) before the first operation. It defines `<yaps>`, account readiness, local permissions, and file handling.

Required Yaps version: 2.3.124 or newer. Check installed command help for later capabilities.

Feature readiness: Audio Cleaner; use the installed feature catalogue for required models and supported quality modes.

## Workflow

Choose `recommended` by default, including for long recordings. Choose `quick` when the user prioritizes speed or requests a test pass. Use `maximum` for difficult noise when the user values quality over processing time, and explain that it can take several times the recording duration.

Run `<yaps> audio clean <input> --quality recommended --output <new.wav> --pretty`. Omit the output only if Yaps's safe naming is appropriate. Never pass `--overwrite` without permission for the exact output; never target the source.

Confirm non-empty output, duration, and channels from the result or media probe. Listen to representative sections when audio review is available, especially consonants, quiet speech, and noisy transitions. Return the cleaned file and reported processing metrics. A smaller noise floor alone is not proof of preserved speech. Keep separate versions for quality comparisons.

## Boundaries

- Do not promise perfect restoration or choose Quick only because the file is long.
- Denoising must preserve spoken content, timing, and the original recording.
- Do not automatically launch a second expensive quality pass.
