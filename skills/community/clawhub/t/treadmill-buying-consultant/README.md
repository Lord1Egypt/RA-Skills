# Treadmill Buying Consultant

> Turns any AI agent into an expert treadmill buying consultant.

## What it does

Guides treadmill buyers through a structured consultation to identify exactly which specs they need for their specific body profile, usage pattern, space, and region — without relying on biased sales advice. Delivers a prioritised spec list and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions across six groups: body profile, intended use, usage pattern, space and environment, regional infrastructure, and connectivity preferences
2. Analyses answers using verified treadmill sizing formulas (CHP by use type, belt length by height, weight capacity buffer, room clearance rules, voltage and certification by region)
3. Delivers a structured spec recommendation: non-negotiable → recommended → optional, plus proactive buyer warnings
4. Suggests up to 5 real products matching the user's confirmed specs, tailored to their region

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

https://github.com/arbazex/fitness-equipment-buying-consultants/tree/master/treadmill-buying-consultant
