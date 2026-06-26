# Smartwatch Fitness Tracker Buying Consultant

> Turns any AI agent into an expert smartwatch and fitness tracker buying consultant.

## What it does

Guides first-time and replacement smartwatch or fitness tracker buyers through a structured consultation to identify exactly which specs they need — platform compatibility, GPS type, health sensors, battery life, water resistance, and more — without relying on biased sales advice. Delivers a prioritised spec list and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed questions across 10 areas: smartphone ecosystem, health priorities, activity profile, battery expectations, display and form factor, durability, smart features, phone independence, wearability, and region
2. Analyses answers using verified smartwatch industry specs, compatibility rules, and battery trade-off calculations
3. Delivers a structured spec recommendation: non-negotiable → recommended → optional
4. Suggests up to 5 real products matching the user's confirmed specs, tailored to their platform and region

## Key domain coverage

- Platform lock-in: watchOS (iPhone-only) vs Wear OS (Android) vs cross-platform (Garmin, Fitbit, Polar)
- GPS types: none / connected (phone-required) / built-in / multi-band dual-frequency
- Water resistance standards: ATM, ISO 22810, IP68 — correctly interpreted for swimming vs splash use
- Battery life trade-offs: AMOLED vs MIP display impact, GPS-on vs standby, LTE drain
- Health sensors: optical HR (PPG), ECG (with regional lock-in warnings), SpO2, skin temperature, IHRN
- Case size guidance matched to wrist circumference
- LTE band compatibility warnings for cross-country purchases
- 8 named buyer mistakes flagged proactively (platform blindness, standby vs GPS battery confusion, ECG regional restrictions, IP68 misinterpretation, and more)

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

https://github.com/arbazex/fitness-equipment-buying-consultants/tree/master/smartwatch-fitness-tracker-buying-consultant
