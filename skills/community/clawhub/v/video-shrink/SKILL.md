---
name: video-shrink
description: Shrink videos to a target file size with a quality-first ladder (stream copy, then same-resolution NVENC/x264 at low CQ, then downscale only as a last resort). Use when a video exceeds an upload or chat attachment limit (Feishu/Lark 28MB, Discord 25MB, Telegram 50MB, email), when asked to "compress video", "make it smaller", "fit under X MB", "压到28M以内", "视频太大发不出去", or when preparing 4K/HDR phone footage for delivery.
---

# Video Shrink

Reduce a video to a hard size limit without throwing away resolution unless it is
the only way to fit. Encodes with NVIDIA NVENC when available and falls back to
libx264.

## Why this order matters

Re-encoding always loses something; only `-c copy` is lossless. So the ladder
tries, in order:

1. Stream copy (remux / strip audio) — truly lossless, instant.
2. Same resolution, CQ 19 (visually lossless; SSIM ~0.986 on 4K phone footage).
3. Same resolution, CQ 22, then CQ 24 — still same pixel count.
4. Short edge 1080, CQ 20 then CQ 24 — first real quality drop.
5. Short edge 720, CQ 24 — last resort.

Each rung computes a `maxrate` ceiling from the size budget and duration, so a
single pass lands close to the target instead of overshooting.

## Usage

```bash
python scripts/video_shrink.py input.mp4 --limit-mb 28 --out output.mp4
```

Common flags:

```bash
# keep the audio track (default: keep; --strip-audio removes it)
python scripts/video_shrink.py in.mp4 --limit-mb 28 --out out.mp4

# drop audio entirely (silent clips, GIF-like loops)
python scripts/video_shrink.py in.mp4 --limit-mb 28 --out out.mp4 --strip-audio

# force H.265 for archives (smaller, worse compatibility)
python scripts/video_shrink.py in.mp4 --limit-mb 28 --out out.mp4 --codec hevc

# prefer 1080 short edge even if 4K would fit (smoother phone playback)
python scripts/video_shrink.py in.mp4 --limit-mb 28 --out out.mp4 --prefer-1080

# machine-readable result for automation
python scripts/video_shrink.py in.mp4 --limit-mb 28 --out out.mp4 --json
```

Batch:

```bash
python scripts/video_shrink.py "clips/*.mp4" --limit-mb 28 --out-dir shrunk/
```

## Output contract

Prints one `[SHRINK]` line per file and a final `[SUMMARY]`:

```
[SHRINK] in.mp4 2160x3840 29.3s 109.7MB -> 24.9MB tier=cq19@orig 2160x3840
[SUMMARY] ok=1 over=0 total_in=109.7MB total_out=24.9MB
```

Exit code is 0 when every file fits, 1 when at least one still exceeds the limit
after the whole ladder.

With `--json`, emits a JSON object per file:

```json
{"input":"in.mp4","output":"out.mp4","limit_mb":28,"input_mb":109.7,
 "output_mb":24.9,"tier":"cq19@orig","width":2160,"height":3840,
 "duration":29.3,"fits":true,"encoder":"h264_nvenc"}
```

## Rules of thumb

1. Feishu/Lark caps video attachments at 28MB, so use `--limit-mb 26` to leave
   headroom; a file at 27.9MB can still be rejected server-side.
2. Deliver H.264 High, not HEVC: HEVC is 35-40% smaller at equal quality but
   breaks on some Feishu/iOS/Android clients. Use `--codec hevc` only for
   archives or platforms that accept it.
3. Never hardcode a resolution. The script reads the real display size
   (including rotation) and keeps aspect ratio, even dimensions.
4. HDR sources (HLG/PQ, 10-bit) should be tonemapped to SDR before shrinking for
   chat delivery, otherwise players show washed-out or blown-out color. The
   script detects HDR and tonemaps with zscale+hable automatically; pass
   `--keep-hdr` to skip it.
5. Keep the pre-shrink master. Shrinking a shrunk file compounds artifacts.
6. For long videos (5+ minutes) at 4K, even CQ 19 will not fit 28MB; the ladder
   will reach 1080p or 720p, which is the correct trade-off.

## Requirements

- `ffmpeg` and `ffprobe` on PATH with `h264_nvenc`/`hevc_nvenc` for GPU speed;
  pure-software x264 fallback works everywhere.
- Python 3.9+ (stdlib only).
