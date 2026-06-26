---
name: Vidu Video Generation
description: Video generation provider plugin for Vidu (viduq3-pro, viduq3-turbo, viduq2, viduq1). Supports text-to-video, image-to-video, reference-to-video, and start-end-to-video.
version: 1.0.0
metadata:
  openclaw:
    primaryEnv: VIDU_API_KEY
    requires:
      env:
        - VIDU_API_KEY
    emoji: "🎬"
    homepage: https://platform.vidu.com
---

# Vidu Video Generation Provider

A video generation provider plugin for [OpenClaw](https://github.com/openclaw/openclaw) that integrates with the [Vidu API](https://platform.vidu.com).

## Features

- Text-to-video generation
- Image-to-video generation
- Reference-to-video generation (character/subject consistency)
- Start-end-to-video generation (keyframe interpolation)
- Supports both Global (`api.vidu.com`) and China (`api.vidu.cn`) endpoints

## Supported Models

| Model | text2video | img2video | reference2video | start-end2video |
|-------|:---:|:---:|:---:|:---:|
| viduq3-pro | ✓ | ✓ | | ✓ |
| viduq3-turbo | ✓ | ✓ | | ✓ |
| viduq2-pro | | ✓ | ✓ | ✓ |
| viduq2-pro-fast | | ✓ | | ✓ |
| viduq2-turbo | | ✓ | | ✓ |
| viduq2 | ✓ | | ✓ | |
| viduq1 | ✓ | ✓ | ✓ | ✓ |
| viduq1-classic | | ✓ | | ✓ |
| vidu2.0 | | ✓ | ✓ | ✓ |

## Setup

1. Get an API key from [Vidu](https://platform.vidu.com)
2. Set `VIDU_API_KEY` in your environment
3. Install this plugin via ClawHub: `clawhub install vidu-video-generation`
