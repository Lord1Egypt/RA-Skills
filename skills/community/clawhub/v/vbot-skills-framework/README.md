# 🎨 VBot Skills Framework

> Build, share, and discover AI agent skills like never before.

## What Is This?

A framework for creating reusable skills (prompt templates + code) that any AI agent can use.

Inspired by: mattpocock/skills, anthropics/skills, obra/superpowers

## Quick Start

### 1. Create a Skill

```bash
cp -r template my-skill
cd my-skill
# Edit SKILL.md
```

### 2. Define Your Skill

Edit `SKILL.md`:

```yaml
---
name: my-skill
description: When user wants to do X
---

# My Skill

Describe what it does...
```

### 3. Document It

Update `README.md` with usage examples.

## Framework Philosophy

1. **Discoverable** - Clear triggers and descriptions
2. **Composable** - Skills should work together
3. **Testable** - Include examples and edge cases
4. **Documented** - Users should understand at a glance

## Skill Structure

```
skill-name/
├── SKILL.md      # Definition (YAML frontmatter + markdown)
├── README.md     # User documentation
├── action.js     # Optional: executable code
└── examples/     # Optional: test cases
```

## SKILL.md Format

```yaml
---
name: skill-name           # Unique ID (kebab-case)
description: When to use   # One-liner
triggers: []               # Optional activation keywords
author: your-name          # Optional
version: 1.0.0             # Optional
---

# Skill Title

Longer description...

## Usage

How to use this skill.

## Examples

1. Example usage
2. Another example
```

## Included Skills

| Skill | Description |
|-------|-------------|
| template | Start here - copy to create new skills |

## Contribute

Found a bug? Have an idea? PRs welcome!

## License

MIT - Go wild!
