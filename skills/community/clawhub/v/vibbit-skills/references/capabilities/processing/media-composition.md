# Cloud media composition

Use [compose](../../api/compose.md), task type `MEDIA_PRODUCTION`, for supported cloud assembly. Preserve the exact nested field names and mixed casing in `packing_origin`, tracks, and `video_packing_template`. The CLI's top-level validation does not validate every nested track field.

Use real accessible input URLs, actual source intervals and target placement, deliberate original-audio handling, and the selected template's known configuration and time units. Upload local outputs when required. Do not invent library IDs or claim a platform project was saved.

Cloud composition assembles media; it does not run Remotion or Hyperframes projects. See [hybrid workflow](../../workflows/hybrid-video.md), [templates](../../resources/packaging-templates.md), and [media inputs](../../runtime/media-inputs.md).
