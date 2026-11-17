# Claude Code Skills Specification

This document describes the official specification for Claude Code skills,
based on the [plugin-dev skill-development](https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev/skills/skill-development)
reference from the Claude Code repository.

## Overview

Skills are modular, self-contained packages that extend Claude's capabilities
by providing specialized knowledge, workflows, and tools. They transform Claude
from a general-purpose agent into a specialized agent equipped with procedural
knowledge for specific domains or tasks.

## Skill Structure

Every skill consists of a required `SKILL.md` file and optional bundled
resources:

```text
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   ├── description: (required)
│   │   └── disable-model-invocation: (optional, boolean)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation loaded into context as needed
    ├── commands/         - Sub-command definitions
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

## SKILL.md Front-matter Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | string | Short name of the skill, used for invocation (e.g., `spex`) |
| `description` | Yes | string | Determines when Claude will use the skill. Should use third-person and include specific trigger phrases. |
| `disable-model-invocation` | No | boolean | When `true`, prevents the model from automatically triggering the skill. The skill can only be invoked manually by the user via `/<name>`. |
| `version` | No | string | Semantic version of the skill (e.g., `0.1.0`) |

### Description Best Practices

Use third-person format with specific trigger phrases:

```yaml
description: "This skill should be used when the user asks to 'specific phrase 1',
  'specific phrase 2'. Include exact phrases users would say."
```

### disable-model-invocation

Set `disable-model-invocation: true` when a skill should only respond to
explicit user invocation (e.g., `/spex create`). This prevents the model from
auto-triggering the skill based on conversation context.

## Progressive Disclosure

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** — Always in context (~100 words)
2. **SKILL.md body** — Loaded when skill triggers (target <5k words)
3. **Bundled resources** — Loaded as needed by Claude (unlimited)

### SKILL.md Body Guidelines

- Target 1,500–2,000 words (max 5,000)
- Include core concepts, essential procedures, and quick references
- Move detailed documentation to `references/`
- Reference all bundled resources so Claude knows they exist

## Bundled Resources

### Scripts (`scripts/`)

Executable code for tasks requiring deterministic reliability or repeated use.

- Token efficient — may be executed without loading into context
- Should be documented and tested

### References (`references/`)

Documentation loaded into context as needed.

- Database schemas, API docs, domain knowledge, policies
- Keeps SKILL.md lean; loaded only when Claude determines it's needed
- For files >10k words, include grep search patterns in SKILL.md

### Assets (`assets/`)

Files used in output, not loaded into context.

- Templates, images, icons, boilerplate code, fonts
- Copied or modified as part of skill output

## Writing Style

### Imperative/Infinitive Form

Write using verb-first instructions, not second person:

```markdown
# Correct
Parse the frontmatter using sed.
Validate the input before processing.

# Incorrect
You should parse the frontmatter.
You need to validate the input.
```

### Third-Person in Description

```yaml
# Correct
description: "This skill should be used when the user asks to..."

# Incorrect
description: "Use this skill when you want to..."
```

## Validation Checklist

- [ ] `SKILL.md` exists with valid YAML frontmatter
- [ ] Frontmatter has `name` and `description` fields
- [ ] Description uses third person with specific trigger phrases
- [ ] Markdown body uses imperative/infinitive form
- [ ] Body is lean (1,500–2,000 words ideal, <5k max)
- [ ] Detailed content moved to `references/`
- [ ] All referenced files actually exist
- [ ] Scripts are executable and documented
