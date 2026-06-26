# Tokenrouter Video API Reference

## Purpose

Use this reference after the workspace tokenrouter config has been updated so the requested video model (`MiniMax-Hailuo-2.3`, `kling-v3`, `kling-v2-6`, `dreamina-seedance-2-0-fast-260128`, or `dreamina-seedance-2-0-260128`) is routed correctly.

## Required Endpoints

### Create Video

- Method: `POST`
- Path: `/v1/video/generations`

#### MiniMax-Hailuo-2.3

Request body:

```json
{
  "model": "MiniMax-Hailuo-2.3",
  "prompt": "A man picks up a book [Pedestal up], then reads [Static shot].",
  "size": "1080P",
  "duration": 6
}
```

Supported `size` and `duration` combinations for `MiniMax-Hailuo-2.3`:

- `size: "1080P"` with `duration: 6`
- `size: "768P"` with `duration: 10`
- `size: "768P"` with `duration: 6`

Validation rule:

- Reject or correct any request that uses a different `size` and `duration` pairing.

#### kling-v3

Supports both text-to-video and image-to-video.

**Text-to-video:**

```json
{
  "model": "kling-v3",
  "prompt": "A silver robot walking through a rainy neon alley",
  "mode": "pro",
  "duration": "5",
  "metadata": {
    "aspect_ratio": "16:9",
    "sound": "on",
    "negative_prompt": "blurry, low quality"
  }
}
```

**Image-to-video:**

```json
{
  "model": "kling-v3",
  "prompt": "The girl smiles slightly and the camera slowly pushes in",
  "image": "https://example.com/portrait.png",
  "mode": "pro",
  "duration": "5",
  "metadata": {
    "sound": "off",
    "negative_prompt": "flicker, blur"
  }
}
```

`duration` is a string. Common values include `"5"`. `mode` is a string such as `"pro"`. `metadata` is optional but may include `aspect_ratio`, `sound`, and `negative_prompt`. `image` is optional; when present, it triggers image-to-video generation.

Validation rule:

- `size` must NOT be present for Kling requests.
- `mode` must be present and be a string.
- `duration` must be a string value such as `"5"`.
- If `image` is present, it must be a valid URL string (image-to-video mode).
- If `image` is NOT present, `prompt` must be present (text-to-video mode).

#### kling-v2-6

Supports both text-to-video and image-to-video.

**Text-to-video:**

```json
{
  "model": "kling-v2-6",
  "prompt": "A silver robot walking through a rainy neon alley",
  "mode": "pro",
  "duration": "5",
  "metadata": {
    "aspect_ratio": "16:9",
    "sound": "on",
    "negative_prompt": "blurry, low quality"
  }
}
```

**Image-to-video:**

```json
{
  "model": "kling-v2-6",
  "prompt": "The girl smiles slightly and the camera slowly pushes in",
  "image": "https://example.com/portrait.png",
  "mode": "pro",
  "duration": "5",
  "metadata": {
    "sound": "off",
    "negative_prompt": "flicker, blur"
  }
}
```

`duration` is a string. `mode` is a string such as `"pro"`. `metadata` is optional but may include `aspect_ratio`, `sound`, and `negative_prompt`. `image` is optional; when present, it triggers image-to-video generation.

Validation rule:

- `size` must NOT be present for Kling requests.
- `mode` must be present and be a string.
- `duration` must be a string value such as `"5"`.
- If `image` is present, it must be a valid URL string (image-to-video mode).
- If `image` is NOT present, `prompt` must be present (text-to-video mode).

#### dreamina-seedance-2-0-fast-260128

Supports both text-to-video and image-to-video.

**Text-to-video:**

```json
{
  "model": "dreamina-seedance-2-0-fast-260128",
  "prompt": "A vintage sports car driving along a coastal road at sunset",
  "metadata": {
    "duration": 5,
    "resolution": "1080p",
    "ratio": "16:9",
    "generate_audio": true
  }
}
```

**Image-to-video:**

```json
{
  "model": "dreamina-seedance-2-0-fast-260128",
  "prompt": "The subject looks up toward the camera while hair moves gently in the wind",
  "images": [
    "https://example.com/input-image.png"
  ],
  "metadata": {
    "duration": 5,
    "resolution": "720p",
    "ratio": "9:16"
  }
}
```

`prompt` is required for text-to-video, optional but recommended for image-to-video. `metadata` is optional but may include `duration`, `resolution`, `ratio`, and `generate_audio`. `images` is optional; when present, it triggers image-to-video generation. Do not send Hailuo-only fields (`size`) or Kling-only fields (`mode`, `image`) when using Seedance models.

Validation rule:

- If `images` is NOT present (text-to-video mode):
  - `prompt` must be present and be a string.
  - `size`, `mode`, and `image` must NOT be present.
- If `images` is present (image-to-video mode):
  - `images` must be a non-empty array of valid URL strings.
  - `size`, `mode`, and `image` must NOT be present.
- `metadata.duration` must be an integer if present.

#### dreamina-seedance-2-0-260128

Supports both text-to-video and image-to-video.

**Text-to-video:**

```json
{
  "model": "dreamina-seedance-2-0-260128",
  "prompt": "A vintage sports car driving along a coastal road at sunset",
  "metadata": {
    "duration": 5,
    "resolution": "1080p",
    "ratio": "16:9",
    "generate_audio": true
  }
}
```

**Image-to-video:**

```json
{
  "model": "dreamina-seedance-2-0-260128",
  "prompt": "The subject looks up toward the camera while hair moves gently in the wind",
  "images": [
    "https://example.com/input-image.png"
  ],
  "metadata": {
    "duration": 5,
    "resolution": "720p",
    "ratio": "9:16"
  }
}
```

`prompt` is required for text-to-video, optional but recommended for image-to-video. `metadata` is optional but may include `duration`, `resolution`, `ratio`, and `generate_audio`. `images` is optional; when present, it triggers image-to-video generation. Do not send Hailuo-only fields (`size`) or Kling-only fields (`mode`, `image`) when using Seedance models.

Validation rule:

- If `images` is NOT present (text-to-video mode):
  - `prompt` must be present and be a string.
  - `size`, `mode`, and `image` must NOT be present.
- If `images` is present (image-to-video mode):
  - `images` must be a non-empty array of valid URL strings.
  - `size`, `mode`, and `image` must NOT be present.
- `metadata.duration` must be an integer if present.

### Parameter Validation Rule

Before calling the create endpoint, always validate the request according to the chosen model:

**For MiniMax-Hailuo-2.3:**

1. Check that `prompt` is present and is a string.
2. Check that `size` is exactly `"1080P"` or `"768P"`.
3. Check that `duration` is exactly `6` or `10`.
4. Check that the pair belongs to the allowed set: (`1080P`, `6`), (`768P`, `10`), (`768P`, `6`).
5. Ensure `mode`, `image`, `images`, and `metadata` are NOT present (these fields belong to other models).
6. If validation fails, stop and tell the user the allowed combinations instead of sending the request.

**For kling-v3:**

1. Check that `mode` is present and is a string.
2. Check that `duration` is a string value such as `"5"`.
3. Ensure `size`, `images` are NOT present.
4. If `image` is present (image-to-video mode):
   - Check that `image` is a valid URL string.
   - `prompt` is optional but recommended.
   - `metadata.aspect_ratio` should NOT be present.
5. If `image` is NOT present (text-to-video mode):
   - Ensure `prompt` is present and is a string.
6. If validation fails, stop and tell the user the correct kling-v3 parameters instead of sending the request.

**For kling-v2-6:**

1. Check that `mode` is present and is a string.
2. Check that `duration` is a string value such as `"5"`.
3. Ensure `size`, `images` are NOT present.
4. If `image` is present (image-to-video mode):
   - Check that `image` is a valid URL string.
   - `prompt` is optional but recommended.
   - `metadata.aspect_ratio` should NOT be present.
5. If `image` is NOT present (text-to-video mode):
   - Ensure `prompt` is present and is a string.
6. If validation fails, stop and tell the user the correct kling-v2-6 parameters instead of sending the request.

**For dreamina-seedance-2-0-fast-260128:**

1. Ensure `size`, `mode`, `image` are NOT present.
2. If `images` is NOT present (text-to-video mode):
   - Check that `prompt` is present and is a string.
   - `metadata.generate_audio` is optional boolean.
3. If `images` is present (image-to-video mode):
   - Check that `images` is a non-empty array of valid URL strings.
   - `prompt` is optional but recommended.
   - `metadata.generate_audio` should NOT be present.
4. If `metadata.duration` is present, check that it is an integer such as `5`.
5. If validation fails, stop and tell the user the correct Seedance parameters instead of sending the request.

**For dreamina-seedance-2-0-260128:**

1. Ensure `size`, `mode`, `image` are NOT present.
2. If `images` is NOT present (text-to-video mode):
   - Check that `prompt` is present and is a string.
   - `metadata.generate_audio` is optional boolean.
3. If `images` is present (image-to-video mode):
   - Check that `images` is a non-empty array of valid URL strings.
   - `prompt` is optional but recommended.
   - `metadata.generate_audio` should NOT be present.
4. If `metadata.duration` is present, check that it is an integer such as `5`.
5. If validation fails, stop and tell the user the correct Seedance parameters instead of sending the request.

### Get Video Task

- Method: `GET`
- Path: `/video/generations/:task_id`

Replace `:task_id` with the identifier returned by the create call.

Expected behavior:

- The response may include state fields like `status`, `state`, `task_status`, `progress`, `error`, and one or more result URLs.
- Keep polling until the task is clearly complete or failed.
- When result URLs contain query parameters, preserve the complete URL including the query string.
- Decode any `\u0026` sequences in the URL to `&` before presenting or returning the URL.

## Polling Guidance

- Poll every 3 to 5 seconds unless the API response specifies a better interval.
- Stop polling on a terminal state such as `succeeded`, `failed`, `completed`, `success`, or equivalent.
- If the API returns a video URL array or nested output object, report the exact field path used.
- Preserve the full URL with query parameters; decode `\u0026` to `&` in the final output.

## Auth And Base URL

- Detect whether the current workspace already has a channel whose `baseurl` or `baseURL` contains `https://api.tokenrouter.com` or `https://open.palebluedot.ai`.
- If found, reuse that channel's key directly. The request base URL is always `https://api.tokenrouter.com`.
- Reuse the workspace's current auth style, usually `Authorization: Bearer <token>`.
- Do not hardcode secrets into source files.
- If no matching channel exists, stop and instruct the user to register at `https://www.tokenrouter.com` to obtain tokenrouter configuration.

## Config Inference Guidance

When adding a video model to tokenrouter config:

- Copy the nearest existing video model route if available.
- Reuse the same provider/channel object shape.
- Only add fields that are already idiomatic in that config file.
- Ensure this model points at the video-generation upstream path, not a chat/completions path.
