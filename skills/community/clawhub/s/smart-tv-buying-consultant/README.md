# Smart TV Buying Consultant

> Turns any AI agent into an expert Smart TV buying consultant.

## What it does

Guides first-time and replacement Smart TV buyers through a structured consultation to identify exactly which specs they need for their specific room, viewing distance, lighting conditions, use cases, and region — without relying on biased sales advice. Delivers a prioritised spec list and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions across five groups: room and viewing setup, primary use cases, content and connectivity, environment and infrastructure, and user profile
2. Analyses answers using verified display industry standards — THX/SMPTE screen size formulas, human visual acuity resolution thresholds, panel technology selection logic, HDMI 2.1 requirements, and regional certification standards
3. Delivers a structured spec recommendation in three tiers: non-negotiable → recommended → optional
4. Suggests up to 5 real products matching the user's confirmed specs, tailored to their region

## Key specs covered

- Screen size (calculated from viewing distance using THX and SMPTE references)
- Resolution (4K vs 1080p vs 8K — matched to viewing distance and screen size)
- Panel technology (OLED / QLED / Mini-LED / IPS LCD — matched to room lighting and use)
- Native refresh rate (60 Hz vs 120 Hz — matched to gaming and sports use)
- HDR format (Dolby Vision, HDR10, HDR10+, HLG)
- HDMI 2.1 port count (matched to next-gen gaming hardware)
- Input lag in game mode (< 10 ms or < 20 ms)
- Smart OS compatibility with required streaming services
- Regional certifications (FCC, CE, BIS, RCM) and tuner standards (ATSC 3.0, DVB-T2, ISDB-T)
- VRR, ALLM, eARC, Wi-Fi 6, AV1 hardware decoding

## Requirements

- No external APIs or environment variables required
- No runtime dependencies
- Works with any AI agent that supports SKILL.md (OpenClaw, ClawHub, etc.)
- Pure instruction-based — agent reasoning does the work

## Installation

Add via ClawHub or reference the SKILL.md directly in your agent configuration.

## License

MIT

## Homepage

https://github.com/arbazex/home-appliance-buying-consultants/tree/master/smart-tv-buying-consultant
