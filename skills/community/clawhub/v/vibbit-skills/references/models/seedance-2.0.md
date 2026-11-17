# Seedance 2.0

Preserve an explicit 2.0 choice. Use the exact model IDs and limits in [Seedance API](../api/seedance.md). The normal model supports 480p, 720p, 1080p, and 4k; fast and mini support 480p and 720p. Duration is adaptive `-1` or 4–15 seconds.

Reference limits are 9 images, 3 videos, and 3 audio files. Audio references require an image or video reference. Single-image, first/last-frame, and reference-array modes are mutually exclusive; the last frame requires a first frame.

Do not send `omni_reference_task_type` for 2.0 or assume 2.5 editing, extension, or lock behavior applies. If the requested operation needs another model, explain the capability difference before changing the user's choice. See [video generation](../capabilities/generation/video-generation.md).
