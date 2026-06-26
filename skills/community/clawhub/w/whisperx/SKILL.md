---
name: whisperX
description: "WhisperX provides local speech-to-text transcription using OpenAI Whisper, with high-quality offline recognition, no API key required, word-level timestamps, and optional speaker diarization."
metadata:
  {
    "openclaw":
      {
        "emoji": "🎙️",
        "requires": { "bins": ["python3", "ffmpeg"] },
        "install": ["pip install whisperx"],
      },
  }
---

# WhisperX Speech Recognition Skill

**Local offline speech-to-text** - A WhisperX-powered speech recognition skill for OpenClaw. Up to 30x faster than standard OpenAI Whisper, runs fully offline with no API key required.

## Features

- **Pure ASR**: Converts voice messages to text only — no voice replies generated
- **Fully offline**: Model runs locally, no internet or API key needed
- **Word-level timestamps**: Precise per-word time alignment
- **90+ languages**: Includes auto language detection
- **Speaker diarization**: Optional, requires a HuggingFace token

## Installation

```bash
# Install ffmpeg (macOS)
brew install ffmpeg

# Install ffmpeg (Ubuntu/Debian)
apt-get install ffmpeg

# Install WhisperX
pip install whisperx
# or using uvx:
uvx whisperx
```

GPU users: ensure CUDA 12.8 is installed for faster inference.

## Usage

```bash
# Basic transcription (auto-detect language)
whisperx path/to/audio.wav

# Specify model and language
whisperx  --model small --language zh path/to/audio.wav

# CPU mode (low memory)
whisperx --model small --device cpu --compute_type int8  path/to/audio.wav
```

## Notes

- **Dependencies**: `whisperx`, `ffmpeg`
- **Supported formats**: MP3, WAV, OGG, FLAC, M4A, OPUS, AAC, and all other ffmpeg-supported formats
- **Model cache**: Downloaded automatically to `~/.cache/whisper/` on first run
- **Recommended models**: `base` or `small` for CPU; `large-v3` for GPU
