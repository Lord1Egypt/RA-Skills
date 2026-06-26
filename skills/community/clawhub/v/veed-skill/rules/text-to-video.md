---
name: text-to-video
description: Generate a talking video from a photo and written script using VEED Fabric 1.0 text endpoint with AI voice
metadata:
  tags: text-to-speech, tts, voice, script, text, video
---

# Image + Text to Video

Turns a photo of a face into a talking video where an AI-generated voice speaks the provided script. The face lip-syncs to the generated speech.

## Required inputs

1. **Image** — a photo with a clearly visible face
2. **Text** — the script to be spoken (1–2000 characters)

## Supported image formats

JPG, JPEG, PNG, WebP, GIF, AVIF

**MUST** validate the image file extension before uploading.

## Text limits

The Fabric `/text` endpoint has a hard limit of **2000 characters**.

**MUST** check the character count before submitting. If the script exceeds 2000 characters, reject it immediately with:

> Your script is {length} characters ({length - 2000} over the 2000-character limit, roughly 30–45 seconds of speech). Please shorten it or split into multiple videos.

**MUST NOT** truncate or silently modify the user's script. **MUST NOT** attempt to send text over 2000 characters to the API.

## Voice presets

Ask the user to pick a voice style. Offer these presets plus custom free-text:

| Preset | `voice_description` value |
|---|---|
| Professional | `Clear, confident, professional business tone` |
| Casual | `Warm, friendly, conversational tone` |
| Energetic | `Upbeat, enthusiastic, high-energy tone` |
| Custom | User's own description passed directly |

If the user doesn't specify, default to **Professional**.

## Options

**Resolution** (default: `480p`):
- `480p` — $0.08/sec (standard), $0.10/sec (fast)
- `720p` — $0.15/sec (standard), $0.20/sec (fast)

**Speed** (default: standard):
- Standard — uses `https://queue.fal.run/veed/fabric-1.0/text`
- Fast — uses `https://queue.fal.run/veed/fabric-1.0/text/fast`

## API request

The `image_url` **MUST** be a publicly accessible URL. If the user provides a local file path, upload it first — see [./file-upload.md](./file-upload.md).

```bash
RESPONSE=$(curl -s -X POST "https://queue.fal.run/veed/fabric-1.0/text" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/headshot.jpg",
    "text": "Hi, I'\''m the founder of Acme. Let me tell you about our new product.",
    "resolution": "480p",
    "voice_description": "Clear, confident, professional business tone"
  }')
```

For fast mode, change the endpoint to `https://queue.fal.run/veed/fabric-1.0/text/fast`.

The response contains `request_id`, `status_url`, and `response_url`. Proceed to [./queue.md](./queue.md) for polling and retrieval.

## Full workflow

1. Gather image and script text from the user
2. Validate image format and text length (1–2000 chars)
3. Upload local image if needed ([file-upload.md](./file-upload.md))
4. Ask about voice style (show presets)
5. Ask about resolution and speed (show pricing)
6. Submit to queue (this file)
7. Poll for status ([queue.md](./queue.md))
8. Download result ([output.md](./output.md))
