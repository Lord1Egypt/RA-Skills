---
name: episode-to-instagram
version: 1.0.1
description: Full pipeline to turn a video podcast episode into Instagram content (carousel posts, quote cards, and Reels). Transcribes the episode, extracts key quotes with timestamps, pulls video frames, generates aesthetic carousel slides, and posts to Instagram via browser automation. Use when the user provides a full podcast/video episode or a YouTube/video webpage URL and wants Instagram-ready content generated and posted.
---

# Episode to Instagram

End-to-end pipeline: video episode or YouTube/video webpage URL → local media acquisition → transcript → content extraction → carousel/image generation → Instagram posting via browser automation.

## Prerequisites

- `ffmpeg` (installed via Homebrew)
- OpenAI API key (for Whisper transcription)
- Replicate API key (for visual generation — optional, can use built-in image generation)
- `openclaw browser` for Instagram posting
- Instagram account logged in via the OpenClaw browser profile (optional account/series branding can be stored in `brand-config.json`, e.g. `@yourhandle`)

## Pipeline Steps

### Step 0: Acquire Source Media

If the user provides a YouTube URL or a webpage that embeds a podcast/video episode:

1. Resolve the actual video URL from the page if needed
2. Download the best practical local source copy before transcription/frame extraction
3. Save the original source URL alongside the working files for traceability
4. Prefer a stable MP4/MOV source when possible; if only YouTube is available, download the combined video/audio asset first

Expected outputs in the episode working directory:
- `source-url.txt`
- `source-video.mp4` (or equivalent local video file)

### Step 1: Transcribe

Script: `scripts/transcribe.sh`

1. Extract audio from the video file using ffmpeg
2. Split into chunks if >25MB (Whisper API limit)
3. Send to OpenAI Whisper API for transcription
4. Output: timestamped transcript as JSON + plain text

### Step 2: Extract Content

This step is model-driven (not scripted). The agent should:

1. Read the full transcript
2. Identify the 8-12 best moments for Instagram content:
   - 3-4 short quotable moments (for carousel text overlays)
   - 2-3 key insight passages (for carousel takeaway slides)
   - 3-4 high-energy or visually interesting segments (for Reel clip timestamps)
3. For each moment, record:
   - Exact timestamp (start + end)
   - The quote or passage text
   - Content type: quote_card | takeaway | reel_clip
   - Suggested carousel slide text (cleaned up for Instagram)
4. Output a structured content plan as JSON

### Step 3: Extract Video Frames

Script: `scripts/extract-frames.sh`

1. For each quote/takeaway moment, extract a frame at the timestamp using ffmpeg
2. Extract multiple frames around each timestamp (±2 seconds) and pick the best one
3. Output: PNG frames in a working directory

### Step 4: Attach Frames to the Content Plan

Before rendering any carousel slides, the agent must update the content plan so each slide that references a selected moment has a concrete `framePath` pointing at an extracted frame file. Do not render slides until this mapping is present and verified.

Validation before rendering:
- Every non-hook/non-CTA slide should either have a valid `framePath` or be intentionally text-only
- If `framePath` values are missing, stop and repair the plan before running the generator
- Spot-check at least one rendered slide to confirm the background image is visible and not falling back to a plain background unexpectedly

### Step 5: Generate Carousel Slides

Script: `scripts/generate-carousel.js`

For each carousel post (5-7 slides):

1. Slide 1: Hook slide — bold text + video frame background
2. Slides 2-5: Key quotes/takeaways with text overlay on video frames
3. Final slide: CTA ("Follow for more" / episode link)

Carousel image specs:
- 1080x1080px (square) or 1080x1350px (portrait, 4:5 — higher engagement)
- Consistent brand aesthetic (colors, fonts, overlay style)
- Text must be readable over the video frame (use semi-transparent overlay)

For visual enhancement, optionally use Replicate models:
- Background enhancement/style transfer on frames
- Generate complementary visuals from episode themes

### Step 6: Preview & Approve

Before posting, the agent must:

1. Send all generated carousel slides to the user via Slack
2. Send the full proposed caption text verbatim so the user can reply with direct edits
3. Send the content plan summary
4. Wait for explicit approval
5. Accept edits/feedback and regenerate as needed

### Step 7: Post to Instagram

Script: `scripts/post-to-instagram.js`

Uses `openclaw browser` to:

1. Open Instagram in the browser
2. Use the main sidebar/header `+` / `Create` entrypoint
3. Explicitly choose `Post` or `Reel` based on the asset being uploaded (do not assume every `+` opens post creation; profile-page `New` may open Highlight instead)
4. Upload the staged media from OpenClaw's upload temp root
5. For videos/Reels, use the CDP-backed draft helper instead of `openclaw browser upload` so the flow avoids the flaky browser upload bridge
6. Preserve the original image/video aspect ratio via the bottom-left `Select crop` control before moving past the crop step; do not leave it on Instagram's default crop if that changes the intended composition
7. Enter the caption text
8. Screenshot the preview for final confirmation
9. Only post after explicit approval

Crop rule:
- After upload, explicitly check the crop step and switch to the original aspect ratio/original framing when needed.
- Do not accept Instagram's default square crop if it trims important composition or changes the intended look of the source image.

Practical note:
- If Instagram opens `New Highlight` or any non-post flow, back out and retry from the main `Create`/sidebar `+` entrypoint, then select `Post` before uploading media.
- Keep a user-visible working copy in a Desktop folder named `instagram` when helpful (for example: `~/Desktop/instagram/`), but before calling `openclaw browser upload`, copy the final asset(s) into `/tmp/openclaw/uploads/...` because the browser CLI only accepts uploads from that temp root.
- For single-image posts sourced from chat, first copy the inbound image into the Desktop `instagram` folder if you want a visible local working copy, then stage that Desktop copy into `/tmp/openclaw/uploads/...` for browser upload.
- For `.mp4` or `.mov` uploads, prefer the Reel flow unless the user explicitly wants a feed video post.
- For video uploads derived from X posts, prefer an IG-safe working copy that is at most about 89 seconds and at most 1080p. Preserve quality as much as possible while keeping the file under the working upload ceiling.

## Content Rules

### Quote Cards
- Keep text under 150 characters for readability
- Use the speaker's actual words when possible
- Add attribution (guest name / episode title)

### Takeaway Carousels
- 5-7 slides per carousel
- Strong hook on slide 1 (question or bold statement)
- One idea per slide
- Clean, readable typography
- CTA on last slide

### Reel Clips
- 60-90 seconds max
- Include captions/subtitles
- Strong hook in first 3 seconds
- Extracted via ffmpeg from source video

## Brand Aesthetic

To be configured per user. Store in `brand-config.json`:

```json
{
  "primaryColor": "#000000",
  "secondaryColor": "#FFFFFF",
  "accentColor": "#8B5CF6",
  "fontStyle": "clean-modern",
  "overlayOpacity": 0.6,
  "format": "1080x1350",
  "accountHandle": "",
  "seriesName": "",
  "hashtagSets": []
}
```

## Approval Rules (Strict)

- Never post without explicit user approval
- Always show preview screenshots before posting
- In Slack-thread runs, include the full editable caption text in the same thread reply rather than only summarizing it
- If user requests edits, regenerate and re-preview
- Carousel order must be confirmed before posting

## File Structure

```
episode-to-instagram/
├── SKILL.md
├── brand-config.json
├── scripts/
│   ├── transcribe.sh          # Audio extraction + Whisper API
│   ├── extract-frames.sh      # ffmpeg frame extraction
│   ├── generate-carousel.js   # Canvas-based slide generation
│   └── post-to-instagram.js   # Browser automation for IG posting
└── output/                    # Working directory for generated content
    └── {episode-id}/
        ├── transcript.json
        ├── transcript.txt
        ├── content-plan.json
        ├── frames/
        ├── slides/
        └── reels/
```

## Public Repo Notes

- This published version ships with a neutral `brand-config.json`; customize it for your own account before generating slides.
- The repository intentionally does not include any local auth-profile helpers or generated output files.
- `OPENAI_API_KEY` should be provided by your shell, secret manager, or OpenClaw runtime before using `scripts/transcribe.sh`.
