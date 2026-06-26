---
name: self-improving-plus
description: "Enhanced self-improvement skill with skill distillation, knowledge base integration, and automatic skill extraction. Logs errors, corrections, and learnings; distills patterns into reusable skills; integrates with GitHub high-star project knowledge base."
metadata:
  author: opencode
  version: 2.0
  tags: self-improvement, learning, skill-creation, knowledge-base
  compatibility: opencode
  license: MIT
---

# Self-Improving Plus

Enhanced self-improvement skill with automatic skill distillation, knowledge base integration, and GitHub high-star project learning.

## Features

- **Error/Correction Logging**: Track learnings, errors, and feature requests
- **Skill Distillation**: Extract reusable skills from learnings
- **Knowledge Base Integration**: Connect with GitHub high-star project database
- **Automatic Skill Extraction**: Auto-create skills from recurring patterns
- **Periodic Review**: Regular review and promotion of learnings

## Setup

```bash
mkdir -p .learnings
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| Command/operation fails | Log to `.learnings/ERRORS.md` |
| User corrects you | Log to `.learnings/LEARNINGS.md` with category `correction` |
| User wants missing feature | Log to `.learnings/FEATURE_REQUESTS.md` |
| Found better approach | Log to `.learnings/LEARNINGS.md` with category `best_practice` |
| Recurring pattern detected | Extract as reusable skill |
| Knowledge gap identified | Search GitHub high-star projects for solutions |

## Logging Format

### Learning Entry

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

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
- See Also: LRN-20250110-001 (if related to existing entry)
- Pattern-Key: simplify.dead_code | harden.input_validation (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)
```

### Error Entry

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending

### Summary
Brief description of what failed

### Error
Actual error message or output

### Context
- Command/operation attempted
- Input or parameters used
- Environment details if relevant

### Suggested Fix
If identifiable, what might resolve this

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
```

## Skill Distillation Workflow

When a learning becomes valuable enough to be a reusable skill:

### Extraction Criteria

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Has `See Also` links to 2+ similar issues |
| **Verified** | Status is `resolved` with working fix |
| **Non-obvious** | Required actual debugging/investigation to discover |
| **Broadly applicable** | Not project-specific; useful across codebases |

### Extraction Process

1. **Identify candidate**: Learning meets extraction criteria
2. **Create skill directory**: `skills/<skill-name>/`
3. **Write SKILL.md**: Use standard skill format with YAML frontmatter
4. **Update learning**: Set status to `promoted_to_skill`, add `Skill-Path`
5. **Publish to ClawHub**: Share with community

## Knowledge Base Integration

Connect with GitHub high-star project database for research:

```markdown
### Research Query
- Topic: [subject to research]
- Related Projects: [list relevant projects]
- Search Strategy: [how to find solutions]
```

## Periodic Review

Review `.learnings/` at natural breakpoints:

- Before starting a new major task
- After completing a feature
- When working in an area with past learnings
- Weekly during active development

### Review Actions

- Resolve fixed items
- Promote applicable learnings
- Link related entries
- Escalate recurring issues
- Extract recurring patterns as skills

## Best Practices

1. **Log immediately** - context is freshest right after the issue
2. **Be specific** - future agents need to understand quickly
3. **Include reproduction steps** - especially for errors
4. **Link related files** - makes fixes easier
5. **Suggest concrete fixes** - not just "investigate"
6. **Use consistent categories** - enables filtering
7. **Promote aggressively** - if in doubt, add to CLAUDE.md or .github/copilot-instructions.md
8. **Review regularly** - stale learnings lose value
9. **Extract skills** - recurring patterns become reusable skills
10. **Connect to knowledge base** - research solutions from high-star projects
