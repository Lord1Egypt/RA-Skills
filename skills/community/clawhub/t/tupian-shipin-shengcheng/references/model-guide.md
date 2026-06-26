## Model Guide

Use this reference when deciding which model to choose and which parameters are required.

## VEO Video

### `veo_3_1-fast`

- Use for text-to-video.
- Use for reference-image video with up to 3 images.
- Builder mode:
  - `--prompt`
  - optional `--size`
  - optional repeated `--reference-file`
- If reference images are present, the script uses multipart upload and also sends Base64 fallback data.

### `veo_3_1-fast-fl`

- Use for start/end frame mode.
- Requires 1 or 2 images.
- The first image is the start frame.
- The second image, if present, is the end frame.
- Builder mode:
  - `--prompt`
  - `--start-frame-file`
  - optional `--end-frame-file`
  - optional `--size`
- If the user selects this model and does not provide 1 or 2 images, stop and tell them exactly what is missing.

### `veo_3_fast` and `veo_3`

- Treat as general VEO video models.
- Use raw JSON if the user needs fields not covered by builder mode.

## Banana Image

### Standard Banana

Models:
- `nano_banana_2`
- `nano_banana_pro`
- `nano_banana_pro-1K`
- `nano_banana_pro-2K`
- `nano_banana_pro-4K`

Builder mode:
- `--prompt`
- optional `--aspect-ratio`
- optional repeated `--reference-url`
- optional repeated `--reference-file`

### Gemini Banana

Models:
- `nano_banana_2-landscape`
- `nano_banana_2-portrait`
- `nano_banana_pro-1K-landscape`
- `nano_banana_pro-1K-portrait`
- `nano_banana_pro-2K-landscape`
- `nano_banana_pro-2K-portrait`
- `nano_banana_pro-4K-landscape`
- `nano_banana_pro-4K-portrait`

Builder mode:
- `--prompt`
- optional repeated `--reference-file`

Use raw JSON if the user wants to hand-author `contents` or `generationConfig`.

## Sora Video

Models:
- `sora-2-landscape-10s`
- `sora-2-portrait-10s`
- `sora-2-landscape-15s`
- `sora-2-portrait-15s`
- `sora-2-pro-landscape-25s`
- `sora-2-pro-portrait-25s`
- `sora-2-pro-landscape-hd-15s`
- `sora-2-pro-portrait-hd-15s`

Builder mode:
- `--prompt`
- optional `--style`
- optional `--image-url`
- optional `--reference-file`

Rules:
- `--image-url` and `--reference-file` are mutually exclusive.
- Local file mode supports one image file.
- If the user needs extra upstream fields, switch to raw JSON or raw multipart mode.
