# Tomoviee Image-to-Image API Reference

## Provenance and Endpoint Mapping

- Vendor portals: `https://www.tomoviee.ai` and `https://www.tomoviee.cn`
- Runtime gateway host used by this skill: `https://openapi.wondershare.cc`
- Primary capability: `tm_reference_img2img`

All runtime API calls in this skill target only:

1. `https://openapi.wondershare.cc/v1/open/capacity/application/tm_reference_img2img`
2. `https://openapi.wondershare.cc/v1/open/pub/task`

## Text Parameters

- `prompt` (required): Prompt text (preserve + modify instructions)

## Control Parameters

- `control_type` (required): `"0"`, `"1"`, `"2"`, `"3"`
- `control_intensity` (required): `0-1`

## Image Parameters

- `reference_image` (required): reference image URL
- `init_image` (optional): backend-required when `control_type="2"`

## Output Parameters

- `width` (required): `512-2048`
- `height` (required): `512-2048`
- `batch_size` (required): `1-4`

## Optional Callback Parameters

- `callback` (optional): callback URL
- `params` (optional): transparent callback passthrough

## Result Endpoint

`https://openapi.wondershare.cc/v1/open/pub/task`

## Status Codes

- `1` queued
- `2` processing
- `3` success
- `4` failed
- `5` cancelled
- `6` timeout

## Example

```python
from scripts.tomoviee_img2img_client import TomovieeImg2ImgClient

client = TomovieeImg2ImgClient("app_key", "app_secret")
task_id = client.image_to_image(
    prompt="Keep identity and composition, change background to modern office",
    reference_image="https://example.com/reference.jpg",
    control_type="2",
    init_image="https://example.com/reference.jpg",
    width=1024,
    height=1024,
    batch_size=1,
    control_intensity=0.5,
)
result = client.poll_until_complete(task_id)
```