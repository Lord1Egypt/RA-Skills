# Learnings

Tone mismatches, context losses, hallucinations, and dialogue insights captured during conversations.

**Categories**: tone_mismatch | misunderstanding | escalation_failure | context_loss | sentiment_drift | hallucination
**Areas**: greeting | intent_detection | response_generation | handoff | follow_up | closing
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being investigated |
| `resolved` | Dialogue issue fixed or pattern integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to SOUL.md, AGENTS.md, or conversation playbook |
| `promoted_to_skill` | Extracted as a reusable conversational skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250115-001] tone_mismatch

**Logged**: 2025-01-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/tone-adaptation
**Area**: response_generation

### Summary
Agent consistently uses formal register when users write casually
...
```

---
