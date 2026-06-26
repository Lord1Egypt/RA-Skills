# CLAUDE.md - Repository Guide

This file provides guidance to AI agents on how to work with this repository.

## Repository Overview

This is an OpenClaw skill repository containing a single skill: `team-planner`.

## What is a Skill?

A skill is a directory containing a `SKILL.md` file that provides instructions and tool definitions to an AI agent. Skills extend the capabilities of OpenClaw.

## Directory Structure

```
team-planner/
├── SKILL.md              # Main skill file (required)
├── README.md             # Human-readable documentation
├── CLAUDE.md             # This file - AI guidance
└── references/           # Additional reference materials
    └── examples.md       # Usage examples and patterns
```

## For AI Agents

### Adding New Examples
When adding new examples to `references/examples.md`:
1. Follow the existing format (task description → output plan)
2. Include real-world scenarios
3. Keep explanations clear

### Updating SKILL.md
When modifying the skill behavior:
1. Maintain the existing YAML frontmatter format
2. Keep the 8-step planning process structure
3. Update examples to reflect new capabilities

### Versioning
This repository follows semantic versioning:
- MAJOR: Breaking changes to skill interface
- MINOR: New features or examples
- PATCH: Bug fixes or documentation updates

## ClawHub Integration

To submit to ClawHub:
1. Ensure SKILL.md is complete and tested
2. Add clear README.md with usage examples
3. Tag release with version number
4. Submit to ClawHub registry

## Quality Standards

- SKILL.md must have valid YAML frontmatter
- All trigger phrases should be specific and testable
- Examples should be realistic and actionable
- Documentation should be in English (README) and match SKILL.md language
