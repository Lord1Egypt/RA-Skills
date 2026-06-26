# Rowing Machine Buying Consultant

> Turns any AI agent into an expert rowing machine buying consultant.

## What it does

Guides rowing machine buyers through a structured consultation to identify exactly which specs they need for their specific body profile, fitness goals, noise constraints, space, and region — without relying on biased sales advice. Delivers a prioritised spec list and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions across seven groups: body profile, fitness goals and experience, noise environment, space, usage pattern, connectivity preferences, and regional infrastructure
2. Analyses answers using verified sizing rules (weight capacity buffer, seat rail inseam formula, stroke clearance rule) and resistance-type matching logic keyed to noise constraints and training goals
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

https://github.com/arbazex/fitness-equipment-buying-consultants/tree/master/rowing-machine-buying-consultant
