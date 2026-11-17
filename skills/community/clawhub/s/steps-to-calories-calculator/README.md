# Steps To Calories Calculator — Steps-to-Calories AI Skill Backed by Peer-Reviewed Research

**Find out exactly how many calories your walk burned — calculated from a real biomechanics study, not a generic guess.**

An open-standard [agentskills.io](https://agentskills.io/specification) skill that turns any compatible AI agent into a walking-calorie calculator. It asks for body weight and step count, then computes net calories burned walking using the metabolic-cost-per-stride relationship established in a controlled treadmill study published in the _Journal of Experimental Biology_.

100% self-contained. No API keys, no fitness-tracker integration, no external services — just weight, steps, and one formula.

## Compatible with

- **Claude** (Claude Code, Claude apps, Claude Skills)
- **OpenClaw** / **ClawHub**
- **Hermes Agent** (Nous Research)
- Any other agent supporting the [agentskills.io](https://agentskills.io/specification) open standard

## What it does

1. Asks for body weight (kg or lb, auto-converts).
2. Asks for step count (a walk, or a daily total).
3. Optionally checks pace/terrain to flag when the estimate is less reliable (steep inclines, loaded backpacks, non-walking gaits).
4. Computes: `calories_kcal = 2.74 × weight_kg × (steps ÷ 2) ÷ 4184`.
5. Shows the full calculation so the result is auditable, and states the ~9% margin of error the source study reports — no false precision.

## The science

Formula is derived from:

> Weyand, P. G., Smith, B. R., Puyau, M. R., & Butte, N. F. (2010). _The mass-specific energy cost of human walking is set by stature._ Journal of Experimental Biology, 213(23), 3972–3979. DOI: [10.1242/jeb.048199](https://doi.org/10.1242/jeb.048199)

The study measured, via indirect calorimetry, that humans spanning a 6-fold range in body mass and ages 5–32 expend an essentially constant **2.74 J per kg of body mass per stride** when walking at a normal, self-selected pace on level ground. A stride = 2 steps, so the formula divides step count by 2. The result converts joules to kilocalories using the exact 4184 J/kcal conversion.

Full derivation, boundary conditions, and citation details are in `sources` section — this skill doesn't just apply a number, it explains where the number comes from and when it doesn't apply.

## Usage

Ask your agent:

> "How many calories did I burn walking 8,000 steps?"

The agent will ask for your body weight if it doesn't have it, then return the calculation with its assumptions and margin of error stated plainly.

## Disclaimer

This is a research-based fitness estimate, not medical, clinical, or nutrition advice. For medical or weight-management decisions, consult a doctor or registered dietitian.

## License

MIT — free to use, modify, and redistribute.

## Version

1.0.0
