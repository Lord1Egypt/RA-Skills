# trio-vision — Turn Any Camera Into a Smart Camera

Stop getting dumb motion alerts for every shadow. **Describe what actually matters in plain English** — get notified only when it happens, right in your chat.

Powered by [Trio by MachineFi](https://machinefi.com).

## The Problem

You have cameras everywhere — doorbell, baby monitor, security, warehouse — but nobody watches them. Motion detection alerts on every shadow and breeze. Enterprise video AI costs $50K+/year.

## The Solution

Ask your cameras questions in plain English. Get answers in WhatsApp, Telegram, or Slack — wherever you already use OpenClaw.

| What You Say | What Happens | Cost |
|-------------|-------------|------|
| "Is anyone at my front door?" | Instant answer with explanation | $0.01 |
| "Alert me when a package is delivered" | Continuous watch, notifies on match | $0.02/min |
| "Summarize this stream every 10 minutes" | Periodic narrative digests | $0.02/min |
| "How many people are in this photo?" | Single image analysis | $0.01 |

Works with YouTube Live, Twitch, RTSP/RTSPS cameras, and HLS streams.

## Install

```bash
# From ClawHub
openclaw skills install machinefi/trio-vision

# Or clone directly
git clone https://github.com/machinefi/trio-openclaw-skill.git ~/.openclaw/skills/trio-vision
```

## Setup

1. Get a free API key (100 credits / $1.00) at https://console.machinefi.com
2. Set your key:
   ```bash
   export TRIO_API_KEY="your_key_here"
   ```
3. That's it. No ML setup, no model downloads, no GPU required.

## Real-World Use Cases

**Home & Security**
> "Watch my front door camera and tell me when a person (not a cat) approaches"
> "Is the garage door open or closed right now?"
> "Is the baby sleeping or awake?"

**Business & Warehouse**
> "Monitor the loading dock — alert me when a delivery truck arrives"
> "Are there more than 10 packages on the sorting table?"
> "Summarize foot traffic at the store entrance every 30 minutes"

**Streaming & Content**
> "What's happening on this Twitch stream right now?"
> "Summarize this YouTube live stream every 5 minutes"

**Smart Home Verification**
> "Check the garage camera — the sensor says the door is open, is it actually open?"
> "Is anyone in the living room right now?"

**Prototyping & Development**
> "Test if this camera can reliably detect when a parking spot is empty"
> "Check this condition on the stream: 'Is there a line of more than 5 people?'"

## Links

- [Trio API Docs](https://docs.machinefi.com)
- [Trio Console & Free API Key](https://console.machinefi.com)
- [OpenClaw](https://openclaw.ai)
- [ClawHub](https://clawhub.ai)

## License

Apache-2.0
