# The Founder's Playbook

> AI-native startup lifecycle: Idea → MVP → Launch → Scale.
> Adapted from Anthropic's founder playbook for any AI agent, any platform.

## What is this?

This repository contains the **Agent Skill** version of "The Founder's Playbook: Building an AI-Native Startup" — adapted for use with **any AI agent** (no platform lock-in).

The skill converts the full AI-native startup lifecycle framework into reusable, stage-aware workflows that activate automatically when the user describes where they are in their journey.

## Repository structure

```
the-founders-playbook/
├── skills/
│   └── the-founders-playbook/
│       ├── SKILL.md              # Main skill — the full playbook
│       ├── README.md             # Skill documentation
│       ├── skill-card.md         # ClawHub marketplace metadata
│       ├── setup.md              # First-use setup guidance
│       └── references/
│           └── stage-reference.md  # Quick reference cheat sheet
├── AGENTS.md                     # Guidelines for AI agents
├── LICENSE                       # MIT-0
├── CONTRIBUTING.md               # Contribution guide
└── README.md                     # This file
```

## Installation

```bash
# Via ClawHub (any OpenClaw agent)
npx clawhub install the-founders-playbook

# Via skills.sh (any agent — Claude Code, Cursor, Copilot, Gemini, etc.)
npx skills add casvian/the-founders-playbook
```

## The four stages

| Stage | Focus | Exit Criterion |
|-------|-------|---------------|
| **Idea** | Validate before building | Problem-solution fit confirmed |
| **MVP** | Build what's necessary | Product-market fit evidence |
| **Launch** | Build the company | Repeatable revenue + operations |
| **Scale** | Build the institution | Enterprise infrastructure + moats |

## Usage

Just start talking naturally to any AI agent:

> *"I have an idea for..."* → Activates **Idea** stage
> *"Help me build the MVP"* → Activates **MVP** stage
> *"We're ready to launch"* → Activates **Launch** stage
> *"We need to scale"* → Activates **Scale** stage

The agent detects your stage and activates the appropriate playbook section.

## License

MIT-0 — Free to use, modify, redistribute. No attribution required.
