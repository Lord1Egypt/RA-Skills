# Learnings

{DOMAIN_DESCRIPTION}

**Categories**: {DOMAIN_CATEGORIES}
**Areas**: {DOMAIN_AREAS}
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill | superseded

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to {PROMOTION_TARGETS} |
| `promoted_to_skill` | Extracted as a reusable skill |
| `superseded` | User corrected again; this learning is no longer valid |

## Learning Entry Format

Append entries in this format:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: {DOMAIN_AREAS_EXAMPLE}

### Summary
One-line description of what was learned

### Details
Full context: what happened, what was wrong, what's correct

### Suggested Action
Specific fix or improvement to make

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-YYYYMMDD-XXX (if related to existing entry)
- Recurrence-Count: 1 (optional, bump when pattern recurs)
- Last-Valid: YYYY-MM-DD (optional, when user contradicted)
- Contradicted-By: LRN-YYYYMMDD-XXX (optional, when superseded)

---
```

## Placeholders to Replace

- `{DOMAIN_DESCRIPTION}`: e.g., "Corrections, insights, and style preferences captured for [skill-name]."
- `{DOMAIN_CATEGORIES}`: e.g., "correction | insight | knowledge_gap | best_practice | style_mismatch | scene_adaptation"
- `{DOMAIN_AREAS}`: e.g., "文案 | 口播 | 短视频脚本" or "系统优化 | 卡顿 | 报错"
- `{DOMAIN_AREAS_EXAMPLE}`: One example area from the list
- `{PROMOTION_TARGETS}`: e.g., "[skill-name]-专属进化规则.md, [skill-name]-最佳实践.md"

---
