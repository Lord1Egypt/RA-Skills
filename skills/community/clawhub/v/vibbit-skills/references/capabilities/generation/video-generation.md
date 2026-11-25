# Video generation

For a reference video whose facial features/hair must change to a selected person, first follow [facial identity replacement](../../workflows/face-identity-replacement.md) to establish appearance references and remove competing source identity. Then submit actual multi-reference fields. Retaining the performer or only changing clothes does not add this stage.

Choose text, single-image, first/last-frame, reference, edit, or extension mode according to the actual request and the [Seedance API](../../api/seedance.md). Preserve an explicit model and supported parameters. Otherwise Seedance 2.5 is the general route; a simple unspecified clip can start with one 5-second, 16:9 output. User requirements, input constraints, and mode restrictions still govern ratio and duration. Resolve paid generation resolution below; local template export settings are separate.

## Paid video settings

- Set actual requests to `resolution: "720p"` for new generation, reference adaptation, editing, extension, and localized regeneration unless the user explicitly specifies another supported resolution. Carry an explicit 720p requirement through revisions, retries, and batches without reconfirming it.
- A source, reference image, previous output, template, or historical request at 1080p/4k describes that asset or record; it does not authorize paid generation at that resolution. Higher resolution requires an explicit user requirement. Broad goals such as high quality, stability, or better detail do not raise the resolution automatically.
- Keep the user's selected model when it supports the task. Do not upgrade, downgrade, or switch models on your own for repairs or consistency. Explain actual incompatibilities rather than automatically changing model or resolution and resubmitting.
- Record paid generation resolution separately from local composition/export dimensions. Match a 720p repair to a higher-resolution base as needed for assembly and inspect joins; do not pay for 1080p regeneration solely to match the base or describe local scaling as native high-resolution generation.
- Before submission, check the actual model, `resolution`, duration, and count against the user's requirements and these defaults, then dry-run. Inspect inherited requests instead of copying them wholesale.

Describe visible actions within the time budget. Assign each real reference a clear role and maintain its array order. Preserve useful user wording; do not add unrelated scenes, sound, or effects. Audio options and prompt intent must agree.

Read only the relevant [model guide](../../models/index.md). Reference generation is not guaranteed precise editing or lip sync. Check downstream assembly requirements before paying for incompatible assets.

After submission, poll the same task ID. Review the returned video for the requested content and actual media properties. Do not silently regenerate when an output needs revision. See [video review](../analysis/video-review.md).
