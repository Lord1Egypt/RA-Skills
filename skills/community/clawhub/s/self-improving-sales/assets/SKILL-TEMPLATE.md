# Sales Skill Template

Template for creating sales skills extracted from learnings and deal reviews. Copy and customize.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Concise description of the sales skill and when to use it. Include trigger conditions."
---

# Skill Name

Brief introduction explaining the sales problem this skill addresses and its origin.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Sales trigger 1] | [Response or process 1] |
| [Sales trigger 2] | [Response or process 2] |

## Background

Why this sales knowledge matters. What deals it helps win. What revenue impact it has. Context from the original finding.

## The Approach

### Step-by-Step

1. First step with talk track or process change
2. Second step
3. Verification step (deal outcome, conversion rate, feedback)

### Talk Track Example

> **Prospect**: "[Objection or question]"
>
> **Rep**: "[Proven response]"
>
> **Follow-up**: "[Question to advance the conversation]"

## Common Variations

- **Variation A**: Different segment or deal size specifics
- **Variation B**: Alternative approach for different buyer persona

## Gotchas

- Warning or common mistake when applying this approach
- Edge case to watch for
- **NEVER** log customer PII or exact contract values

## Related

- Related battle card or objection handler
- Related qualification framework section
- Related pricing playbook entry

## Source

Extracted from sales learning or deal review.
- **Entry ID**: LRN-YYYYMMDD-XXX or DEAL-YYYYMMDD-XXX
- **Original Category**: objection_pattern | pipeline_leak | pricing_error | competitor_shift
- **Extraction Date**: YYYY-MM-DD
```

---

## Minimal Template

For simple sales skills:

```markdown
---
name: skill-name-here
description: "What this sales skill does and when to use it."
---

# Skill Name

[Sales problem statement in one sentence]

## Approach

[Talk track, process change, or qualification criteria]

## Source

- Entry ID: LRN-YYYYMMDD-XXX or DEAL-YYYYMMDD-XXX
```

---

## Template with Scripts

For sales skills that include analysis or detection helpers:

```markdown
---
name: skill-name-here
description: "What this sales skill does and when to use it."
---

# Skill Name

[Introduction]

## Quick Reference

| Command | Purpose |
|---------|---------|
| `./scripts/analyze.sh` | [What it analyzes] |
| `./scripts/detect.sh` | [What it detects] |

## Usage

### Automated (Recommended)

\`\`\`bash
./skills/skill-name/scripts/analyze.sh [target]
\`\`\`

### Manual Steps

1. Step one
2. Step two

## Scripts

| Script | Description |
|--------|-------------|
| `scripts/analyze.sh` | Pipeline or deal pattern analyzer |
| `scripts/detect.sh` | Objection or competitive signal detector |

## Source

- Entry ID: LRN-YYYYMMDD-XXX
```

---

## Naming Conventions

- **Skill name**: lowercase, hyphens for spaces
  - Good: `incumbent-displacement`, `enterprise-procurement-nav`, `budget-freeze-objection`
  - Bad: `IncumbentDisplacement`, `budget_freeze`, `objection1`

- **Description**: Start with action verb, mention sales trigger
  - Good: "Handles 'we already have a vendor' objection with differentiation framework. Use when prospect raises incumbent vendor during discovery or negotiation."
  - Bad: "Sales stuff"

- **Files**:
  - `SKILL.md` - Required, main documentation
  - `scripts/` - Optional, analysis and detection helpers
  - `references/` - Optional, detailed case studies
  - `assets/` - Optional, templates

---

## Extraction Checklist

Before creating a skill from a sales finding:

- [ ] Approach is verified (status: resolved, used successfully in 2+ deals)
- [ ] Solution is broadly applicable (not one-off deal or customer quirk)
- [ ] **No customer PII, exact contract values, or confidential terms**
- [ ] Content is complete (has all needed context for a rep to execute)
- [ ] Name follows conventions
- [ ] Description is concise but includes sales triggers
- [ ] Quick Reference table maps situations to actions
- [ ] Talk track examples are realistic and tested
- [ ] Source entry ID is recorded

After creating:

- [ ] Update original entry with `promoted_to_skill` status
- [ ] Add `Skill-Path: skills/skill-name` to entry metadata
- [ ] Test skill by reading it in a fresh session
- [ ] Verify no customer-sensitive data leaked into the skill
- [ ] Share with sales team for feedback
