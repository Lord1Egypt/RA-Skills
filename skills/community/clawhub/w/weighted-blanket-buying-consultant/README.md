# Weighted Blanket Buying Consultant

> Turns any AI agent into an expert weighted blanket buying consultant.

## What it does

Guides weighted blanket buyers through a structured consultation to identify exactly which specs they need for their specific body weight, sleep needs, thermal preferences, and region — without relying on biased sales advice. Delivers a prioritised spec list and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions covering user profile, sensory/sleep needs, thermal preferences, size/usage context, care constraints, and region
2. Applies the standard occupational-therapy 10%-of-body-weight guideline and verified sizing/fill/fabric selection logic
3. Delivers a structured spec recommendation: non-negotiable → recommended → optional
4. Raises safety flags proactively for children, elderly users, and users with conditions affecting mobility or respiration
5. Suggests up to 5 real products matching the user's confirmed specs

## Key specs covered

- Blanket weight (lb / kg)
- Blanket dimensions (throw, twin, full/queen, king)
- Fill material (glass beads, poly pellets, natural fills)
- Cover fabric (cotton, bamboo/Tencel, minky, fleece, dual-sided)
- Construction type (removable cover vs single-layer)
- Internal tie density and pocket size (even weight distribution)
- Safety certifications (OEKO-TEX, CPSC/ASTM, EN 71 — region-aware)
- Washability ceiling (home vs commercial machine constraints)

## Requirements

- No external APIs or environment variables required
- No runtime dependencies
- Works with any AI agent that supports SKILL.md (OpenClaw, ClawHub, etc.)
- Pure instruction-based — agent reasoning does the work

## Safety guardrails built in

- Blocks recommendations for children under 2 years old or under ~50 lb without directing user to a healthcare provider
- Flags respiratory conditions, limited mobility, and claustrophobia before proceeding
- Caps weight recommendations within the professionally accepted range

## Installation

Add via ClawHub or reference the SKILL.md directly in your agent configuration.

## License

MIT

## Homepage

https://github.com/arbazex/bedroom-essentials-buying-consultants/tree/master/weighted-blanket-buying-consultant
