---
name: subclip-timeline-story
description: Restructure pacing and story with Subclip UnifiedTimeline using cuts, splits, timing, ordering, B-roll, text beats, and audio synchronization. Use for shortening, removing sections, rearranging scenes, pacing, hooks, highlights, montage construction, or timeline cleanup.
---

# Subclip Timeline Story

1. Call `list_editor_assets`; inspect media, audio, text, captions, duration, and playhead.
2. Identify dependencies before a cut: linked captions, audio, text, and overlapping layers.
3. Use `split_timeline_item` for reversible cuts. Media, audio, text, and canvas-background items can be split when the requested time is strictly between the item's start and end. The tool saves both items directly and returns their IDs. Use `delete_timeline_item` only for an exact intended item ID, including `itemType="background"` for a selected canvas-background segment. Timeline deletion is checkpointed and Undo-recoverable, so an explicit user request such as “delete the muted duplicate” does not require another approval prompt. Re-list assets and confirm that exact ID is absent.
   - Timeline deletion keeps the backing MediaPanel/AudioPanel file. When the user explicitly asks to clean the project library too, use `delete_project_assets` with exact file IDs and `confirmed: true`; it removes every linked placement, so do not also delete those items individually.
4. Use `update_media_item`, `update_audio_item`, or `update_text_item` for timing and panel controls while preserving source windows and IDs. Use raw `update_editor_state` only when no named tool exposes the property.
5. Verify continuity and project duration. The canvas-background row follows the project clock and is not content: after shortening an edit, call `set_project_duration` so it cannot leave a background-only blank tail. If the tool reports later items, shorten, move, or delete those exact items first. Inspect frames before and after important cut points and near the exact final frame.

## Compact lane grammar

- UnifiedTimeline reads lanes from top to bottom: lane 0 is the top visible row.
- Keep non-overlapping sequential cuts in one compact lane. A later cut belongs on the same row when the earlier cut has ended.
- Allocate another lane only when time ranges actually overlap.
- For overlapping media, set compositing order deliberately: the higher `zIndex` layer appears in front and in the visually higher lane.
- Do not persist arbitrary lane numbers to force spacing. Split at scene boundaries first, then layer only the overlapping middle segments.

## Reference-audio montage workflow

1. Extract and import the reference video soundtrack first with `extract_attachment_audio_to_timeline`; make its end time the exact project duration when the user says it is the final clock.
2. Transcribe that returned native `audioItemId`. Use its words and beats to decide what action belongs at each cut; do not transcribe an unrelated source clip.
3. Inspect all relevant source storyboards. For heavy-action requests, select only identifiable action-rich frames and skip dark, duplicate, idle, obstructed, or ambiguous material.
4. Import the authorized originals. If an original is incompatible, call `import_attachment_clip_with_ffmpeg` once with the exact selected trim. Store its returned `jobId` and end the in-app agent turn without polling; Subclip resumes the same conversation when it becomes terminal. Queued/running is normal and is not a reason to start another conversion. On completion, the job atomically imports a full compatible source and applies that selection as non-destructive native in/out points.
5. Arrange cuts across the master audio without extending beyond its duration. Keep the extracted soundtrack editable and audible, then call `set_all_video_audio` with `muted: true` so source clips cannot compete with it.
6. Verify every cut visually and verify the last frame lands at or before the master audio end.

## Learning from a reference edit

Treat a reference as evidence, not a template to copy mechanically. Infer which qualities matter for the user's request—such as shot choice, pacing, ordering, audio overlap, transition rhythm, framing, or caption timing—and reproduce only those qualities that serve the new material.

- Inspect enough timestamped visual and audio context to distinguish deliberate editing patterns from incidental details.
- Choose cuts, splits, overlaps, lanes, and source ranges from the actual request and available footage. Do not assume a fixed number of scenes, a continuous master track, or a J-cut/L-cut structure unless the evidence supports it.
- Preserve non-destructive source windows and use the smallest set of timeline mutations that achieves the intended result.
- Re-list the edited items and validate the timing/source fields that substantiate the claimed change. Inspect representative live frames around meaningful boundaries.
- If the reference is ambiguous or a requested characteristic cannot be verified, state the uncertainty rather than inventing a rigid reconstruction recipe.

For several incompatible originals, enqueue each conversion once and store the distinct job IDs. Subclip serializes the work to keep the editor responsive and resumes the agent for each terminal event. Do not block on or repeatedly invoke a long synchronous transcode. Cancel obsolete jobs with `cancel_media_import` before changing the cut plan.

Prefer reversible, small edit batches. Do not silently ripple unrelated tracks. Keep dialogue captions synchronized with their source speech. Use undo or project history when an operation produces an inconsistent timeline.
