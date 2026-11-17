---
name: socialkit-youtube-assemble
description: Renders a YouTube video from shot-list.json - images and clips scaled to the target resolution, voiceover, optional background music and subtitles - into an H.264/AAC MP4 using FFmpeg. Use when the user wants to assemble, render, stitch or export the final video file for a YouTube project.
license: MIT
compatibility: Requires Node.js 22.12+ and FFmpeg (FFMPEG_PATH, the ffmpeg-static binary from a global install of social-agent-skills, or ffmpeg on PATH).
metadata:
  author: Ahmad Hussain
  platform: youtube
  requires: socialkit-social-core
---

# YouTube assemble

## Steps

1. Validate first:
   `node scripts/assemble.mjs --dir <project-folder> --check`
   It reports missing files, unsupported types, missing durations and a voiceover longer
   than the visuals. Fix `shot-list.json` or ask the user for the missing assets.
2. Render:
   `node scripts/assemble.mjs --dir <project-folder>`
   Output goes to `output/video.mp4` unless the shot list sets `output`.
3. Tell the user the output path and length, and ask them to watch it. Collect changes,
   update the shot list or assets, and re-render with `--overwrite`.

Run `node scripts/assemble.mjs --help` for the shot list format.

## Output contract

JSON on stdout with `ok`, `output` and `totalSeconds`, and an MP4 in the project folder.

## Failure handling

- `FFMPEG_MISSING`: show the hint; the user installs FFmpeg or sets `FFMPEG_PATH`.
- `OUTPUT_EXISTS`: ask before re-running with `--overwrite`. Overwriting invalidates an
  existing upload approval.
- `FFMPEG_FAILED`: show the last lines of the error. Common causes are corrupt inputs or
  unsupported codecs; re-encode the asset or replace it.
