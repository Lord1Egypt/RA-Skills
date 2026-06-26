---
name: runwayml
description: Generate AI videos, images, and audio with Runway API. Use when generating video from images, text-to-video, video-to-video, character performance, text-to-image, text-to-speech, sound effects, or voice processing with Runway.
license: MIT
compatibility: Requires internet access and a RunwayML API key stored as RUNWAYML_API_SECRET environment variable.
metadata:
  author: slightly-unrelated
  version: 1.0.0
---

# Runway API Skill

Generate AI videos, images, and audio using Runway's API. Features **Gen-4.5** — Runway's latest and most capable model — supporting both text-to-video and image-to-video generation, plus Gen-4 variants and third-party models from Google (Veo) and ElevenLabs.

## Setup

1. Get your API key from [dev.runwayml.com](https://dev.runwayml.com)
2. Store it as `RUNWAYML_API_SECRET` in your environment
3. Install the Node.js SDK: `npm install @runwayml/sdk`

## Quick Start

### Text-to-Video (gen4.5)

```javascript
import RunwayML from "@runwayml/sdk";

const client = new RunwayML(); // reads RUNWAYML_API_SECRET automatically

const task = await client.textToVideo.create({
  model: "gen4.5",
  promptText: "A steaming bowl of noodles in a busy hawker centre, warm light, slow camera push-in",
  duration: 5,
  ratio: "1280:720"
}).waitForTaskOutput();

console.log("Video URL:", task.output[0]);
```

### Image-to-Video (gen4.5)

```javascript
import RunwayML from "@runwayml/sdk";
import fs from "fs";

const client = new RunwayML();

const imageData = fs.readFileSync("product.jpg");
const promptImage = `data:image/jpeg;base64,${imageData.toString("base64")}`;

const task = await client.imageToVideo.create({
  model: "gen4.5",
  promptImage,
  promptText: "Slow dolly-in toward the product jar, warm side lighting, sauce shimmer visible through glass",
  duration: 5,
  ratio: "1280:720"
}).waitForTaskOutput();

console.log("Video URL:", task.output[0]);
```

### cURL (direct API)

```bash
# Text-to-video
curl -X POST "https://api.dev.runwayml.com/v1/image_to_video" \
  -H "Authorization: Bearer $RUNWAYML_API_SECRET" \
  -H "X-Runway-Version: 2024-11-06" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gen4.5",
    "promptText": "A serene mountain landscape at sunset",
    "ratio": "1280:720",
    "duration": 5
  }'
```

## Available Models

### Video Generation

| Model | Input | Credits/sec | Notes |
|-------|-------|-------------|-------|
| **`gen4.5`** ⭐ | Text or Image | 12 | **Newest & recommended** |
| `gen4_turbo` | Image only | 5 | Fast I2V iteration |
| `veo3.1` | Text or Image | 40 | Google Veo — includes audio |
| `veo3.1_fast` | Text or Image | 15 | Veo — audio, cheaper |
| `gen4_aleph` | Video + Text/Image | 15 | Video-to-video transformation |
| `act_two` | Image or Video | 5 | Character performance/motion |

### Image Generation

| Model | Credits | Notes |
|-------|---------|-------|
| `gen4_image` | 5–8/image | High quality, supports style references |
| `gen4_image_turbo` | 2/image | Fast iteration (requires reference image) |

### Audio (ElevenLabs via Runway)

| Model | Output | Credits |
|-------|--------|---------|
| `eleven_multilingual_v2` | Text → Speech | 1/50 chars |
| `eleven_text_to_sound_v2` | Text → Sound FX | 1/6 sec |
| `eleven_voice_dubbing` | Audio → Dubbed | 1/2 sec |

## Valid Ratios

| Ratio | Format |
|-------|--------|
| `1280:720` | 16:9 landscape (standard) |
| `720:1280` | 9:16 portrait (Reels/Stories) |
| `1584:672` | 21:9 ultra-wide |
| `1104:832` | 4:3 |
| `832:1104` | 3:4 |
| `960:960` | Square |

## Duration

- **gen4.5:** 2–10 seconds
- **gen4_turbo:** 5 or 10 seconds

## Task Polling

All operations are async. The SDK's `.waitForTaskOutput()` handles polling automatically (10 min timeout).

**Statuses:** `PENDING` → `THROTTLED` → `RUNNING` → `SUCCEEDED` / `FAILED`

Manual poll:
```bash
curl "https://api.dev.runwayml.com/v1/tasks/{task_id}" \
  -H "Authorization: Bearer $RUNWAYML_API_SECRET" \
  -H "X-Runway-Version: 2024-11-06"
```

## Prompting Tips

- Describe single scenes (5–10 sec clips)
- Use clear physical descriptions, not abstract concepts
- For camera movement: "slow dolly-in", "tracking shot", "push toward subject"
- **Avoid negative phrasing** — "no blur" produces unpredictable results
- Keep prompts grounded and physically plausible

## Official Docs

- [Runway API Documentation](https://docs.dev.runwayml.com/)
- [Model Guide](https://docs.dev.runwayml.com/guides/models/)
- [Developer Portal](https://dev.runwayml.com/)
