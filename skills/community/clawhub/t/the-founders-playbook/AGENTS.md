# AGENTS.md — Instructions for AI Agents

This repository contains an **Agent Skill** following the [Agent Skills specification](https://agentskills.io/specification.md). The skill installs to `.agents/skills/` and is designed for any AI agent.

## Repository Structure

```
the-founders-playbook/
├── skills/
│   └── the-founders-playbook/
│       ├── SKILL.md              # Main skill file — read this
│       ├── README.md             # Skill documentation
│       ├── skill-card.md         # ClawHub metadata
│       ├── setup.md              # First-use setup guidance
│       └── references/
│           └── stage-reference.md  # Quick reference
├── AGENTS.md                     # This file
├── CONTRIBUTING.md               # Contribution guide
├── LICENSE                       # MIT-0
└── README.md                     # Repository README
```

## Key Files

- **`skills/the-founders-playbook/SKILL.md`** — The core skill. Read this first. Contains the full 4-stage AI-native startup framework.
- **`skills/the-founders-playbook/setup.md`** — First-use integration guidance for the skill.

## Stage Detection

The skill auto-detects which startup stage to activate based on trigger phrases. If the stage is ambiguous, ask the user: *"What stage is your startup at? Idea (validating), MVP (building), Launch (first customers), or Scale (growing)?"*

## Build / Lint / Test

This is a content skill (no build step). Verify:
- YAML frontmatter is valid
- `name` field matches directory name
- `description` covers all trigger phrases
- All Claude-specific references are removed (this skill is platform-agnostic)
