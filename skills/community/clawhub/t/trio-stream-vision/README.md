# trio-stream-vision — Analyze Any Livestream with Natural Language

Paste a YouTube Live URL, RTSP camera feed, or HLS stream — ask questions about what's happening in plain English. Detect specific events, monitor conditions continuously, or get periodic summaries. No ML pipelines, no model downloads, no GPU required.

Powered by [Trio's Reality-as-an-API](https://machinefi.com) vision models.

## The Problem

Live video is everywhere — YouTube streams, security cameras, webcams, Twitch channels — but extracting useful information from them requires building ML pipelines, managing frame extraction, and serving vision models. Enterprise video AI starts at $50K+/year.

## The Solution

Describe what you want to know in plain English. Trio's vision models analyze the stream and return structured answers.

| What You Say | What Happens | Cost |
|-------------|-------------|------|
| "Is anyone visible on this stream?" | Instant yes/no + explanation of what the VLM sees | $0.01 |
| "Alert me when a delivery truck appears" | Continuous monitoring, triggers when condition is met | $0.02/min |
| "Summarize this livestream every 10 minutes" | Periodic narrative digests of stream activity | $0.02/min |

Works with **YouTube Live**, **RTSP/RTSPS cameras**, and **HLS streams**.

## Install

```bash
# From ClawHub
openclaw skills install machinefi/trio-stream-vision

# Or clone directly
git clone https://github.com/machinefi/trio-openclaw-skill.git ~/.openclaw/skills/trio-stream-vision
```

## Setup

1. Get a free API key (100 credits / $1.00) at https://console.machinefi.com
2. Set your key:
   ```bash
   export TRIO_API_KEY="your_key_here"
   ```
3. That's it. No ML setup, no model downloads, no GPU required.

## What You Can Do

**Instant Stream Analysis**
> "What's happening on this YouTube livestream right now?"
> "Is there anyone visible in the frame?"
> "How many cars are in the parking lot?"

**Continuous Event Detection**
> "Watch this stream and alert me when a person appears"
> "Monitor the loading dock — notify me when a truck arrives"
> "Tell me when the streamer starts a new game"

**Periodic Summaries**
> "Summarize this livestream every 5 minutes"
> "Give me a digest of this security feed every 30 minutes"

**Smart Home & Security Cameras**
> "Check the garage camera — is the door open or closed?"
> "Is the baby sleeping or awake?"
> "Watch my front door and tell me when a person (not a cat) approaches"

## How It Works

1. You paste a live stream URL and describe what you want to know
2. Trio extracts frames (or short clips) from the stream
3. A vision language model (VLM) analyzes the visual content against your condition
4. You get a structured response: `triggered` (yes/no), `explanation` (what the VLM sees), and optional frame data

Three analysis modes:
- **Frames** (default) — single frame analysis, best for static objects
- **Clip** — short video segment (1-10s), best for motion and actions
- **Hybrid** — combined analysis for maximum accuracy

## Links

- [Trio API Reference](https://docs.machinefi.com/api-reference/)
- [Trio Console & Free API Key](https://console.machinefi.com)
- [OpenClaw](https://openclaw.ai)
- [ClawHub](https://clawhub.ai)

## License

Apache-2.0
