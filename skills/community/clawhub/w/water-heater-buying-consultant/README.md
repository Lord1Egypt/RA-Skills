# Water Heater Buying Consultant

> Turns any AI agent into an expert water heater buying consultant.

## What it does

Guides water heater buyers through a structured consultation to identify exactly which specs they need for their specific household size, fuel availability, hot water demand, climate, installation space, and region — without relying on biased sales advice. Delivers a prioritised spec list (non-negotiable → recommended → optional) and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed question groups covering: household size and simultaneous demand, fuel source and circuit capacity, installation space and type, climate and incoming water temperature, usage timing and pattern, and water quality
2. Applies verified industry formulas — First-Hour Rating (FHR) calculation against peak-hour demand (US DOE method), tankless flow rate and required kW formula, BTU/h to kW conversion for gas units, heat pump viability criteria (COP, ambient temperature, air volume), recovery rate adequacy, and incoming water temperature by climate zone
3. Proactively flags common buyer mistakes: sizing by headcount alone without FHR, under-rated circuits for instant electric units, HPWH in cold/sealed spaces, tankless under-sizing for cold climates, anode rod neglect in hard-water areas, pressure rating mismatch, solar heater backup assumptions
4. Delivers a structured spec recommendation: non-negotiable → recommended → optional
5. Suggests up to 5 real products matching the user's confirmed specs, tailored to their country/region

## Requirements

- No external APIs or environment variables required
- No runtime dependencies
- Works with any AI agent that supports SKILL.md (OpenClaw, ClawHub, etc.)
- Pure instruction-based — agent reasoning does the work

## Installation

Add via ClawHub or reference the SKILL.md directly in your agent configuration.

## Coverage

- **Regions supported:** USA/Canada (UL/ETL, AGA, Energy Star, UEF), Europe (CE, ErP A–G label), UK (UKCA, Gas Safe), India (BIS, BEE stars), Saudi Arabia (SASO), Pakistan (PSQCA), Australia (MEPS, Energy Rating), and others via voltage/certification logic
- **Heater types covered:** Electric storage tank, gas storage, instant/tankless electric (point-of-use and whole-house), gas tankless/combi, heat pump water heater (HPWH), solar-compatible storage
- **Standards applied:** US DOE First-Hour Rating (FHR), Uniform Energy Factor (UEF), EU ErP Directive, BEE star rating, ASHRAE sizing guidance, AHAM recovery rate standards, IEC pressure vessel safety principles

## License

MIT

## Homepage

https://github.com/arbazex/home-appliance-buying-consultants/tree/master/water-heater-buying-consultant
