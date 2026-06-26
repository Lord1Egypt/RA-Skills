# WeryAI Video Generation Models

Model capabilities are now fetched dynamically from the WeryAI API.
Display names in this file follow the shared `core/weryai-core/model-display.js` normalization, while `model_key` remains the request parameter.

## Querying Models

Run the `models` command to see all available video models and their capabilities:

```sh
node scripts/models-video.js
node scripts/models-video.js --mode text_to_video
node scripts/models-video.js --mode image_to_video
node scripts/models-video.js --mode multi_image_to_video
```

The output includes per-model metadata: supported aspect ratios, durations, resolutions, prompt length limits, upload image limits, and feature flags such as `generate_audio`, `negative_prompt`, and `support_multiple_images`.

## Default Configuration

- Default model: **Seedance 2.0** (`SEEDANCE_2_0`)
- Default aspect_ratio: `9:16`
- Default duration: first allowed value from model metadata (typically 5s)
- Default resolution: `720p`
- `generate_audio` defaults to `true` on audio-capable models

## Notes

- Image-to-video uses a single `image` field (string URL).
- Multi-image-to-video uses `images` field (array of URLs), trimmed to model's upload_image_limit.
- First-frame / last-frame workflows can be passed as ordered `images`, `first_frame` + `last_frame`, or `image` + `last_image`.
- If a model reports `support_multiple_images: false`, reports `upload_image_limit < 2`, or is absent from the multi-image registry while still existing in the image-to-video registry, the runtime falls back to `image-to-video` and uses only the first image from `images`.
- Video generation takes significantly longer than image generation; default poll timeout is 10 minutes.
- If the models API is unreachable, the CLI falls back to permissive mode with hardcoded defaults.
- In permissive mode, unsupported multi-image models cannot be pre-detected; the backend may still reject those submissions.
