---
name: viral-reels-creator
description: >
  Full-featured viral Reels creator and editor powered by ffmpeg. Use this skill whenever
  the user wants to create, edit, find, or produce viral Instagram Reels, TikTok videos,
  YouTube Shorts, or any vertical short-form video content. Triggers include: "create a reel",
  "make a viral video", "make a short video", "Instagram reel", "TikTok video", "YouTube Shorts",
  "vertical video", "reels editor", "video editor", "add subtitles to video", "auto captions",
  "merge clips", "slideshow video", "add music to video", "beat sync video", "sync cuts to music",
  "video transitions", "caption video", "color grade video", "slow motion", "speed ramp",
  "text animation on video", "video effects", "video overlay", "ken burns effect", "video filter",
  "find best moments in video", "find highlights", "scene detection", "export for TikTok",
  "export for multiple platforms", "batch export video", "viral hook", "viral opening",
  "make my video go viral", or any request involving ffmpeg-based video editing for social media.
  Also trigger when the user uploads video/image/audio files and asks to combine, trim, stylize,
  color grade, beat-sync, or export them as a reel. Supports all formats: mp4, mov, avi, mkv,
  webm, jpg, png, gif, mp3, wav, aac, and more.
---

# Viral Reels Creator — Full Video Production Suite

A comprehensive ffmpeg-based skill for creating viral Instagram Reels, TikTok videos, and YouTube Shorts — including finding the best moments in raw footage, beat-synced editing, multi-platform export, and viral content strategy.

---

## Quick Start — Read Before Doing Anything

1. **Install dependencies** if not available:
   ```bash
   apt-get update && apt-get install -y ffmpeg fonts-noto fonts-noto-color-emoji fontconfig
   # For scene detection + beat sync:
   pip install --break-system-packages opencv-python numpy librosa soundfile
   ```
2. **Check uploaded files**: Look in `/mnt/user-data/uploads/` for user assets.
3. **Copy assets** to `/home/claude/` before processing.
4. **Output** all final videos to `/mnt/user-data/outputs/` and present to user.

---

## Platform Specs (Primary: Instagram Reels)

| Property         | Instagram / TikTok / YT Shorts       |
|------------------|--------------------------------------|
| Resolution       | 1080×1920 (9:16 portrait)           |
| FPS              | 30 fps (60fps for YouTube Shorts)    |
| Max Duration     | 90s (IG/FB) · 60s (TikTok/YT/Snap)  |
| Codec            | H.264 (libx264)                      |
| Audio Codec      | AAC, 44100 Hz, stereo               |
| Pixel Format     | yuv420p                              |
| Container        | .mp4                                 |

**Base output flags (always use):**
```
-c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 -c:a aac -ar 44100 -ac 2 -movflags +faststart
```

For full platform-specific specs and export commands → **`references/platform-specs.md`**

---

## Workflow Decision Tree

```
User Request
├── "Find best moments / highlights"?
│   └── Run scripts/scene-detect.py → get timestamps → trim clips
├── "Make it viral" / "viral hook"?
│   └── Load references/viral-hooks.md → apply hook formula
├── Single video input?
│   ├── Trim/Cut           → Section: TRIMMING
│   ├── Add captions       → load references/caption-templates.md
│   ├── Add music          → Section: AUDIO MIXING
│   ├── Sync cuts to beats → load references/beat-sync.md + scripts/beat-detect.py
│   ├── Color grade        → load references/color-grading.md
│   ├── Speed change       → Section: SPEED RAMP
│   ├── Add effects/anim   → load references/animations.md
│   └── Resize only        → Section: RESIZING
├── Multiple video inputs?
│   └── Merge with transitions → load references/transitions.md
├── Images input (slideshow)?
│   └── Ken Burns / Slideshow → Section: SLIDESHOW
├── Export for multiple platforms?
│   └── Run scripts/batch-export.sh → exports all platforms at once
├── Full reel from scratch?
│   └── Combine all: scene detect → hook → content → beat sync → captions + music
└── "Make it look good" / generic?
    └── Auto-resize + color grade (Golden Hour or Clarendon) + caption template + fade transitions
```

**IMPORTANT**: For captions, animations, color grading, transitions, viral strategy, beat sync, and platform specs — **always read the corresponding reference file** before generating ffmpeg commands.

---

## FINDING THE BEST MOMENTS (Scene Detection)

When the user has raw footage and wants the best clips extracted:

```bash
# Find top 10 most visually interesting moments
python scripts/scene-detect.py raw_footage.mp4 --top 10 --thumbnail

# Extract a specific number of clips for a 30s reel (5s each = 6 clips)
python scripts/scene-detect.py raw_footage.mp4 --top 6 --clip-duration 5 --thumbnail

# For fast-paced content with many scene changes
python scripts/scene-detect.py video.mp4 --threshold 0.2 --top 15

# Output as JSON for further processing
python scripts/scene-detect.py video.mp4 --json > moments.json
```

Then trim each moment using the generated ffmpeg commands from the script output.

---

## VIRAL STRATEGY — Quick Reference

Load **`references/viral-hooks.md`** for the full strategy. Core principles:

1. **Hook in 3 seconds** — pattern interrupt, bold claim, or curiosity gap in text overlay
2. **Retention triggers** at 7s, 12s, 20s, 25s to fight viewer drop-off
3. **Beat-sync all cuts** — biggest single factor in watch time and shares
4. **End with a loop** — last frame should nearly match first frame so viewers rewatch
5. **On-screen text always** — 85% of viewers watch without sound

**The viral reel formula:**
```
[0–3s]  HOOK     → Bold text claim or pattern interrupt
[3–7s]  SETUP    → Context, "here's what you'll see"
[7–20s] CONTENT  → Core value, fast cuts, visual variety
[20–25s] PAYOFF  → Reveal, transformation, punchline
[25–30s] CTA     → "Save this", "Comment X for part 2"
```

---

## BEAT-SYNCED EDITING — Quick Reference

Load **`references/beat-sync.md`** for the full workflow.

```bash
# Step 1: Detect beats
python scripts/beat-detect.py music.mp3
# → outputs timestamps like: 0.469, 0.938, 1.407, 1.876...

# Step 2: Use beat timestamps as cut points
# (see beat-sync.md for full ffmpeg multi-clip assembly)

# Step 3: Add zoom pulse on every beat (120 BPM = 2Hz)
ffmpeg -i video.mp4 -filter_complex "
  zoompan=z='1+0.05*abs(sin(PI*t*2))':
    x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30
" OUTPUT_FLAGS zoom_pulse.mp4
```

---

## Core Operations

### RESIZING — Fit Any Video to 9:16

```bash
# Scale + crop (fill frame — preferred for Reels)
ffmpeg -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" OUTPUT_FLAGS output.mp4

# Blurred background fill (cinematic — best for landscape source)
ffmpeg -i input.mp4 -filter_complex "
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:5[bg];
[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];
[bg][fg]overlay=(W-w)/2:(H-h)/2
" OUTPUT_FLAGS output.mp4
```

### TRIMMING — Cut Clips

```bash
# Fast trim (copy — no re-encode)
ffmpeg -ss 00:00:05 -i input.mp4 -t 00:00:30 -c copy trimmed.mp4

# Precise trim (re-encode for frame accuracy)
ffmpeg -i input.mp4 -ss 00:00:05 -to 00:00:35 OUTPUT_FLAGS trimmed.mp4
```

### SPEED RAMP — Slow Motion & Fast Forward

```bash
# 0.5x slow motion
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" -map "[v]" -map "[a]" OUTPUT_FLAGS slow.mp4

# 2x speed
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" OUTPUT_FLAGS fast.mp4

# Speed ramp: normal → slow → normal
ffmpeg -i input.mp4 -filter_complex "
[0:v]trim=0:3,setpts=PTS-STARTPTS[v1];
[0:v]trim=3:6,setpts=2*(PTS-STARTPTS)[v2];
[0:v]trim=6:10,setpts=PTS-STARTPTS[v3];
[v1][v2][v3]concat=n=3:v=1:a=0[v]
" -map "[v]" OUTPUT_FLAGS ramp.mp4
```

### AUDIO MIXING — Add Background Music

```bash
# Mix original audio + music (music at 30% volume)
ffmpeg -i video.mp4 -i music.mp3 -filter_complex "
[0:a]volume=1.0[voice];
[1:a]volume=0.3[music];
[voice][music]amix=inputs=2:duration=shortest
" -map 0:v OUTPUT_FLAGS output.mp4

# Fade music in/out
ffmpeg -i video.mp4 -i music.mp3 -filter_complex "
[1:a]afade=t=in:st=0:d=3,afade=t=out:st=27:d=3,volume=0.3[music];
[0:a]volume=1.0[voice];
[voice][music]amix=inputs=2:duration=shortest
" -map 0:v OUTPUT_FLAGS output.mp4
```

### SLIDESHOW — Images to Video

```bash
# Ken Burns (zoom + pan)
ffmpeg -loop 1 -i image.jpg -vf "
scale=2160:3840,
zoompan=z='min(zoom+0.001,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1080x1920:fps=30
" -t 5 OUTPUT_FLAGS kenburns.mp4
```

---

## Advanced Features — Reference Files

Always read the reference file before generating ffmpeg commands for these features.

| Feature                  | Reference File                         | What's Inside                                      |
|--------------------------|----------------------------------------|----------------------------------------------------|
| Viral strategy & hooks   | `references/viral-hooks.md`           | Hook formulas, formats, retention tactics, CTAs     |
| Beat-synced editing      | `references/beat-sync.md`             | Beat assembly, zoom pulse, drop effects             |
| Multi-platform export    | `references/platform-specs.md`        | Specs, safe zones, aspect ratio variants            |
| Caption Templates        | `references/caption-templates.md`     | 10 Instagram-style caption designs                  |
| Animations (50+)         | `references/animations.md`            | 50 text/video animations: bounce, typewriter, etc.  |
| Color Grading            | `references/color-grading.md`         | 20 LUT-free color grades and Instagram filters      |
| Transitions              | `references/transitions.md`           | 12+ transitions: fade, wipe, zoom, glitch, etc.     |

---

## Scripts

| Script                    | Purpose                                                  |
|---------------------------|----------------------------------------------------------|
| `scripts/scene-detect.py` | Find best/most viral-worthy moments in raw footage       |
| `scripts/beat-detect.py`  | Detect beat timestamps for sync-cut editing              |
| `scripts/batch-export.sh` | Export one reel to Instagram, TikTok, YouTube, etc.      |

---

## Combining Multiple Effects

Stack effects in a single `-filter_complex`. Order matters:

```
1. Scale/crop to 1080x1920
2. Apply color grading
3. Apply speed changes
4. Apply animations/effects
5. Overlay captions/text
6. Add transitions (for multi-clip)
```

**Example: Full viral reel pipeline**
```bash
ffmpeg -i clip1.mp4 -i music.mp3 -filter_complex "
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
eq=brightness=0.06:saturation=1.4:contrast=1.05,
vignette=PI/5,
drawtext=text='Wait for it...':fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=72:fontcolor=white:borderw=4:bordercolor=black:
  x=(w-tw)/2:y=(h-th)/2:enable='between(t,0,3)',
drawtext=text='Your Caption Here':fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=56:fontcolor=white:borderw=3:bordercolor=black:
  x=(w-tw)/2:y=h-th-250:enable='between(t,3,28)',
drawtext=text='Save this!':fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:
  fontsize=40:fontcolor=yellow:borderw=3:bordercolor=black:
  x=(w-tw)/2:y=h-th-120:enable='between(t,25,30)',
fade=t=in:st=0:d=1,fade=t=out:st=28:d=2[v];
[1:a]afade=t=in:st=0:d=2,afade=t=out:st=27:d=3,volume=0.4[a]
" -map "[v]" -map "[a]" -t 30 \
-c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 \
-c:a aac -ar 44100 -ac 2 -movflags +faststart \
/mnt/user-data/outputs/reel_final.mp4
```

---

## Multi-Platform Export

After finishing the reel, export for all platforms at once:

```bash
bash scripts/batch-export.sh /mnt/user-data/outputs/reel_final.mp4 my_reel all
# Creates: my_reel_instagram.mp4, my_reel_tiktok.mp4, my_reel_youtube_shorts.mp4,
#          my_reel_facebook.mp4, my_reel_snapchat.mp4, my_reel_pinterest.mp4
```

Or export to specific platforms:
```bash
bash scripts/batch-export.sh reel.mp4 cooking_video instagram,tiktok,youtube
```

---

## Watermark / Logo Overlay

```bash
# Animated logo (fade in, semi-transparent)
ffmpeg -i video.mp4 -i logo.png -filter_complex "
[1:v]scale=120:-1,format=rgba,colorchannelmixer=aa=0.7[logo];
[0:v][logo]overlay=W-w-30:H-h-30
" OUTPUT_FLAGS output.mp4
```

---

## Auto-Captions from Audio (Whisper)

```bash
pip install --break-system-packages openai-whisper pysrt
```

```python
import whisper

model = whisper.load_model("base")
result = model.transcribe("audio.mp3", word_timestamps=True)

with open("captions.srt", "w") as f:
    for i, seg in enumerate(result["segments"], 1):
        start = seg["start"]
        end = seg["end"]
        text = seg["text"].strip()
        f.write(f"{i}\n")
        f.write(f"{int(start//3600):02}:{int(start%3600//60):02}:{start%60:06.3f} --> ")
        f.write(f"{int(end//3600):02}:{int(end%3600//60):02}:{end%60:06.3f}\n")
        f.write(f"{text}\n\n")
```

Then burn captions (see `references/caption-templates.md` for styled options):
```bash
ffmpeg -i video.mp4 -vf "subtitles=captions.srt:force_style='FontSize=22,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,Alignment=2'" OUTPUT_FLAGS output.mp4
```

---

## Error Handling & Tips

- **Check for audio:** `ffprobe -i input.mp4 -show_streams -select_streams a`
- **Silent video?** Add `-an` or generate silent audio: `-f lavfi -i anullsrc`
- **Fonts missing?** `apt-get install -y fonts-noto fonts-liberation`
- **Preview fast:** Add `-t 5 -preset ultrafast` to render only 5 seconds
- **Emoji in text?** Use `fontfile=/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf`
- **Always use** `-movflags +faststart` for web/mobile playback
- **Duration limits:** 90s Instagram/Facebook · 60s TikTok/YouTube Shorts/Snapchat

---

## Output Checklist

Before delivering the final video:
- [ ] Resolution is 1080×1920
- [ ] Duration within platform limit (90s Instagram, 60s TikTok/Shorts)
- [ ] FPS is 30 (or 60 for YouTube Shorts)
- [ ] Has audio track (even if silent)
- [ ] Uses H.264 + AAC codecs
- [ ] Hook text visible in first 3 seconds
- [ ] CTA text visible in last 5 seconds
- [ ] File is in `/mnt/user-data/outputs/`
- [ ] Platform variants exported via `batch-export.sh` if needed
