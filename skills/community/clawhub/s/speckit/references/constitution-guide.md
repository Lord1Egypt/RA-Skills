# Constitution Management Guide

## Purpose

The project constitution (`.specify/memory/constitution.md`) is the source of truth for all development principles. Every spec, plan, and task must align with it.

## Who Can Amend

- **CEO/CTO**: Full authority to create and amend
- **Other agents**: May propose amendments via Slack to #engineering, but cannot directly modify

## Amendment Process

1. Run `/speckit.constitution [changes description]`
2. The system auto-increments version (MAJOR/MINOR/PATCH)
3. All dependent templates are checked for consistency
4. A Sync Impact Report is generated listing affected files

## Versioning Rules

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| Remove/redefine principle | MAJOR | 1.0.0 → 2.0.0 |
| Add new principle | MINOR | 1.0.0 → 1.1.0 |
| Clarification/typo fix | PATCH | 1.0.0 → 1.0.1 |

## Template Locations

| Template | Path |
|----------|------|
| Constitution | `.specify/templates/constitution-template.md` |
| Specification | `.specify/templates/spec-template.md` |
| Plan | `.specify/templates/plan-template.md` |
| Tasks | `.specify/templates/tasks-template.md` |
| Checklist | `.specify/templates/checklist-template.md` |
| Agent file | `.specify/templates/agent-file-template.md` |

## Placeholder Tokens

The constitution template uses `[ALL_CAPS]` placeholders:
- `[PROJECT_NAME]` — Project name
- `[PRINCIPLE_N_NAME]` — Principle name (N = 1, 2, 3...)
- `[RATIFICATION_DATE]` — Original adoption date (ISO)
- `[LAST_AMENDED_DATE]` — Last change date (ISO)
- `[CONSTITUTION_VERSION]` — Semantic version

All placeholders must be replaced. Unexplained remaining tokens are invalid.
