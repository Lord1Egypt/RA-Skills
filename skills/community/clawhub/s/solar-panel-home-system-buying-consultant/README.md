# Solar Panel Home System Buying Consultant

> Turns any AI agent into an expert home solar panel system buying consultant.

## What it does

Guides homeowners through a structured consultation to calculate exactly which solar components they need — panel capacity (kWp), battery bank (Ah), inverter type and size, charge controller, and system voltage — based on their actual electricity consumption, location, roof space, and grid situation. Delivers a prioritised spec list with explicit calculations and up to 5 matched product or system suggestions.

## How it works

1. Agent interviews the user across seven areas: location and sun resource, electricity consumption, grid situation and system type, roof space, existing infrastructure, battery requirements, and user profile
2. Applies verified solar-sizing formulas (PSH-based panel sizing, loss-factor adjustment, DoD-based battery Ah calculation, inverter surge sizing)
3. Flags common mistakes proactively — undersized batteries, modified sine wave inverters on sensitive loads, PWM controllers on high-voltage panels, temperature derating in hot climates
4. Delivers a structured spec recommendation: non-negotiable → recommended → optional, with calculations shown
5. Suggests up to 5 real system configurations matching the user's confirmed specs, tailored to their region and certifications

## Key formulas applied

| What                    | Formula                                         |
| ----------------------- | ----------------------------------------------- |
| Daily consumption       | Monthly kWh ÷ 30                                |
| Adjusted demand         | Daily kWh × 1.25 (loss factor)                  |
| Required panel capacity | Adjusted kWh/day ÷ Peak Sun Hours = kWp         |
| Battery bank (Ah)       | (kWh to backup × 1000) ÷ (System voltage × DoD) |
| Inverter size           | Peak simultaneous load × 1.25                   |

## Regional coverage

Certifications and standards flagged for: EU/UK (IEC 61215, IEC 61730, CE, MCS), USA (UL 1703, UL 1741, NEC 690), Australia (CEC approved list, AS 4777), India (BIS IS 14286, MNRE), and general IEC-standard regions.

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

https://github.com/arbazex/power-energy-buying-consultants/tree/master/solar-panel-home-system-buying-consultant
