# Video Subtitle Translation & Dubbing Skill

[English] | [简体中文](./README.zh-CN.md)

[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/framework-OpenClaw-orange.svg)](https://github.com/OpenClaw)

A professional-grade **OpenClaw Skill** designed to translate video subtitles and dub audio across multiple languages (e.g., English, Chinese, Japanese, Spanish, French, German, Korean, etc.). It optionally synthesizes target-language voiceovers (TTS) with automatic voice mapping, aligns audio duration, and outputs high-quality, multi-track, multi-subtitle videos.

---

## 🌟 Key Features

- 🛠 **Dual Processing Modes**:
  - **`subtitle_only`**: Translates subtitles only. Keeps the original audio track as the default, embeds both original source and translated target subtitle tracks, and outputs an independent target-language `.srt`/`.vtt` subtitle file.
  - **`subtitle_and_dubbing`** (Default): Translates subtitles and dubs audio. Synthesizes voiceovers in the target language via TTS, automatically aligns and stretches audio clips to fit the original timeline, and muxes them into a dual-audio, dual-subtitle video (target-language audio and subtitles enabled by default).
- ⚖ **3D Adaptive Scheduler**:
  - Implements an advanced scheduling algorithm that adaptively balances **Batch Size**, **Payload Size (tokens/chars)**, and **Concurrency**.
  - Gracefully handles API rate limits (HTTP 429) and context window overflows by dynamically scaling back concurrency, resizing batches, and re-slicing payloads with randomized exponential backoff.
- 🔌 **Pluggable Architecture**:
  - **Translation Providers**: Built-in support for `llm` (LLM chat-completion endpoint with robust JSON parsing, auto-stripping `<think>` blocks) and `web` (Translation web APIs).
  - **TTS Providers**: Built-in support for `llm` and `web` TTS.
- ⚡ **Lossless Muxing**: Employs `ffmpeg` under the hood to perform lossless multi-track video container encapsulation (MKV) without degrading original video quality.

---

## 🧱 Project Structure

```
src/translation_dubbing_skill/
├── models/          # Data models (ProcessingMode, SubtitleEntry, etc.)
├── subtitle/        # Subtitle parser & serializer (SRT/VTT support)
├── providers/       # Pluggable backend adapters
│   ├── translation/ # LLM & Web translation adapters
│   └── tts/         # LLM & Web TTS adapters
├── scheduler/       # 3D Adaptive Scheduler (batch/payload/concurrency sizing)
├── align/           # Audio duration aligner & time-stretching utilities
├── mux/             # FFmpeg wrapper for multi-track video packaging
├── progress/        # Progress reporting & state event listener
├── errors/          # Unified domain exception hierarchy
└── entry/           # Skill entry points & manifest.yaml parser
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.11+**
- **FFmpeg** (Ensure `ffmpeg` is available in your system's `PATH`)
  - **macOS**: `brew install ffmpeg`
  - **Ubuntu**: `sudo apt install ffmpeg`

### 2. Installation
Clone the repository and install the dependencies:
```bash
pip install -e .
# Or install with development requirements for testing:
pip install -e ".[dev]"
```

### 3. Setup Configuration
Copy the environment template and fill in your API credentials:
```bash
cp .env.example .env
```
Fill in the credentials according to the instructions in the `.env` file.

---

## ⚙ Manifest Configuration (manifest.yaml)

As an OpenClaw skill, the configuration parameters are declared in the `manifest.yaml` file:

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `video_path` | `path` | Yes | - | Path to the source video file |
| `subtitle_path` | `path` | No | - | Path to external subtitle (.srt/.vtt); extracts embedded track if omitted |
| `source_language` | `string`| Yes | `en` | Source language of the video/subtitle (e.g., `en`, `zh-CN`, `ja`) |
| `target_language` | `string`| Yes | `zh-CN` | Target language for translation/TTS (e.g., `zh-CN`, `en`, `ja`) |
| `processing_mode` | `enum` | Yes | `subtitle_and_dubbing` | Running mode: `subtitle_only` or `subtitle_and_dubbing` |
| `translation_provider` | `enum` | Yes | - | Translation backend provider: `llm` or `web` |
| `translation_endpoint` | `string`| Yes | - | HTTP endpoint for the translation service |
| `translation_credential`| `secret`| Yes | - | API credential / key for the translation service |
| `tts_provider` | `enum` | Conditionally | - | Required for dubbing: `llm` or `web` |
| `tts_endpoint` | `string`| Conditionally | - | Required for dubbing: HTTP endpoint for TTS |
| `tts_credential` | `secret`| Conditionally | - | Required for dubbing: API key for TTS |

> For advanced scheduling tuning (e.g. custom token batch limits), see the full specification in [manifest.yaml](manifest.yaml).

---

## 🧪 Testing

The project uses `pytest` and property-based testing (`hypothesis`):

```bash
# Run all tests
pytest

# Run fast unit tests only (excluding integration tests)
pytest -m "not integration"
```

---

## 📄 License

This project is licensed under the [Apache-2.0 License](LICENSE).
