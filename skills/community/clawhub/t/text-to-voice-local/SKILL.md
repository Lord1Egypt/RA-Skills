---
name: text-to-voice-local
description: Local text-to-voice generation for OpenClaw workspaces using a canonical txt-to-mp3 pipeline. Use when the user wants to turn any prepared text into voice, asks to set up or reuse a local text-to-speech workflow, wants one canonical output mp3 path, wants a reusable wrapper for Telegram voice delivery, or wants to replicate the same text-to-voice setup on another OpenClaw instance.
---

# Text to Voice Local

Use the bundled scripts to create one stable local text-to-voice path.

## Goal

Produce voice from any text file with:
- one canonical input text path,
- one canonical output mp3 path,
- one high-level wrapper for routine use,
- low-level scripts for debugging only.

## Canonical paths

Default input text:
- `tmp/text-to-voice-input.txt`

Canonical output:
- `tmp/voice-mode-latest.mp3`

State directory:
- `skills/text-to-voice-local/state/`

State pointer:
- `skills/text-to-voice-local/state/last-output.txt`

## Main command

For normal use, run:
- `scripts/text_to_voice.sh voice <text-file> [voice] [max_direct_chars]`

Useful helpers:
- `scripts/text_to_voice.sh status`
- `scripts/text_to_voice.sh voices`

`status` now also checks runtime dependencies and prints install hints when something is missing.

Examples:
```bash
scripts/text_to_voice.sh text
scripts/text_to_voice.sh voice ./tmp/text-to-voice-input.txt
scripts/text_to_voice.sh voice ./tmp/text.txt ru-RU-SvetlanaNeural 280
```

## What the scripts do

- `scripts/text_to_voice.sh`
  - high-level entrypoint for normal use
- `scripts/tts_from_file.sh`
  - one text file to one mp3
- `scripts/tts_from_file_chunked.sh`
  - long text to multiple chunks and final merged mp3
- `scripts/voice_reply.sh`
  - safe wrapper that updates canonical output and pointer
- `scripts/voice_reply_latest.sh`
  - always refresh canonical latest mp3
- `state/text-to-voice.json`
  - stores default voice, max chars, and canonical paths
- `scripts/edge_tts.js`
  - low-level TTS helper used by the file wrappers

## Install notes

Ensure these dependencies exist on the target machine:
- `node`
- `ffmpeg`
- `node-edge-tts`

The skill checks these at runtime and, if something is missing, prints suggested install commands instead of failing silently.

Verify:
```bash
node -v
ffmpeg -version
node -e "require('node-edge-tts'); console.log('node-edge-tts ok')"
```

If `node-edge-tts` is missing:
```bash
npm i -g node-edge-tts
```

## Setup steps on another OpenClaw

1. Copy this skill folder into the target workspace skills directory.
2. Make scripts executable.
3. Ensure `tmp/` exists.
4. Put text into a txt file.
5. Run the main command.

Minimal setup:
```bash
chmod +x skills/text-to-voice-local/scripts/*.sh
mkdir -p tmp
skills/text-to-voice-local/scripts/text_to_voice.sh voice ./tmp/text-to-voice-input.txt
```

## Delivery rule

If the result is sent as Telegram voice, send only the canonical file:
- `./tmp/voice-mode-latest.mp3`

Prefer sending text and voice as separate messages.

## Important constraint

Progress printed by shell scripts is useful in terminal diagnostics, but chat-side live progress editing depends on OpenClaw preview streaming, not shell stdout alone.

## When to use low-level scripts

Use low-level scripts only for debugging or careful manual control.
Default to the high-level wrapper unless there is a reason not to.
