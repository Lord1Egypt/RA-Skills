---
name: video-subtitle-generator
description: Generate and translate video subtitles using WhisperX and LLM translation. Use when processing video files to create .srt subtitle files. Supports multilingual transcription (auto-detect source language), translation to any target language, and bilingual subtitle generation.
---

# Video Subtitle Generator

Multilingual video subtitle generation and translation toolkit built on WhisperX.

## Features

- **Speech transcription**: Extract audio from video and transcribe it into subtitles with automatic source language detection
- **Multilingual translation**: Translate subtitles from any source language into a configurable target language
- **Bilingual subtitles**: Generate source + target bilingual subtitles

## Prerequisites

- Python 3.9+
- [ffmpeg](https://ffmpeg.org/) (required by WhisperX for audio extraction)

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Windows (Chocolatey)
choco install ffmpeg

# Windows (Scoop)
scoop install ffmpeg
```

## Resource requirements

Before running, confirm the user is aware of the following costs:

| Resource | Details |
|----------|---------|
| **Disk** | ffmpeg ~80 MB; Python packages (torch, whisperx, etc.) **2–5 GB**; Whisper model weights 39 MB – 1.5 GB depending on model size |
| **CPU / GPU** | WhisperX runs model inference locally. A CUDA GPU is strongly recommended for `medium` and `large` models. CPU and Apple MPS also work but are significantly slower |
| **Network / API** | Translation step calls a remote LLM API and incurs token-based charges. No network is needed for the transcription step once the model is downloaded |

**Always confirm with the user before installing packages or downloading models**, as these operations consume storage and bandwidth.

**Translation requires an LLM API and will incur costs.** Before executing the translation step:
1. Ask the user for the API provider, key, and base URL — or present any auto-discovered configuration for review
2. Inform the user that translation calls a remote LLM and will consume tokens (i.e. real money)
3. **Do NOT proceed with translation until the user explicitly confirms the provider and acknowledges the cost**

## Usage

### 1. Environment setup

```bash
# Install dependencies (requires ~2–5 GB disk space for PyTorch and WhisperX)
pip install -r requirements.txt

# Set the API key (used for translation)
# macOS / Linux
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://openrouter.ai/api/v1"  # Optional, defaults to OpenRouter

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key"
$env:OPENAI_BASE_URL="https://openrouter.ai/api/v1"
```

> On Windows, use `python` instead of `python3` in all commands below.

### 2. Transcribe video (auto-detect language)

```bash
python3 scripts/transcribe.py "/path/to/video.mp4" -o ./output -m small
```

Output: `video.{detected_lang}.srt` (e.g. `video.en.srt`, `video.ja.srt`)

Arguments:
- `-o`: Output directory
- `-m`: Model size (`tiny`, `base`, `small`, `medium`, `large`)
- `-d`: Device (`cuda`, `cpu`, `mps`), auto-detected by default
- `-l`: Force source language code (e.g. `en`, `ja`, `zh`). Auto-detect if omitted

### 3. Batch-process a directory

```bash
python3 scripts/transcribe.py "/path/to/video/folder" -o ./output -m small
```

### 4. Translate subtitles

> **Cost warning**: This step calls a remote LLM API. Ensure the user has confirmed the API provider, key, and billing awareness before running.

```bash
# Translate to Chinese (default)
python3 scripts/translate.py ./output -o ./translated

# Translate to Japanese
python3 scripts/translate.py ./output -o ./translated -t ja

# Only generate bilingual subtitles
python3 scripts/translate.py ./output -o ./translated --bilingual
```

Arguments:
- `-t`, `--target-lang`: Target language code (default: `zh`)
- `--bilingual`: Generate bilingual (source + target) subtitles
- `--target-only`: Generate target-language-only subtitles
- `--model`: Translation model (default: `google/gemini-3-flash-preview`)
- `--batch-size`: Batch size (default: `10`)

When neither `--bilingual` nor `--target-only` is specified, both are generated.

### 5. Run the full pipeline

```bash
python3 scripts/run.py

# Customize via environment variables
VIDEO_DIR="/path/to/videos" TARGET_LANG=en python3 scripts/run.py
```

Environment variables for `run.py`:
- `VIDEO_DIR`: Video source directory (default: `./videos`)
- `OUTPUT_DIR`: Transcription output directory (default: `./output`)
- `TRANSLATED_DIR`: Translation output directory (default: `./translated`)
- `TARGET_LANG`: Target language code (default: `zh`)
- `WHISPER_MODEL`: Whisper model size (default: `medium`)

## Model selection

| Model | Size | Speed | Accuracy | Best for |
|------|------|------|--------|----------|
| tiny | 39 MB | Fastest | Fair | Quick tests |
| base | 74 MB | Fast | Good | Real-time usage |
| small | 244 MB | Medium | Good | **Recommended** |
| medium | 769 MB | Slower | Very good | Higher quality |
| large | 1550 MB | Slow | Best | Professional use |

## Output files

For each video, the tool generates:
- `*.{lang}.srt` - Source-language subtitles (language auto-detected, e.g. `video.en.srt`)
- `*.json` - Full transcription data with timestamps
- `*.bilingual.srt` - Bilingual subtitles (source + target) after translation
- `*.{target}.srt` - Target-language-only subtitles after translation (e.g. `video.zh.srt`)

## Script overview

### scripts/transcribe.py

Uses WhisperX for transcription and supports:
- Automatic source language detection (or manual override via `-l`)
- Timestamp alignment
- Batch processing with model reuse across files

### scripts/translate.py

Uses an LLM API to translate subtitles and supports:
- Configurable target language (`-t`)
- Batch translation for better efficiency
- Bilingual or target-language-only output
- Custom models and API endpoints
- Automatic retry with exponential backoff on API failures

### scripts/run.py

Cross-platform one-command runner that executes the transcription and translation pipeline automatically.
Paths, target language, and model size are configurable via environment variables.
