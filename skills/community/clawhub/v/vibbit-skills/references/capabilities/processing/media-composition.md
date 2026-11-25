# Cloud media composition

Use [compose](../../api/compose.md), task type `MEDIA_PRODUCTION`, for supported cloud assembly. Preserve the exact nested field names and mixed casing in `packing_origin`, tracks, and `video_packing_template`. The CLI's top-level validation does not validate every nested track field.

This is the default execution path for ordinary editing and [Agent semantic mixcut](../../workflows/semantic-mixcut.md). The Agent’s [audio/picture plan](../../contracts/semantic-mixcut.md) is not a request body: map only verified source intervals, placements, audio choices, and captions to supported fields. Verify per-clip muting, video-source sound, independent audio placement, and gain against the real contract; global original_volume does not establish per-clip control. Neither mixcut.js nor compose dry-run proves complex edits executable. Retain the plan and identify missing fields rather than using private website endpoints or silently rendering locally.

Use real accessible input URLs, actual source intervals and target placement, deliberate original-audio handling, and the selected template's known configuration and time units. Upload local outputs when required. Do not invent library IDs or claim a platform project was saved.

Cloud composition assembles media; it does not run Remotion or Hyperframes projects. See [hybrid workflow](../../workflows/hybrid-video.md), [templates](../../resources/packaging-templates.md), and [media inputs](../../runtime/media-inputs.md).

For requested Jianying drafts, use [desktop draft handoff](../../workflows/jianying-draft.md). Current OpenAPI cannot supply the required Job ID. Without a separate valid ID, retain the cloud output and report draft export blocked; do not substitute task_id or repeatedly poll an unavailable field. Guide official installation when absent; a real ID is still required after installation. Distinguish cloud completion, client launch and a written draft.
