# Voice Cloning — Advanced Guide

Clone any voice by providing a reference audio clip. The server extracts the speaker's
characteristics and generates new speech in that voice.

## Setup

```bash
tts-router pull qwen3-tts-clone   # clone-capable model
tts-router serve                   # starts on port 8091
```

## Method 1: Clone from a Direct Audio URL

If you have a direct link to an audio file (`.mp3`, `.wav`, `.m4a`, etc.):

```bash
# Register the reference audio by URL
curl -X POST http://localhost:8091/v1/audio/references/from-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/speaker.mp3", "ref_id": "my-speaker"}' \
  | jq .

# Clone the voice
curl -X POST http://localhost:8091/v1/audio/clone \
  -H "Content-Type: application/json" \
  -d '{"input": "Text to speak in this voice", "ref_id": "my-speaker"}' \
  --output cloned.wav
```

## Method 2: Clone from YouTube / Bilibili / Any Streaming Site

tts-router bundles `yt-dlp`, so it can extract audio from thousands of sites.
Just pass the video URL — the server downloads and processes it automatically.

```bash
# YouTube
curl -X POST http://localhost:8091/v1/audio/references/from-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=VIDEO_ID", "ref_id": "yt-speaker"}' \
  | jq .

# Bilibili
curl -X POST http://localhost:8091/v1/audio/references/from-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.bilibili.com/video/BVXXXXXXX", "ref_id": "bili-speaker"}' \
  | jq .

# Then generate speech
curl -X POST http://localhost:8091/v1/audio/clone \
  -H "Content-Type: application/json" \
  -d '{"input": "这段话会用视频里的声音来朗读", "ref_id": "bili-speaker"}' \
  --output cloned.wav
```

## Method 3: Upload a Local Audio File

```bash
curl -X POST http://localhost:8091/v1/audio/references/upload \
  -F "file=@/path/to/speaker.wav" \
  -F "ref_id=local-speaker" \
  | jq .

curl -X POST http://localhost:8091/v1/audio/clone \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello in your cloned voice", "ref_id": "local-speaker"}' \
  --output cloned.wav
```

## Method 4: CLI one-liner with `tts-router say`

```bash
tts-router say "Text to speak" --ref-audio speaker.wav -o output.wav

# With ref text (improves clone quality if you know what was said in the ref clip)
tts-router say "Text to speak" \
  --ref-audio speaker.wav \
  --ref-text "What the speaker said in the clip" \
  -o output.wav
```

## Tips for Best Results

- **Clip length**: 5–15 seconds of clear speech works best. Too short = poor capture, too long = slow.
- **Clean audio**: Avoid background music or noise in the reference clip.
- **Language**: The reference clip and target text don't need to be the same language — cross-lingual cloning works.
- **ref_text**: Providing a transcript of the reference audio improves accuracy significantly.
