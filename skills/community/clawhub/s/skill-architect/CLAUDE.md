# Skill Architect

## Project Overview

This repo contains `skill-architect`, a Claude skill for creating new Claude skills with the right internal structure using Google's 5 Agent Skill Design Patterns (Tool Wrapper, Generator, Reviewer, Inversion, Pipeline).

## Key Files

- `SKILL.md` — Main skill definition (the skill itself)
- `references/patterns.md` — Full pattern definitions, decision criteria, combinations
- `references/templates/` — Pattern-specific SKILL.md templates (one per pattern + combined)

## Development & Testing

- To test the skill, install it in a Claude Code project and use trigger phrases like "create a skill", "build a skill", "help me write a skill"
- The skill follows the Inversion pattern itself — it interviews users before making pattern recommendations
- Keep SKILL.md under 500 lines; move detailed content into `references/`

## Conventions

- Pattern templates should be standalone and usable as starting points
- Each template should include frontmatter placeholder, phase structure, and pattern-specific guidance
- The `combined.md` template covers multi-pattern skills
