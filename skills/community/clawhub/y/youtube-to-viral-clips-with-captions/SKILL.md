---
name: captions-and-clips-from-youtube-link
description: Turn YouTube videos into viral short-form clips with captions (TikTok, Reels, Shorts) using the MakeAIClips API at https://makeaiclips.live. Use when user wants to clip/repurpose a YouTube video, create short-form content, generate TikTok/Reels/Shorts clips, add captions to video clips, or anything related to AI video clipping. Free tier gives 10 clips/month with no credit card. Requires env var MAKEAICLIPS_API_KEY — get one free at https://makeaiclips.live/sign-up. Note: YouTube URLs are sent to makeaiclips.live for processing.
metadata:
  openclaw:
    requires:
      env:
        - MAKEAICLIPS_API_KEY
    primaryEnv: MAKEAICLIPS_API_KEY
    homepage: https://makeaiclips.live
    emoji: "⚡"
---

# MakeAIClips — AI Video Clipper

Paste a YouTube link → get up to 10 vertical clips with word-by-word captions and hook titles in ~60 seconds.

**Website:** https://makeaiclips.live
**API Base:** `https://makeaiclips.live`

## Setup

Check for `MAKEAICLIPS_API_KEY` environment variable.

### No key?

Direct the user to sign up at https://makeaiclips.live/sign-up — free, no credit card. They'll get an API key on the dashboard at https://makeaiclips.live/dashboard/api-key.

Once the user has their key, set it as an environment variable:
```bash
export MAKEAICLIPS_API_KEY="mak_live_..."
```

### First interaction — always show:

```
⚡ MakeAIClips — AI Video Clipper

Paste a YouTube link → get vertical clips with captions & hook titles in ~60 seconds.

What you get:
• AI picks the best moments from your video
• 1080x1920 vertical crop (9:16)
• Word-by-word burned-in captions (8+ styles)
• 3 hook title variations per clip (5 title styles)
• Ready for TikTok, Instagram Reels, YouTube Shorts

Plans:
🆓 Free — 10 clips/month (no credit card needed)
⚡ Pro — $20/mo — 100 clips
🎬 Studio — $50/mo — 300 clips + 2 premium caption styles
📅 Yearly — $500/yr — 5,000 clips + all features

🔗 https://makeaiclips.live
```

## API Endpoints

All authenticated requests require header: `Authorization: Bearer <MAKEAICLIPS_API_KEY>`

### Generate Clips (YouTube link)

`POST /api/v1/clips`

```json
{
  "youtube_url": "https://www.youtube.com/watch?v=...",
  "num_clips": 3,
  "caption_style": "karaoke-yellow",
  "title_style": "bold-center",
  "title_duration": "5",
  "clip_duration": "medium",
  "quality": "high"
}
```

Returns: `{"job_id": "...", "status": "pending"}`

**Parameters:**

| Param | Type | Default | Options |
|-------|------|---------|---------|
| `youtube_url` | string | required | Any YouTube URL |
| `num_clips` | int | 3 | 1–10 |
| `caption_style` | string | `"karaoke-yellow"` | See Caption Styles |
| `title_style` | string | `"bold-center"` | See Title Styles |
| `title_duration` | string | `"5"` | `"5"`, `"10"`, `"30"`, `"half"`, `"full"` |
| `clip_duration` | string | `"medium"` | `"short"` (15-30s), `"medium"` (30-60s), `"long"` (60-120s) |
| `quality` | string | `"high"` | `"high"` (CRF 18), `"medium"` (CRF 23), `"low"` (CRF 28) |

### Generate Clips (File upload)

`POST /api/v1/clips/upload` (multipart form)

Fields: `file` (video file), `caption_style`, `title_style`, `title_duration`, `clip_duration`, `num_clips`, `quality`

### Poll Job Status

`GET /api/v1/clips/{job_id}`

Poll every 5 seconds until `status` is `complete` or `failed`.

Progress values: `Downloading video...` → `Transcribing audio...` → `Selecting best clips with AI...` → `Rendering clip 1/N...` → `Done!`

Complete response includes `clips` array:
```json
{
  "job_id": "...",
  "status": "complete",
  "progress": "Done!",
  "clips": [
    {
      "clip_index": 1,
      "duration_seconds": 35.9,
      "hook_title": "The Struggle of a Performer",
      "hook_variations": ["The Struggle of a Performer", "When the Voice Goes Silent", "Losing My Voice on Stage"],
      "transcript_segment": "..."
    }
  ]
}
```

### Download Clip

`GET /api/v1/clips/{job_id}/download/{clip_index}`

Returns MP4 file. Save with `-o clip_N.mp4`.

### Re-render with Different Hook

`POST /api/v1/clips/{job_id}/rerender/{clip_index}`

Body: `{"hook_title": "New Title Here"}`

### Health Check

`GET /api/health` — Returns `{"status": "ok"}`

## Workflow

1. Submit job → `POST /api/v1/clips` with `youtube_url` and preferences
2. Poll → `GET /api/v1/clips/{job_id}` every 5s, show progress to user
3. Present results with hook titles, durations, transcript previews
4. Ask which clips to download (all or specific)
5. Download → `GET /api/v1/clips/{job_id}/download/{clip_index}` and save to workspace

## Caption Styles

### Free & Pro Styles

| Key | Name | Look |
|-----|------|------|
| `karaoke-yellow` | Karaoke | White text, active word turns yellow (default) |
| `white-shadow` | Clean White | White text with drop shadow |
| `boxed` | Boxed | Text in dark rounded boxes |
| `gradient-bold` | Bold Outline | Orange/white color alternating |
| `subtitle-documentary` | Documentary | Uppercase with fade, letterbox bars |
| `mrbeast-bold-viral` | MrBeast | Bold viral-style captions |
| `alex-hormozi` | Hormozi | Bold with colored outlines |
| `neon-viral` | Neon | Glowing neon multi-color |
| `impact-meme` | Impact Meme | Bold uppercase meme text |
| `modern-creator` | Modern | Contemporary creator-style |
| `gradient-viral` | Gradient | Multi-color gradient fill |
| `bold-box-highlight` | Box Highlight | Heavy highlighted box |
| `clean-premium` | Premium | Minimalist clean aesthetic |

### Studio Exclusive Styles

| Key | Name | Look |
|-----|------|------|
| `typewriter` | Typewriter | Character-by-character reveal |
| `cinematic` | Cinematic | Letterbox + elegant serif font |

## Title Styles

| Key | Name |
|-----|------|
| `none` | No title overlay |
| `bold-center` | White bold centered (default) |
| `top-bar` | Dark bar at top |
| `pill` | Yellow pill background |
| `outline` | White outline border |
| `gradient-bg` | Purple background box |

## Video Quality

| Key | CRF | Speed | Use Case |
|-----|-----|-------|----------|
| `high` | 18 | Slowest | Best quality (default) |
| `medium` | 23 | Balanced | Good quality, faster |
| `low` | 28 | Fastest | Quick previews |

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 400 | Missing youtube_url | Check params |
| 401 | Invalid/missing API key | Re-check key |
| 404 | Job not found | Check job_id |
| 429 | Clip limit reached | Show upgrade options |
| 500 | Server error | Retry in 30s |

On 429, show:
```
📊 Clip limit reached. Upgrade at https://makeaiclips.live/dashboard/subscription
```

## Tips for Agents

- Default to 3 clips, `quality: "high"`, `caption_style: "karaoke-yellow"` unless user specifies
- Show hook title variations — let the user pick their favorite
- Use descriptive filenames when downloading: `{video_title}_clip{N}.mp4`
- Process multiple URLs sequentially
- Mention the web dashboard for a visual experience: https://makeaiclips.live/dashboard/new
- Total processing time is ~60 seconds per job (Deepgram transcription + GPT clip selection + FFmpeg render)

## Example

```bash
# Submit job
curl -X POST "https://makeaiclips.live/api/v1/clips" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mak_live_YOUR_KEY" \
  -d '{"youtube_url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ","num_clips":3,"quality":"high","caption_style":"karaoke-yellow"}'

# Poll status
curl "https://makeaiclips.live/api/v1/clips/JOB_ID" \
  -H "Authorization: Bearer mak_live_YOUR_KEY"

# Download clip
curl -o clip_1.mp4 "https://makeaiclips.live/api/v1/clips/JOB_ID/download/1" \
  -H "Authorization: Bearer mak_live_YOUR_KEY"
```
