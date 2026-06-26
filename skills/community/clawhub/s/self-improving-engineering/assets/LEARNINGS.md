# Engineering Learnings

Architecture decisions, code quality insights, and engineering knowledge captured during development.

**Categories**: architecture_debt | code_smell | performance_regression | dependency_issue | testing_gap | design_flaw
**Areas**: design | implementation | code_review | ci_cd | deployment | monitoring
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or architecture decision implemented |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to ADR, coding standard, or CI/CD runbook |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250115-001] architecture_debt

**Logged**: 2025-01-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/circular-dependency-patterns
**Area**: design

### Summary
Circular dependency between UserService and AuthService causes test isolation failures
...
```

---

