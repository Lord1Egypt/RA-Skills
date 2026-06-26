# Coding Skill Template

Template for creating skills extracted from coding learnings. Copy and customize.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Concise description of the coding pattern, bug fix, or idiom this skill addresses. Include trigger conditions."
---

# Skill Name

Brief introduction: what coding problem this skill solves, what language(s) it applies to, and its origin.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Error/pattern trigger] | [Fix or idiom to apply] |
| [Related trigger] | [Alternative approach] |

## Background

Why this coding knowledge matters. What bugs it prevents. What performance or maintainability improvements it provides.

## The Problem

### Problematic Code

\`\`\`language
// Code that demonstrates the bug or anti-pattern
\`\`\`

### Why It Fails

Explanation of the root cause: memory model, type system, concurrency, etc.

## Solution

### Corrected Code

\`\`\`language
// Fixed or idiomatic version
\`\`\`

### Step-by-Step

1. Identify the pattern in existing code
2. Apply the fix
3. Add test to prevent regression
4. Add lint rule if applicable

## Prevention

### Lint Rule

\`\`\`toml
# ruff.toml or .eslintrc equivalent
[lint]
select = ["RULE_ID"]
\`\`\`

### Type Annotation

\`\`\`language
// Type-level prevention if applicable
\`\`\`

## Common Variations

- **Variation A**: Description and how to handle
- **Variation B**: Description and how to handle

## Languages Affected

| Language | Manifestation | Fix |
|----------|---------------|-----|
| Python | [How it appears] | [Language-specific fix] |
| TypeScript | [How it appears] | [Language-specific fix] |
| Rust | [How it appears] | [Language-specific fix] |

## Gotchas

- Warning or common mistake when applying the fix
- Edge case to watch for

## Related

- Link to related lint rule documentation
- Link to language specification section
- Link to related skill

## Source

Extracted from coding learning entry.
- **Learning ID**: LRN-YYYYMMDD-XXX
- **Original Category**: bug_pattern | anti_pattern | idiom_gap | debugging_insight
- **Language**: python | typescript | rust | go | java
- **Extraction Date**: YYYY-MM-DD
```

---

## Minimal Template

For simple coding skills that don't need all sections:

```markdown
---
name: skill-name-here
description: "What coding pattern this addresses and when to apply it."
---

# Skill Name

[Problem statement in one sentence]

## Problem

\`\`\`language
// problematic code
\`\`\`

## Solution

\`\`\`language
// corrected code
\`\`\`

## Prevention

[Lint rule or type annotation to prevent recurrence]

## Source

- Learning ID: LRN-YYYYMMDD-XXX
```

---

## Naming Conventions

- **Skill name**: lowercase, hyphens for spaces
  - Good: `mutable-default-args`, `async-race-conditions`, `pagination-off-by-one`
  - Bad: `MutableDefaultArgs`, `async_race`, `fix1`

- **Description**: Start with action verb, mention the error or pattern
  - Good: "Prevents mutable default argument bugs in Python. Use when function parameters use lists or dicts as defaults."
  - Bad: "Python stuff"

- **Files**:
  - `SKILL.md` — Required, main documentation
  - `scripts/` — Optional, executable code (linter wrapper, fixer)
  - `references/` — Optional, detailed docs
  - `assets/` — Optional, templates

---

## Extraction Checklist

Before creating a skill from a coding learning:

- [ ] Bug/pattern is verified (status: resolved, fix tested)
- [ ] Solution is broadly applicable (not one-off project quirk)
- [ ] Code examples are minimal and self-contained
- [ ] Language(s) affected are specified
- [ ] Prevention method is documented (lint rule, type annotation, test)
- [ ] Name follows conventions
- [ ] Description is concise but informative

After creating:

- [ ] Update original learning with `promoted_to_skill` status
- [ ] Add `Skill-Path: skills/skill-name` to learning metadata
- [ ] Test skill by reading it in a fresh session
- [ ] Verify code examples compile/run correctly
