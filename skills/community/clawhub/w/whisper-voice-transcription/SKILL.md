---
name: whisper-voice-transcription
description: Build and use whisper.cpp for local speech-to-text workflows, with optional cloud fallback when local transcription is not practical.
tags: [speech-to-text, stt, voice, transcription, whisper, audio]
version: 1.1.1
---

# Whisper Voice Transcription with whisper.cpp

## When to use

- You want local speech-to-text without sending audio to a third party.
- You need a fallback workflow when a built-in transcription tool fails.
- You want an operator guide for compiling and running `whisper.cpp`.

## Prerequisites

- `git`
- `cmake`
- a C or C++ compiler
- `ffmpeg`

## Build steps

```bash
git clone --depth 1 https://github.com/ggerganov/whisper.cpp.git ~/whisper.cpp
cd ~/whisper.cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j4
```

Download a model from the official `ggerganov/whisper.cpp` releases or Hugging Face repository and place it under `~/whisper.cpp/models/`.

## Standard transcription flow

```bash
ffmpeg -y -i input_audio.ogg -ar 16000 -ac 1 -f wav /tmp/voice.wav
~/whisper.cpp/build/bin/whisper-cli \
  -m ~/whisper.cpp/models/ggml-large-v3.bin \
  -f /tmp/voice.wav \
  -l auto \
  --no-timestamps
```

## Fallback workflow

If a higher-level tool fails, first locate the exact cache or upload path used by that tool. Search only within the expected application cache directory instead of scanning the entire home directory.

## Cloud fallback

If local transcription is too slow or unavailable, use an approved speech API and tell the user that audio will leave the machine.

## Guardrails

- Download binaries and models only from official sources.
- Verify hashes when possible.
- Do not search unrelated directories for audio files.
- Be explicit when using a cloud provider because that changes the privacy model.
