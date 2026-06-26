---
name: twitter-content-generator
description: AI-powered Twitter/X content generator. Generate engaging tweets, threads, and content strategies using Sloan agent.
version: 1.0.9
author: Matt
tags:
  - twitter
  - content-generation
  - social-media
  - ai
pricing:
  type: pay-per-use
  price: 0.002
  currency: USDT
  payment_provider: skillpay.me
---

# Twitter/X Content Generator

Generate engaging Twitter/X content with AI. Perfect for content creators, marketers, and social media managers.

## Features

- **AI Content Generation** - Generate tweets, threads, and content strategies
- **Multiple Styles** - Engaging, professional, casual, witty
- **Customizable** - Control tone, hashtags, emojis
- **Instant Results** - Powered by Sloan agent

## Usage

```bash
# Generate a tweet
twitter-content-generator "AI trends in 2026" --style engaging

# Generate a thread
twitter-content-generator "How to build AI agents" --type thread --length 5

# Generate a content strategy
twitter-content-generator "Remote work tips" --type strategy
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--style` | Content style (engaging, professional, casual, witty) | engaging |
| `--type` | Content type (tweet, thread, strategy) | tweet |
| `--length` | Thread length | 5 |
| `--tone` | Tone (professional, casual, provocative) | professional |
| `--no-hashtags` | Disable hashtags | - |
| `--no-emojis` | Disable emojis | - |

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

Sloan is your AI columnist - a professional content creator specializing in:
- Viral tweets and threads
- Engagement optimization
- Platform-native storytelling

## Support

- GitHub: https://github.com/icepopma/twitter-content-generator
- Discord: https://discord.gg/clawd
- Email: icepopma@hotmail.com

## License

MIT © Matt
