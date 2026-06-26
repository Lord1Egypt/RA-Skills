# Image Models

## Generation

| Model ID | Description |
|----------|-------------|
| `mm/img` | Default image generation |
| `vertex/gemini-2.5-flash-image-preview` | Gemini 2.5 Flash Image (preferred) |
| `vertex/gemini-3-pro-image-preview` | Gemini 3 Pro Image |
| `replicate/black-forest-labs/flux-schnell` | FLUX Schnell — fast |
| `replicate/black-forest-labs/flux-dev` | FLUX Dev — high quality |

## Processing

| Model ID | Description |
|----------|-------------|
| `fal/upscale` | Creative upscaler (2x or 4x) |
| `fal/img2img` | Image-to-image transformation (FLUX dev) |
| `replicate/lucataco/remove-bg` | Background removal |
| `replicate/851-labs/background-remover` | Background removal v2 |

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "mm/img", "inputs": {"prompt": "A sunset over mountains"}}'
```
