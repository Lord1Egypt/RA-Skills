# AgentSkills Specification Reference

This document provides a quick reference for skill structure and conventions.

## Directory Structure

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown body (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code
    ├── references/       - Documentation to load as needed
    └── assets/           - Files used in output
```

## SKILL.md Format

```markdown
---
name: skill-name
description: What this skill does and when to use it. Include triggers and contexts.
---

# Skill Title

## Overview

Brief description of the skill's purpose.

## Usage

Instructions for how to use the skill.
```

## Naming Conventions

- Lowercase letters, digits, and hyphens only
- Must start with a letter
- Under 64 characters
- Prefer verb-led phrases (e.g., `pdf-watermarker`, `data-validator`)

## Description Best Practices

The `description` field in frontmatter is the **primary triggering mechanism**. Include:

1. **What** the skill does
2. **When** to use it (specific scenarios, file types, triggers)
3. **Who** should use it (if domain-specific)

Example:
```yaml
description: "Add watermarks to PDF files. Use when processing PDFs for branding, security, or document identification. Triggers on requests to watermark, stamp, or brand PDF documents."
```

## Resource Types

### scripts/
Executable code for deterministic or repeated operations.
- Python scripts, shell scripts
- Should be self-contained and well-documented
- Can be executed without loading into context

### references/
Documentation loaded as needed.
- API references, schemas, detailed guides
- Keep SKILL.md lean, put details here
- Organize by domain/variant for selective loading

### assets/
Files used in output generation.
- Templates, images, fonts, boilerplate
- Not loaded into context
- Copied or modified for final output

## Progressive Disclosure

Skills use three loading levels:

1. **Metadata** (name + description) - Always in context
2. **SKILL.md body** - When skill triggers
3. **Bundled resources** - As needed

Design for efficient context usage.

## Common Patterns

### Workflow-Based
Sequential processes with decision trees.
```
Overview → Decision Tree → Step 1 → Step 2 → ...
```

### Task-Based
Collection of operations.
```
Overview → Quick Start → Task A → Task B → ...
```

### Capabilities-Based
Integrated feature set.
```
Overview → Core Capabilities → 1. Feature → 2. Feature → ...
```
