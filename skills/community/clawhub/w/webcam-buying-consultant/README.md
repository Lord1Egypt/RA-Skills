# Webcam Buying Consultant

> Turns any AI agent into an expert webcam buying consultant.

## What it does

Guides first-time and upgrading webcam buyers through a structured consultation to identify exactly which specs they need for their use case, lighting environment, room depth, and platform — without relying on marketing claims or retailer advice. Corrects the most common first-time buyer mistake (fixating on resolution when sensor size and aperture are the real image quality determinants). Delivers a prioritised spec list, a Spec Summary Card, and up to 5 matched product suggestions.

## How it works

1. Agent asks targeted, research-backed questions grouped by theme: use case, lighting environment, room depth and framing, mounting and placement, audio requirements, platform and connectivity, streaming-specific needs, and regional standards
2. Analyses lighting condition to determine minimum aperture (f-stop) and sensor size — the two specs that most affect real-world image quality
3. Matches field of view to desk distance and framing need; flags wide-angle distortion risk at close distances
4. Determines autofocus type (fixed / software AF / phase-detection) based on movement patterns and lighting
5. Flags common buyer mistakes proactively (resolution obsession in dim rooms, backlight without HDR/WDR, USB 2.0 for 4K, proprietary drivers on Linux, thin-bezel clip incompatibility)
6. Delivers: Non-negotiable specs → Recommended specs → Optional extras → Spec Summary Card → up to 5 product suggestions

## Requirements

- No external APIs or environment variables required
- No runtime dependencies
- Works with any AI agent that supports SKILL.md (OpenClaw, ClawHub, etc.)
- Pure instruction-based — agent reasoning does the work

## Specs covered

| Spec              | What the skill determines                                                                    |
| ----------------- | -------------------------------------------------------------------------------------------- |
| Resolution        | 720p / 1080p / 4K based on use case — with explanation of when it matters vs when it doesn't |
| Frame rate        | 30 fps vs 60 fps based on content type and motion                                            |
| Aperture (f-stop) | Maximum f-number for the user's lighting condition                                           |
| Sensor size       | Minimum sensor size for low-light performance                                                |
| HDR / WDR         | Required if backlit or high-contrast environment                                             |
| Field of view     | FOV range matched to desk distance and framing preference                                    |
| Autofocus type    | Fixed / contrast-detect / phase-detection based on movement and lighting                     |
| Microphone        | Built-in (mono / stereo / beamforming) vs external-only recommendation                       |
| USB standard      | USB 2.0 vs USB 3.0 based on resolution and format                                            |
| Connector type    | USB-A vs USB-C based on host computer ports                                                  |
| UVC compliance    | Plug-and-play compatibility for Linux, Chromebook, cross-platform                            |
| OS compatibility  | Windows / macOS / Linux / Chromebook                                                         |

## Installation

Add via ClawHub or reference the SKILL.md directly in your agent configuration.

## License

MIT

## Homepage

https://github.com/arbazex/personal-tech-buying-consultants/tree/master/webcam-buying-consultant
