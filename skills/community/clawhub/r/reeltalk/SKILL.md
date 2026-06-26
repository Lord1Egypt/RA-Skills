---
name: reeltalk
description: >
  Helper for processing shared video links. Takes a URL, downloads the
  audio track, creates a text transcript, and produces a summary.
  Supports all major platforms. Good for understanding video content
  without watching it.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "os": ["darwin", "linux"],
        "requires": { "bins": ["yt-dlp", "whisper", "tesseract", "ffmpeg"] },
        "install":
          [
            {
              "id": "brew-yt-dlp",
              "kind": "brew",
              "formula": "yt-dlp",
              "bins": ["yt-dlp"],
              "label": "Install yt-dlp (brew)",
            },
            {
              "id": "brew-whisper",
              "kind": "brew",
              "formula": "whisper",
              "bins": ["whisper"],
              "label": "Install Whisper (brew)",
            },
            {
              "id": "brew-tesseract",
              "kind": "brew",
              "formula": "tesseract",
              "bins": ["tesseract"],
              "label": "Install Tesseract OCR (brew)",
            },
            {
              "id": "brew-tesseract-lang-hin",
              "kind": "brew",
              "formula": "tesseract-lang",
              "bins": [],
              "label": "Install Hindi language pack for Tesseract (brew)",
            },
          ],
      },
  }
---

# ReelTalk

Process a video link: download audio, transcribe, and summarize. Falls back to image text extraction when no speech is present.

⚠️ **Videos longer than 5 minutes** will take roughly 1 min of processing per minute of video on CPU. Warn the user before starting.

## Steps

### 0. Fresh start
```bash
rm -rf /tmp/reeltalk_*
mkdir -p /tmp/reeltalk_work
```

### 1. Validate URL
Store the user-provided URL in a variable and reject anything that looks like a shell injection. Only allow `http://`, `https://`, or `www.` prefixes. Reject inputs containing shell metacharacters (`;`, `|`, `&`, `` ` ``, `$`, `(`, `)`).
```bash
URL="<url>"
# Reject shell metacharacters
if printf '%s' "$URL" | grep -qE '[;|&`$()]'; then
  echo "Invalid URL: contains disallowed characters"
  exit 1
fi
```

### 2. Get metadata
```bash
yt-dlp --print title --print description --print uploader "$URL" \
  2>/dev/null > /tmp/reeltalk_work/metadata.txt
```

### 3. Audio
```bash
yt-dlp -f "bestaudio" -o "/tmp/reeltalk_work/audio.%(ext)s" "$URL"
```

### 4. Check length & split
```bash
ffprobe -v error -show_entries format=duration -of \
  default=noprint_wrappers=1:nokey=1 /tmp/reeltalk_work/audio.m4a
```
If duration > 300, warn user, then split:
```bash
ffmpeg -i /tmp/reeltalk_work/audio.m4a -f segment -segment_time 300 \
  -acodec pcm_s16le -ac 1 -ar 16000 /tmp/reeltalk_work/chunk_%03d.wav
```

### 4. Transcribe
Use the `base` Whisper model (memory-efficient on 8GB machines).
```bash
for chunk in /tmp/reeltalk_work/chunk_*.wav; do
  base=$(basename "$chunk" .wav)
  whisper "$chunk" --model base --language en --task transcribe \
    2>/dev/null > "/tmp/reeltalk_work/transcript_${base}.txt"
done
```
For short videos, transcribe directly:
```bash
whisper /tmp/reeltalk_work/audio.m4a --model base --language en --task transcribe \
  2>/dev/null > /tmp/reeltalk_work/full_transcript.txt
```

### 5. Assemble
```bash
> /tmp/reeltalk_work/full_transcript.txt
for f in /tmp/reeltalk_work/transcript_chunk_*.txt; do
  echo "=== $(basename "$f" .txt) ===" >> /tmp/reeltalk_work/full_transcript.txt
  cat "$f" >> /tmp/reeltalk_work/full_transcript.txt
  echo "" >> /tmp/reeltalk_work/full_transcript.txt
done
```

### 7. OCR fallback
If transcript is empty or under 20 words:
```bash
yt-dlp -f "bv*+ba/b" -o "/tmp/reeltalk_work/video.mp4" "$URL"
mkdir -p /tmp/reeltalk_work/frames
ffmpeg -i /tmp/reeltalk_work/video.mp4 -vf "fps=1" -vsync vfr \
  -q:v 2 /tmp/reeltalk_work/frames/frame_%04d.jpg
for f in /tmp/reeltalk_work/frames/frame_*.jpg; do
  tesseract "$f" stdout --psm 6 2>/dev/null
done > /tmp/reeltalk_work/ocr_output.txt
```

### 7. Summarize
Combine metadata + transcript (or OCR) into a plain English summary.

## Platform notes

- **X/Twitter**: use fxtwitter API (yt-dlp fails). Extract the user and status ID from the original URL, then call the API with a constructed URL (do not pass the raw user URL to curl):
  ```bash
  curl -sL "https://api.fxtwitter.com/<user>/status/<id>" | jq -r '.media.videos[0].url'
  ```
  Validate the returned video URL (must start with `https://`) before downloading with curl.
- **TikTok**: yt-dlp handles fine.
- **Instagram**: yt-dlp handles fine.

## Requirements
- `yt-dlp` (brew), `whisper` (brew), `tesseract` (brew), `ffmpeg` (brew)
- Whisper cache: `~/.cache/whisper/` (base model ~142MB)
