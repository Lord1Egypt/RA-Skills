# Veevid API Reference — Complete Parameters

## Endpoint

```
POST https://veevid.ai/api/generate-video
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

## Veo 3.1 (`mode: "veo3"`)

**Duration is NOT configurable. Fixed at 8 seconds.**

| Parameter | Allowed Values | Notes |
|-----------|---------------|-------|
| `prompt` | string | Scene description |
| `video_quality` | `"standard"` (20 cr) or `"pro"` (140 cr) | Any non-`standard` value maps to the quality tier, but external callers should send `"pro"` explicitly |
| `aspect_ratio` | `"16:9"`, `"9:16"` | |
| `generation_type` | `"text-to-video"`, `"image-to-video"`, `"reference-to-video"` | |
| `image` | URL | For I2V. Single image |
| `images` | URL[] | For R2V. 1-3 reference images |
| `watermark` | string (max 200) | Custom watermark text |
| `remove_watermark` | boolean | Remove watermark |

**External callers should omit `duration`. Veo 3.1 output is fixed at 8s. If passed, only `"4"`, `"6"`, `"8"` are accepted; other values return 400.**

## Kling 3.0 (`mode: "kling-3"`)

| Parameter | Allowed Values | Default | Notes |
|-----------|---------------|---------|-------|
| `prompt` | string | — | |
| `duration` | `"3"` to `"15"` (any integer) | `"5"` | 3-15 seconds |
| `aspect_ratio` | `"16:9"`, `"9:16"`, `"1:1"` | `"16:9"` | T2V only; I2V ignores this |
| `generation_type` | `"text-to-video"`, `"image-to-video"` | | |
| `image` | URL | — | Required for I2V |
| `images` | URL[] | — | `images[0]`=start, `images[1]`=end frame |
| `model_version` | `"kling-3-standard"`, `"kling-3-pro"` | `"kling-3-standard"` | Pro = higher quality |
| `generate_audio` | boolean | `true` | Enable sound generation |
| `cfg_scale` | number | `0.5` | Prompt adherence strength |
| `negative_prompt` | string | — | What to avoid |
| `shot_type` | `"single"`, `"multi"`, `"customize"`, `"intelligent"` | `"customize"` | Camera shot mode |
| `multi_prompt` | `[{prompt, duration}]` | — | For multi-shot sequences |

## LTX 2.3 (`mode: "ltx-2-3"`)

| Parameter | Allowed Values | Default | Notes |
|-----------|---------------|---------|-------|
| `prompt` | string | — | |
| `duration` | Pro: `"6"`, `"8"`, `"10"`. Fast: `"6"`, `"8"`, `"10"`, `"12"`, `"14"`, `"16"`, `"18"`, `"20"` | `"6"` | External callers must use one of these exact values |
| `video_quality` | `"1080p"`, `"1440p"`, `"2160p"` | `"1080p"` | Fast >10s forces 1080p |
| `aspect_ratio` | `"16:9"`, `"9:16"`, `"auto"` | `"auto"` | |
| `model_version` | `"ltx-2.3"` (Pro), `"ltx-2.3-fast"` (Fast) | `"ltx-2.3"` | |
| `target_fps` | `24`, `25`, `48`, `50` | `24` | Frame rate (integer, not string) |
| `generate_audio` | boolean | `true` | Audio generation |
| `generation_type` | `"text-to-video"`, `"image-to-video"` | | |
| `image` | URL | — | Required for I2V |

## Sora 2 Stable (`mode: "sora2-stable"`)

| Parameter | Allowed Values | Default | Notes |
|-----------|---------------|---------|-------|
| `prompt` | string | — | |
| `duration` | `"4"`, `"8"`, `"12"`, `"16"`, `"20"` | `"4"` | Must be exact; invalid values return 400 |
| `video_quality` | `"standard"` (720p), `"hd"` (1080p) | `"standard"` | HD = Pro only |
| `aspect_ratio` | `"16:9"`, `"9:16"` | `"16:9"` | |
| `model_version` | `"sora-2"`, `"sora-2-pro"` | `"sora-2"` | |
| `generation_type` | `"text-to-video"`, `"image-to-video"` | | |
| `image` | URL | — | Required for I2V |

## Sora 2 (`mode: "sora2"`)

| Parameter | Allowed Values | Default | Notes |
|-----------|---------------|---------|-------|
| `prompt` | string | — | |
| `duration` | `"10"`, `"15"`, `"25"` | `"10"` | |
| `video_quality` | `"standard"`, `"hd"` | `"standard"` | |
| `aspect_ratio` | `"16:9"`, `"9:16"` | `"16:9"` | |
| `model_version` | `"sora-2"`, `"sora-2-pro"`, `"sora-2-pro-storyboard"` | | |
| `scenes` | `[{description, duration}]` | — | Storyboard mode only |
| `remove_watermark` | boolean | `false` | Remove Sora watermark (affects credit cost) |

## Wan 2.6 (`mode: "wan-2-6"`)

| Parameter | Allowed Values | Default | Notes |
|-----------|---------------|---------|-------|
| `prompt` | string | — | |
| `duration` | `"5"`, `"10"`, `"15"` | `"5"` | |
| `video_quality` | `"720p"`, `"1080p"` | `"720p"` | |
| `aspect_ratio` | `"16:9"`, `"9:16"`, `"1:1"`, `"4:3"`, `"3:4"`, `"landscape"`, `"portrait"` | `"16:9"` | |
| `generation_type` | `"text-to-video"`, `"image-to-video"`, `"video-to-video"` | | V2V also supported |
| `image` | URL | — | Required for I2V |
| `negative_prompt` | string | — | What to avoid |
| `shot_type` | `"single"`, `"multi"` | `"single"` | Shot mode |
| `enable_prompt_expansion` | boolean | `true` | AI prompt enhancement |
| `seed` | integer | `-1` | Reproducibility (-1=random) |

## Grok Imagine (`mode: "grok-imagine"`)

| Parameter | Allowed Values | Default | Notes |
|-----------|---------------|---------|-------|
| `prompt` | string | — | |
| `duration` | `"6"`, `"10"`, `"15"` | `"6"` | ⚠️ NOT 3 or 5 |
| `video_quality` | `"480p"`, `"720p"` | `"720p"` | |
| `aspect_ratio` | `"16:9"`, `"9:16"`, `"1:1"`, `"2:3"`, `"3:2"` | `"1:1"` | |
| `grokMode` | `"fun"`, `"normal"`, `"spicy"` | `"normal"` | |
| `generation_type` | `"text-to-video"`, `"image-to-video"` | | |
| `image` | URL | — | Required for I2V, passed as `image_urls` |

## Seedance 1.5 Pro (`mode: "seedance-1.5-pro"`)

| Parameter | Allowed Values | Default | Notes |
|-----------|---------------|---------|-------|
| `prompt` | string | — | |
| `duration` | 4-12 (integer) | `"5"` | External callers outside this range get `400`; no auto-clamping |
| `video_quality` | `"480p"`, `"720p"`, `"1080p"` | `"720p"` | |
| `aspect_ratio` | `"auto"`, `"16:9"`, `"9:16"`, `"1:1"`, `"4:3"`, `"3:4"`, `"21:9"` | `"auto"` | |
| `generate_audio` | boolean | `false` | |
| `camera_fixed` | boolean | `false` | |
| `seed` | integer | — | |
| `generation_type` | `"text-to-video"`, `"image-to-video"` | | |
| `image` | URL | — | Passed as `start_image` |

## Veevid 1.0 Pro (`mode: "veevid-1.0-pro"`)

Same as Seedance 1.5 Pro.

## Kling 2.6 (`mode: "kling-2-6"`)

| Parameter | Allowed Values | Default | Notes |
|-----------|---------------|---------|-------|
| `prompt` | string | — | |
| `duration` | `"5"`, `"10"` | `"5"` | |
| `video_quality` | `"720p"`, `"1080p"` | `"720p"` | |
| `aspect_ratio` | `"16:9"`, `"9:16"`, `"1:1"` | `"16:9"` | |
| `generation_type` | `"text-to-video"`, `"image-to-video"` | | |
| `image` | URL | — | Passed as `start_image` |

---

## Other Endpoints

### Quote (pre-flight cost estimate)

Call this **before** generating to get the exact credit cost.

```
POST https://veevid.ai/api/quote
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

Request body: billing-relevant fields only — `mode`, `generation_type`,
`duration`, `video_quality`, `aspect_ratio`, `model_version`, and
model-specific options (`generate_audio`, `remove_watermark`, `grokMode`,
`scale`, `target_fps`, etc.). **Do not pass** `prompt`, `image`, or video
URLs — they are ignored and not required.

Response:
```json
{
  "required_credits": 48,
  "current_balance": 311,
  "sufficient": true
}
```

### Status Check
```
GET https://veevid.ai/api/video-generation/{generation_id}/status
Authorization: Bearer <API_KEY>
```

Response shape (processing):
```json
{
  "id": "vg_xxx",
  "status": "processing",
  "video_url": null,
  "error_message": null,
  "credits_used": 20,
  "created_at": "2026-03-19T12:34:56.000Z"
}
```

Response shape (completed — additional fields):
```json
{
  "id": "vg_xxx",
  "status": "completed",
  "video_url": "https://cdn.veevid.ai/videos/xxx.mp4",
  "error_message": null,
  "credits_used": 20,
  "created_at": "2026-03-19T12:34:56.000Z",
  "completed_at": "2026-03-19T12:35:12.000Z",
  "provider_task_id": "task_xxx",
  "video_quality": "720p",
  "video_metadata": {
    "content_type": "video/mp4",
    "file_name": "xxx.mp4",
    "file_size": 1234567
  }
}
```

### Credit Balance
```
GET https://veevid.ai/api/credits
Authorization: Bearer <API_KEY>
```

### Image Upload
```
POST https://veevid.ai/api/storage/upload
Authorization: Bearer <API_KEY>
Content-Type: multipart/form-data
file: <binary>
```

Response:
```json
{
  "url": "https://cdn.veevid.ai/uploads/xxx.jpg",
  "key": "uploads/xxx.jpg"
}
```

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Invalid parameter (check error message for details) |
| 401 | Invalid or expired API Key |
| 402 | Insufficient credits (response includes `required` and `balance`) |
| 403 | Account suspended / forbidden |
| 404 | Generation record not found |
| 500 | Server error (retry) |

_Last updated: 2026-03-20._
