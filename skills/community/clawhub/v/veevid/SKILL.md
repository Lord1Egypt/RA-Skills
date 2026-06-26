---
name: veevid
description: "AI video generator — text to video, image to video, and reference-to-video via Veevid API. Supports Kling 3.0, Sora 2, Veo 3.1, LTX 2.3, Seedance, Wan 2.6, and more. Use when: user asks to generate a video from text, turn an image into a video, create AI-generated video content, or compare AI video models."
keywords:
  - ai video generator
  - text to video
  - image to video
  - video generation
  - text-to-video
  - image-to-video
  - ai video
  - generate video
  - kling
  - sora
  - veo
  - veevid
metadata:
  clawdis:
    config:
      stateDirs:
        - "~/.config/veevid"
      requiredEnv: []
    requires:
      env: []
      config:
        - path: "~/.config/veevid/api_key"
          description: "Veevid API key for authentication (get one at veevid.ai/settings/api-keys)"
---

# Veevid — AI Video Generator

All-in-one AI video generator: **text to video**, **image to video**, and **reference-to-video** via [Veevid AI](https://veevid.ai). One API, 10+ state-of-the-art video generation models including Kling 3.0, Sora 2, Veo 3.1, LTX 2.3, Seedance 1.5 Pro, and Wan 2.6.

## Setup

1. **Get your API Key** at [veevid.ai/settings/api-keys](https://veevid.ai/settings/api-keys)
2. **Save the key** locally:

```bash
mkdir -p ~/.config/veevid
echo "YOUR_API_KEY" > ~/.config/veevid/api_key
```

## What You Can Say

These phrases trigger this skill:

- "Generate a video of a sunset over the ocean"
- "Turn this image into a video"
- "Make a 10-second product ad with Kling 3.0"
- "Create a vertical video for TikTok"
- "How much does it cost to generate a video?"
- "What AI video models are available?"
- "Check my credit balance"

## Image Retrieval from Chat (Discord / Group Chats)

When the user requests **image-to-video** but no image URL is provided in the message:

1. Use `message read` (channel=discord, limit=10) to scan recent messages in the current channel.
2. Filter attachments by the **sender's user id** to avoid picking up someone else's image.
3. Collect **all recent image attachments** (content_type starts with `image/`) from the sender, ordered newest first.
4. **Preview by quoting**: Use `message send` with `replyTo` set to the **message id** of the image message. This quotes the original message with its image preview inline, so the user can visually confirm. Add text like "Is this the right image?" Don't just show the filename — filenames like `IMG_20260203_xyz.jpg` are meaningless.
5. **Single image needed** (standard I2V): quote the most recent image message and ask the user to confirm.
6. **Multiple images needed** (Kling 3.0 start+end frames, Veo 3.1 reference-to-video with 1-3 refs): quote each image message with a number label and ask the user which ones to use and in what order.
6. If not enough images are found, ask the user to send the missing ones or provide URLs.

This ensures image-to-video works seamlessly even when Discord doesn't forward attachments directly to the agent. Applies to **all models**, not just a specific one.

## Important: Always Confirm Before Generating

**Before calling the generate API, ALWAYS:**

1. Call `POST /api/quote` with the billing-relevant params for your planned generation (see Step 1 below) — it returns the precise credit cost and current balance.
2. Tell the user which model you'll use and the exact cost from the quote response.
3. For image-to-video: also confirm the image is correct (show filename/URL).
4. Wait for the user to confirm before proceeding.

If the generate API returns `402`, report the exact `required` and `balance` values from the response body to the user.

If balance is insufficient, suggest a cheaper model or link to [veevid.ai/pricing](https://veevid.ai/pricing).

## Step 1 — Quote (get exact cost before generating)

`/api/quote` only needs the **billing-relevant** params: `mode`, `generation_type`, `duration`, `video_quality`, `aspect_ratio`, and model-specific options (e.g. `model_version`, `generate_audio`). It does **not** require `prompt`, `image`, or other content fields — those don't affect credit cost.

```bash
curl -X POST https://veevid.ai/api/quote \
  -H "Authorization: Bearer $(cat ~/.config/veevid/api_key)" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "veo3",
    "generation_type": "text-to-video",
    "video_quality": "standard"
  }'
```

Returns: `{"required_credits": 20, "current_balance": 451, "sufficient": true}`

If `sufficient` is `false`, suggest a cheaper model before asking the user to confirm.

## Step 2 — Generate Video (Text to Video)

```bash
curl -X POST https://veevid.ai/api/generate-video \
  -H "Authorization: Bearer $(cat ~/.config/veevid/api_key)" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A golden retriever running through sunflowers, cinematic lighting",
    "mode": "veo3",
    "aspect_ratio": "16:9",
    "video_quality": "standard"
  }'
```

Returns either:

- Async case: `{"generation_id": "vg_xxx", "status": "processing", "video_url": null, "image_url": null}`
- Sync case: `{"generation_id": "vg_xxx", "status": "completed", "video_url": "https://..."}`

If `status` is already `completed` and a `video_url` is present, return it to the user immediately instead of polling.

## Generate Video — Image to Video

If the user provides an **online image URL**, pass it directly:

```bash
curl -X POST https://veevid.ai/api/generate-video \
  -H "Authorization: Bearer $(cat ~/.config/veevid/api_key)" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Gently animate this scene with camera movement",
    "mode": "veo3",
    "aspect_ratio": "16:9",
    "video_quality": "standard",
    "image": "https://example.com/photo.jpg",
    "generation_type": "image-to-video"
  }'
```

If the user provides a **local file**, the image URL isn't known yet — but credit cost doesn't depend on it, so quote first with billing params, then upload:

```bash
# Step 1: Quote (image URL not needed for pricing)
curl -X POST https://veevid.ai/api/quote \
  -H "Authorization: Bearer $(cat ~/.config/veevid/api_key)" \
  -H "Content-Type: application/json" \
  -d '{"mode": "veo3", "generation_type": "image-to-video", "video_quality": "standard"}'

# Step 2: Upload (only after user confirms)
curl -X POST https://veevid.ai/api/storage/upload \
  -H "Authorization: Bearer $(cat ~/.config/veevid/api_key)" \
  -F "file=@/path/to/image.jpg"

# Returns: {"url": "https://cdn.veevid.ai/uploads/xxx.jpg", "key": "uploads/xxx.jpg"}

# Step 3: Generate with uploaded URL
curl -X POST https://veevid.ai/api/generate-video \
  -H "Authorization: Bearer $(cat ~/.config/veevid/api_key)" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Animate this scene",
    "mode": "veo3",
    "video_quality": "standard",
    "image": "https://cdn.veevid.ai/uploads/xxx.jpg",
    "generation_type": "image-to-video"
  }'
```

## Step 3 — Poll Status

If the generate response is still `processing`, poll until `status` is `completed`:

```bash
curl -H "Authorization: Bearer $(cat ~/.config/veevid/api_key)" \
  https://veevid.ai/api/video-generation/{generation_id}/status
```

Status values: `processing` → `completed` or `failed`. Typical time: 60-180 seconds.

## Check Credit Balance

```bash
curl -H "Authorization: Bearer $(cat ~/.config/veevid/api_key)" \
  https://veevid.ai/api/credits
```

Returns: `{"success": true, "credits": 451, "balance": 451}`

## Available Models

Choose model based on the user's needs. Credit ranges depend on duration, resolution, and quality — use `/api/quote` for the exact cost before confirming with the user.

| Model | `mode` | Strengths | Credit Range |
|-------|--------|-----------|-------------|
| Veo 3.1 | `veo3` | Native audio, budget-friendly, fixed 8s | 20 / 140 credits |
| Grok Imagine | `grok-imagine` | Native audio, fastest generation | 10–60 credits |
| Veevid 1.0 Pro | `veevid-1.0-pro` | Audio, wide aspect ratios | 12–288 credits |
| Seedance 1.5 Pro | `seedance-1.5-pro` | Audio, wide aspect ratios | 12–288 credits |
| Kling 3.0 | `kling-3` | Audio, multi-shot, 3-15s | 48–495 credits |
| LTX 2.3 | `ltx-2-3` | Audio, open-source, up to 4K (2160p) | 48–960 credits |
| Kling 2.6 | `kling-2-6` | Audio, cinematic, multi-shot | 70–280 credits |
| Sora 2 Stable | `sora2-stable` | Native audio, best prompt accuracy, 4-20s | 80–2000 credits |
| Sora 2 | `sora2` | Native audio, 10-25s, storyboard/multi-scene | 20–315 credits |
| Wan 2.6 | `wan-2-6` | Audio, multi-shot, video-to-video | 100–450 credits |

## Quick Model Picker

| User wants... | Use this |
|---------------|----------|
| Cheapest option | `grok-imagine` (10 cr at 480p/6s) or `veo3` standard (20 cr) |
| Fastest result | `grok-imagine` or `ltx-2-3` fast |
| Best quality | `sora2-stable` pro or `kling-3` |
| Longer clips (>15s) | `sora2` (up to 25s) |
| Vertical/TikTok | `ltx-2-3` (native portrait) |
| Product ads | `kling-3` (multi-shot + text rendering) |
| YouTube content | `veo3` |

## Model Parameters

Each model has specific allowed values. See [references/api-reference.md](references/api-reference.md) for the complete per-model parameter table.

Common parameters:

| Parameter | Description |
|-----------|-------------|
| `prompt` | Scene description (max 5000 chars) |
| `mode` | Model selector (see table above) |
| `duration` | Video length in seconds (varies by model) |
| `aspect_ratio` | `"16:9"` \| `"9:16"` \| `"1:1"` (varies by model) |
| `video_quality` | Quality tier (varies by model — see api-reference.md) |
| `generation_type` | `"text-to-video"` \| `"image-to-video"` \| `"reference-to-video"` (Veo 3.1) |
| `image` | Image URL (required for image-to-video) |
| `model_version` | Sub-variant for some models (e.g. `"kling-3-pro"`, `"ltx-2.3-fast"`) |

## Error Codes

| Code | Meaning | What to do |
|------|---------|------------|
| 400 | Invalid parameter | Check allowed values in api-reference.md |
| 401 | Invalid API Key | Verify key at veevid.ai/settings/api-keys |
| 402 | Insufficient credits | Show user the `required` vs `balance` from response, suggest cheaper model or [veevid.ai/pricing](https://veevid.ai/pricing) |
| 403 | Account suspended / forbidden | Tell the user their account cannot access the API and they need support |
| 404 | Generation record not found | Check the `generation_id` and whether it belongs to this account |
| 500 | Server error | Wait a few seconds and retry |

## Example Conversations

**Simple text-to-video:**
```
User: "Make a 4-second video of a cat sleeping on a couch"
Agent: [calls /api/quote with mode=veo3, video_quality=standard]
Agent: "Note: Veo 3.1 always generates 8-second videos (duration is fixed). Cost: 20 credits. You have 311 credits. Proceed?"
User: "Yes"
Agent: [generates] "Done! Here's your 8-second video: [URL]."
```

**Image-to-video:**
```
User: "Turn this product photo into a short video" [attaches image]
Agent: [calls /api/quote with mode=veo3, generation_type=image-to-video]
Agent: "I'll upload your image and animate it with Veo 3.1. Cost: 20 credits. You have 200 credits. Proceed?"
User: "Go ahead"
Agent: [uploads image, generates] "Done! Here's your animated product video: [URL]"
```

**Budget-conscious:**
```
User: "Generate a video but keep it cheap"
Agent: [calls /api/quote with mode=grok-imagine, duration=6, video_quality=480p]
Agent: "The cheapest option is Grok Imagine at 10 credits for a 6-second 480p video. You have 50 credits. Want me to use that?"
```

## Links

- [Veevid AI](https://veevid.ai)
- [Get API Key](https://veevid.ai/settings/api-keys)
- [Pricing & Credits](https://veevid.ai/pricing)
- [Blog & Tutorials](https://veevid.ai/blog)
