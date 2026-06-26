---
name: beat-sync-video-editing
description: This skill should be used when the user asks to "edit a video to music", "create a beat-synced edit", "make a montage", "sync cuts to beats", "cut a video to the beat", "make a music video edit", "edit clips to a song", "build FFmpeg filters for video editing", or mentions combining video clips with audio tracks using timed cuts. Provides knowledge of the EditPlan format, FFmpeg filter_complex construction, and beat-sync editing workflows.
---

# Beat-Sync Video Editing

## Purpose

Provide domain expertise for creating beat-synced video edits: taking a source video and an audio track, selecting clips from the video that align with the music's rhythm, and rendering the final output with FFmpeg.

## Core Concept: The EditPlan

Every edit starts as an EditPlan — a JSON structure that describes which video clips to use and where in the audio to place them:

```json
{
  "audio_start": "00:13",
  "audio_duration": 6.5,
  "clips": [
    { "video_start": "00:08", "duration": 2.0, "description": "Opening shot" },
    { "video_start": "00:45", "duration": 1.5, "description": "Action moment" },
    { "video_start": "01:22", "duration": 3.0, "description": "Build-up" }
  ],
  "reasoning": "Matches rising intensity with beat drops"
}
```

**Timestamp format:** `audio_start` and `video_start` use MM:SS strings (e.g. `"01:15"` for 1 minute 15 seconds). `audio_duration` and clip `duration` use numbers in seconds.

**Critical constraints:**
- `audio_start` must be valid MM:SS format, non-negative
- `audio_duration` must be positive (seconds)
- Every clip must have valid MM:SS `video_start` and positive `duration` (seconds)
- Sum of all clip durations must equal `audio_duration` (within 0.5s tolerance)
- Clip order is intentional — not necessarily chronological. Non-linear ordering creates dynamic edits.

## Workflow: From Files to Final Video

### Step 1: Generate EditPlan via Gemini

Run the Gemini script to analyze video + audio and produce a plan:

```bash
# Fresh upload (default: files kept 48h for reuse, ECLIPTIC_FILES printed on stderr):
bash ${CLAUDE_PLUGIN_ROOT}/scripts/gemini-edit-plan.sh \
  --video <video_path> \
  --audio <audio_path> \
  --prompt "<user's edit description>"

# Reuse previously uploaded files (skips upload, much faster):
bash ${CLAUDE_PLUGIN_ROOT}/scripts/gemini-edit-plan.sh \
  --video-uri <uri> --video-mime <mime> \
  --audio-uri <uri> --audio-mime <mime> \
  --prompt "<different description>"

# One-shot mode (delete files immediately after use):
bash ${CLAUDE_PLUGIN_ROOT}/scripts/gemini-edit-plan.sh \
  --video <video_path> \
  --audio <audio_path> \
  --prompt "<description>" --cleanup
```

- Outputs EditPlan JSON to stdout, progress to stderr
- Requires `GEMINI_API_KEY`, `curl`, and `jq`
- Gemini watches the video and listens to the audio simultaneously

**File lifecycle.** The script keeps uploaded files by default so subsequent runs can reuse them without re-uploading. Gemini enforces a 48-hour TTL — after that, URIs go stale and must be re-uploaded. Each run emits an `ECLIPTIC_FILES` JSON line on stderr containing `video_name`, `audio_name`, URIs, and MIME types — capture this to iterate with `--video-uri` / `--audio-uri`. The script also prints the exact `cleanup-gemini-files.sh` command at the end of every run so deletion is explicit and copy-pasteable. To flip the default to one-shot deletion, pass `--cleanup` or export `ECLIPTIC_CLEANUP=1` in the environment. `--no-cleanup` is accepted as a no-op alias for the default.

**Model selection.** The script defaults to `gemini-3-flash-preview`. To use a different model, export `GEMINI_MODEL` before invocation:

```bash
export GEMINI_MODEL=gemini-3.1-pro-preview   # stronger reasoning, slower
# or
export GEMINI_MODEL=gemini-2.5-flash         # stable (non-preview) fallback
```

The model name is passed straight into the request URL, so any Gemini model that supports video + audio input and structured JSON output will work.

### Step 2: Validate the Plan

```bash
echo '<plan_json>' | bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate-plan.sh
```

- Outputs `{"valid": true, "errors": []}` or `{"valid": false, "errors": [...]}`
- Exit code 0 = valid, 1 = invalid

### Step 3: Build FFmpeg Filters

```bash
echo '<plan_json>' | bash ${CLAUDE_PLUGIN_ROOT}/scripts/build-filter.sh
```

- Outputs `{"videoFilter": "...", "audioFilter": "...", "fullFilter": "..."}`
- The `fullFilter` field is what goes into FFmpeg's `-filter_complex` argument

### Step 4: Render with FFmpeg

```bash
ffmpeg -y -i "<video_path>" -i "<audio_path>" \
  -filter_complex "<fullFilter>" \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -shortest \
  "<output_path>"
```

## FFmpeg Filter Anatomy

For a 3-clip edit, the `fullFilter` looks like:

```
[0:v]trim=start=8.000:duration=2.000,setpts=PTS-STARTPTS[v0];
[0:v]trim=start=45.000:duration=1.500,setpts=PTS-STARTPTS[v1];
[0:v]trim=start=22.000:duration=3.000,setpts=PTS-STARTPTS[v2];
[v0][v1][v2]concat=n=3:v=1:a=0[outv];
[1:a]atrim=start=13.000:duration=6.500,asetpts=PTS-STARTPTS[outa]
```

- `[0:v]` = first input (video), `[1:a]` = second input (audio)
- `trim` extracts a segment, `setpts=PTS-STARTPTS` resets timestamps
- `concat` joins all video segments in order
- `atrim` extracts the audio section

For the full FFmpeg filter reference, see `${CLAUDE_SKILL_DIR}/references/ffmpeg-filters.md`.

## Troubleshooting

**Duration mismatch error**: Clip durations don't sum to `audio_duration`. Fix by adjusting the last clip's duration to absorb the difference, or re-run Gemini with a stricter prompt.

**FFmpeg "Error" in stderr**: FFmpeg writes progress and warnings to stderr. Only treat it as a real error if the output file wasn't created. Check for actual error patterns like `No such file`, `Invalid data`, or `Conversion failed`.

**Gemini returns poor clips**: Add specificity to the prompt. Instead of "make an edit", say "make a fast 30-second action edit, cut every 1-2 seconds on the beat drops, start from the chorus".

## Additional Resources

### Reference Files

- **`${CLAUDE_SKILL_DIR}/references/ffmpeg-filters.md`** — Detailed FFmpeg filter_complex syntax, encoding options, common flags
- **`${CLAUDE_SKILL_DIR}/references/edit-plan-schema.md`** — Full EditPlan JSON schema, validation rules, edge cases

### Scripts

- **`${CLAUDE_PLUGIN_ROOT}/scripts/gemini-edit-plan.sh`** — Upload to Gemini via REST API, get EditPlan (supports `--no-cleanup` and file reuse)
- **`${CLAUDE_PLUGIN_ROOT}/scripts/validate-plan.sh`** — Validate EditPlan JSON
- **`${CLAUDE_PLUGIN_ROOT}/scripts/build-filter.sh`** — Convert EditPlan to FFmpeg filters
- **`${CLAUDE_PLUGIN_ROOT}/scripts/cleanup-gemini-files.sh`** — Delete uploaded files from Gemini when done iterating
