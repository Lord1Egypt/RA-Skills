# Washing Machine Buying Consultant

> Turns any AI agent into an expert washing machine buying consultant.

## What it does

Guides washing machine buyers through a structured consultation to identify exactly which specs they need for their specific household size, laundry habits, space, water supply, electrical infrastructure, and region — without relying on biased sales advice. Delivers a prioritised spec list (non-negotiable → recommended → optional) and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed question groups covering: household size, installation space, water supply, electrical infrastructure, usage patterns, noise constraints, and regional standards
2. Applies verified industry formulas — drum capacity sizing, residual moisture content by RPM, energy labelling standards (EU, US Energy Star, BEE, WELS), and power draw thresholds for off-grid situations
3. Proactively flags common buyer mistakes (voltage mismatch, spin speed oversight, water usage in scarce areas, washer-dryer combo trade-offs)
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

- **Regions supported:** Europe (EU energy label), UK, USA (Energy Star / MEF / WF), India (BEE stars), Australia (WELS), Pakistan, Middle East, and others via voltage/certification logic
- **Machine types:** Front-load, top-load (agitator and impeller), washer-dryer combos
- **Capacity range:** 5 kg – 12 kg drum (household sizing) and equivalent US cubic footage

## License

MIT

## Homepage

https://github.com/arbazex/home-appliance-buying-consultants/tree/master/washing-machine-buying-consultant
