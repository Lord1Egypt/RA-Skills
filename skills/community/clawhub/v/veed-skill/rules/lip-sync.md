---
name: lip-sync
description: Generate a talking video from a photo and audio file using VEED Fabric 1.0 lip-sync endpoint
metadata:
  tags: lip-sync, audio, video, face, animation
---

# Image + Audio Lip-Sync

Turns a photo of a face into a talking video that moves its lips in sync with an audio file.

## Required inputs

1. **Image** — a photo with a clearly visible face (headshot, selfie, AI-generated portrait)
2. **Audio** — a voiceover, narration, or any speech audio

## Supported formats

- **Image**: JPG, JPEG, PNG, WebP, GIF, AVIF
- **Audio**: MP3, OGG, WAV, M4A, AAC

**MUST** validate file extensions before uploading. **MUST NOT** attempt to send unsupported formats to the API.

## Options

**Resolution** (default: `480p`):
- `480p` — $0.08/sec (standard), $0.10/sec (fast)
- `720p` — $0.15/sec (standard), $0.20/sec (fast)

Default to `480p` unless the user explicitly asks for higher quality.

**Speed** (default: standard):
- Standard — uses `https://queue.fal.run/veed/fabric-1.0`
- Fast — uses `https://queue.fal.run/veed/fabric-1.0/fast` (~25% more expensive, faster generation)

## API request

Both `image_url` and `audio_url` **MUST** be publicly accessible URLs. If the user provides local file paths, upload them first — see [./file-upload.md](./file-upload.md).

```bash
RESPONSE=$(curl -s -X POST "https://queue.fal.run/veed/fabric-1.0" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/headshot.jpg",
    "audio_url": "https://example.com/voiceover.mp3",
    "resolution": "480p"
  }')
```

For fast mode, change the endpoint to `https://queue.fal.run/veed/fabric-1.0/fast`.

The response contains `request_id`, `status_url`, and `response_url`. Proceed to [./queue.md](./queue.md) for polling and retrieval.

## Full workflow

1. Gather image and audio from the user
2. Validate file formats against supported list
3. Upload local files if needed ([file-upload.md](./file-upload.md))
4. Ask about resolution and speed (show pricing)
5. Submit to queue (this file)
6. Poll for status ([queue.md](./queue.md))
7. Download result ([output.md](./output.md))
