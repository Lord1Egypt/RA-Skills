# VDOT Running Calculator — Jack Daniels Training Pace Calculator for AI Agents

**Get your VDOT score and all five Jack Daniels training paces (Easy, Marathon, Threshold, Interval, Repetition) from one recent race time.**

An open-standard [agentskills.io](https://agentskills.io/specification) skill that turns any compatible AI agent into a VDOT running-pace calculator. It asks for one recent race result, then computes VDOT and personalized training paces using Jack Daniels and Jimmy Gilbert's published running-economy equations — the same model that's been the gold standard for distance-running coaches since 1979 and remains unchanged across four editions of _Daniels' Running Formula_.

100% self-contained. No API keys, no GPS watch integration, no external services — one race result and pure arithmetic.

## Compatible with

- **Claude** (Claude Code, Claude apps, Claude Skills)
- **OpenClaw** / **ClawHub**
- **Hermes Agent** (Nous Research)
- Any other agent supporting the [agentskills.io](https://agentskills.io/specification) open standard

## What it does

1. Asks for a recent, honestly-raced result (distance + finish time).
2. Computes the oxygen cost of that race pace and the sustainable %VO2max for that duration.
3. Derives VDOT — Daniels' single-number running fitness score.
4. Inverts the same equations to calculate all five training paces: **Easy, Marathon, Threshold, Interval, Repetition** — in min/km and min/mile.
5. States the assumptions and limitations plainly (honest race effort, normal conditions, not a substitute for medical guidance).

## Why this formula never goes stale

Unlike calculators built on shifting product data or API-dependent lookups, VDOT is a fixed physiological model published in 1979 and still used unmodified in the current (4th) edition of Daniels' Running Formula. The coefficients in this skill are the same ones professional coaches use today — there's nothing to update as "the science evolves," because this _is_ the science, and it hasn't changed.

## Usage

Ask your agent:

> "I ran a 5K in 22:30 — what's my VDOT and what paces should I train at?"

The agent will compute VDOT and return Easy, Marathon, Threshold, Interval, and Repetition paces, with the full calculation shown for transparency.

## Folder structure

```
vdot-running-calculator/
├── SKILL.md    # entry point — formula, derivation, training zones, and workflow all in one file
└── README.md
```

## Sources

- Daniels, J. & Gilbert, J. (1979). _Oxygen Power: Performance Tables for Distance Runners._
- Daniels, J. (2021). _Daniels' Running Formula_, 4th ed. Human Kinetics.

## Disclaimer

This is a training-planning tool based on a published physiological model, not medical advice. Consult a doctor before starting a new or intense training program, especially if returning from injury or managing a cardiovascular condition.

## License

MIT — free to use, modify, and redistribute.

## Version

1.0.0 — initial release.
