# Meta Learnings

Prompt drift, rule conflicts, skill gaps, hook failures, context bloat, and instruction ambiguity captured during agent infrastructure work.

**Categories**: prompt_drift | rule_conflict | skill_gap | hook_failure | context_bloat | instruction_ambiguity
**Areas**: agent_config | skill_authoring | hook_scripts | prompt_files | rule_files | memory_management | extension_api
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to prompt file, rule, hook code, or configuration |
| `promoted_to_skill` | Extracted as a reusable meta-skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250415-001] instruction_ambiguity

**Logged**: 2025-04-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/prompt-file-compression
**Area**: agent_config

### Summary
AGENTS.md delegation section uses vague thresholds causing inconsistent sub-agent usage
...
```

---
