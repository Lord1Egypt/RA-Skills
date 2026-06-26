---
name: clip-local
description: Clips a YouTube video locally using yt-dlp and ffmpeg. Supports auto-highlight detection, translation, and CapCut-style karaoke subtitle burning. Triggers when the user wants local video clipping, highlight extraction, or subtitle generation. Optional GROQ_API_KEY env var enables Whisper transcription fallback when YouTube has no subtitles.
argument-hint: "[youtube-url-or-id] [start] [end] [output]"
---

# Video Clip (Local)

Requires `yt-dlp`, `ffmpeg`, and `python3`. Check with `command -v`.

## Finding plugin scripts

The ASS karaoke generator is bundled with this plugin. Locate it once at the start (this only searches for the plugin's own bundled file):

```bash
ASS_SCRIPT=$(find ~/.claude/plugins -path '*/clip-local/*/scripts/ass-karaoke.py' 2>/dev/null | head -1)
```

## Auto-highlight mode

When the user does NOT specify start/end times (e.g., "幫我剪這個影片的精華" or "clip the best parts"):

1. Download the full transcript (step 1–2 below)
2. Read the entire transcript and identify 3–5 highlight segments. For each, note:
   - Start and end timestamps
   - A short description of why it's interesting (key insight, funny moment, dramatic turn, etc.)
3. Present the highlights to the user as numbered options and ask which ones to clip
4. Clip only the segments the user picks, then continue with the normal pipeline (translate, subtitle, etc.)

## Pipeline

### 1. Get video info and original language

```bash
yt-dlp --print title --print duration_string --print language \
  --no-playlist --no-warnings --force-ipv4 "<URL>"
```

The third line is the original language code (e.g., `en`, `en-US`, `ja`, `zh-Hant`). Use the base code (before `-`) for subtitle download.

### 2. Download original language subtitles

```bash
yt-dlp --write-auto-sub --sub-lang "<LANG>*" --sub-format vtt --skip-download \
  --no-playlist --no-warnings --force-ipv4 \
  --extractor-args 'youtube:player-client=default,mweb' \
  -o "subs" "<URL>"
```

Replace `<LANG>` with the base language code from step 1 (e.g., `en`, `ja`). The `*` wildcard matches variants like `en-orig`. Do NOT use YouTube's auto-translated subs — they are low quality. All translation is done by you.

### 3. Trim VTT to clip range

When clipping a portion (e.g., 10–130s), filter the VTT to only include cues whose timestamps fall within the range. **Keep the original absolute timestamps — do NOT adjust them.** The `--offset` flag in `ass-karaoke.py` handles the time shift.

When filtering, strip any extra metadata from timestamp lines (e.g., `align:start position:0%`) — keep only `HH:MM:SS.mmm --> HH:MM:SS.mmm`. The ASS parser regex expects clean timestamp lines.

### 4. Translate subtitles

Write and execute a Python script that:
1. Parses the trimmed VTT (regex: `HH:MM:SS.mmm --> HH:MM:SS.mmm` + text lines)
2. Collects all text lines into a list
3. You translate the list (print a Python list of translated strings)
4. Writes a new VTT with identical timestamps and translated text

Example structure:
```python
import re

# Parse original VTT
with open("clip.vtt") as f:
    content = f.read()
cues = re.findall(r'(\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3})\n((?:(?!\d{2}:\d{2}).+\n?)*)', content)

# Translations — fill this list with your translations, one per cue
translations = [
    "translated line 1",
    "translated line 2",
    # ...
]

# Write translated VTT
with open("clip_translated.vtt", "w") as f:
    f.write("WEBVTT\n\n")
    for (timestamp, _), translation in zip(cues, translations):
        f.write(f"{timestamp}\n{translation.strip()}\n\n")
```

Generate this script with the `translations` list filled in, then execute it. This ensures timestamps stay exact and VTT format is correct.

### 5. Generate ASS karaoke subtitles

```bash
python3 "$ASS_SCRIPT" <original.vtt> -o subs.ass -t <translated.vtt> --offset <START_SECONDS>
```

- First arg = **original language** VTT (karaoke timing on top line)
- `-t` = **translated** VTT (shown below karaoke line)
- `--offset` = clip start time (adjusts timestamps relative to clip start)

Handles YouTube rolling caption dedup, CJK per-char splitting, and bilingual layout.

### 6. Resolve stream URLs and clip

Get both video + audio URLs in **one call**:

```bash
URLS=$(yt-dlp --get-url -f 'bv[height<=720]+ba/b[height<=720]' \
  --no-playlist --no-warnings --force-ipv4 \
  --extractor-args 'youtube:player-client=default,mweb' "<URL>")
VIDEO_URL=$(echo "$URLS" | head -1)
AUDIO_URL=$(echo "$URLS" | tail -1)
```

Then clip with ffmpeg:

- With subtitles: `-vf "ass=subs.ass" -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k -movflags +faststart`
- Without subtitles: `-c copy -avoid_negative_ts make_zero`
- Input seeking: `-ss <START>` before each `-i`
- Separate streams: `-map 0:v:0 -map 1:a:0`

### Whisper fallback (no YouTube subs)

If yt-dlp finds no auto-subs and user has `GROQ_API_KEY` set:

1. Download audio: `yt-dlp -f ba -x --audio-format mp3 --postprocessor-args 'ffmpeg:-ac 1 -ar 16000 -b:a 64k'`
2. Transcribe: `POST https://api.groq.com/openai/v1/audio/transcriptions` with `model=whisper-large-v3`, `response_format=verbose_json`
3. Convert segments to VTT

If `GROQ_API_KEY` is not set, inform the user that no subtitles are available and ask how to proceed (clip without subs, or set the key).

## Common issues

- YouTube throttling: export cookies to a file and use `--cookies cookies.txt`
- Missing CJK fonts for ASS: `brew install font-noto-sans-cjk-tc` (macOS)
- Groq 25MB audio limit: split audio for videos >50min
- Stream URLs expire ~6h: re-resolve if clip fails
- Subtitle burning re-encodes video (~1–3 min for 60s clip)
