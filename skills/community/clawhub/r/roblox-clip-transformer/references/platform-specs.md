# Platform Specifications

Video requirements for TikTok, YouTube Shorts, Instagram Reels, and YouTube.

## TikTok

| Property | Recommended | Notes |
|----------|-------------|-------|
| Aspect Ratio | 9:16 (vertical) | Native format |
| Resolution | 1080x1920 | Minimum 720x1280 |
| Duration | 15-60 seconds | Max 10 minutes, but 15-60s performs best |
| FPS | 30 | 24-60 accepted |
| Format | MP4 (H.264) | |
| File Size | < 287 MB | |
| Bitrate | 516 kbps - 30 Mbps | |

**Best Practices:**
- Hook viewers in first 1-2 seconds
- Use trending sounds/music
- Add captions (85% watch muted)
- Keep text within safe zone (not too close to edges)

**Safe Zone:**
- Top: 150px from top (username, caption area)
- Bottom: 340px from bottom (username, caption, CTA)
- Left/Right: Keep text centered

---

## YouTube Shorts

| Property | Recommended | Notes |
|----------|-------------|-------|
| Aspect Ratio | 9:16 (vertical) | |
| Resolution | 1080x1920 | Minimum 720x1280 |
| Duration | < 60 seconds | Must be under 60s to be a Short |
| FPS | 30 | |
| Format | MP4 | |
| File Size | No limit | YouTube handles compression |

**Best Practices:**
- Strong opening (first 3 seconds critical)
- Add #Shorts in title or description
- Use Shorts shelf-friendly thumbnails
- Loop-friendly content works well

**Safe Zone:**
- Top: 100px (channel name)
- Bottom: 250px (action buttons)

---

## Instagram Reels

| Property | Recommended | Notes |
|----------|-------------|-------|
| Aspect Ratio | 9:16 (vertical) | |
| Resolution | 1080x1920 | |
| Duration | 15-90 seconds | 15, 30, or 90s options |
| FPS | 30 | |
| Format | MP4 | |
| File Size | < 4 GB | |

**Best Practices:**
- Use Instagram's audio library
- Add stickers, text, effects in-app when possible
- Story-style content works well
- Post during peak engagement times

**Safe Zone:**
- Top: 250px (username, audio info)
- Bottom: 450px (caption, buttons)

---

## YouTube (Horizontal)

| Property | Recommended | Notes |
|----------|-------------|-------|
| Aspect Ratio | 16:9 (horizontal) | |
| Resolution | 1920x1080 (1080p) | 4K: 3840x2160 |
| Duration | Any | Monetization requires 8+ min for mid-rolls |
| FPS | 30 (24-60) | |
| Format | MP4 (H.264) | |
| Bitrate | 8-12 Mbps (1080p) | |

**Best Practices:**
- Custom thumbnail (1280x720)
- End screens in last 20 seconds
- Chapters for longer videos
- Intro sequence < 5 seconds

---

## Comparison Table

| Platform | Aspect | Duration | Max Size | Captions Needed |
|----------|--------|----------|----------|-----------------|
| TikTok | 9:16 | 15-60s | 287 MB | Yes (85% muted) |
| Shorts | 9:16 | <60s | No limit | Yes |
| Reels | 9:16 | 15-90s | 4 GB | Yes |
| YouTube | 16:9 | Any | No limit | Recommended |

---

## Export Presets

### FFmpeg Commands

#### TikTok / Shorts / Reels (9:16 vertical)
```bash
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -c:a aac \
  -r 30 -t 60 \
  output.mp4
```

#### YouTube (16:9 horizontal)
```bash
ffmpeg -i input.mp4 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -c:a aac \
  -r 30 \
  output.mp4
```

#### With Burned Captions
```bash
ffmpeg -i input.mp4 -vf "subtitles=captions.srt:force_style='FontSize=24'" output.mp4
```

---

## Thumbnail Sizes

| Platform | Thumbnail Size | Notes |
|----------|----------------|-------|
| TikTok | Auto-generated | Can customize |
| Shorts | Auto from frame | Not customizable |
| Reels | 1080x1920 | Cover frame selection |
| YouTube | 1280x720 | Custom required |

---

## Audio Specifications

| Platform | Sample Rate | Bitrate | Codec |
|----------|-------------|---------|-------|
| TikTok | 44100 Hz | 192 kbps | AAC |
| Shorts | 44100 Hz | 128 kbps | AAC |
| Reels | 44100 Hz | 192 kbps | AAC |
| YouTube | 44100 Hz | 384 kbps | AAC |

**Music Guidelines:**
- Use royalty-free or licensed music
- TikTok/Reels have extensive music libraries
- For original audio, ensure clear voice separation
- Normalize audio levels to -14 LUFS