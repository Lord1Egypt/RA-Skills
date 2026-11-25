# Subtitles and video packaging

Use the contents to read only the section needed for the current operation. Each section retains its own parameters, authorization, and execution boundaries.

- [Adding Vibbit subtitles](#subtitle-addition)
- [Subtitle removal](#subtitle-removal)
- [Video packaging](#video-packaging)

<a id="subtitle-addition"></a>

## Adding Vibbit subtitles

Use this cloud path when Vibbit subtitles are specifically requested. Ordinary subtitles can be completed locally through [hybrid production](../../workflows/hybrid-video.md).

Public `MEDIA_PRODUCTION` examples include text/subtitle tracks; use [media composition](media-composition.md). Distinguish an existing timed transcript, a need for transcription, and dynamic subtitle styling.

<a id="subtitle-addition-correct-segment-and-time-captions"></a>

### Correct, segment, and time captions

1. Fix the adopted media and script. Reuse applicable SRT/VTT, transcripts, or measured timing; a script without timing needs [ASR](../analysis/speech-transcription.md) or other real evidence. Unspoken titles/information cards do not require ASR. Preserve raw recognition and media identity; corrected captions are a derived output.
2. Compare actual speech with the script, checking omissions, repeats, names, numbers, units, and mixed languages. Correct ASR mistakes in captions. Actual spoken mistakes need audio repair or an explicit remaining issue; correct captions cannot hide wrong speech. Listen to uncertain passages, or mark them unverified.
3. Normalize display spelling, numbers, abbreviations, and punctuation without changing meaning. Keep displayed text separate from pronunciation and do not rewrite the adopted script to match recognition errors.
4. Break at short clauses, semantic groups, and actual pauses. Keep names, number-unit pairs, and fixed phrases together. Fit the frame, font, and reading speed, usually in one or two lines, instead of applying a universal character count.
5. Ordinary captions use actual video-breakdown segment `from/to` values or audio ASR sentence `begin_time/end_time` in milliseconds. Divide audio values by 1000; establish video units before mapping to the composition timeline. Line wrapping within a caption keeps its time span. Splitting into sequential captions needs actual subsegment/word boundaries or boundaries established by listening. Without them, keep the original interval and wrap lines; never divide time by character count. Only word highlighting or word-triggered animation needs [word-level binding](../../creation/script-and-timing.md).
6. Composite through the selected production path and check readability, bounds, overlap, synchronization, and transitions. Text/style changes reuse speech and avatar footage and rerender only affected postproduction. New audio requires corresponding new timing.

Captions and B-roll share the actual timeline. Account for trims, speed changes, or inserted intervals; picture-only overlays can retain timing when soundtrack and temporal relationships are unchanged. Missing word timestamps must not block ordinary segment captions.

For subtitle-file delivery, export SRT/VTT through [transcript tools](../../runtime/transcript-tools.md); corrected/bilingual display files bind to the source transcript. Burning captions uses the existing local project/FFmpeg or verified cloud fields; do not assume compose accepts arbitrary SRT files. Speech reports help locate uncertainties, but listen before deciding whether captions or audio need correction.

Vibbit dynamic subtitle templates are temporarily unavailable; do not submit their parameters. Continue ordinary captions through this page. Read [subtitle template boundaries](../../resources/subtitle-templates.md) when that specific style is requested.

If runnable composition configuration is missing, deliver text/timing and explain it has not been burned into the video. Do not claim complete automatic transcription and dynamic-styling integration.

<a id="subtitle-removal"></a>

## Subtitle removal

Use [remove_subtitles](../../api/remove_subtitles.md) for one directly accessible `video_url`. Resolve share pages first. Follow media conditions in the API; URL validation by the CLI does not probe remote video.

Preserve the original and follow the returned task ID. Do not append translation, voice, packaging, or image generation to a subtitle-only request. There is no region-selection field; do not invent bounding boxes.

For multiple videos, use [bounded client batching](../../workflows/batch-production.md), not nonexistent server batch/cancel/callback operations. Removal may damage foreground or background details. Inspect representative frames with and without original captions, duration, and sound. Disclose defects or unavailable quality checks, and do not automatically regenerate.

<a id="video-packaging"></a>

## Video packaging

For specifically requested Vibbit packaging, use [media composition](media-composition.md) with the actual `video_packing_template` configuration. Do not assume that passing an ID alone applies a template. Ordinary titles/backgrounds/decorations can instead be rendered locally.

Preserve an existing valid configuration. With only a template name or ID, query [packaging templates](../../resources/packaging-templates.md) and inspect actual detail/configuration. Match ratio, title, and background to supported fields without adding unsolicited branding or watermarks.

If no matching template/configuration is available, deliver a packaging plan or use an already valid configuration. A guessed template is not a real resource.
