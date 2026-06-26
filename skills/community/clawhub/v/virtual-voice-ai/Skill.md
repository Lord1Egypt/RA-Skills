---
name: voice-pipeline
description: Wires a real microphone through an AI brain (STT → LLM → TTS) and routes the output to a virtual audio cable so apps like Google Meet hear the processed voice. Use when building a real-time voice interception layer in a Node.js project.
requires:
  env:
    - DEEPGRAM_API_KEY
    - LLM_PROVIDER
    - LLM_API_KEY
    - LLM_MODEL
    - TTS_PROVIDER
    - TTS_API_KEY
    - VIRTUAL_CABLE_NAME
  system:
    - ffmpeg (must be in PATH)
    - VB-Audio Cable (Windows) or BlackHole 2ch (macOS)
---

# Voice Pipeline Skill

Guide the user through building a real-time audio interception pipeline in Node.js.
The pipeline: Mic → ffmpeg resample → Deepgram STT → LLM → Sentence chunker → TTS → PCM decode → VB-Cable.

## Capabilities

1. **OS Prep**: Walk through virtual audio driver install and ffmpeg setup.
2. **Device Discovery**: Run `scripts/01_list_devices.js` to find the exact VB-Cable name.
3. **Step-by-step build**: Execute scripts 01–07 in order, stress-testing each before proceeding.
4. **Kill switch**: Export a `stop()` function the host app calls to instantly halt the pipeline.
5. **Env wiring**: Write required keys to the project's `.env` file.

## Critical Rules

- Never use `naudiodon` or `electron` — both are incompatible with a portable Node.js skill.
- Always resample to 16kHz mono PCM before sending to Deepgram.
- Never stream raw LLM tokens to TTS — buffer to sentence boundaries first.
- TTS output (MP3) must be decoded to PCM before writing to VB-Cable.
- The kill switch must be IPC-based, not `globalShortcut` (Electron-only).

## Execution Order

Run each script independently to stress-test before wiring together.

```
Step 1 → OS prep (no code, see references/step_by_step.md)
Step 2 → scripts/package.json + npm install
Step 3 → node scripts/01_list_devices.js
Step 4 → node scripts/02_capture_resample.js
Step 5 → node scripts/03_deepgram_ws.js
Step 6 → node scripts/04_llm_stream.js + scripts/05_sentence_chunker.js
Step 7 → node scripts/06_tts_ws.js + scripts/07_pcm_write.js
```

## Progressive Loading

For architecture diagram and signal flow: read `references/architecture.md`.
For full corrected step-by-step: read `references/step_by_step.md`.
For all required env vars: read `references/env_schema.md`.