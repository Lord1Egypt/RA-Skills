# WeryAI Image Generation Models

Model lists are now fetched dynamically from the WeryAI API.
Display names in this file follow the shared `core/weryai-core/model-display.js` normalization, while `model_key` remains the request parameter.

## Query Available Models

```sh
# List all models (text-to-image + image-to-image)
node {baseDir}/scripts/models-image.js

# List only image-to-image models
node {baseDir}/scripts/models-image.js --mode image_to_image
```

The output includes per-model metadata: `model_key`, `title`, `image_sizes` (allowed aspect ratios), `num_images` (allowed output counts), `resolutions`, and `upload_image_limit` (for image-to-image).

## Important Notes

- Model keys may differ between text-to-image and image-to-image modes for the same product (e.g. `SEEDREAM_4` vs `SEEDREAM`).
- `image_sizes` may include resolution aliases like `"2k"`, `"3k"` in addition to aspect ratios.
- Default model: **WeryAI Image 2.0** (`WERYAI_IMAGE_2_0`)
- Default aspect_ratio: `9:16`
- Default image_number: `1`
- `image` can be normalized into the API `images` array for single-reference image-to-image requests.
- Parameters are validated dynamically against model capabilities.
