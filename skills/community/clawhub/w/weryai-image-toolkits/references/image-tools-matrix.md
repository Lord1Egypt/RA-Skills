# WeryAI Image Tools Matrix

Use this file when you need the exact parameter surface for a WeryAI image tool instead of relying on memory.

## Shared Contract

- Base URL: `https://api.weryai.com`
- Auth: `Authorization: Bearer <WERYAI_API_KEY>`
- Most image tools are async submit -> `task_id` -> poll task status
- `image-to-prompt` is synchronous and returns the prompt directly
- Async status values: `waiting`, `processing`, `succeed`, `failed`
- Async result field: `images`

## Tool Summary

### `image-to-prompt`

- Endpoint: `/v1/generation/image-to-prompt`
- Use for: analyze an image and return a descriptive prompt
- Required:
  - `img_url`
  - `image_size`
- Optional:
  - `language`
  - `model`
- Notes:
  - synchronous response
  - `image_size` is the source image size in KB

### `background-change`

- Endpoint: `/v1/generation/image-bg-change`
- Use for: replace or modify the background of an image
- Required:
  - `img_url`
- Additional rule:
  - either `prompt` or `bg_color` must be provided
- Optional:
  - `prompt`
  - `bg_color`
  - `webhook_url`
  - `caller_id`

### `background-remove`

- Endpoint: `/v1/generation/image-bg-remove`
- Use for: automatically remove the background
- Required:
  - `img_url`

### `expand`

- Endpoint: `/v1/generation/image-expand`
- Use for: expand the canvas around an image
- Required:
  - `img_url`
  - `original_image_size`
  - `canvas_size`
  - `original_image_location`
- Format rules:
  - `original_image_size`: `WIDTHxHEIGHT`
  - `canvas_size`: `WIDTHxHEIGHT`
  - `original_image_location`: `x,y`

### `face-swap`

- Endpoint: `/v1/generation/image-face-swap`
- Use for: swap a face in a source image
- Required:
  - `img_url`
  - `face_img_url`

### `reframe`

- Endpoint: `/v1/generation/image-reframe`
- Use for: change an image aspect ratio
- Required:
  - `img_url`
  - `aspect_ratio`
- Supported aspect ratios:
  - `16:9`
  - `9:16`
  - `1:1`
  - `4:3`
  - `3:4`
  - `21:9`
  - `9:21`

### `repair`

- Endpoint: `/v1/generation/image-repair`
- Use for: restore and enhance old or damaged photos
- Required:
  - `img_url`

### `text-erase`

- Endpoint: `/v1/generation/image-text-erase`
- Use for: erase text or watermarks from an image
- Required:
  - `img_url`
- Optional:
  - `model`

### `translate`

- Endpoint: `/v1/generation/image-translate`
- Use for: translate text inside an image
- Required:
  - `img_url`
  - `target_lang`
- Optional:
  - `type`
- Supported `type` values:
  - `text`
  - `image`
- Default in this skill:
  - `type=image`

### `upscale`

- Endpoint: `/v1/generation/image-upscale`
- Use for: enhance image quality and resolution with 2x upscale
- Required:
  - `img_url`

## Guidance Rules

- Ask only for the smallest missing parameter set for the selected tool.
- Prefer defaults only where the API clearly documents them.
- Keep all input asset URLs public `https://` URLs.
- Treat `WERYAI_API_KEY` as the only runtime secret and keep it out of the repository.
