# VideoARM-Skill 🎬

This repository contains the **official OpenClaw implementation** of [VideoARM](https://arxiv.org/abs/2512.12360) accepted at CVPR 2026. VideoARM is a coarse-to-fine video reasoning paradigm over hierarchical multimodal memory (HM<sup>3</sup>) for long-form video understanding. By leveraging the proposed complementary toolsets and HM<sup>3</sup>, VideoARM can progressively localize, interpret, and abstract evidence in an adaptive observe–think–act–memorize loop. Extensive experiments on prevalent long-video understanding benchmarks demonstrate that VideoARM maintains strong performance while significantly reducing token consumption.


## How It Works

```
Main Session (clean context)
  └── spawn VideoQA Controller
        ├── videoarm-download    → download YouTube / URL
        ├── videoarm-info        → get metadata (fps, duration, frames)
        ├── videoarm-audio       → transcribe audio segments
        ├── videoarm-extract-frames → extract frame grids
        ├── spawn Image Analyzer → analyze frames in clean context
        └── return final answer
```

The controller runs in an **isolated sub-agent** to keep the main session context clean. Frame analysis is delegated to further sub-agents — no vision API keys needed, just OpenClaw's built-in image understanding.

## Installation

**Prerequisites:**
- Python 3.10+
- [ffmpeg](https://ffmpeg.org/) (`brew install ffmpeg` / `apt install ffmpeg`)
- [OpenClaw](https://github.com/openclaw/openclaw) running

```bash
git clone https://github.com/qiankemeng/VideoARM-skill.git
cd VideoARM-skill

# Basic install
pip install -e .

# With audio transcription
pip install -e ".[audio]"

# With YouTube download
pip install -e ".[download]"

# Everything
pip install -e ".[all]"
```

After installing, verify your environment:

```bash
videoarm-doctor
```

This checks Python version, ffmpeg, yt-dlp, Python packages, and Whisper model status.

## Quick Start

```bash
# Install
git clone https://github.com/qiankemeng/VideoARM-skill.git
cd VideoARM-skill && pip install -e ".[all]"

# Verify installation
videoarm-doctor

# Try it out
videoarm-info /path/to/video.mp4
videoarm-audio /path/to/video.mp4 --start 0 --end 60
videoarm-extract-frames --video /path/to/video.mp4 \
  --ranges '[{"start_frame":0,"end_frame":1500}]' --num-frames 20
```

## Configuration

### Platform Support

VideoARM works with any video source that yt-dlp supports, including:
- YouTube
- Bilibili (哔哩哔哩)
- Twitter/X
- TikTok / 抖音
- Local files (.mp4, .mkv, .avi, etc.)

For region-restricted content, set `HTTPS_PROXY` in your `.env` file.

**Audio transcription works out of the box** — `faster-whisper` is included as a default dependency. No API keys needed.

On first run, the Whisper `base` model (~150MB) is automatically downloaded.

### Multilingual Support

Whisper auto-detects the language — no configuration needed. It supports 99+ languages.
For better accuracy with non-English videos, use a larger model:

```bash
# In .env
WHISPER_MODEL=small   # better for non-English, accents, dialects
```

### Optional: Use a cloud API instead

If you prefer faster transcription or better accuracy, set a cloud API in `.env`:

```bash
cp .env.example .env
```

| Option | Setup | Speed |
|--------|-------|-------|
| **Local** (default) | Nothing to configure | ~1x realtime on CPU |
| **Groq** | Set `WHISPER_API_KEY` | Very fast, free tier |
| **OpenAI** | Set `WHISPER_API_KEY` | Fast, ~$0.006/min |

### Local model selection

Set `WHISPER_MODEL` in `.env` to choose model size:

| Model | Size | RAM | Accuracy |
|-------|------|-----|----------|
| `tiny` | 39MB | ~1GB | Basic |
| `base` | 74MB | ~1GB | Good (default) |
| `small` | 244MB | ~2GB | Better |
| `medium` | 769MB | ~5GB | Great |
| `large-v3` | 1.5GB | ~10GB | Best |

## Usage with OpenClaw

### As an OpenClaw Skill

Place this directory in your OpenClaw workspace. When you ask a video question, the agent reads `SKILL.md` and spawns a controller sub-agent automatically.

```
User: Analyze this video and tell me who opened the watermelon
      https://www.youtube.com/watch?v=...

Agent: [reads SKILL.md → spawns controller → returns answer]
```

### CLI Tools (Standalone)

Each tool works independently from the command line:

```bash
# Get video metadata
videoarm-info video.mp4

# Extract 30 frames from a time range (returns grid image path)
videoarm-extract-frames --video video.mp4 \
  --ranges '[{"start_frame":0,"end_frame":1500}]' \
  --num-frames 30

# Transcribe audio (start/end in seconds)
videoarm-audio video.mp4 --start 0 --end 300

# Download from YouTube
videoarm-download "https://www.youtube.com/watch?v=..."
```

## CLI Reference

| Command | Description | Output |
|---------|-------------|--------|
| `videoarm-info <video>` | Video metadata | JSON: fps, total_frames, duration, has_audio |
| `videoarm-extract-frames` | Extract frame grid image | JSON: image_path, frame_ranges |
| `videoarm-audio <video>` | Transcribe audio segment | JSON: transcript, segments[] |
| `videoarm-download <url>` | Download video | JSON: path, cached |
| `videoarm-doctor` | Check all dependencies | Human-readable or `--json` |
| `videoarm-clean` | Clean temporary files | Human-readable or `--json`; supports `--dry-run`, `--downloads` |

## Project Structure

```
VideoARM-skill/
├── SKILL.md              # OpenClaw skill instructions (the brain)
├── videoarm_cli/          # CLI tools
│   ├── videoarm_info.py
│   ├── videoarm_extract_frames.py
│   ├── videoarm_audio.py
│   ├── videoarm_download.py
│   ├── videoarm_doctor.py  # Dependency checker
│   └── videoarm_clean.py   # Cache cleaner
├── videoarm_lib/          # Shared library
│   ├── config.py          # Paths and database
│   ├── frames.py          # Frame extraction logic
│   ├── resolve.py         # Video path resolution
│   ├── video_meta.py      # Metadata extraction
│   └── logger.py          # Tool tracer
├── videoarm_local_whisper/ # Local Whisper server
│   ├── server.py
│   └── setup.py
├── examples/              # Usage examples
├── .env.example           # Configuration template
├── pyproject.toml         # Package config
└── LICENSE                # MIT
```

## How the Agent Reasons

1. **Download & Inspect** — Get video metadata (duration, fps, audio availability)
2. **Strategy** — Choose audio-first (dialogue questions) or frames-first (visual questions)
3. **Extract & Analyze** — Use tools iteratively, writing findings to memory
4. **Cross-verify** — Confirm with a second modality if confidence is low
5. **Answer** — Return answer with evidence chain and confidence score

## Data Storage

All cached data stored under `~/.videoarm/`:
- `video_database/temp/downloads/` — Downloaded videos
- `video_database/temp/processing/` — Temporary processing files

## Related Work

- [VideoARM](https://github.com/qiankemeng/VideoARM) — The research paper this skill is based on
- [OpenClaw](https://github.com/openclaw/openclaw) — The agent platform this skill runs on

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `yt-dlp not found` | `pip install yt-dlp` |
| `ffmpeg not found` | `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux) |
| `opencv-python not found` | `pip install opencv-python` |
| Download timeout | Set `HTTPS_PROXY=http://...` in `.env` |
| Poor transcription accuracy | Use larger model: `WHISPER_MODEL=small` in `.env` |
| `videoarm-doctor` shows issues | Follow the suggested fix for each item |

Run `videoarm-doctor` to diagnose most issues automatically.

## License

MIT — see [LICENSE](LICENSE)
