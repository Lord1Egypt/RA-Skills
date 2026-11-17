# Seedance 2.5

Model ID: `doubao-seedance-2-5-260628`. The current entry supports 480p, 720p, and 1080p; adaptive `-1` or 4–30 seconds; and up to 30 image, 10 video, and 10 audio references. Use [the API contract](../../api/seedance.md) for the complete compatibility matrix and media limits.

Choose the mode from the requested result, while preserving any explicit model:
- Text and action description: [prompting](prompting.md).
- New content informed by assets: [reference generation](reference-generation.md).
- Start/end appearance or narrative frames: [frames and storyboards](frames-and-storyboards.md).
- Modify an existing video or continue it: [editing and extension](editing-and-extension.md).

Reference generation does not guarantee preservation of a source video's structure. Do not label a reference task as a precise edit. Do not carry 2.5-only fields into 2.0. Review complex bindings against the returned video rather than assuming that acceptance proves adherence.
