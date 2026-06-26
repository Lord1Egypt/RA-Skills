# Yollomi AI Image & Video Generator (All Models)

An AI image and video generator skill for OpenClaw. Text-to-image, image-to-image, text-to-video, and image-to-video across many AI models via one unified Yollomi API.

Keywords: image, video, ai image, ai video, image generator, video generator, text-to-image, image-to-image, text-to-video, multimodel.

## Install (ClawHub)

```bash
clawhub install yollomi
```

## Configuration

Set the following environment variable for OpenClaw:

- `YOLLOMI_API_KEY` (required)

## Usage

Ask the agent to generate an image. The skill uses the unified endpoint:

`POST /api/v1/generate` with `{ type: "image", modelId, ... }`

See [SKILL.md](SKILL.md) and [models-reference.md](models-reference.md) for modelIds and parameters.
