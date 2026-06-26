# VEED Fabric — Talking Video Skill

A [Claude Code skill](https://skills.sh) that generates talking head videos from a single photo using [VEED Fabric 1.0](https://fal.ai/models/veed/fabric-1.0).

Built for founders and non-video-makers who need professional video content without video editing skills. Give it a headshot and a script (or audio file), and get back a lip-synced talking video.

## Install

```bash
npx skills add mattdotroberts/veed-skill
```

## What it does

Two input paths:

- **Image + Audio** — provide a photo and an audio file, get a lip-synced video
- **Image + Text** — provide a photo and a written script, get a video with AI-generated voice

Features:
- Accepts local files or URLs (auto-uploads local files to fal.ai CDN)
- Voice style presets: Professional, Casual, Energetic, or custom
- 480p (default) or 720p resolution
- Standard or fast generation speed
- Async queue with progress updates
- Downloads finished video to `./output/`

## Setup

You need a fal.ai API key:

1. Sign up at [fal.ai](https://fal.ai)
2. Get your key from [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys)
3. Set it in your environment:

```bash
export FAL_KEY=your_key_here
```

## Usage

Once installed, use it in Claude Code by mentioning "veed", "fabric", or "talking video":

> "Use veed to make a talking video from my headshot.png with this script: Hi, I'm building the future of payments."

> "Create a fabric video from photo.jpg and voiceover.mp3"

## Pricing

Charged per second of generated video by fal.ai:

| Resolution | Standard | Fast |
|---|---|---|
| 480p | $0.08/sec | $0.10/sec |
| 720p | $0.15/sec | $0.20/sec |

## Skill structure

```
SKILL.md              # Skill entry point — triggers, prerequisites, rule index
rules/
  lip-sync.md         # Image + audio workflow
  text-to-video.md    # Image + text workflow with voice presets
  file-upload.md      # Local file upload to fal.ai CDN
  queue.md            # Async queue polling and result retrieval
  output.md           # Video download and save
  errors.md           # Validation and error handling
specs/
  veed-fabric-skill.md  # Original spec
```

## License

MIT
