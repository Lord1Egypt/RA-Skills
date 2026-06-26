# Tomoviee Image APIs (Redrawing Focus)

## Provenance and Endpoint Mapping

- Vendor portals: `https://www.tomoviee.ai` and `https://www.tomoviee.cn`
- Gateway host used by SDK/client scripts: `https://openapi.wondershare.cc`
- This skill's primary capacity: `tm_redrawing`

All runnable scripts in this skill package call only:

1. `https://openapi.wondershare.cc/v1/open/capacity/application/tm_redrawing`
2. `https://openapi.wondershare.cc/v1/open/pub/task`

## Image Redrawing (tm_redrawing)

Use image redrawing with optional mask control.

### Endpoint

`https://openapi.wondershare.cc/v1/open/capacity/application/tm_redrawing`

### Required Parameters

- `prompt`: positive prompt text
- `init_image`: source image URL
  - supported format: `jpg/png`
  - width and height: `>512` and `<2048`
  - aspect ratio: `<3`

### Optional Parameters

- `mask_url`: mask image URL
  - should have same resolution as `init_image`
  - supported format: `jpg/png`
  - width and height: `>512` and `<2048`
  - aspect ratio: `<3`
- `callback`: callback URL
- `params`: passthrough params

### Result Polling Endpoint

`https://openapi.wondershare.cc/v1/open/pub/task`

### Status Codes

- `1` queued
- `2` processing
- `3` success
- `4` failed
- `5` cancelled
- `6` timeout

### Example

```python
from scripts.tomoviee_redrawing_client import TomovieeRedrawingClient

client = TomovieeRedrawingClient("app_key", "app_secret")
task_id = client.image_redrawing(
    prompt="Clear blue sky with fluffy clouds",
    init_image="https://example.com/input.png",
    mask_url="https://example.com/mask.png",
)
result = client.poll_until_complete(task_id)
```
