---
name: mlx-whisper
description: Local speech-to-text with MLX Whisper (Apple Silicon optimized, no API key).
homepage: https://github.com/ml-explore/mlx-examples/tree/main/whisper
---

# MLX Whisper

Local speech-to-text using Apple MLX, optimized for Apple Silicon Macs.

## Quick Start

```bash
mlx_whisper /path/to/audio.mp3 --model mlx-community/whisper-large-v3-turbo
```

Always pass `--model mlx-community/whisper-large-v3-turbo`, unless the user explicitly asks for a different model.

## Common Usage

```bash
# Transcribe to text file
mlx_whisper audio.m4a -f txt -o ./output

# Transcribe with language hint
mlx_whisper audio.mp3 --language en --model mlx-community/whisper-large-v3-turbo

# Generate subtitles (SRT)
mlx_whisper video.mp4 -f srt -o ./subs

# Translate to English
mlx_whisper foreign.mp3 --task translate
```

## Notes

- Requires Apple Silicon Mac (M1/M2/M3/M4)
- Models cache to `~/.cache/huggingface/`