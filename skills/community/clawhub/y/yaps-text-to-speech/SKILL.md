---
name: yaps-text-to-speech
description: "Turn text into spoken audio with Yaps. Choose a supported voice and language, then save the file. New users: install Yaps and sign in."
---

# Yaps Text to Speech

Read [the runtime guide](references/runtime.md) before the first operation. It defines `<yaps>`, account readiness, local permissions, and file handling.

Required Yaps version: 2.3.124 or newer. Check installed command help for later capabilities.

Feature readiness: Reading engines: Kokoro for English, Chatterbox for supported expressive English on Apple Silicon, Supertonic for its supported languages. Query installed support before downloading or selecting voices.

## Workflow

Choose the engine for the language rather than whichever model is installed. Kokoro and Chatterbox are English-only; unsupported characters can disappear while the result sounds fluent. Use Supertonic for a language its installed catalogue supports; do not substitute English pronunciation for an unsupported language. Chatterbox additionally requires a supported Apple Silicon machine.

Use `<yaps> speech synthesize --text-file <input.txt> --mode <kokoro|chatterbox|supertonic> --output <new.wav> --pretty`. Use `--text` only for short, safely quoted input; prefer a private temporary text file for multiline text or shell characters. `--mode` applies to this run and must not change the user's global default. A selected `--voice` belongs to its engine and cannot be carried across an engine change.

Default to a new `<source> Audio.wav`, or `Yaps Speech.wav` with a unique suffix. Verify the file is playable and non-empty, and check beginning/end completeness and pronunciation when playback review is available. Voice cloning is only for a user-provided, authorized voice reference supported by the installed command schema.

## Boundaries

- Do not claim every language is supported or promise a cloned voice without checking the installed schema.
- Preserve existing voice settings and other installed engines.
- Generated audio must contain the supplied text completely, not just have a plausible duration.
