---
name: skill-template
description: Template for creating new VBot Skills. Use this as a starting point for any new skill.
---

# 🎯 Skill Template

> Copy this file to create a new skill. Fill in the blanks and go!

## Structure

```
your-skill/
├── SKILL.md          # This file - defines the skill
├── README.md         # User-facing documentation
├── action.js         # Main logic (optional)
└── examples/         # Example usage (optional)
```

## SKILL.md Fields

| Field | Required | Description |
|-------|----------|-------------|
| name | Yes | Unique skill identifier (kebab-case) |
| description | Yes | When to use this skill |
| triggers | No | Keywords that activate this skill |
| actions | No | What this skill can do |

## Example SKILL.md

```yaml
---
name: my-awesome-skill
description: Use when user wants to do X
triggers: ["do X", "make X happen"]
---

# My Awesome Skill

## Overview
Brief description of what this skill does.

## Usage
How to use it.

## Examples
1. Example one
2. Example two
```

## Tips

- Keep SKILL.md concise - detail goes in README.md
- Use triggers sparingly, prefer exact matches
- Include error handling in action.js
- Add tests in examples/ if possible

---

*Part of VBot-Skills-Framework*
