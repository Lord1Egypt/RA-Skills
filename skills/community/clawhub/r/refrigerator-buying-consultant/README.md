# Refrigerator Buying Consultant

> Turns any AI agent into an expert refrigerator buying consultant.

## What it does

Guides first-time and replacement refrigerator buyers through a structured consultation to identify exactly which specs they need for their specific household size, kitchen space, climate, and power situation — without relying on biased sales advice. Delivers a prioritised spec list and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions across household needs, kitchen space, climate class, power stability, and usage patterns
2. Analyses answers using verified refrigerator industry standards (IEC 62552 climate classes, IEC 60068 freezer star ratings, inverter compressor efficiency data)
3. Delivers a structured spec recommendation: non-negotiable → recommended → optional
4. Suggests up to 5 real products matching the user's confirmed specs, region-aware

## Key specs covered

- Net capacity (litres) — calculated from household size and grocery habits
- Climate class (SN / N / ST / T) — matched to local ambient temperature
- Freezer star rating (★ to ★★★★) — based on storage needs
- Compressor type (inverter vs single-speed) — factoring in power stability and duration of use
- Cooling technology (frost-free vs direct cool)
- Physical dimensions and door hinge direction
- Stabilizer-free voltage range (for unstable grid regions)
- Energy efficiency rating

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

https://github.com/arbazex/home-appliance-buying-consultants/tree/master/refrigerator-buying-consultant
