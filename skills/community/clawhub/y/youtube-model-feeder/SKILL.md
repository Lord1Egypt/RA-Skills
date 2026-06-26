---
name: "YouTube Model Feeder"
description: "Food for your model — extract transcripts, key frames, OCR, slides, and LLM summaries from YouTube videos into structured AI-ready knowledge."
version: "1.0.0"
emoji: "🧠"
homepage: "https://github.com/celstnblacc/youtube-model-feeder"
user-invocable: true
disable-model-invocation: false

requires:
  bins: ["docker"]
  anyBins: ["ffmpeg"]
  env: []
---

# YouTube Model Feeder

> **Food for your model.**

Stop pausing videos every 30 seconds to screenshot, paste into Obsidian, and caption. Every 20-minute tutorial shouldn't take an hour to document.

YouTube Model Feeder extracts everything from a YouTube video — timestamped transcript, key frame snapshots, OCR of code and slides, presentation slide detection, and LLM-generated summaries — and packages it into structured knowledge your AI assistant can search, reference, and reason about.

## Why This Exists

The problem isn't transcription — ten tools do that. The problem is **structured context**. When you feed a raw transcript to a model, it has no visual context. It doesn't know what was on screen when the speaker said "as you can see here." It can't read the code in the terminal, the diagram on the slide, or the config file being edited.

YouTube Model Feeder captures all of that. The output isn't just text — it's a knowledge bundle: transcript segments aligned to timestamps, screenshots of every key moment, OCR text from code snippets and slides, and an LLM summary that ties it all together.

**Combined with [obsidian-semantic-search](https://clawhub.ai/skills/obsidian-semantic-search)** (also on ClawHub), every video you watch becomes permanently searchable by meaning in your Obsidian vault.

## What It Extracts

### Full Pipeline

| Step | Tool | What it produces |
|------|------|-----------------|
| **Download** | yt-dlp | Video + audio + metadata (title, duration, thumbnail) |
| **Transcribe** | Whisper (Ollama) or YouTube captions | Timestamped transcript segments |
| **Frame Extraction** | FFmpeg | Key frame snapshots every 5s (configurable) |
| **Slide Detection** | SSIM analysis (OpenCV) | Identifies presentation slides via structural similarity between frames |
| **OCR** | Tesseract | Reads code, terminal output, and text from captured frames |
| **LLM Summary** | Ollama / OpenAI / Anthropic | Structured markdown with sections, code blocks, and key takeaways |

### Slide Detection (Deep)

Not just frame captures — intelligent slide boundary detection:

1. **Layout detection** — classifies video as full-frame, picture-in-picture, or split panel
2. **SSIM transition scan** — compares consecutive frames for structural changes (threshold: SSIM < 0.85)
3. **LLM disambiguation** — borderline transitions (0.85–0.93 SSIM) sent to LLM for classification
4. **Slide grouping** — merges transitions into slides with enforced minimum duration (3s)
5. **Final-state capture** — saves the last frame of each slide as JPEG
6. **OCR extraction** — runs Tesseract on each slide image
7. **Transcript alignment** — maps transcript segments to slide time ranges

### Output Formats

| Format | What you get |
|--------|-------------|
| **Markdown** | Timestamped sections with headings, code blocks, image references |
| **HTML** | Styled single-page doc with embedded screenshots |
| **Obsidian bundle** | ZIP export: markdown + images, ready to drop into your vault |

## Installation

### Prerequisites

```bash
# macOS
brew install ffmpeg tesseract

# Linux
apt install ffmpeg tesseract-ocr
```

Docker Desktop must be running for the full backend.

### Start the Stack

```bash
git clone https://github.com/celstnblacc/youtube-model-feeder.git
cd youtube-model-feeder
docker-compose up -d
```

This starts 5 services:

| Service | Port | Purpose |
|---------|------|---------|
| **api** | 8000 | FastAPI backend + Swagger docs at `/docs` |
| **celery_worker** | — | Background video processing |
| **postgres** | 5432 | Job tracking, transcripts, documents |
| **redis** | 6379 | Task queue (Celery broker) |
| **web** | 3000 | Next.js frontend (optional) |

### Verify

Open `http://localhost:8000/docs` — you should see the Swagger API documentation.

## Usage

### Via AI Assistant

**Extract a video:**
> "Extract everything from this YouTube video and save it to my vault: https://youtube.com/watch?v=..."

**Transcript only:**
> "Get the timestamped transcript for this video"

**Slides and code screenshots:**
> "Extract all the code screenshots and presentation slides from this tutorial"

**Obsidian export:**
> "Convert this video into an Obsidian note with screenshots and timestamps"

### Via API

```bash
# Submit a video for processing
curl -X POST http://localhost:8000/jobs \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/watch?v=dQw4w9WgXcQ"}'

# Check job status
curl http://localhost:8000/jobs/{job_id}

# Get the generated document
curl http://localhost:8000/videos/{video_id}
```

### Via Web UI

Open `http://localhost:3000`, paste a YouTube URL, and watch the extraction happen in real time with progress tracking.

## LLM Provider Selection

Per-user configuration — choose your summarization engine:

| Provider | Model (default) | Setup | Cost |
|----------|----------------|-------|------|
| **Ollama** (default) | Mistral 7B | Pre-installed locally | Free |
| **OpenAI** | GPT-4o-mini | Set `OPENAI_API_KEY` | Per-token |
| **Anthropic** | Claude Sonnet 4.6 | Set `ANTHROPIC_API_KEY` | Per-token |

Configure via the API: `PATCH /settings/me` with your preferred provider and API key (encrypted at rest with Fernet).

## The Knowledge Pipeline

YouTube Model Feeder is designed to work with other ClawHub skills:

```
YouTube Video
  → youtube-model-feeder (extract transcript + snapshots + OCR + summary)
    → Obsidian vault (structured markdown + images)
      → obsidian-semantic-search (index with embeddings, search by meaning)
        → Your AI assistant (full context from every video you've ever watched)
```

Every video becomes permanent, searchable knowledge. Not buried in a playlist — indexed and queryable.

## Architecture

```
youtube-model-feeder/
├── backend/           # FastAPI + Celery (Python 3.12)
│   ├── app/
│   │   ├── services/  # Core extraction pipeline (6372 LOC)
│   │   │   ├── youtube.py          # yt-dlp wrapper
│   │   │   ├── transcript.py       # Whisper + YouTube captions
│   │   │   ├── snapshot.py         # FFmpeg frame extraction
│   │   │   ├── slide_detection.py  # SSIM + OCR + alignment (643 LOC)
│   │   │   ├── llm.py             # Summarization engine (1229 LOC)
│   │   │   └── llm_providers.py   # Ollama/OpenAI/Anthropic abstraction
│   │   ├── routes/    # REST API endpoints
│   │   └── tasks.py   # Celery background jobs
├── frontend/          # Next.js 14 + React 18 + Tailwind + Zustand
├── docker-compose.yml # 5 services
└── migrations/        # Alembic database migrations
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| VirusTotal "suspicious" warning on install | False positive — skill describes video extraction patterns. Use `clawhub install youtube-model-feeder --force` |
| Docker services won't start | Ensure Docker Desktop is running. Check `docker-compose logs api` for errors |
| Transcription is slow | First run pulls the Whisper model (~1.5 GB). Subsequent runs are fast. Try YouTube captions first (faster, no model needed) |
| No slides detected | SSIM threshold may need tuning for your video type. Presentation-style videos work best |
| LLM summary is empty | Check LLM provider config. Default is Ollama — ensure Ollama is running with a model pulled |
| FFmpeg not found | `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux) |

## Links

- **Source:** https://github.com/celstnblacc/youtube-model-feeder
- **Obsidian Semantic Search:** https://clawhub.ai/skills/obsidian-semantic-search
- **License:** MIT-0 (this skill) / Apache 2.0 (source)

---

*Built by [celstnblacc](https://github.com/celstnblacc) — food for your model. 226 tests, 6 extraction stages, 3 LLM providers, Obsidian-ready output.*
