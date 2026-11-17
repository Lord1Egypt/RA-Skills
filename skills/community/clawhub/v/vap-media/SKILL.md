---
name: vap-media
description: VAP Media API skill for image, video, music, and media editing through VAP. Uses VAP product keys with current Media API endpoints.
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["curl"]}}}
---

# VAP Media API Skill

Generate images, video, and music through VAP Media API. Edit and enhance media with inpaint, AI edit, upscale, background removal, video trim, and video merge.

This skill is a Media API distribution surface for agent ecosystems such as ClawHub. Keep the agent workflow direct and useful: improve prompts, choose the matching VAP Media API endpoint, poll the task or operation, and return the final media URL.

## Product Boundary

Use this skill for VAP Media API work only:

- image generation
- video generation
- music generation
- media editing and enhancement

Do not route coding-model requests through this skill. Coding agents and IDE model workflows use the separate VAP Coding Plan API with model ID `vap-code`.

## Access

Use `VAP_API_KEY` as a Bearer token. This key is product-scoped to VAP Media API access.

If `VAP_API_KEY` is not set, ask the user to get a Media API key from Developer Hub:
https://vapagent.com/developer/?key=media#keys

View Room and Media plans:
https://vapagent.com/new-dashboard/?billing=monthly#plans

---

## Generation

Use `POST /api/v1/generations` for image, video, and music generation.

### Create Generation

```bash
curl -s -X POST https://api.vapagent.com/api/v1/generations \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"kind":"image","prompt":"PROMPT","params":{"aspect_ratio":"1:1"}}'
```

Returns a task id:

```json
{"generation_id":"UUID","task_id":"UUID","status":"pending","kind":"image"}
```

### Poll Generation

```bash
curl -s https://api.vapagent.com/api/v1/generations/GENERATION_ID \
  -H "Authorization: Bearer $VAP_API_KEY"
```

When complete, return the media URL from `result_url`, `image_url`, `video_url`, `audio_url`, or the primary URL inside `result`.

### Generation Types And Params

#### Image

```json
{
  "kind": "image",
  "prompt": "A clean product photo of a violet-white AI media emblem on a studio desk",
  "params": {
    "aspect_ratio": "1:1"
  }
}
```

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| `aspect_ratio` | enum | `1:1` | `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `21:9`, `9:21` |
| `width` | int | optional | Target width when supported |
| `height` | int | optional | Target height when supported |
| `negative_prompt` | string | optional | What to avoid |
| `output_format` | string | optional | Requested output format when supported |
| `quantity` | int | optional | Number of images when supported |

#### Video

```json
{
  "kind": "video",
  "prompt": "Drone shot over misty mountains at sunrise",
  "params": {
    "duration": 8,
    "aspect_ratio": "9:16",
    "resolution": "1080p"
  }
}
```

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| `duration` | int | `8` | `4`, `6`, or `8` seconds |
| `aspect_ratio` | enum | `16:9` | `16:9` landscape or `9:16` portrait |
| `generate_audio` | bool | `true` | Include audio track |
| `resolution` | enum | `720p` | `720p` or `1080p` |
| `negative_prompt` | string | optional | What to avoid |
| `source_image` | string | optional | Input image URL for image-to-video when supported |

#### Music

```json
{
  "kind": "music",
  "prompt": "Upbeat lo-fi hip hop beat, warm vinyl crackle, chill atmosphere",
  "params": {
    "duration": 120,
    "instrumental": true,
    "audio_format": "mp3"
  }
}
```

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| `duration` | int | `120` | 30-480 seconds |
| `instrumental` | bool | `false` | No vocals |
| `audio_format` | enum | `mp3` | `mp3` or `wav` |
| `loudness_preset` | enum | `streaming` | `streaming`, `apple`, or `broadcast` |
| `style` | string | optional | Genre/style |
| `title` | string | optional | Song title |
| `custom_mode` | bool | `false` | Enable custom lyrics and style mode |

---

## Operations

Use `POST /api/v1/operations` for edit and enhancement operations.

### Create Operation

```bash
curl -s -X POST https://api.vapagent.com/api/v1/operations \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"operation":"background_remove","media_url":"https://example.com/photo.png"}'
```

### Poll Operation

```bash
curl -s https://api.vapagent.com/api/v1/operations/OPERATION_ID \
  -H "Authorization: Bearer $VAP_API_KEY"
```

When complete, return the media URL from `result_url`, `image_url`, `video_url`, or the primary URL inside `result`.

### Available Operations

| Operation | Required Params | Description |
| --- | --- | --- |
| `inpaint` | `media_url`, `prompt` | AI editing with optional `mask_url` |
| `ai_edit` | `media_url`, `prompt` | AI-powered image editing with optional `additional_images` |
| `background_remove` | `media_url` | Remove background |
| `upscale` | `media_url` | Enhance resolution with `options.scale`: 2 or 4 |
| `video_trim` | `media_url`, `options.start_time`, `options.end_time` | Trim video |
| `video_merge` | `media_urls` array, min 2 | Merge video clips |

---

## Agent Instructions

When a user asks to create, generate, or make an image, video, or music:

1. Improve the prompt with useful style, lighting, composition, mood, or production details.
2. Require `VAP_API_KEY`; if it is missing, send the user to Developer Hub for a Media API key.
3. Submit `POST /api/v1/generations` with top-level `kind`, top-level `prompt`, and optional `params`.
4. Set aspect ratio based on the content need:
   - portrait/social -> `9:16`
   - YouTube/web/widescreen -> `16:9`
   - square feed asset -> `1:1`
5. Poll `GET /api/v1/generations/{id}` until completed or failed.
6. Return the final media URL to the user with concise status.

When a user asks to edit, enhance, or modify an existing image or video:

1. Identify the operation: `inpaint`, `ai_edit`, `upscale`, `background_remove`, `video_trim`, or `video_merge`.
2. Get the media URL from a previous generation or user-provided URL.
3. Submit `POST /api/v1/operations`.
4. Poll `GET /api/v1/operations/{id}` until completed or failed.
5. Return the output URL.

Do not expose internal provider details as the product identity. The visible product is VAP Media API.

---

## Examples

### Image

```bash
curl -s -X POST https://api.vapagent.com/api/v1/generations \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"kind":"image","prompt":"A fluffy orange tabby cat on a sunlit windowsill, soft bokeh, golden hour light, photorealistic","params":{"aspect_ratio":"16:9"}}'

curl -s https://api.vapagent.com/api/v1/generations/GENERATION_ID \
  -H "Authorization: Bearer $VAP_API_KEY"
```

### Video

```bash
curl -s -X POST https://api.vapagent.com/api/v1/generations \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"kind":"video","prompt":"Drone shot over misty mountains at sunrise","params":{"duration":8,"aspect_ratio":"9:16","resolution":"1080p"}}'
```

### Music

```bash
curl -s -X POST https://api.vapagent.com/api/v1/generations \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"kind":"music","prompt":"Upbeat lo-fi hip hop beat, warm vinyl crackle, chill vibes","params":{"duration":120,"instrumental":true,"audio_format":"wav","loudness_preset":"streaming"}}'
```

### AI Edit

```bash
curl -s -X POST https://api.vapagent.com/api/v1/operations \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"operation":"ai_edit","media_url":"https://example.com/photo.jpg","prompt":"Change the background to a sunset beach"}'
```

### Upscale

```bash
curl -s -X POST https://api.vapagent.com/api/v1/operations \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"operation":"upscale","media_url":"https://example.com/photo.jpg","options":{"scale":4}}'
```

### Background Remove

```bash
curl -s -X POST https://api.vapagent.com/api/v1/operations \
  -H "Authorization: Bearer $VAP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"operation":"background_remove","media_url":"https://example.com/photo.jpg"}'
```

## Prompt Tips

- Style: "oil painting", "3D render", "watercolor", "photograph", "flat illustration"
- Lighting: "golden hour", "neon lights", "soft diffused light", "dramatic shadows"
- Composition: "close-up", "aerial view", "wide angle", "rule of thirds"
- Mood: "serene", "energetic", "mysterious", "premium", "playful"
- Aspect ratio: mention "widescreen", "portrait", or "16:9" when relevant.

## Setup

1. Get a Media API key: https://vapagent.com/developer/?key=media#keys
2. View Room and Media plans if access is needed: https://vapagent.com/new-dashboard/?billing=monthly#plans
3. Set: `export VAP_API_KEY=vap_xxxxxxxxxxxxxxxxxxxx`

## Links

- Developer Hub: https://vapagent.com/developer/
- Media API key: https://vapagent.com/developer/?key=media#keys
- Room and Media plans: https://vapagent.com/new-dashboard/?billing=monthly#plans
- VAP AI: https://vapagent.com/
- GitHub: https://github.com/vapagentmedia/vap-media-skill
