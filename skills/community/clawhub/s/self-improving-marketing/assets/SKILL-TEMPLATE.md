# Marketing Skill Template

Template for creating marketing skills extracted from learnings and campaign insights. Copy and customize.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Concise description of the marketing skill and when to use it. Include trigger conditions."
---

# Skill Name

Brief introduction explaining the marketing problem this skill addresses and its origin.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Marketing trigger 1] | [Recommended action 1] |
| [Marketing trigger 2] | [Recommended action 2] |

## Background

Why this marketing knowledge matters. What campaign failures, audience misalignment, or brand risks it prevents. Context from the original finding.

## Playbook

### Step-by-Step

1. First action step with specific metric or threshold
2. Second step
3. Verification step (analytics check, A/B test, brand review)

### Example

**Before (underperforming):**
- Channel: [channel]
- CTR: X.X% (below Y.Y% benchmark)
- Messaging: [problematic approach]

**After (optimized):**
- CTR: X.X% (above benchmark)
- Messaging: [improved approach]
- Lift: +XX%

## Common Variations

- **Variation A**: Different channel or segment specifics
- **Variation B**: Alternative messaging or targeting approach

## Gotchas

- Warning or common mistake during optimization #1
- Warning or common mistake during optimization #2
- **NEVER** log customer PII — always redact before documenting

## Benchmarks

| Metric | Poor | Average | Good | Excellent |
|--------|------|---------|------|-----------|
| CTR | <0.5% | 0.5-1.0% | 1.0-2.0% | >2.0% |
| CVR | <1% | 1-3% | 3-5% | >5% |
| CPL | >$XXX | $XX-$XXX | $XX-$XX | <$XX |

## Source

Extracted from marketing learning or campaign issue entry.
- **Entry ID**: LRN-YYYYMMDD-XXX or CMP-YYYYMMDD-XXX
- **Original Category**: messaging_miss | channel_underperformance | audience_drift | brand_inconsistency | attribution_gap | content_decay
- **Extraction Date**: YYYY-MM-DD
```

---

## Minimal Template

For simple marketing skills:

```markdown
---
name: skill-name-here
description: "What this marketing skill does and when to use it."
---

# Skill Name

[Marketing problem statement in one sentence]

## Playbook

[Direct fix with specific actions, metrics, and thresholds]

## Source

- Entry ID: LRN-YYYYMMDD-XXX or CMP-YYYYMMDD-XXX
```

---

## Template with Scripts

For marketing skills that include monitoring or audit helpers:

```markdown
---
name: skill-name-here
description: "What this marketing skill does and when to use it."
---

# Skill Name

[Introduction]

## Quick Reference

| Command | Purpose |
|---------|---------|
| `./scripts/audit.sh` | [What it audits] |
| `./scripts/monitor.sh` | [What it monitors] |
| `./scripts/report.sh` | [What it reports] |

## Usage

### Automated (Recommended)

\`\`\`bash
./skills/skill-name/scripts/audit.sh [target]
\`\`\`

### Manual Steps

1. Step one
2. Step two

## Scripts

| Script | Description |
|--------|-------------|
| `scripts/audit.sh` | Brand consistency or attribution auditor |
| `scripts/monitor.sh` | Performance threshold monitor |
| `scripts/report.sh` | Campaign performance summary generator |

## Source

- Entry ID: CMP-YYYYMMDD-XXX
```

---

## Naming Conventions

- **Skill name**: lowercase, hyphens for spaces
  - Good: `enterprise-messaging-framework`, `email-deliverability-checklist`, `utm-taxonomy-standard`
  - Bad: `Enterprise_Messaging`, `EmailDeliverability`

- **Description**: Start with action verb, mention marketing trigger
  - Good: "Standardizes enterprise messaging to lead with ROI metrics. Use when launching campaigns targeting enterprise segment."
  - Bad: "Enterprise marketing stuff"

- **Files**:
  - `SKILL.md` - Required, main documentation
  - `scripts/` - Optional, audit and monitoring scripts
  - `references/` - Optional, benchmark data and examples
  - `assets/` - Optional, templates

---

## Extraction Checklist

Before creating a skill from a marketing finding:

- [ ] Finding is verified (status: resolved, improvement measured)
- [ ] Solution is broadly applicable (not campaign-specific one-off)
- [ ] **No customer PII, revenue figures, or ad account credentials in any content**
- [ ] Content is complete (has all needed context, metrics, and benchmarks)
- [ ] Name follows conventions
- [ ] Description is concise but includes marketing triggers
- [ ] Quick Reference table maps situations to actions
- [ ] Before/after metrics are included
- [ ] Benchmarks are realistic for the channel and segment
- [ ] Source entry ID is recorded

After creating:

- [ ] Update original entry with `promoted_to_skill` status
- [ ] Add `Skill-Path: skills/skill-name` to entry metadata
- [ ] Test skill by reading it in a fresh session
- [ ] Verify no sensitive data leaked into the skill
