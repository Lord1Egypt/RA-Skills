---
name: tubeify
description: AI video editor for YouTube creators — removes pauses, filler words, and dead air automatically via API
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [curl]
    homepage: https://tubeify.xyz
    emoji: "🎬"
---

# Tubeify

> AI-powered video editing for solo YouTube creators. Upload a raw recording, get back a tight, polished video — no manual editing required.

Tubeify automatically removes dead air, filler words, and awkward pauses from raw video recordings. It accepts a video URL, processes it with GPU-accelerated AI, and returns a cleaned-up version in minutes.

## What This Skill Does

Use this skill to automate video cleanup workflows end-to-end via Tubeify's agent API:

- **Authenticate** using a Web3 wallet address (no passwords or email required)
- **Submit** a raw video URL with processing options
- **Poll** for completion and retrieve the processed video
- **Payment** is 2 USDC on Ethereum per video (under 15 minutes)

## API Reference

**Base URL:** `https://tubeify.xyz`

### Authenticate

```bash
curl -c session.txt -X POST https://tubeify.xyz/index.php \
  -d "wallet=<YOUR_WALLET_ADDRESS>"
```

### Submit Video for Processing

```bash
curl -b session.txt -X POST https://tubeify.xyz/process.php \
  -d "video_url=<VIDEO_URL>" \
  -d "tx_hash=<USDC_TX_HASH>" \
  -d "speed=1.0" \
  -d "remove_pauses=true" \
  -d "remove_fillers=true"
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `video_url` | string | Publicly accessible URL of the raw video |
| `tx_hash` | string | Ethereum transaction hash for 2 USDC payment |
| `speed` | float | Playback speed multiplier (1.0–2.0) |
| `remove_pauses` | bool | Remove dead air and long pauses |
| `remove_fillers` | bool | Remove filler words (um, uh, etc.) |

### Check Status

```bash
curl -b session.txt https://tubeify.xyz/status.php
```

Returns JSON with `status` (`processing` | `done` | `error`) and a `download_url` when complete.

## Pricing

- **$2 per video** (videos under 15 minutes)
- Pay in USDC (ERC-20) on Ethereum

## Example Workflow

```bash
# 1. Authenticate
curl -c session.txt -X POST https://tubeify.xyz/index.php \
  -d "wallet=0xYOUR_WALLET"

# 2. Submit video (include your 2 USDC tx hash)
curl -b session.txt -X POST https://tubeify.xyz/process.php \
  -d "video_url=https://example.com/raw-recording.mp4" \
  -d "tx_hash=0xABC123..." \
  -d "remove_pauses=true" \
  -d "remove_fillers=true"

# 3. Poll until done
curl -b session.txt https://tubeify.xyz/status.php
```

## Setup

No API keys or environment variables required. Authentication is wallet-based — connect with MetaMask, Rainbow, or any Web3-compatible wallet.

## Links

- **Website:** https://tubeify.xyz
- **Pricing:** $2/video, no subscription
