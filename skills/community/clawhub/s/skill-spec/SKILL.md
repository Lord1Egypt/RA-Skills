---
name: skill-spec
description: Use when identifying skill candidates from repeated work, managing skill change proposals, reviewing candidates, or chaining skills into workflows. Also invoke directly to scaffold a new skill or review accumulated candidates.
---

# Skill Spec Engineering

## Overview

Skills are living specs that need continuous iteration. This methodology covers the full lifecycle: auto-detection → candidate logging → scaffolding → change management → downstream composition.

## Phase 1: Detection

### Hook-driven (0 tokens)

- **PostToolUse** (async) — increments counter + logs tool names, pure shell
- **Stop** — writes to `data/candidates.md` when threshold exceeded, injects one prompt (~30 tokens)

Default threshold: 15. Override: `SKILL_CANDIDATE_THRESHOLD=20`

### Candidate format

Auto-written to `data/candidates.md`:
```markdown
## 2026-05-03 | 23 calls | 6 tool types
- **Session:** abc123
- **Tools:** Bash,Edit,Write,Agent,WebFetch,Read
- **Status:** pending
```

### Review mode

When invoked directly, read candidates.md and for each pending entry:
1. Summarize key steps from the session
2. Evaluate three criteria: multi-step, multi-turn, repeatable
3. If YES → proceed to Phase 2 (Scaffold with duplicate check); if NO → mark skipped

## Phase 2: Scaffold

Before creating a new skill, check for duplicates:

1. Scan `~/.claude/skills/*/SKILL.md` frontmatter (name + description)
2. If a similar skill exists → create a **proposal** in that skill's CHANGE.md instead of a new skill
3. If no match → generate from `templates/SKILL.template.md`

```
~/.claude/skills/[new-skill-name]/
├── SKILL.md        # Generated from template, pre-filled with steps
└── CHANGE.md       # Empty, ready for proposals
```

## Phase 3: Change Management

### Two tiers

| Tier | Criteria | Process |
|------|----------|---------|
| **Patch** | Won't surprise users (wording, typo, edge case) | Direct edit + git commit |
| **Proposal** | Changes behavior (add/remove steps, reorder, change logic) | CHANGE.md → user review |

**Rule of thumb:** If someone using this skill would say "wait, what?" — it needs a proposal.

### Proposal format

```markdown
## #001 - [Title]
- **Status:** proposed | accepted | rejected | implemented
- **Date:** 2026-05-03
- **Trigger:** What scenario triggered this change
- **Proposal:** What to change + why
- **Breaking?:** yes/no
```

## Phase 4: Composition

### Next Steps format (append to each skill)

```markdown
## Next Steps
- **If [specific condition]**: invoke [skill-name] — [one-line reason]
- **If [other condition]**: invoke [another-skill] — [reason]
```

### Chains registry

`data/chains.md` records input/output relationships between skills:

```
[publisher-matcher] --{matched list}--> [publisher-review]
[publisher-review] --{confirmed list}--> [email-generator]
[email-generator] --{email content}--> [mail-send-batch]
```

After a skill completes, check chains.md for downstream → suggest to user.

## Quick Reference

| Phase | Trigger | Token cost | Output |
|-------|---------|-----------|--------|
| Detection | Every session (auto) | 0 (shell) | data/candidates.md |
| Scaffold | User confirms candidate | On-demand | New skill directory |
| Change | Issue found during use | 0 | CHANGE.md or direct commit |
| Composition | After skill execution | On-demand | Next Steps / chains.md |

## Common Mistakes

- **Treating patches as proposals** — fixing a typo doesn't need a proposal, just commit
- **Letting candidates pile up** — review periodically or they lose value
- **Vague chaining** — Next Steps must include specific conditions, not "you might want to use X"
- **Treating scaffold as final** — template output is a starting point, always customize
