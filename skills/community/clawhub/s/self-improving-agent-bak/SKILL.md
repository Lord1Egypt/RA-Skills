---
name: self-improvement
description: "Captures learnings, errors, and corrections for continuous improvement. Use when: (1) a command fails, (2) user corrects you, (3) user requests a missing capability, (4) an API/tool fails, (5) knowledge is outdated, (6) a better approach is found. Also review learnings before major tasks."
metadata:
---

# Self-Improvement Skill

Log learnings to `.learnings/` for continuous improvement. Promote broadly applicable entries to workspace files.

## Setup

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Create three log files: `LEARNINGS.md` · `ERRORS.md` · `FEATURE_REQUESTS.md`

## Routing Table

| Situation | File | Category |
|---|---|---|
| Command/operation fails | `ERRORS.md` | — |
| User corrects you | `LEARNINGS.md` | `correction` |
| Missing capability requested | `FEATURE_REQUESTS.md` | — |
| Knowledge was outdated | `LEARNINGS.md` | `knowledge_gap` |
| Found better approach | `LEARNINGS.md` | `best_practice` |
| Recurring pattern (simplify-and-harden) | `LEARNINGS.md` | `Source: simplify-and-harden` + `Pattern-Key` |

## Promotion Targets

| Learning Type | Promote To |
|---|---|
| Behavioral patterns | `SOUL.md` |
| Workflow improvements | `AGENTS.md` |
| Tool gotchas | `TOOLS.md` |
| Project facts / conventions | `CLAUDE.md` |

Promote when: applies across multiple files, prevents recurring mistakes, or any contributor should know it.

## Log Formats

### LEARNINGS.md entry
```markdown
## [LRN-YYYYMMDD-XXX] category
**Logged**: ISO-8601  **Priority**: low|medium|high|critical  **Status**: pending  **Area**: frontend|backend|infra|tests|docs|config

### Summary
One-line description

### Details
What happened, what was wrong, what's correct

### Suggested Action
Specific fix or improvement

### Metadata
- Source: conversation|error|user_feedback
- Related Files:
- Tags:
- See Also: (if related entry exists)
- Pattern-Key: (optional, for recurring patterns)
- Recurrence-Count: 1
---
```

### ERRORS.md entry
```markdown
## [ERR-YYYYMMDD-XXX] command_name
**Logged**: ISO-8601  **Priority**: high  **Status**: pending  **Area**: …

### Summary / Error / Context / Suggested Fix
### Metadata
- Reproducible: yes|no|unknown
- See Also:
---
```

### FEATURE_REQUESTS.md entry
```markdown
## [FEAT-YYYYMMDD-XXX] capability_name
**Logged**: ISO-8601  **Priority**: medium  **Status**: pending  **Area**: …

### Requested Capability / User Context / Complexity Estimate / Suggested Implementation
### Metadata
- Frequency: first_time|recurring
---
```

## Resolving Entries

Change `**Status**: pending` → `resolved` | `in_progress` | `wont_fix` | `promoted`, then add:
```markdown
### Resolution
- **Resolved**: ISO-8601
- **Notes**: what was done
```

## Recurring Pattern Detection

1. Search first: `grep -r "keyword" .learnings/`
2. If similar entry exists: increment `Recurrence-Count`, update `Last-Seen`, add `See Also`
3. Promote to system prompt files when: `Recurrence-Count >= 3` + seen in 2+ tasks + within 30 days

## Periodic Review

```bash
grep -h "Status\*\*: pending" .learnings/*.md | wc -l          # count pending
grep -B5 "Priority\*\*: high" .learnings/*.md | grep "^## \["  # list high-priority
```

Review before major tasks, after completing features, or weekly during active development.

## Detection Triggers

- **Correction**: "No, that's wrong…" / "Actually…" → `LEARNINGS.md` `correction`
- **Feature request**: "Can you also…" / "I wish you could…" → `FEATURE_REQUESTS.md`
- **Knowledge gap**: user provides info you didn't know → `LEARNINGS.md` `knowledge_gap`
- **Error**: non-zero exit / exception / timeout → `ERRORS.md`

## Skill Extraction

Extract a learning into a reusable skill when: recurring (2+ `See Also` links) + resolved + non-obvious + broadly applicable.

```bash
./skills/self-improvement/scripts/extract-skill.sh skill-name
```

Or manually: create `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`).

## Priority / Area Reference

Priority: `critical` (blocks core / data loss) · `high` (common workflow) · `medium` (workaround exists) · `low` (edge case)

Area: `frontend` · `backend` · `infra` · `tests` · `docs` · `config`
