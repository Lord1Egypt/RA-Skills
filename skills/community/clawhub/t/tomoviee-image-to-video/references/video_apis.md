# Tomoviee Image-to-Video API Reference

## Provenance and Endpoint Mapping

- Vendor portals: `https://www.tomoviee.ai` and `https://www.tomoviee.cn`
- Runtime gateway host used by this skill package: `https://openapi.wondershare.cc`
- Compatible gateway alias: `https://open-api.wondershare.cc`
- Primary capability in this skill: `tm_img2video_b`

All runtime requests from this skill target only:

1. `https://openapi.wondershare.cc/v1/open/capacity/application/tm_img2video_b`
2. `https://openapi.wondershare.cc/v1/open/pub/task`

## Image-to-Video (tm_img2video_b)

Generate a 5-second video from a still image and prompt.

### Parameters

- `prompt` (required): motion guidance text
- `image` (required): source image URL
- `resolution` (optional): `720p` or `1080p`, default `720p`
- `duration` (optional): only `5` supported
- `aspect_ratio` (optional): `16:9`, `9:16`, `4:3`, `3:4`, `1:1`, `original`
- `camera_move_index` (optional): camera movement index `1-46`
- `callback` (optional): callback URL
- `params` (optional): transparent callback passthrough

### Input Constraints

- Maximum file size: `<200M`
- Formats: `JPG`, `JPEG`, `PNG`, `WEBP`

### Result Endpoint

`https://openapi.wondershare.cc/v1/open/pub/task`

### Status Codes

- `1` queued
- `2` processing
- `3` success
- `4` failed
- `5` cancelled
- `6` timeout

## Credential and Dependency Notes

- Sensitive credentials required: `app_key`, `app_secret`
- Auth pattern: `Authorization: Basic <base64(app_key:app_secret)>`
- Runtime dependency: `requests>=2.31.0,<3.0.0`

### Example

```python
from scripts.tomoviee_img2video_client import TomovieeImg2VideoClient

client = TomovieeImg2VideoClient("app_key", "app_secret")
task_id = client.image_to_video(
    prompt="Camera slowly pushes in with natural movement",
    image="https://example.com/image.jpg",
    resolution="720p",
    duration=5,
    aspect_ratio="original",
)
result = client.poll_until_complete(task_id)
```