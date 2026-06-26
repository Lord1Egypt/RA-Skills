# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Cursor, Copilot, etc.) when working with code in this repository.

## Repository Overview

A collection of skills for building network asset discovery (空间测绘) queries. Supports FOFA, Quake (鹰图), ZoomEye, and Shodan platforms.

## Creating or Updating Skills

### Directory Structure

```
{skill-name}/           # kebab-case directory name
  SKILL.md              # Required: skill definition
  scripts/              # Helper scripts (optional)
    {script-name}.sh    # Bash scripts
  resources/            # Supporting documentation (optional)
    {file}.md          # Reference files
```

### Naming Conventions

- **Skill directory**: `kebab-case` (e.g., `space-query-skill`)
- **SKILL.md**: Always uppercase, always this exact filename
- **Scripts**: `kebab-case.sh`
- **Resources**: `kebab-case.md` or `kebab-case/`

### SKILL.md Format

```markdown
---
name: {skill-name}
description: {One sentence describing when to use this skill. Include trigger phrases.}
---

# {Skill Title}

{Brief description of what the skill does.}

## How It Works

{Numbered list explaining the skill's workflow}

## Usage

{How to use the skill}
```

### Best Practices for Context Efficiency

Skills are loaded on-demand — only the skill name and description are loaded at startup. The full `SKILL.md` loads into context only when the agent decides the skill is relevant. To minimize context usage:

- **Keep SKILL.md under 500 lines** — put detailed reference material in separate files
- **Write specific descriptions** — helps the agent know exactly when to activate the skill
- **Use progressive disclosure** — reference supporting files that get read only when needed
- **Prefer scripts over inline code** — script execution doesn't consume context (only output does)
- **File references work one level deep** — link directly from SKILL.md to supporting files

## Skill Structure

Each skill contains:
- `SKILL.md` - Instructions for the agent
- `scripts/` - Helper scripts for automation (optional)
- `resources/` - Supporting documentation (optional)

## Distribution

Skills are packaged as zip files for distribution. Include all necessary files in the skill directory.
