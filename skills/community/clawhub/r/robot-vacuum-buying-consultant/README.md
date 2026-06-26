# Robot Vacuum Buying Consultant

> Turns any AI agent into an expert robot vacuum buying consultant.

## What it does

Guides first-time and replacement robot vacuum buyers through a structured consultation to identify exactly which specs they need for their specific home size, floor type, pet situation, allergy status, and automation preference — without relying on biased sales advice. Delivers a prioritised spec list and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions across home size, floor type, carpet pile, pet ownership, furniture clearances, allergy status, Wi-Fi setup, and desired automation level
2. Analyses answers using verified robot vacuum standards (suction Pa vs carpet pile guidelines, the 0.7× real-world coverage correction, HEPA filter classification, robot height clearance rule)
3. Delivers a structured spec recommendation: non-negotiable → recommended → optional
4. Suggests up to 5 real products matching the user's confirmed specs, with regional availability in mind

## Key specs covered

- Suction power (Pa) — matched to floor type and carpet pile height
- Navigation technology — random, gyroscope, or LiDAR based on home size and complexity
- Battery runtime and coverage area — with real-world correction and auto-resume assessment
- Robot height — validated against the user's lowest furniture clearance
- Brush roll type — rubber recommended for pet hair households
- Filter type — HEPA-grade for allergy and asthma sufferers
- Obstacle avoidance tier — matched to presence of cables, toys, or pet waste
- Auto-empty base — prioritised for pets, allergies, and low-maintenance users
- Mopping capability — with honest performance tier clarification (drag vs vibrating vs rotating)
- Wi-Fi band compatibility — 2.4 GHz vs 5 GHz flagged against user's router
- Multi-floor mapping — required for multi-storey homes

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

https://github.com/arbazex/home-appliance-buying-consultants/tree/master/robot-vacuum-buying-consultant
