---
name: "video-to-screenplay"
description: "Turn video/audio transcripts into original screenplays. Faster-whisper → LLM story DNA → screenplay (.md + .fountain). Supports 6 LLM providers and CPU/GPU."
---

# video-to-screenplay

Turn video/audio/transcript files into original screenplays via a two-stage LLM pipeline.

## When to use

- User wants to generate a screenplay, script, or story from a video/audio file
- User has a podcast, interview, or narration transcript and wants to develop it into a story
- User wants to extract story DNA (themes, characters, conflicts) from spoken content
- User needs Fountain-format output for import into screenwriting software

## When NOT to use

- User just wants a transcript → use `transcribe_to_srt.py`
- User wants to summarize a video → use `web_fetch` + LLM
- User wants to generate video from script → opposite direction

## Pipeline

1. **Transcribe** (optional): audio/video → SRT via faster-whisper
2. **Extract**: transcript → story DNA (JSON) via LLM
3. **Generate**: story DNA → original screenplay (.md + .fountain)

## Requirements

- faster-whisper (`pip install faster-whisper`)
- One LLM API key in `openclaw.json` (deepseek, kimi, zhipu, longcat, google, or agnes)

## Usage

```bash
# From existing SRT
python scripts/video_to_screenplay.py --srt input.srt --out-dir ./output

# From audio/video (auto-transcribe first)
python scripts/video_to_screenplay.py --audio input.mp3 --out-dir ./output

# Specify genre and length
python scripts/video_to_screenplay.py --srt input.srt --out-dir ./output --target-minutes 15 --genre "科幻"

# Use GPU for transcription
python scripts/video_to_screenplay.py --audio input.mp3 --out-dir ./output --device cuda --compute-type float16

# Use a different LLM provider
python scripts/video_to_screenplay.py --srt input.srt --out-dir ./output --provider kimi --model kimi-k3

# Extract story DNA only (no screenplay)
python scripts/video_to_screenplay.py --srt input.srt --out-dir ./output --extract-only
```

## Output files

- `transcript.txt` — plain text transcript
- `story_dna.json` — extracted story elements (themes, characters, conflicts, motifs)
- `screenplay.md` — human-readable screenplay
- `screenplay.fountain` — Fountain format for screenwriting software import

## Provider support

| Provider | Default Model | Notes |
|---|---|---|
| deepseek | deepseek-v4-flash | Default, fast |
| kimi | kimi-k3 | temperature auto-set to 1.0 |
| zhipu | glm-5.2 | 1M context |
| longcat | LongCat-2.0 | Reasoning model |
| google | gemini-2.0-flash | Multimodal |
| agnes | agnes-2.0-flash | Free tier available |
