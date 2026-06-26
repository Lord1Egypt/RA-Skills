# Learnings

Methodology insights, statistical corrections, and knowledge gaps captured during research.

**Categories**: methodology_flaw | data_quality | reproducibility_issue | statistical_error | hypothesis_revision | experiment_design
**Areas**: data_collection | preprocessing | analysis | modeling | validation | publication
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being investigated |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to experiment checklist, model card, or methodology standard |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20260412-001] methodology_flaw

**Logged**: 2026-04-12T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/leakage-detection
**Area**: preprocessing

### Summary
Timestamp features leak target variable when timestamps encode label assignment time
...
```

---

