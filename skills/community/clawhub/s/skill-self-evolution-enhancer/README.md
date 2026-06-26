# Skill Self-Evolution Enhancer

A Cursor skill that enables **any skill** to gain self-evolution capabilities. Based on self-improving-agent, it equips skills with: logging, learning from user feedback, promotion of experience to rules, and a Review→Apply→Report loop—all tailored to the target skill's domain.

[中文](README.zh.md)

## Features

- **Domain analysis**: Deep analysis of target skill's capabilities, scenarios, and evolution directions
- **Generate .learnings/**: Domain-specific LEARNINGS.md, ERRORS.md, FEATURE_REQUESTS.md
- **Generate EVOLUTION.md**: Triggers, Review-Apply-Report workflow, OpenClaw feedback rules
- **Multi-skill scaling**: Support multiple skills, each with its own evolution logic

## When to Use

- User says: "Add self-evolution to skill X"
- Scaling self-improvement across many skills (each with its own evolution direction)
- Target skill is non-coding (e.g., content rewriting, system optimization) and needs domain-specific triggers

## Quick Start

1. Enable this skill in Cursor
2. Provide the target skill's path (e.g., `skills/xxx`, `~/.cursor/skills/xxx`)
3. Follow the flow: Read target skill → Domain analysis → Generate .learnings/ and EVOLUTION.md

## Structure

```
skill-self-evolution-enhancer/
├── SKILL.md              # Main skill doc
├── assets/               # Templates
│   ├── DOMAIN-CONFIG-TEMPLATE.md
│   ├── EVOLUTION-RULES-TEMPLATE.md
│   ├── LEARNINGS-TEMPLATE.md
│   ├── ERRORS-TEMPLATE.md
│   └── FEATURE_REQUESTS-TEMPLATE.md
├── references/           # Examples
│   ├── domain-examples.md
│   └── openclaw-feedback.md
└── scripts/
    └── generate-evolution.sh   # Optional scaffold generator
```

## References

- [SKILL.md](SKILL.md) — Full workflow and documentation
- [references/domain-examples.md](references/domain-examples.md) — Domain examples (e.g., content rewriting, system optimization)

## Source

- Based on: self-improving-agent 3.0.1
- Purpose: Enable any skill to gain self-evolution capabilities similar to self-improving-agent
