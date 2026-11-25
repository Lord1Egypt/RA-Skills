---
name: subclip-rough-cut
description: Build a clean first-draft spoken-video sequence by ordering uploaded clips, conservatively removing dead air from the actual media, transcribing each surviving item, and ripple-cutting standalone filler words such as um, uh, ah, and erm. Use for rough cuts, first assemblies, talking-head cleanup, silence removal from video, or filler-word removal. Do not use for audio-only enhancement or highlight/viral clip selection.
---

# Subclip Rough Cut

Produce an editable first assembly, not a polished social edit. Read [references/workflow.md](references/workflow.md) before analyzing waveforms or making cuts.

## Invariants

- Keep the requested order in one compact media lane 0 with no overlaps or unexplained gaps.
- Cut actual media with `trim_media_item`, `split_timeline_item`, and `delete_timeline_item`; deleting captions alone never cleans video.
- Treat normalized waveform peaks as boundary evidence, not semantic truth.
- Apply cut ranges latest-to-earliest and re-list after each ripple deletion; IDs and later times may change.
- Preserve MediaPanel sources and original file durations. Do not add polish that was not requested.

## Workflow

1. Inspect the active project and asset inventory; resolve/import every requested source in creator order.
2. Build the compact lane-0 sequence, then perform the conservative waveform silence pass from the reference.
3. Re-list the surviving items and transcribe each exact `mediaItemId`, sequentially. Follow normal Cloud authorization and local-only-on-request rules; persist pending IDs before each background callback.
4. Derive only high-confidence standalone filler ranges from the saved words, refine them at nearby quiet boundaries, and merge adjacent ranges.
5. Split and delete those media ranges latest-to-earliest. Let native ripple deletion remove and shift owned captions; do not delete the same captions separately first.
6. Re-read state, set duration to the final surviving content end, and verify representative joins and the final frame.
7. Update the director brief with ordered sources, transcription mode, removed ranges/count, and uncertain fillers deliberately retained for review.

Favor a slightly human pause over an over-cut, robotic sentence. When confidence is low, leave the interval and identify it for manual review.
