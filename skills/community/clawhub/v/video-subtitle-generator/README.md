# Video Subtitle Generator

Multilingual video subtitle generation and translation toolkit built on [WhisperX](https://github.com/m-bain/whisperX).

Automatically detect the source language from video audio, transcribe it into timestamped subtitles, and optionally translate into any target language via LLM.

## Features

- **Multilingual transcription** — auto-detect source language (or force with `-l`), powered by WhisperX with word-level timestamp alignment
- **Flexible translation** — translate subtitles to any target language via configurable LLM API
- **Bilingual output** — generate source + target bilingual `.srt` files
- **Batch processing** — point at a directory and process all videos in one go
- **One-command pipeline** — `run.py` chains transcription and translation together
- **Cross-platform** — works on macOS, Linux, and Windows with no platform-specific scripts

## Prerequisites

| Dependency | macOS | Linux | Windows |
|-----------|-------|-------|---------|
| Python 3.9+ | `brew install python` | `apt install python3` | [python.org](https://www.python.org/downloads/) |
| ffmpeg | `brew install ffmpeg` | `sudo apt install ffmpeg` | `choco install ffmpeg` or `scoop install ffmpeg` |

## Resource Requirements

| Resource | Details |
|----------|---------|
| Disk | Python packages (PyTorch, WhisperX, etc.) **2–5 GB**; Whisper model weights 39 MB – 1.5 GB depending on model size |
| CPU / GPU | WhisperX runs model inference locally. CUDA GPU strongly recommended for `medium` / `large` models. CPU and Apple MPS work but are significantly slower |
| Network | Translation step calls a remote LLM API (token-based charges apply). Transcription runs fully offline once the model is downloaded |

## Quick Start

```bash
# 1. Clone
git clone https://github.com/yourname/video-subtitle-generator.git
cd video-subtitle-generator

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Transcribe a video (source language auto-detected)
python3 scripts/transcribe.py "/path/to/video.mp4" -o ./output -m small

# 4. Translate subtitles to Chinese (default)
export OPENAI_API_KEY="your-api-key"
python3 scripts/translate.py ./output -o ./translated
```

> **Windows note**: use `python` instead of `python3`, and set environment variables with `$env:OPENAI_API_KEY="your-api-key"` in PowerShell.

## Usage

### Transcribe

```bash
python3 scripts/transcribe.py <video_or_dir> -o ./output -m small
```

| Argument | Description |
|----------|-------------|
| `-o` | Output directory |
| `-m` | Model size: `tiny`, `base`, `small` (recommended), `medium`, `large` |
| `-d` | Device: `cuda`, `cpu`, `mps` (auto-detected if omitted) |
| `-l` | Force source language code (e.g. `en`, `ja`, `zh`). Auto-detect if omitted |

Output: `{name}.{lang}.srt` + `{name}.json`

### Translate

```bash
# Default: translate to Chinese, generate both bilingual and target-only
python3 scripts/translate.py ./output -o ./translated

# Translate to Japanese, bilingual only
python3 scripts/translate.py ./output -o ./translated -t ja --bilingual
```

| Argument | Description |
|----------|-------------|
| `-t` | Target language code (default: `zh`) |
| `--bilingual` | Generate bilingual (source + target) subtitles |
| `--target-only` | Generate target-language-only subtitles |
| `--model` | LLM model name (default: `google/gemini-3-flash-preview`) |
| `--base-url` | API base URL (default: `OPENAI_BASE_URL` env or `https://openrouter.ai/api/v1`) |
| `--batch-size` | Sentences per API call (default: `10`) |

When neither `--bilingual` nor `--target-only` is specified, both are generated.

### Full Pipeline

```bash
python3 scripts/run.py

# Customize via environment variables
VIDEO_DIR="/path/to/videos" TARGET_LANG=en python3 scripts/run.py
```

| Variable | Default | Description |
|----------|---------|-------------|
| `VIDEO_DIR` | `./videos` | Video source directory |
| `OUTPUT_DIR` | `./output` | Transcription output directory |
| `TRANSLATED_DIR` | `./translated` | Translation output directory |
| `TARGET_LANG` | `zh` | Target language code |
| `WHISPER_MODEL` | `medium` | Whisper model size |

## Model Selection

| Model | Size | Speed | Accuracy | Best for |
|-------|------|-------|----------|----------|
| tiny | 39 MB | Fastest | Fair | Quick tests |
| base | 74 MB | Fast | Good | Real-time usage |
| **small** | **244 MB** | **Medium** | **Good** | **Recommended** |
| medium | 769 MB | Slower | Very good | Higher quality |
| large | 1550 MB | Slow | Best | Professional use |

## Output Files

For each video, the tool generates:

```
output/
├── video.en.srt            # Source-language subtitles (lang auto-detected)
└── video.json              # Full transcription data with timestamps

translated/
├── video.bilingual.srt     # Bilingual subtitles (source + target)
└── video.zh.srt            # Target-language-only subtitles
```

## Project Structure

```
video-subtitle-generator/
├── SKILL.md                # Agent skill definition
├── README.md
├── requirements.txt
└── scripts/
    ├── transcribe.py       # WhisperX transcription
    ├── translate.py        # LLM-based translation
    └── run.py              # Cross-platform pipeline runner
```

## License

MIT
