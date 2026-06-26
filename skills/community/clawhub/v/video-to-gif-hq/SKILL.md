---
name: video-to-gif
description: Convert video files or clips into animated GIFs/WebP using ffmpeg, with resizing, fps control, trimming, palette generation, and file-size optimization. Use when the user asks to turn video into GIF/动图, make a GIF from mp4/mov/webm/mkv, extract a video segment as an animation, compress an animated GIF, or create a shareable short looping animation.
---

# Video To GIF

## Quick workflow

1. Identify the input video path or ask the user to upload/provide it if missing.
2. Choose sensible defaults unless the user specifies otherwise:
   - `fps=12`
   - keep the original video resolution by default; only resize when the user asks for compression/smaller file size or a target dimension
   - trim duration to ≤10 seconds if the user asks for a generic “动图” but the video is long
   - use palette generation for GIF quality
3. Run `scripts/video_to_gif.py` from this skill directory.
4. Verify the output exists and report path/size. Attach with `MEDIA:<path>` if delivering in chat.

## Script usage

```bash
python3 /root/.openclaw/workspace/skills/video-to-gif/scripts/video_to_gif.py \
  input.mp4 output.gif \
  --start 00:00:02 --duration 4 \
  --fps 12 --width 480
```

Useful options:

- `--start`: clip start time, e.g. `3.5` or `00:00:03.500`
- `--duration`: clip length in seconds or timestamp format
- `--end`: alternative to duration
- `--fps`: lower values reduce size; 10–15 is usually good
- `--width`: scale output width while preserving aspect ratio
- `--height`: scale output height while preserving aspect ratio
- `--output-format gif|webp`: WebP is usually much smaller than GIF
- `--loop`: `0` means loop forever
- `--max-colors`: GIF palette colors, default 256; lower reduces size

## Quality and size guidance

- Default to original resolution for clarity.
- For Feishu/chat stickers or size-sensitive sharing, ask/choose a smaller width such as `--width 360 --fps 10`.
- If GIF is too large, reduce in this order: duration, width, fps, colors.
- If the user only needs an animated image and not strict GIF, recommend WebP because it is smaller and smoother.

## Dependencies

The script requires `ffmpeg` and `ffprobe` on PATH. If missing, tell the user the dependency is absent and do not attempt risky system installation without confirmation.
