---
name: youtube-video-ideas
description: AI-powered YouTube video ideas generator. Generate viral video concepts, titles, and hooks.
version: 1.0.7
author: Matt
tags:
  - youtube
  - video
  - content-ideas
  - viral
pricing:
  type: pay-per-use
  price: 0.002
  currency: USDT
  payment_provider: skillpay.me
---

# YouTube Video Ideas Generator

Generate viral YouTube video ideas with titles, hooks, and content outlines.

## Features

- **Viral Ideas** - Trending topics and formats
- **Click-Worthy Titles** - Optimized for CTR
- **Content Hooks** - First 30 seconds that work
- **SEO Keywords** - Rank in search

## Usage

```bash
# Generate video ideas
youtube-video-ideas "AI agents"

# For specific niche
youtube-video-ideas "productivity" --niche tech

# Generate content outline
youtube-video-ideas "how to code" --outline
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--niche` | Target niche (tech, gaming, lifestyle) | - |
| `--outline` | Include content outline | - |

## Pricing

- **Pay per use**: 0.002 USDT per generation

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SKILLPAY_MERCHANT_KEY` | Payment merchant key (optional, embedded key used by default) | No |
| `OPENCLAW_GATEWAY_TOKEN` | Gateway auth token for local API fallback | No |

## Requirements

- OpenClaw with Sloan agent (AI columnist)
- OpenClaw Gateway running locally (for API fallback)

## About Sloan

Sloan is your AI columnist - a professional YouTube content strategist specializing in viral video ideas.

## Support

- GitHub: https://github.com/icepopma/youtube-video-ideas
- Discord: https://discord.gg/clawd
- Email: icepopma@hotmail.com

## License

MIT © Matt
