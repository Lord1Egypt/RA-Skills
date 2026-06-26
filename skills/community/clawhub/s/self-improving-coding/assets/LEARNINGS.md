# Coding Learnings

Bug patterns, anti-patterns, idiom gaps, debugging insights, and tooling issues captured during development.

**Categories**: bug_pattern | anti_pattern | refactor_opportunity | idiom_gap | tooling_issue | debugging_insight
**Areas**: syntax | logic | data_structures | algorithms | error_handling | testing | tooling
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to lint rule, style guide, snippet library, or debug playbook |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250415-001] anti_pattern

**Logged**: 2025-04-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/mutable-default-args
**Area**: logic

### Summary
Mutable default arguments in Python cause shared state across function calls
...
```

---
