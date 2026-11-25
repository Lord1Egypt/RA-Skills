---
name: subclip-ai-clipping
description: Find high-retention, standalone social clips from video transcripts and assemble editable candidates with gaps, hooks, vertical reframing, face crops, podcast layouts, tutorial screen-and-presenter layouts, or Aura fill. Use for AI clipping, viral moments, shorts, reels, TikToks, podcast clips, talking-head highlights, or screen-recording clips. Do not use for linear first-draft cleanup or generic montage requests without transcript-led highlight selection.
---

# Subclip AI Clipping

Create an editable clips-only candidate reel in the active project. Read [references/selection-and-layout.md](references/selection-and-layout.md) before scoring candidates, choosing a layout, or assembling the reel.

## Workflow

1. Inspect the request, director brief, source items, captions, and canvas. Honor an explicit canvas; otherwise use 9:16.
2. Use a trustworthy timestamped host-provided YouTube transcript when present. Otherwise transcribe exact source `mediaItemId` values sequentially under the normal Cloud/local authorization rules. Keep that source transcript available until candidate caption ownership has been rebuilt.
3. Select distinct, non-overlapping intervals using the reference scoring contract. Respect a requested count; otherwise keep the strongest 3–5 and never add weak filler candidates.
4. Assemble candidate groups in source order beginning at exactly `1.0s`, with constituent pieces contiguous and exactly `2.0s` between groups. A request to make clips, shorts, reels, or highlights is clips-only intent by default: after the candidate reel and captions are verified, remove the original full-length timeline placements but keep their source files in Project Media. Preserve source placements only when the creator explicitly asks for a source-plus-candidates review timeline.
5. Place native copies by file ID, convert timeline ranges to exact source in/out, and trim them non-destructively. Keep one audible copy per interval.
6. Choose an evidence-based `fill_face`, `fill_faces_split`, `tutorial`, or `fit_canvas`/Aura layout. Inspect the start, end, sentence/shot boundaries, and at least every 3–5 seconds. When the speaker, object, or shot position materially changes, split on a natural boundary and apply a new stable focus/layout for that segment; do not use face-chasing keyframes.
7. Write a truthful source-language hook under 12 words, then follow the reference's Subclip-web layout policy. For `fill_face` and `fill_faces_split`, do not add a separate TextPanel by default; let the opening Dynamic Captions carry the hook without covering a face. For `fit_canvas`, add a compact hook only in verified negative space above the contained media. For `tutorial`, use the compact four-second tutorial card. Never place a three-line headline over a face.
8. Rebuild candidate captions without unnecessary transcription. If the source item owns editor captions, call `reuse_caption_timing_for_media_items` after all target copies are trimmed and before the full source item is deleted. If the host supplied timestamped YouTube/SRT/VTT cues but the source has no editor captions, call `import_caption_cues_for_media_item` for each audible candidate using only exact source-file-relative cues that overlap its trim. Only if neither route is available should you transcribe each newly placed audible candidate item sequentially. When Dynamic Captions are requested or part of the chosen AI-clips treatment, load `subclip-dynamic-captions` with `read_subclip_skill` after timing ownership is rebuilt and run its full semantic intelligence; applying a preset without word analysis and page refinement is incomplete.
9. Persist each candidate's number, title, exact duration, score, hook, evidence-based reason, source range, output range, layout, interval checks, and caption-reuse decision in the director brief.
10. Verify each candidate's first spoken frame, midpoint, end, every layout boundary, and any separate hook placement, then re-list state to prove count, the `1.0s` lead-in, `2.0s` gaps, trims, caption ownership, mute policy, lanes, and duration.
11. In the completion message, report every clip separately with its title, `M:SS` duration, viral score out of 100, and one concrete sentence explaining why the selected source moment can retain, help, surprise, or move viewers. The reported values must match the director brief; never finish with only a generic candidate summary.

Do not call a nonexistent viral-clipping endpoint, fabricate face tracks, or replace the project with generated video. Selection and assembly must remain native and manually editable.

## Publish individual clips

If the user requests uploading the generated clips, read `subclip-youtube` (or `subclip-social-media` for other platforms). Use each candidate's saved OUTPUT timeline start/end range with a meaningful filename, preserve the reel, and export sequentially. Publish the resulting files directly with `youtube_upload_file` / `publish_video_file_to_social`, or publish the exact ranges with the segment tools. Do not clone one project per clip, delete other clips, or import/delete exported files in a temporary upload timeline. Obtain an exact per-item or reviewed batch publishing confirmation, including schedule mechanism and timezone, and keep operation/publication IDs for safe resume.
