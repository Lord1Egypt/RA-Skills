---
name: subclip-export
description: Configure and run Subclip video or frame exports when container, codec, quality, alpha transparency, output location, or timeline range matters.
---

# Subclip export

Choose the export from the delivery requirement rather than guessing a container.

## Required flow

1. Call `get_export_configuration` when the user has not explicitly chosen a format or when transparency matters.
2. Confirm that the saved project and requested timeline range are valid.
3. Call `export_video` only after the user explicitly asks to export.
4. Use the request ID with `get_export_status` when the client is not automatically resumed.

## One shared render queue

Every render in Subclip goes through one queue: the creator's exports, yours, and recording exports. One project render runs at a time (a recording export may run next to it), in the order they were requested.

- Waiting is normal. While other renders are ahead, `get_export_status` reports `state: "queued"` with `queuePosition`; keep waiting (in-app agent runs are resumed automatically). `etaSeconds` appears once the render runs.
- The export renders a snapshot of the project as saved when `export_video` was called. Edits made afterwards, by you or the creator, do not change that file. Export again after further edits.
- Do not start a second export of the same unchanged project. Call `list_render_queue` first: it lists what runs, what waits and the latest finished renders with their files.
- `cancel_job` with the export's request ID cancels it: a queued render is removed, a running one is stopped and its partial file deleted.
- If the app quits or restarts during a render, that render is reported as failed ("The app closed during this render") and a waiting one as canceled; export again.

## Missing Remotion elements

If the user reports missing elements in an exported video, identify their owning layer. For an affected Remotion layer, convert it to HyperFrames and match the original design and animation exactly; client-side Remotion export can omit elements visible in preview. Read `subclip-remotion-layer` with `resourcePath: "references/export-recovery.md"`, then `subclip-hyperframes-layer`. Verify the repaired export at the reported timestamps, not just the editor preview.

## Format decisions

- Use `mp4` for ordinary delivery, browser playback, social publishing, and maximum compatibility. It uses H.264 and never preserves alpha.
- Use `webm` for transparent client-rendered video when the destination supports VP9 WebM.
- Use `mkv` for VP9 transparency in production workflows that accept Matroska.
- Use `mov` for ProRes 4444 editing or compositing deliverables. Subclip renders an alpha WebM intermediate and converts it with bundled FFmpeg.
- Use `export_current_frame` for a PNG still at the current playhead.

## Transparency

- Set `transparent=true` only with `webm`, `mkv`, or `mov`.
- First verify that `currentCanvas.alphaAvailable` is true.
- If alpha is required but unavailable, use `set_canvas_background_visibility` to hide the full background track, or use `set_canvas_background` to create a timed transparent segment when only part of the video should expose alpha.
- Never claim that MP4 contains transparency.

## Quality and range

- Default to `1080p` unless the user requests another resolution or the downstream workflow requires 2K/4K.
- Preserve the project aspect ratio at every quality.
- Omit `startTime` and `endTime` for a complete export.
- For a segment, provide both values and a meaningful `outputFileName`.
- Do not include an extension in `outputFileName`; Subclip applies the selected format.

## Output behavior

- Use `outputDirectory` only when the user specifies an absolute destination.
- Otherwise allow Subclip to open its native save picker after rendering.
- Completed video exports are revealed in Finder or Explorer automatically.

## Publish individual clips

If the user requests uploading the generated clips, read `subclip-youtube` (or `subclip-social-media` for other platforms). Use each candidate's saved OUTPUT timeline start/end range with a meaningful filename, preserve the reel, and export sequentially. Publish the resulting files directly with `youtube_upload_file` / `publish_video_file_to_social`, or publish the exact ranges with the segment tools. Do not clone one project per clip, delete other clips, or import/delete exported files in a temporary upload timeline. Obtain an exact per-item or reviewed batch publishing confirmation, including schedule mechanism and timezone, and keep operation/publication IDs for safe resume.
