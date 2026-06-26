---
name: video-metadata-analyzer
description: "Video content analysis pipeline — extract frames, transcribe audio, run LLM visual+audio analysis, synthesize structured Bilibili publish metadata (title, intro, tags, category, cover suggestion). Use when user says '生成投稿元数据', '视频元数据分析', or explicitly requests this skill. ⚠️ API modes send video frames and audio to external LLM providers — see Privacy section."
privacy_notice: "API modes (vision-llm, audio-llm, cloud, api) transmit extracted video frames, audio, transcripts, and derived metadata to user-configured external endpoints. Videos may contain faces, voices, on-screen text, documents, or other sensitive data. Users should verify endpoint trust and data retention policies before processing. Use agent-direct or local modes for confidential media."
version: 1.2.0
author: CyberKurry
license: MIT
homepage: https://github.com/CyberKurry/video-metadata-analyzer
compatibility: "Requires ffmpeg, ffprobe, Python 3.8+. Optional: Pillow (frame compression), openai-whisper (local mode). External LLM API (OpenAI-compatible chat completions) for full analysis."
platforms: [macos, linux]
metadata:
  openclaw:
    requires:
      bins: ["ffmpeg", "python3"]
    primaryEnv: VIDEO_ANALYZER_LLM_KEY
  hermes:
    tags: [video, analysis, bilibili, transcription, vision-llm, publishing]
    category: media
---

# Video Analyzer

Three-stage video analysis pipeline: parallel visual + audio observation, then metadata synthesis for Bilibili publishing.

## When to Use

- User says "生成投稿元数据", "视频元数据分析", "analyze video metadata"
- User explicitly requests this skill for structured content analysis from a video file
- User wants to prepare a video for Bilibili publishing (title, intro, tags, category, cover)
- Upstream of `bilibili-publish-playwright`: this skill generates the metadata that feeds into Bilibili publishing

> ⚠️ **Privacy Notice:** API modes (`audio-llm`, `cloud`, `vision-llm`, `api`) transmit video frames, audio, transcripts, and derived metadata to user-configured external LLM endpoints. Videos often contain faces, voices, on-screen text, or other sensitive data. Before using API modes, verify the endpoint trust, provider data retention policy, and your approval to process the media. Use `agent-direct` or `local` modes for confidential or regulated content.

## Architecture

```
Input Video ──────────────────────────────────────────────────────
    │                                                            │
    ├── Stage 1a: visual.py ──→ observations_visual.json          │
    │      (ffmpeg extract frames → encode → vision LLM observe)  │ PARALLEL
    │                                                            │
    ├── Stage 1b: transcribe.py ──→ observations_audio.json       │
    │      (ffmpeg extract audio → transcribe + structure)         │
    │                                                            │
    └── Stage 2: analyze.py ──→ metadata.json ←───────────────────┘
           (merge V+A observations → publishable metadata via LLM)
```

`run.sh` orchestrates: launches visual.py and transcribe.py as background processes (`&`), `wait` for both, then optionally runs analyze.py.

### Output Directory

```
$OUTPUT/
├── observations_visual.json    # JSON array: one object per frame
├── observations_audio.json     # JSON object: transcript + structured info
├── metadata.json               # (optional) Synthesized Bilibili metadata
└── frames/                     # (only with --keep-frames, auto-cleaned otherwise)
```

## Procedure

### 1. Full pipeline (recommended — all external LLM API)

```bash
bash scripts/run.sh \
  --video VIDEO_PATH --output /tmp/va-out \
  --transcribe audio-llm \
  --audio-llm-key KEY --audio-llm-base URL --audio-llm-model MODEL \
  --vision-llm-key KEY --vision-llm-base URL --vision-llm-model MODEL \
  --max-frames 15 \
  --synthesize-method api \
  --analyze-llm-key KEY --analyze-llm-base URL --analyze-llm-model MODEL
```

### 2. Agent-direct mode (no external API — agent reads frames/audio directly)

```bash
bash scripts/run.sh \
  --video VIDEO_PATH --output /tmp/va-out --keep-frames
```

Agent then reads `observations_visual.json` (placeholder frames), `observations_audio.json` (audio file path), and optionally the frame images + audio file directly to generate metadata.

### 3. Mixed / observe-only

Omit `--synthesize-method` to observe only, then run `analyze.py` separately later. Each stage (visual, audio, synthesize) can use different keys and models.

### Key Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `--video PATH` | — | **Required.** Input video file |
| `--output DIR` | — | **Required.** Output directory |
| `--transcribe MODE` | `agent-direct` | `local` / `cloud` / `agent-direct` / `audio-llm` |
| `--max-frames N` | `15` | Max frames per 4-min segment |
| `--keep-frames` | `false` | Keep extracted frame images |
| `--synthesize-method METHOD` | — | `api` / `agent` / `manual`. Omit = observe only |

All `*-key`, `*-base`, `*-model` parameters follow the pattern: `--vision-llm-key`, `--audio-llm-key`, `--analyze-llm-key` etc. See [references/REFERENCE.md](references/REFERENCE.md) for the complete parameter table.

## Scripts

| File | Role |
|------|------|
| `scripts/common.py` | Shared utilities: HTTP retry with backoff, media duration via ffprobe, JSON parse from LLM output |
| `scripts/visual.py` | Frame extraction (auto-segment, auto-compress >200KB) + vision LLM observation. Long videos: segments processed in parallel (max 4 concurrent) |
| `scripts/transcribe.py` | Audio extraction + transcription (4 modes). Auto-chunks large audio with 2s overlap for dedup |
| `scripts/analyze.py` | Observations → publish metadata (3 methods: api/agent/manual). Heuristic fallback on API failure |
| `scripts/run.sh` | Orchestrator: parallel visual+audio, then optional synthesis |

## Output Summary

**`observations_visual.json`** — JSON array, one object per frame with `frame`, `objects`, `desc`, `texts`, `actions`, `style`, `cover_candidate`, `segment`, `segment_start`.

**`observations_audio.json`** — `transcript`, `speakers`, `key_points`, `tone`. Agent-direct mode includes `audio_file` path.

**`metadata.json`** — `title` (≤80 chars), `intro` (≤2000 chars), `tags` (≤10), `category` (B站 type2 平铺分区，30 个一级分区), `cover_suggestion` (primary + reason + secondary), `declaration` (6 选 1), `copyright_claim`, `watermark`, `author_marks`.

## Pitfalls

- **API keys in chat**: Some platforms truncate keys with `…`. Always pass keys via command-line arguments, not through messages.
- **Model capability**: Vision requires `image_url` support. Audio-LLM requires `input_audio` support. Check your provider.
- **Game recordings**: Frames are large (~300-380KB vs ~30-80KB for phone). Auto-compression handles this, but plan rate limits for long videos.
- **Long videos = parallel API calls**: 30-min video = 8 segments × 15 frames = 8 vision API calls (capped at 4 concurrent). Consider rate limits.
- **Missing credentials auto-degrade**: Omitting LLM keys → preprocess-only or agent-direct mode. Scripts never crash on missing keys.
- **`--interval` deprecated**: Ignored. Interval auto-calculated per segment based on `--max-frames`.
- **Timeout protection**: `run.sh` auto-wraps with `timeout $VA_TIMEOUT` (default 3600s = 1h). Override via `VA_TIMEOUT` env var.

## Error Handling

Three-layer defense:
1. **HTTP retry** — 3 retries with exponential backoff on 5xx / connection errors
2. **JSON parse retry** — 3 attempts with error feedback sent back to LLM
3. **Graceful degradation** — placeholder observations on visual failure, raw text on audio failure, heuristic fallback on synthesis failure

## Verification

1. Check exit code: `run.sh` returns 0 on success
2. Verify `observations_visual.json` has entries for expected frame count
3. Verify `observations_audio.json` has `transcript` field (non-empty for speech videos)
4. If `--synthesize-method` used, verify `metadata.json` has all required fields (`title`, `intro`, `tags`, `category`, `cover_suggestion`)

For complete parameter reference, output schemas, standalone usage per script, and detailed error handling, see [references/REFERENCE.md](references/REFERENCE.md).
