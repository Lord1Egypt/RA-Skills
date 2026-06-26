# Resistance Training Equipment Buying Consultant

> Turns any AI agent into an expert resistance training equipment buying consultant.

## What it does

Guides first-time and upgrading resistance training equipment buyers through a structured consultation to identify exactly which equipment type, weight capacity, safety features, and construction specs they need — for their specific space, goals, experience level, and training style — without relying on biased sales advice. Delivers a prioritised spec list and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions across 10 areas: training goals, space dimensions, ceiling height, floor loading, solo safety, weight range, equipment type preference, user count, noise constraints, and region
2. Analyses answers using verified resistance training equipment standards, load calculation rules, and ceiling clearance requirements
3. Delivers a structured spec recommendation: non-negotiable → recommended → optional
4. Suggests up to 5 real products matching the user's confirmed specs, tailored to their region

## Key domain coverage

- Equipment category selection: free weights, barbell + power rack, Smith machine, cable/functional trainer, multi-gym, adjustable dumbbells, resistance bands — with explicit decision logic
- Ceiling height compliance: per-category minimum clearance requirements (rack: 240–260 cm; cable machine: 210–230 cm)
- Barbell systems: Olympic (2" / 50 mm) vs standard (1" / 25 mm) — incompatibility flagged
- Rated load requirements with 20–30% growth buffer applied to projected maximums
- Floor loading guidance for upstairs installations; rubber mat thickness recommendations
- Solo training safety: spotter arms, safety straps, Smith machine as alternatives — solo barbell bench press flagged as non-negotiable safety item
- Rack upright sizing (2×2 vs 3×3) and hole spacing for accessory ecosystem compatibility
- Bumper plates vs iron plates for noise and floor protection
- 8 named buyer mistakes flagged proactively (ceiling height blind spot, standard vs Olympic incompatibility, plate weight accumulation underestimation, solo bench press risk, and more)
- Regional plate convention (kg vs lb) and safety certification references (EN 957 / ISO 20957 / ASTM F1749)

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

https://github.com/arbazex/fitness-equipment-buying-consultants/tree/master/resistance-training-equipment-buying-consultant
