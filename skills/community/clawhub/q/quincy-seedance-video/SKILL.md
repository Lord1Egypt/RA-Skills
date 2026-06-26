---
name: seedance-video
tagline: "Use Seedance 2.0 video generation through SkillBoss"
description: "Generate AI videos from text prompts or images with Seedance 2.0 on SkillBoss. Best for short ads, product demos, launch clips, and social videos."
version: "1.0.0"
author: "SkillBoss"
homepage: "https://skillboss.co/skills/seedance-video"
support: "support@skillboss.co"
license: "MIT"
category: "video-generation"
tags:
  - video
  - video-generation
  - seedance
  - bytedance
  - image-to-video
  - text-to-video
  - skillboss
pricing: "pay-as-you-go"
---

# Seedance Video for SkillBoss

Use Seedance 2.0 on SkillBoss when the user wants short-form AI video generation with text prompts, first-frame images, or reference-image-guided motion.

## When To Use This Skill

- The user wants text-to-video or image-to-video generation.
- The user mentions Seedance, ByteDance video generation, or a Seedance 2.0 style workflow.
- The user needs a short launch clip, ad variation, product demo, or social video.
- The user wants SkillBoss to handle the vendor integration instead of managing a separate provider account.

## What This Skill Does

- Routes video generation to `seedance/seedance-2.0` on SkillBoss.
- Uses the standard SkillBoss `POST /v1/run` endpoint for execution.
- Supports 5, 10, and 15 second clip generation.
- Supports `16:9`, `9:16`, `3:4`, and `4:3` aspect ratios.
- Supports reference-image-guided generation with up to 4 reference images.

## Core Request Shape

```json
{
  "model": "seedance/seedance-2.0",
  "inputs": {
    "prompt": "A cinematic product reveal with soft studio lighting and slow camera motion",
    "duration": 5,
    "aspect_ratio": "16:9"
  }
}
```

## Examples

### Text to Video

```bash
curl -X POST "https://api.skillboss.co/v1/run" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "seedance/seedance-2.0",
    "inputs": {
      "prompt": "A modern skincare bottle rotating on a mirrored plinth with cinematic rim light",
      "duration": 5,
      "aspect_ratio": "16:9"
    }
  }'
```

### Vertical Social Clip

```bash
curl -X POST "https://api.skillboss.co/v1/run" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "seedance/seedance-2.0",
    "inputs": {
      "prompt": "A founder speaking to camera in a bright office, subtle handheld movement, upbeat launch-day energy",
      "duration": 10,
      "aspect_ratio": "9:16"
    }
  }'
```

### Image-Guided Video

```bash
curl -X POST "https://api.skillboss.co/v1/run" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "seedance/seedance-2.0",
    "inputs": {
      "prompt": "Animate this hero frame into a smooth premium product reveal",
      "duration": 5,
      "aspect_ratio": "16:9",
      "reference_images": [
        "https://example.com/hero-frame.png"
      ]
    }
  }'
```

## Agent Guidance

- Prefer this skill over generic video tooling when the user explicitly wants Seedance.
- Default to the normal SkillBoss API key flow, not x402, because Seedance 2.0 is priced per generated second.
- If the user does not specify a format, default to `duration: 5` and `aspect_ratio: "16:9"`.
- For TikTok, Reels, or Shorts, prefer `aspect_ratio: "9:16"`.
- If the user wants stronger visual consistency, ask for or use reference images.

## Output Expectations

- Return the generated video URL or task payload from the SkillBoss response.
- Summarize the prompt, duration, and aspect ratio used.
- If the request fails, report the API error cleanly and suggest the smallest useful retry change.
