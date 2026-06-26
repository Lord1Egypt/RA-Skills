# Video Models

| Model ID | Description |
|----------|-------------|
| `mm/t2v` | Default text-to-video |
| `mm/i2v` | Default image-to-video |
| `vertex/veo-3.1-fast-generate-preview` | Google Veo 3.1 |

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "mm/t2v", "inputs": {"prompt": "A cat playing with yarn"}}'
```
