# Water Purifier Buying Consultant

> Turns any AI agent into an expert water purifier buying consultant.

## What it does

Guides first-time and replacement water purifier buyers through a structured consultation to identify exactly which specs they need for their specific situation, water source, contaminant profile, household size, and region — without relying on biased sales advice. Delivers a prioritised spec list and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions across four groups: water quality, household usage, infrastructure, and regional profile
2. Analyses answers using verified water purifier industry standards, WHO guidelines, NSF/ANSI and BIS certification requirements, and TDS-based technology selection logic
3. Delivers a structured spec recommendation in three tiers: non-negotiable → recommended → optional
4. Suggests up to 5 real products matching the user's confirmed specs, tailored to their region

## Key specs covered

- Purification technology (RO / UV / UF / gravity — matched to source water and TDS)
- Daily output capacity (calculated from household size and usage)
- Storage tank size
- Inlet pressure requirements and booster pump need
- RO water recovery rate (reject water ratio)
- Regional certifications (NSF/ANSI 58, BIS IS 10500, EU Drinking Water Directive, AS/NZS 4348)
- Specific contaminant removal (fluoride, arsenic, iron, nitrates — where applicable)

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

https://github.com/arbazex/home-appliance-buying-consultants/tree/master/water-purifier-buying-consultant
