# WIT Skill

WIT (`whatifthen`) is an OpenClaw skill for early-stage product thinking, requirement clarification, and decision review.

It is designed for moments when the user has a vague idea, a feature request, a project proposal, a rewrite/integration direction, or a strategic choice — and the real job is to clarify the problem first, then make a concrete decision.

## What WIT does

WIT guides the conversation in two phases:

1. **Break the problem open**
   - verify the problem is real
   - separate observations from assumptions
   - challenge the current framing
   - identify the narrowest useful wedge

2. **Make the decision**
   - decide whether this is worth doing now
   - define the smallest viable move
   - name explicit non-goals
   - end with a concrete next step

## Good fit

Use WIT when the user needs to:

- clarify a fuzzy product or feature idea
- reduce scope before planning
- review whether a proposal is worth doing now
- separate observed reality from storytelling
- merge or rewrite notes in service of a real decision
- move from open exploration to a crisp decision memo

## Core behavior

WIT is intentionally not generic brainstorming.

It pushes toward:

- concrete scenarios over abstract market talk
- narrow wedges over broad platforms
- explicit assumptions over hidden guesses
- decisions over endless discussion
- a clear **not doing now** list

## Repository structure

- `SKILL.md` — main skill definition
- `references/framework.md` — facilitation sequence and operating logic
- `references/evidence-basis.md` — rationale behind the framework
- `references/output-template.md` — output structure
- `references/examples.md` — example use cases

## Installation

Copy this skill into your OpenClaw skills directory, or package/distribute it as a `.skill` file.

Typical skill layout:

```text
wit/
├── SKILL.md
└── references/
    ├── framework.md
    ├── evidence-basis.md
    ├── output-template.md
    └── examples.md
```

## Output shape

WIT ends with a structured synthesis instead of only asking questions. The default output includes:

1. Problem definition
2. Target user and specific scenario
3. Status quo today
4. Observations vs assumptions
5. Framing check
6. Narrowest wedge
7. Decision for this round
8. Not doing now
9. Next step

## Publishing note

This repository tracks the source form of the skill for review, iteration, and sharing.

## Version

Current public release: `1.0.0`

## License

MIT
