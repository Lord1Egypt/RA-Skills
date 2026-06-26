# Video Models

| Model ID | Description |
|----------|-------------|
| `mm/t2v` | Default text-to-video |
| `mm/i2v` | Default image-to-video |
| `vertex/veo-3.1-fast-generate-preview` | Google Veo 3.1 |

```bash
run.mjs --model mm/t2v --prompt "A cat playing" --output video.mp4
run.mjs --model mm/i2v --prompt "Zoom in slowly" --image "https://example.com/photo.jpg" --output video.mp4
```
