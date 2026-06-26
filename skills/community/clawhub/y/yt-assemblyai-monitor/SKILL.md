---
name: yt-assemblyai-monitor
description: >
  YouTube channel monitor and video transcription using AssemblyAI cloud API.
  Pure Python + requests only — no ffmpeg, no Whisper, no extra tools needed.
  Monitors YouTube channels for new videos, extracts audio URLs via innertube API,
  submits to AssemblyAI for cloud transcription, and returns text + AI summary.
  Works on Mac, Linux, Windows. Only dependency: requests (usually pre-installed).
  Use when: user asks to monitor YouTube channels, transcribe YouTube videos,
  summarize video content, or set up YouTube content monitoring.
---

# YouTube Channel Monitor (AssemblyAI)

Monitor YouTube channels and auto-transcribe new videos using AssemblyAI cloud API. Zero local dependencies beyond `requests`.

## Prerequisites

1. **AssemblyAI account**: https://www.assemblyai.com/app/signup (free, 100 hours/month)
2. **API Key**: from Dashboard
3. **`requests`** library (usually pre-installed with OpenClaw/Python)

## Setup API Key

Choose one:

```bash
# Option A: environment variable
export ASSEMBLYAI_API_KEY="your-key"

# Option B: config file
echo '{"api_key": "your-key"}' > data/config.json
```

## How It Works

```
Channel page → innertube API → audio direct URL → AssemblyAI cloud → text + summary
```

No local audio download, no Whisper, no ffmpeg. AssemblyAI handles everything server-side.

## Commands

```bash
# Transcribe a single video
python3 scripts/monitor.py now "https://www.youtube.com/watch?v=VIDEO_ID"

# Add a channel to monitor
python3 scripts/monitor.py add "https://www.youtube.com/@ChannelName/videos" "Alias"

# Check all channels for new videos + transcribe
python3 scripts/monitor.py check [count_per_channel]

# List channels
python3 scripts/monitor.py list

# Remove channel
python3 scripts/monitor.py remove "Alias"
```

## Important Notes

- Audio URL extraction uses YouTube's innertube API (pure requests).
- Works on normal residential IPs. Datacenter IPs may get blocked by YouTube.
- If audio URL extraction fails with UNPLAYABLE, the IP may be flagged — this is a YouTube limitation, not a bug.
- Free tier: 100 hours/month of transcription.
- Transcription takes ~70-80% of video duration.
- Results saved to `data/summaries/{video_id}.json`.

## Output Format

Each result includes:
- `text`: full transcription
- `summary`: AI-generated paragraph summary
- `confidence`: transcription confidence score
- `utterances`: timestamped segments with speaker labels

## Files

| Path | Purpose |
|------|---------|
| `data/channels.json` | monitored channels |
| `data/processed.json` | already-transcribed video IDs |
| `data/summaries/*.json` | transcription results |
| `data/config.json` | API key (optional) |
