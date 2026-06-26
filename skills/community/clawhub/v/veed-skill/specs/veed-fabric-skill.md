# VEED Fabric 1.0 Talking Video Skill — Spec

## Problem

Founders and non-video-makers need to create professional talking-head videos (product demos, LinkedIn content, investor updates) but lack video editing skills, equipment, or time. VEED's Fabric 1.0 API can turn a photo + audio/text into a realistic talking video, but using a raw API is intimidating for non-technical users.

This skill wraps the Fabric 1.0 API into a conversational Claude Code experience where a founder can go from "here's my headshot and script" to a finished talking video in one interaction.

## Solution Overview

A public Claude Code skill (published to skills.sh) that orchestrates VEED Fabric 1.0 video generation. It supports two input paths:

1. **Image + Audio** → calls `/` endpoint to lip-sync audio onto a face
2. **Image + Text** → calls `/text` endpoint to generate speech and lip-sync in one step

The skill handles local file uploads, async queue polling with status updates, and downloads the finished video to the user's project directory.

## Detailed Requirements

### Trigger / Activation

The skill activates on **branded triggers only** to avoid conflicts with other video tools:
- User mentions "veed", "fabric", or "talking video"
- Examples: "create a talking video with veed", "use fabric to make a video", "generate a talking video from my photo"
- Does NOT activate on generic "make a video" or "create content" requests

### Input Path 1: Image + Audio

1. User provides an image (local file path or URL) and an audio file (local path or URL)
2. Skill validates file formats:
   - Image: JPG, JPEG, PNG, WebP, GIF, AVIF
   - Audio: MP3, OGG, WAV, M4A, AAC
3. If local files detected, upload to fal.ai storage to get public URLs
4. Ask user for resolution (default: 480p) and speed (default: standard)
5. Submit to Fabric API

### Input Path 2: Image + Text

1. User provides an image (local file path or URL) and a text script
2. Skill validates:
   - Image format (same as above)
   - Text length: must be 1–2000 characters
   - If text exceeds 2000 chars → **reject with clear guidance**: "Your script is {X} characters ({X - 2000} over the 2000-char limit, roughly 30–45 seconds of speech). Please shorten it or split into multiple videos."
3. User provides the exact script text — the skill does NOT assist with writing/editing scripts
4. Ask user for voice style via **presets + free text option**:
   - Presets: "Professional" (clear, confident, business tone), "Casual" (warm, conversational), "Energetic" (upbeat, enthusiastic), or "Custom" (user types their own description)
   - These map to the `voice_description` parameter
5. Ask for resolution (default: 480p) and speed (default: standard)
6. Submit to Fabric API `/text` endpoint

### File Handling

- **Local files**: Auto-detect local file paths (vs URLs). Upload to fal.ai storage using their file upload API to get a public URL.
- **URLs**: Use directly — validate they're accessible before submitting.
- Supported image formats: JPG, JPEG, PNG, WebP, GIF, AVIF
- Supported audio formats: MP3, OGG, WAV, M4A, AAC

### Resolution Options

- **480p** (default): $0.08/sec standard, $0.10/sec fast
- **720p**: $0.15/sec standard, $0.20/sec fast
- Default to 480p to keep costs low for iterating founders
- Show pricing when asking so user can make an informed choice

### Speed Options

- **Standard** (default): Normal generation speed, lower cost
- **Fast** (`/fast` endpoint): ~25% more expensive, faster generation
- Expose as an option, not the default

### Async Processing & Status

1. Submit job to fal.ai async queue
2. Poll for status periodically
3. Show progress updates to user (e.g., "Generating video... 45% complete", "Almost done...")
4. On completion, download video

### Output

- Download the generated MP4 to `./output/` in the current working directory
- Filename format: `fabric-video-{timestamp}.mp4` (e.g., `fabric-video-2026-03-16-143022.mp4`)
- Create `./output/` directory if it doesn't exist
- Display the local file path and the fal.ai hosted URL to the user upon completion

### Authentication

- Expects `FAL_KEY` environment variable to be set
- If missing, fail with a helpful message: "FAL_KEY environment variable not found. Get your API key at https://fal.ai/dashboard/keys and set it with: export FAL_KEY=your_key_here"
- Do NOT store or prompt for the key interactively

## Technical Approach

### Skill Structure (skills.sh format)

```
veed-skill/
├── SKILL.md          # Skill definition with frontmatter + instructions
└── specs/            # This spec
```

The `SKILL.md` file contains YAML frontmatter (`name`, `description`) and markdown instructions that tell Claude how to orchestrate the API calls.

### API Integration

All API calls made via `curl` from the Bash tool (no external dependencies needed):

**Authentication header:**
```
Authorization: Key $FAL_KEY
```

**Endpoints:**
| Endpoint | URL | Use |
|---|---|---|
| Image + Audio | `POST https://fal.run/veed/fabric-1.0` | Lip-sync with provided audio |
| Image + Audio (fast) | `POST https://fal.run/veed/fabric-1.0/fast` | Faster lip-sync |
| Image + Text | `POST https://fal.run/veed/fabric-1.0/text` | TTS + lip-sync |
| Image + Text (fast) | `POST https://fal.run/veed/fabric-1.0/text/fast` | Faster TTS + lip-sync |

**Queue-based flow:**
1. `POST` to queue endpoint → get `request_id`
2. `GET` status endpoint with `request_id` → poll until complete
3. Retrieve result with video URL
4. `curl` download video to local `./output/`

**File upload (for local files):**
Use fal.ai's file upload mechanism to get public URLs for local files before submitting to the generation endpoint.

### Voice Presets (for /text endpoint)

| Preset | `voice_description` value |
|---|---|
| Professional | "Clear, confident, professional business tone" |
| Casual | "Warm, friendly, conversational tone" |
| Energetic | "Upbeat, enthusiastic, high-energy tone" |
| Custom | User's free-text input passed directly |

## Out of Scope

- **Script writing/editing**: The skill does not help draft or refine scripts. User provides exact text.
- **Video editing/post-processing**: No trimming, adding music, subtitles, or effects after generation.
- **Batch processing**: One video at a time. No bulk generation from multiple scripts.
- **Image generation**: User must provide their own photo. No AI headshot generation.
- **Audio generation outside Fabric**: No integration with external TTS services. Only Fabric's built-in `/text` endpoint.
- **Video stitching**: If a script is too long, user must manually split and combine. Skill does not auto-stitch.
- **Persistent configuration**: No saved profiles, preferences, or templates between sessions.

## Edge Cases & Error Handling

| Scenario | Handling |
|---|---|
| `FAL_KEY` not set | Clear error message with link to get a key |
| Invalid image format | Reject with list of supported formats |
| Invalid audio format | Reject with list of supported formats |
| Text > 2000 chars | Reject with char count, overage amount, and guidance to shorten |
| Empty text | Reject: "Please provide a script for the video" |
| Local file doesn't exist | "File not found: {path}. Please check the path and try again." |
| File upload fails | "Failed to upload {filename}. Check your FAL_KEY and internet connection." |
| API returns error | Show the error message from fal.ai. Common: invalid key, rate limit, unsupported file |
| Generation times out | After reasonable timeout (~5 min), inform user and provide the request ID so they can check later |
| Queue polling fails | Retry a few times, then surface the error with the request ID |
| Video download fails | Show the hosted URL so user can download manually |
| `./output/` dir not writable | Inform user and suggest an alternative location |

## Success Criteria

1. **End-to-end flow works**: A founder with a headshot and script can generate a talking video in a single Claude Code session
2. **Both paths functional**: Image+Audio and Image+Text both produce valid MP4 output
3. **Local files work**: User can reference `./headshot.png` and `./script.mp3` without needing to host them
4. **Non-technical UX**: Voice preset menu, clear pricing info, progress updates — no API jargon exposed
5. **Error messages are actionable**: Every failure tells the user exactly what to do next
6. **Installable from skills.sh**: `npx skills add` works and the skill activates on branded triggers

## Open Questions

1. **fal.ai file upload API**: Need to verify the exact endpoint and mechanism for uploading local files to fal.ai storage. The docs reference it but specifics need confirmation.
2. **Queue polling endpoint**: Need to confirm the exact URL pattern for checking job status (likely `https://queue.fal.run/veed/fabric-1.0/requests/{request_id}/status`).
3. **Fast + Text combo**: Need to verify that `/text/fast` is a valid endpoint (the docs show `/fast` and `/text` separately).
4. **Rate limits**: Are there per-key rate limits that founders should know about?
