---
name: veed-fabric
description: Generate talking head videos from a photo using VEED Fabric 1.0. Triggers on mentions of "veed", "fabric", or "talking video". Turns a headshot + audio or text script into a lip-synced MP4 video via fal.ai.
metadata:
  tags: veed, fabric, video, talking-head, lip-sync, avatar, fal
---

# VEED Fabric — Talking Video Generator

Create realistic talking head videos from a single photo. Built for founders and non-video-makers who need professional video content without video editing skills.

## When to Use

Activate this skill when the user mentions:
- "veed" or "fabric" (the product/model name)
- "talking video" or "talking head video"
- "lip sync" or "lipsync" with a photo
- "animate my photo" to speak

**MUST NOT** activate on generic video requests like "make a video" or "create content" unless they specifically mention VEED or Fabric.

## Prerequisites

**MUST** check that the `FAL_KEY` environment variable is set before doing anything else. If it is not set, show the user:

```
FAL_KEY environment variable not found.

1. Get your API key at https://fal.ai/dashboard/keys
2. Set it: export FAL_KEY=your_key_here
```

**MUST NOT** proceed without a valid key. **MUST NOT** ask the user to provide the key inline.

## Lip-sync from audio

When the user has a photo and an audio file (recorded voiceover, podcast clip, etc.), load [./rules/lip-sync.md](./rules/lip-sync.md) for the full workflow.

## Text-to-video

When the user has a photo and a written script (text they want spoken aloud), load [./rules/text-to-video.md](./rules/text-to-video.md) for the full workflow.

## Uploading local files

When the user provides a local file path instead of a URL, load [./rules/file-upload.md](./rules/file-upload.md) for the upload procedure.

## Queue and polling

Video generation is async. Load [./rules/queue.md](./rules/queue.md) for the queue submission, polling, and result retrieval flow.

## How to use

Read individual rule files for detailed explanations and working code:

- [rules/lip-sync.md](rules/lip-sync.md) - Image + audio lip-sync workflow, supported formats, API parameters
- [rules/text-to-video.md](rules/text-to-video.md) - Image + text workflow, voice presets, text limits
- [rules/file-upload.md](rules/file-upload.md) - Uploading local files to fal.ai CDN for use as inputs
- [rules/queue.md](rules/queue.md) - Async queue submission, status polling, result retrieval
- [rules/output.md](rules/output.md) - Downloading and saving the generated video
- [rules/errors.md](rules/errors.md) - Error handling, validation, and troubleshooting
