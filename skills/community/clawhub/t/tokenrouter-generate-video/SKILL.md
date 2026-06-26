---
name: tokenrouter-video-usaging
description: >
  Guide the agent to perform tokenrouter channel and model configuration checks for video generation tasks.
  First, check whether the workspace already has a tokenrouter channel whose baseurl contains `https://api.tokenrouter.com` or `https://open.palebluedot.ai`.
  If no such channel exists, stop and instruct the user to visit `https://www.tokenrouter.com` to register and obtain tokenrouter configuration.
  If the channel exists, then check whether the requested video model (`MiniMax-Hailuo-2.3`, `kling-v3`, `kling-v2-6`, `dreamina-seedance-2-0-fast-260128`, or `dreamina-seedance-2-0-260128`) is already configured in the channel.
  If the model is missing, the agent should auto-configure the model route by inferring the existing schema and adding the smallest correct change.
  After confirming both the channel and the model are ready, use the configured route to create and query video generation tasks.
---

# Tokenrouter Video Usaging

## Overview

Find the tokenrouter channel configuration in the current workspace, infer the existing provider/channel schema from neighboring model entries, and add a `MiniMax-Hailuo-2.3`, `kling-v3`, `kling-v2-6`, `dreamina-seedance-2-0-fast-260128`, or `dreamina-seedance-2-0-260128` route with the smallest correct change. Then use the configured tokenrouter endpoint to create a video generation task and fetch task status until a final video URL or terminal state is returned.

## Workflow

1. **Channel Check**: Discover the tokenrouter config and check whether any configured channel has a `baseurl` or `baseURL` containing `https://api.tokenrouter.com` or `https://open.palebluedot.ai`.
   - If **NO** such channel exists, **STOP** immediately and tell the user: "No tokenrouter channel with `https://api.tokenrouter.com` or `https://open.palebluedot.ai` was found. Please visit `https://www.tokenrouter.com` to register and obtain your channel configuration, then add it to the workspace."
   - If a channel **IS** found, proceed to step 2.
2. **Model Check**: Check whether the requested video model (`MiniMax-Hailuo-2.3`, `kling-v3`, `kling-v2-6`, `dreamina-seedance-2-0-fast-260128`, or `dreamina-seedance-2-0-260128`) already exists in the channel's model map or route list.
   - If the model **IS** already configured, skip to step 4.
   - If the model is **NOT** configured, proceed to step 3.
3. **Auto-Configuration**: Infer the existing provider/channel schema from neighboring model entries, then add the missing model route with the smallest correct change.
   - Reuse the existing video provider pattern if one exists; otherwise mirror the closest neighboring provider entry.
   - Save the config change with the smallest possible edit. Do not rewrite unrelated formatting or reorder large sections unless the file format requires it.
   - Reload or restart the tokenrouter service if the workspace provides a command to do so.
4. **API Call**: Use the detected channel's key and the fixed base URL `https://api.tokenrouter.com` to call the video generation endpoints.
5. **Polling**: Poll task status until success, failure, or timeout.

## Config Discovery

Start by searching for likely tokenrouter config files in the current workspace.

- Prefer files matching names like `*tokenrouter*`, `*channel*`, `*provider*`, `*model*`, `config*.json`, `config*.yaml`, `config*.yml`, `*.toml`, `*.ts`, `*.js`.
- Look for keys such as `channels`, `providers`, `models`, `routes`, `baseURL`, `baseurl`, `apiKey`, `key`, `upstream`, `model_map`, `model_name`, or similar.
- Run `scripts/find_tokenrouter_config.py` first when the workspace is large or the config location is unclear.

Choose the config file that is actually consumed by the running tokenrouter setup, not merely documentation or examples.

Authentication discovery rule:

- Search current channel/provider configs for a `baseurl` or `baseURL` containing `https://api.tokenrouter.com` or `https://open.palebluedot.ai`.
- If found, treat that entry as the tokenrouter channel and reuse its configured key for `Authorization`.
- If not found, stop and instruct the user to register at `https://www.tokenrouter.com` to obtain tokenrouter access and the required channel configuration.

## Config Update Rules

Infer the schema from the file instead of assuming a fixed format.

- If the requested model (`MiniMax-Hailuo-2.3`, `kling-v3`, `kling-v2-6`, `dreamina-seedance-2-0-fast-260128`, or `dreamina-seedance-2-0-260128`) already exists, update only missing or incorrect fields.
- If there is an existing video-generation entry (MiniMax, Hailuo, Kling, Seedance, or another video model), copy that shape and adapt it.
- Preserve existing auth conventions. If an existing `https://api.tokenrouter.com` or `https://open.palebluedot.ai` channel is present, reuse that channel's key exactly as configured instead of introducing a new env var name.
- Prefer adding the new model alongside existing channel/provider definitions rather than introducing a second config mechanism.
- Do not invent fallback compatibility fields unless the surrounding config already uses them.

Minimum target behavior:

- The tokenrouter config must recognize the requested model name (`MiniMax-Hailuo-2.3`, `kling-v3`, `kling-v2-6`, `dreamina-seedance-2-0-fast-260128`, or `dreamina-seedance-2-0-260128`).
- Requests for that model must reach the upstream path `POST /v1/video/generations`.
- Status checks must use `GET /video/generations/:task_id`.

If the local tokenrouter schema distinguishes between chat/completions/image/video APIs, make sure this model is wired into the video path rather than a text generation path.

## API Calls

Use the fixed tokenrouter base URL `https://api.tokenrouter.com` for all API calls.

Auth rule:

- Base URL is always `https://api.tokenrouter.com`.
- If a matching channel exists, use that channel's configured key directly.
- If no matching channel exists, do not fabricate placeholders like `TOKENROUTER_API_KEY`; instead tell the user to register at `https://www.tokenrouter.com` and add tokenrouter config first.

### Model: MiniMax-Hailuo-2.3

Create video task:

```json
{
  "path": "/v1/video/generations",
  "method": "POST",
  "params": {
    "model": "MiniMax-Hailuo-2.3",
    "prompt": "A man picks up a book [Pedestal up], then reads [Static shot].",
    "size": "1080P",
    "duration": 6
  }
}
```

`size` and `duration` must be chosen as one of the supported Hailuo combinations:

- `1080P` with `6`
- `768P` with `10`
- `768P` with `6`

Do not mix unsupported combinations. If the user asks for another pair, ask them to choose one of the three valid options.

### Model: kling-v3

Supports both text-to-video and image-to-video.

**Text-to-video:**

```json
{
  "path": "/v1/video/generations",
  "method": "POST",
  "params": {
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
}
```

**Image-to-video:**

```json
{
  "path": "/v1/video/generations",
  "method": "POST",
  "params": {
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
}
```

`duration` is a string. Common values include `"5"`. `mode` is a string such as `"pro"`. `metadata` is optional but may include `aspect_ratio`, `sound`, and `negative_prompt`. `image` is optional; when present, it triggers image-to-video generation. Do not send Hailuo-only fields (`size`) when using `kling-v3`.

### Model: kling-v2-6

Supports both text-to-video and image-to-video.

**Text-to-video:**

```json
{
  "path": "/v1/video/generations",
  "method": "POST",
  "params": {
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
}
```

**Image-to-video:**

```json
{
  "path": "/v1/video/generations",
  "method": "POST",
  "params": {
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
}
```

`duration` is a string. `mode` is a string such as `"pro"`. `metadata` is optional but may include `aspect_ratio`, `sound`, and `negative_prompt`. `image` is optional; when present, it triggers image-to-video generation. Do not send Hailuo-only fields (`size`) when using `kling-v2-6`.

### Model: dreamina-seedance-2-0-fast-260128

Supports both text-to-video and image-to-video.

**Text-to-video:**

```json
{
  "path": "/v1/video/generations",
  "method": "POST",
  "params": {
    "model": "dreamina-seedance-2-0-fast-260128",
    "prompt": "A vintage sports car driving along a coastal road at sunset",
    "metadata": {
      "duration": 5,
      "resolution": "1080p",
      "ratio": "16:9",
      "generate_audio": true
    }
  }
}
```

**Image-to-video:**

```json
{
  "path": "/v1/video/generations",
  "method": "POST",
  "params": {
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
}
```

`prompt` is required for text-to-video, optional but recommended for image-to-video. `metadata` is optional but may include `duration`, `resolution`, `ratio`, and `generate_audio`. `images` is optional; when present, it triggers image-to-video generation. Do not send Hailuo-only fields (`size`) or Kling-only fields (`mode`, `image`) when using Seedance models.

### Model: dreamina-seedance-2-0-260128

Supports both text-to-video and image-to-video.

**Text-to-video:**

```json
{
  "path": "/v1/video/generations",
  "method": "POST",
  "params": {
    "model": "dreamina-seedance-2-0-260128",
    "prompt": "A vintage sports car driving along a coastal road at sunset",
    "metadata": {
      "duration": 5,
      "resolution": "1080p",
      "ratio": "16:9",
      "generate_audio": true
    }
  }
}
```

**Image-to-video:**

```json
{
  "path": "/v1/video/generations",
  "method": "POST",
  "params": {
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
}
```

`prompt` is required for text-to-video, optional but recommended for image-to-video. `metadata` is optional but may include `duration`, `resolution`, `ratio`, and `generate_audio`. `images` is optional; when present, it triggers image-to-video generation. Do not send Hailuo-only fields (`size`) or Kling-only fields (`mode`, `image`) when using Seedance models.

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

### Fetch task (all models)

```json
{
  "path": "/video/generations/:task_id",
  "method": "GET"
}
```

Implementation notes:

- Treat the create call as asynchronous.
- Extract `task_id` from the create response using the actual response schema returned by the server.
- Poll the fetch endpoint until a terminal state is reached.
- Report the full terminal payload and any resulting video URL(s).
- When extracting video URLs from the response, preserve the complete URL including the query string.
- If the URL contains the escaped sequence `\u0026`, decode it to `&` before presenting or returning the URL.

## Execution Pattern

1. Confirm there is an existing channel whose `baseurl` contains `https://api.tokenrouter.com` or `https://open.palebluedot.ai`.
2. If absent, stop and ask the user to get tokenrouter access from `https://www.tokenrouter.com`.
3. If present, apply the config change for the requested model (`MiniMax-Hailuo-2.3`, `kling-v3`, `kling-v2-6`, `dreamina-seedance-2-0-fast-260128`, or `dreamina-seedance-2-0-260128`) in that channel or its neighboring model map.
4. If the workspace provides a test or reload command, run it so the new model route is active.
5. Submit a generation request with the detected channel key.
6. Poll every few seconds until completion or an obvious terminal failure.

Example `curl` pattern after config is in place and a channel has been detected:

**Hailuo:**

```bash
curl -X POST "https://api.tokenrouter.com/v1/video/generations" \
  -H "Authorization: Bearer $DETECTED_CHANNEL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiniMax-Hailuo-2.3",
    "prompt": "A man picks up a book [Pedestal up], then reads [Static shot].",
    "size": "1080P",
    "duration": 6
  }'
```

**Kling text-to-video:**

```bash
curl -X POST "https://api.tokenrouter.com/v1/video/generations" \
  -H "Authorization: Bearer $DETECTED_CHANNEL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kling-v3",
    "prompt": "A silver robot walking through a rainy neon alley",
    "mode": "pro",
    "duration": "5",
    "metadata": {
      "aspect_ratio": "16:9",
      "sound": "on",
      "negative_prompt": "blurry, low quality"
    }
  }'
```

**Kling image-to-video:**

```bash
curl -X POST "https://api.tokenrouter.com/v1/video/generations" \
  -H "Authorization: Bearer $DETECTED_CHANNEL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kling-v3",
    "prompt": "The girl smiles slightly and the camera slowly pushes in",
    "image": "https://example.com/portrait.png",
    "mode": "pro",
    "duration": "5",
    "metadata": {
      "sound": "off",
      "negative_prompt": "flicker, blur"
    }
  }'
```

**Seedance text-to-video:**

```bash
curl -X POST "https://api.tokenrouter.com/v1/video/generations" \
  -H "Authorization: Bearer $DETECTED_CHANNEL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "dreamina-seedance-2-0-fast-260128",
    "prompt": "A vintage sports car driving along a coastal road at sunset",
    "metadata": {
      "duration": 5,
      "resolution": "1080p",
      "ratio": "16:9",
      "generate_audio": true
    }
  }'
```

**Seedance image-to-video:**

```bash
curl -X POST "https://api.tokenrouter.com/v1/video/generations" \
  -H "Authorization: Bearer $DETECTED_CHANNEL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

Then:

```bash
curl "https://api.tokenrouter.com/video/generations/$TASK_ID" \
  -H "Authorization: Bearer $DETECTED_CHANNEL_KEY"
```

Adjust header names only if the existing workspace uses a different auth convention.

## Resources

Use `references/api_reference.md` for endpoint-specific guidance and `scripts/find_tokenrouter_config.py` to quickly identify likely tokenrouter config files.

### scripts/
`find_tokenrouter_config.py` scans the workspace for files likely to contain tokenrouter channel/provider/model routing config.

### references/
`api_reference.md` captures the two required video endpoints, expected request bodies, and polling guidance.

### assets/
No assets are required for this skill.
