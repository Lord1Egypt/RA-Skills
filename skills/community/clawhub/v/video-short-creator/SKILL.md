---
name: video-short-creator
description: "Two-phase AI-narrated video short creator with human review checkpoints. Phase 1 analyzes source materials, generates TTS narration via edge-tts, and exports a subtitle review sheet for user approval. Phase 2 assembles the final video with FFmpeg including clipping, scaling, xfade transitions, SRT subtitle burning, and audio merge. Use when creating a short-form video with AI voiceover from existing video clips and a script, especially for tech/AI paper explanation videos for social media."
---

# Video Short Creator

Two-phase workflow for creating AI-narrated short videos from source clips and a script, with human review at every critical step.

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| FFmpeg | Video processing | `winget install FFmpeg` or download from ffmpeg.org |
| Python 3.8+ | Script execution | Use the managed runtime |
| edge-tts | Microsoft TTS | `pip install edge-tts` (no API key needed) |
| SimHei font | Chinese subtitle rendering | Usually pre-installed on Windows (`C:\Windows\Fonts\simhei.ttf`) |

## Phase 1: Material Preparation & Review

This phase generates the narration audio and exports a review sheet. **Stop and wait for user approval before proceeding.**

### Step 1.1: Analyze Materials

1. Ask the user for:
   - **Source video clips** (paths or a folder)
   - **Script / narration text** (or generate one from provided reference material)
   - **Target resolution** (default: 1920x1080 landscape)
   - **Voice preference** (default: `zh-CN-YunxiNeural`, young male Mandarin)
   - **Publishing platform** (optional, affects aspect ratio recommendations)
2. Scan all source clips with `ffprobe` to catalog:
   - Resolution, duration, file size
   - Generate a **clip inventory table**
3. If no script is provided but reference material (paper URL, markdown, etc.) is given:
   - Research the content and draft a narration script
   - Structure as 3-5 segments with natural flow

### Step 1.2: Build SCRIPT Data Structure

Create a Python list of segment dicts that maps each narration segment to source clips:

```python
SCRIPT = [
    {
        "id": "seg1",          # unique segment ID
        "text": "...",         # narration text for this segment
        "videos": [            # source clips to use
            {"file": "clip1.mp4", "start": 0, "max_dur": 14},
            {"file": "clip2.mp4", "start": 5, "max_dur": 30},
        ],
    },
    # ... more segments
]
```

Key design decisions:
- Each segment's total available video duration should exceed narration duration by ~0.5s
- Use multiple clips per segment for visual variety
- `max_dur` prevents over-long clips from a single source

### Step 1.3: Generate TTS & Export Review Sheet

Run `scripts/step1_generate_review.py` with the SCRIPT config:

```bash
python scripts/step1_generate_review.py
```

This script:
1. Generates TTS audio for each segment using edge-tts
2. Extracts clean subtitle timing from `SentenceBoundary` events (NOT `WordBoundary`)
3. Exports `subtitle_review.md` with all subtitle entries + timing info

### Step 1.4: Present Review Materials to User

Display the following for user review:

1. **Clip Inventory** - All source clips with metadata
2. **Script Review** - Full narration text organized by segment
3. **Subtitle Review Sheet** (`subtitle_review.md`) - All subtitle entries with:
   - Sequence number, segment ID, start/end time, duration, text content
4. **Segment-to-Clip Mapping** - Which clips are used for each narration segment

Ask the user to review and confirm or provide modifications:
- Text corrections in narration or subtitles
- Timing adjustments
- Clip substitutions or reorderings
- Adding/removing subtitle entries

> **CRITICAL: Do NOT proceed to Phase 2 until the user explicitly approves.**

## Phase 2: Video Assembly

Only start after user approval of Phase 1 materials.

### Step 2.1: Apply User Edits (if any)

If the user provided subtitle edits:
1. Parse their feedback and update the subtitle entries accordingly
2. If they created a `subtitle_edited.txt`, load it (format: `start_sec|end_sec|text` per line)
3. Re-verify that all source clip paths exist

### Step 2.2: Execute Video Assembly

Run `scripts/step2_edit_video.py`:

```bash
python scripts/step2_edit_video.py
```

The assembly pipeline:
1. **Clip & Scale** - Extract clips at specified start/duration, scale to target resolution (1920x1080)
2. **Concatenate** - Join multiple clips per segment using concat demuxer
3. **Burn Subtitles** - Overlay subtitles using `.srt` file + FFmpeg `subtitles` filter
4. **xfade Transitions** - Chain segments with alternating fade/fadeblack transitions (0.8s)
5. **Build Audio** - Concatenate narration segments with short silences between them
6. **Final Merge** - Combine video + audio into final output

### Step 2.3: Output

- Final video at `output/{PROJECT_NAME}_FINAL.mp4`
- Resolution: 1920x1080, 30 FPS
- Subtitle style: SimHei font, size 14, white text, thin outline, bottom-aligned (movie-style)
- Audio: AAC 128kbps
- Video: H.264 CRF 20

### Step 2.4: Present Final Video

Use `open_result_view` to present the final video. Ask user for feedback on:
- Subtitle readability and positioning
- Transition smoothness
- Audio-video sync
- Overall pacing

## Configuration

All configuration lives in the SCRIPT data structure at the top of each script. Key constants:

| Constant | Default | Description |
|----------|---------|-------------|
| `VOICE` | `zh-CN-YunxiNeural` | edge-tts voice (Mandarin, young male) |
| `TARGET_W/H` | 1920x1080 | Output resolution |
| `XFADE_DUR` | 0.8 | Transition duration in seconds |
| `SUBTITLE_FONT_SIZE` | 14 | Subtitle font size |
| `SUBTITLE_MARGIN_V` | 50 | Bottom margin for subtitles |

## Known Pitfalls (Windows)

- **Never use `drawtext` filter** — shell escaping for `\n` and special characters is unreliable on Windows. Always use `.srt` file + `subtitles` filter instead.
- **SRT file paths need escaping** for FFmpeg `subtitles` filter: replace `\` with `/` and `:` with `\:`.
- **edge-tts `SentenceBoundary`** gives clean text; `WordBoundary` may contain artifacts like stray `n` characters.
- **Always re-fetch subtitle timing** even when audio files are cached — edge-tts does not store boundary events.
- **xfade filter labels** must use `tmp0`, `tmp1` format (not `v01`, `v02`) to avoid FFmpeg parsing errors.
- For detailed pitfalls and debugging guidance, see `references/ffmpeg-pitfalls.md`.
