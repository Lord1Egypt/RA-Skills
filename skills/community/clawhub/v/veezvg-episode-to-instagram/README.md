# `openclaw-skills`

First public OpenClaw skill in this repository:

- `episode-to-instagram`

OpenClaw skill for turning a long-form video episode into Instagram-ready outputs:

- timestamped transcript
- structured content plan
- extracted frames
- rendered carousel slides
- Instagram draft automation with preview screenshots

## What is included

- `SKILL.md`: the skill definition and workflow
- `scripts/`: deterministic helpers for transcription, frame extraction, rendering, and Instagram draft prep
- `brand-config.json`: neutral branding defaults you can customize

## What is intentionally not included

- API keys or local auth-profile helpers
- generated `output/` artifacts
- local `node_modules/`

## Requirements

- `ffmpeg` and `ffprobe`
- Node.js
- `OPENAI_API_KEY` for `scripts/transcribe.sh`
- `openclaw browser` for the Instagram draft flow
- an Instagram session already logged into the OpenClaw browser profile

## Setup

1. Copy or symlink this skill folder into your OpenClaw skills workspace.
2. Run `npm install` in the skill directory if you need the local `canvas` dependency for slide generation.
3. Edit `brand-config.json` for your own account branding.
4. Export `OPENAI_API_KEY` before running transcription.

## Verification

Run:

```bash
npm run check
```

## License

MIT
