# Subtitle removal

Use [remove_subtitles](../../api/remove_subtitles.md) for one directly accessible `video_url`. Resolve share pages first. Follow media conditions in the API; URL validation by the CLI does not probe remote video.

Preserve the original and follow the returned task ID. Do not append translation, voice, packaging, or image generation to a subtitle-only request. There is no region-selection field; do not invent bounding boxes.

For multiple videos, use [bounded client batching](../../workflows/batch-production.md), not nonexistent server batch/cancel/callback operations. Removal may damage foreground or background details. Inspect representative frames with and without original captions, duration, and sound. Disclose defects or unavailable quality checks, and do not automatically regenerate.
