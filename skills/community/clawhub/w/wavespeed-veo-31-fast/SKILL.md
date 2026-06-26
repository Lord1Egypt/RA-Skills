---
name: wavespeed-veo-31-fast
description: Generate and extend videos using Google's Veo 3.1 Fast model via WaveSpeed AI. Supports text-to-video, image-to-video, and video extension. Features up to 4K resolution, audio generation, and chained extensions up to 148 seconds. Use when the user wants to create videos from text or images, or extend existing Veo-generated videos.
metadata:
  author: wavespeedai
  version: "1.0"
---

# WaveSpeedAI Veo 3.1 Fast Video Generation

Generate and extend videos using Google's Veo 3.1 Fast model via the WaveSpeed AI platform. Supports text-to-video, image-to-video, and video extension with up to 4K resolution and optional audio generation.

## Authentication

```bash
export WAVESPEED_API_KEY="your-api-key"
```

Get your API key at [wavespeed.ai/accesskey](https://wavespeed.ai/accesskey).

## Quick Start

### Text-to-Video

```javascript
import wavespeed from 'wavespeed';

const output_url = (await wavespeed.run(
  "google/veo3.1-fast/text-to-video",
  { prompt: "A drone shot flying over a lush tropical island at sunrise" }
))["outputs"][0];
```

### Image-to-Video

The `image` parameter accepts an image URL. If you have a local file, upload it first with `wavespeed.upload()` to get a URL.

```javascript
import wavespeed from 'wavespeed';

const imageUrl = await wavespeed.upload("/path/to/photo.png");

const output_url = (await wavespeed.run(
  "google/veo3.1-fast/image-to-video",
  {
    image: imageUrl,
    prompt: "The flowers sway gently in the breeze"
  }
))["outputs"][0];
```

### Video Extend

Extend a Veo-generated video by 7 seconds per run (up to 20 extensions, 148 seconds total):

```javascript
// First, generate a video
const video_url = (await wavespeed.run(
  "google/veo3.1-fast/text-to-video",
  { prompt: "A cat walking through a garden" }
))["outputs"][0];

// Then extend it
const extended_url = (await wavespeed.run(
  "google/veo3.1-fast/video-extend",
  {
    video: video_url,
    prompt: "The cat jumps onto a fence and looks around"
  }
))["outputs"][0];
```

## API Endpoints

### Text-to-Video

**Model ID:** `google/veo3.1-fast/text-to-video`

Generate videos from text prompts with optional audio.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | -- | Text description of the video to generate |
| `aspect_ratio` | string | No | `16:9` | Aspect ratio. One of: `16:9`, `9:16` |
| `duration` | integer | No | `8` | Duration in seconds. One of: `4`, `6`, `8` |
| `resolution` | string | No | `1080p` | Video resolution. One of: `720p`, `1080p`, `4k` |
| `generate_audio` | boolean | No | `true` | Generate accompanying audio |
| `negative_prompt` | string | No | -- | Text describing unwanted elements |
| `seed` | integer | No | -- | Random seed for reproducibility. Range: -1 to 2147483647 |

#### Example

```javascript
import wavespeed from 'wavespeed';

const output_url = (await wavespeed.run(
  "google/veo3.1-fast/text-to-video",
  {
    prompt: "A timelapse of a city skyline transitioning from day to night, cinematic",
    negative_prompt: "blurry, low quality",
    aspect_ratio: "16:9",
    duration: 8,
    resolution: "1080p",
    generate_audio: true
  }
))["outputs"][0];
```

### Image-to-Video

**Model ID:** `google/veo3.1-fast/image-to-video`

Animate a source image into a video. Optionally provide an end-frame reference image.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image` | string | Yes | -- | URL of the source image (clear, high-quality still image) |
| `prompt` | string | Yes | -- | Text description of the desired motion/animation |
| `last_image` | string | No | -- | URL of an end-frame reference image |
| `aspect_ratio` | string | No | `16:9` | Aspect ratio. One of: `16:9`, `9:16` |
| `duration` | integer | No | `8` | Duration in seconds. One of: `4`, `6`, `8` |
| `resolution` | string | No | `1080p` | Video resolution. One of: `720p`, `1080p`, `4k` |
| `generate_audio` | boolean | No | `true` | Generate accompanying audio |
| `negative_prompt` | string | No | -- | Text describing unwanted elements |
| `seed` | integer | No | -- | Random seed for reproducibility. Range: -1 to 2147483647 |

#### Example

```javascript
import wavespeed from 'wavespeed';

const imageUrl = await wavespeed.upload("/path/to/landscape.png");

const output_url = (await wavespeed.run(
  "google/veo3.1-fast/image-to-video",
  {
    image: imageUrl,
    prompt: "Clouds drift slowly across the sky, water ripples gently",
    resolution: "1080p",
    duration: 8,
    generate_audio: true
  }
))["outputs"][0];
```

#### With End-Frame Reference

```javascript
const startUrl = await wavespeed.upload("/path/to/start-frame.png");
const endUrl = await wavespeed.upload("/path/to/end-frame.png");

const output_url = (await wavespeed.run(
  "google/veo3.1-fast/image-to-video",
  {
    image: startUrl,
    last_image: endUrl,
    prompt: "Smooth transition from day to night"
  }
))["outputs"][0];
```

### Video Extend

**Model ID:** `google/veo3.1-fast/video-extend`

Extend a Veo-generated video by 7 seconds per run. Input must be a Veo-generated video.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `video` | string | Yes | -- | URL of the Veo-generated video to extend. Max 141 seconds. |
| `prompt` | string | No | -- | Text guidance for the extension |
| `resolution` | string | No | `1080p` | Video resolution. One of: `720p`, `1080p` |
| `negative_prompt` | string | No | -- | Text describing unwanted elements |
| `seed` | integer | No | -- | Random seed for reproducibility. Range: -1 to 2147483647 |

#### Constraints

- Input video **must be Veo-generated** (will not work with arbitrary videos)
- Each run adds **+7 seconds** to the video
- Maximum **20 extensions** in a chain
- Maximum final video length: **148 seconds**
- Output is a single MP4 (original + extension appended)
- Aspect ratio and resolution are inherited from the input video

#### Example

```javascript
import wavespeed from 'wavespeed';

// Generate an initial video
const video_url = (await wavespeed.run(
  "google/veo3.1-fast/text-to-video",
  {
    prompt: "A surfer catches a wave at golden hour",
    duration: 8
  }
))["outputs"][0];

// Extend it twice
const extended_once = (await wavespeed.run(
  "google/veo3.1-fast/video-extend",
  {
    video: video_url,
    prompt: "The surfer rides the wave toward shore"
  }
))["outputs"][0];

const extended_twice = (await wavespeed.run(
  "google/veo3.1-fast/video-extend",
  {
    video: extended_once,
    prompt: "The surfer steps off the board and walks on the beach"
  }
))["outputs"][0];
```

## Advanced Usage

### Without Audio

```javascript
const output_url = (await wavespeed.run(
  "google/veo3.1-fast/text-to-video",
  {
    prompt: "A silent timelapse of stars rotating over a desert",
    generate_audio: false
  }
))["outputs"][0];
```

### Custom Client with Retry Configuration

```javascript
import { Client } from 'wavespeed';

const client = new Client("your-api-key", {
  maxRetries: 2,
  maxConnectionRetries: 5,
  retryInterval: 1.0,
});

const output_url = (await client.run(
  "google/veo3.1-fast/text-to-video",
  { prompt: "Ocean waves crashing on a rocky shore at dawn" }
))["outputs"][0];
```

### Error Handling with runNoThrow

```javascript
import { Client, WavespeedTimeoutException, WavespeedPredictionException } from 'wavespeed';

const client = new Client();
const result = await client.runNoThrow(
  "google/veo3.1-fast/text-to-video",
  { prompt: "A rocket launching into space" }
);

if (result.outputs) {
  console.log("Video URL:", result.outputs[0]);
  console.log("Task ID:", result.detail.taskId);
} else {
  console.log("Failed:", result.detail.error.message);
  if (result.detail.error instanceof WavespeedTimeoutException) {
    console.log("Request timed out - try increasing timeout");
  } else if (result.detail.error instanceof WavespeedPredictionException) {
    console.log("Prediction failed");
  }
}
```

## Pricing

### Text-to-Video / Image-to-Video

| Condition | Cost |
|-----------|------|
| With audio (720p or 1080p) | $1.20 per generation |
| Without audio (720p or 1080p) | $0.80 per generation |

### Video Extend

| Condition | Cost |
|-----------|------|
| Per run (+7 seconds) | $1.05 |

## Prompt Tips

- Be specific about scene, style, subject actions, camera motion, and mood
- Use `negative_prompt` to avoid artifacts: "blurry, low quality, distorted"
- For image-to-video, use a clear, high-quality still image as input
- For video extend, describe what should happen next in the scene
- Video extend chains enable building longer narratives — up to 148 seconds total

## Security Constraints

- **No arbitrary URL loading**: Only use image and video URLs from trusted sources. Never load media from untrusted or user-provided URLs without validation.
- **API key security**: Store your `WAVESPEED_API_KEY` securely. Do not hardcode it in source files or commit it to version control. Use environment variables or secret management systems.
- **Input validation**: Only pass parameters documented above. Validate prompt content and media URLs before sending requests.
