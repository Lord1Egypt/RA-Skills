# Skill Template

Template for creating skills extracted from engineering learnings. Copy and customize.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Concise description of the engineering problem this skill solves and when to use it. Include trigger conditions."
---

# Skill Name

Brief introduction explaining the engineering problem this skill addresses and its origin.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Build/test/deploy trigger] | [Action to take] |
| [Architecture/design trigger] | [Action to take] |

## Background

Why this engineering knowledge matters. What build failures, regressions, or architectural problems it prevents. Context from the original learning.

## Solution

### Step-by-Step

1. First step with command or code change
2. Second step
3. Verification step (run tests, check build, validate metrics)

### Code Example

\`\`\`language
// Example code demonstrating the engineering fix
\`\`\`

## Common Variations

- **Variation A**: Different CI environment or build tool
- **Variation B**: Different language or framework version

## Gotchas

- Warning about edge case in CI vs local
- Common mistake when applying this fix

## Related

- Link to relevant ADR
- Link to related coding standard
- Link to CI/CD runbook

## Source

Extracted from engineering learning entry.
- **Learning ID**: LRN-YYYYMMDD-XXX
- **Original Category**: architecture_debt | code_smell | performance_regression | dependency_issue | testing_gap | design_flaw
- **Extraction Date**: YYYY-MM-DD
```

---

## Minimal Template

For simple engineering skills that don't need all sections:

```markdown
---
name: skill-name-here
description: "What engineering problem this skill solves and when to use it."
---

# Skill Name

[Engineering problem statement in one sentence]

## Solution

[Direct fix with commands/code]

## Source

- Learning ID: LRN-YYYYMMDD-XXX
```

---

## Template with Scripts

For skills that include build/test/deploy helpers:

```markdown
---
name: skill-name-here
description: "What engineering problem this skill solves and when to use it."
---

# Skill Name

[Introduction]

## Quick Reference

| Command | Purpose |
|---------|---------|
| `./scripts/validate-build.sh` | [What it checks] |
| `./scripts/fix-deps.sh` | [What it fixes] |

## Usage

### Automated (Recommended)

\`\`\`bash
./skills/skill-name/scripts/validate-build.sh [args]
\`\`\`

### Manual Steps

1. Step one
2. Step two

## Scripts

| Script | Description |
|--------|-------------|
| `scripts/validate-build.sh` | Build validation |
| `scripts/fix-deps.sh` | Dependency resolver |

## Source

- Learning ID: LRN-YYYYMMDD-XXX
```

---

## Naming Conventions

- **Skill name**: lowercase, hyphens for spaces
  - Good: `circular-dependency-fix`, `n-plus-one-detection`, `ci-node-version-pin`
  - Bad: `Circular_Dependency_Fix`, `NPlusOneDetection`

- **Description**: Start with action verb, mention engineering trigger
  - Good: "Detects and fixes circular service dependencies. Use when build fails with circular import errors or tests can't isolate services."
  - Bad: "Architecture stuff"

- **Files**:
  - `SKILL.md` - Required, main documentation
  - `scripts/` - Optional, build/test/deploy helpers
  - `references/` - Optional, detailed ADRs or runbooks
  - `assets/` - Optional, templates

---

## Extraction Checklist

Before creating a skill from an engineering learning:

- [ ] Learning is verified (status: resolved, fix confirmed in CI)
- [ ] Solution is broadly applicable (not one-off project config)
- [ ] Content is complete (has all needed context including env details)
- [ ] Name follows conventions
- [ ] Description is concise but informative
- [ ] Quick Reference table is actionable
- [ ] Code examples are tested against CI
- [ ] Source learning ID is recorded

After creating:

- [ ] Update original learning with `promoted_to_skill` status
- [ ] Add `Skill-Path: skills/skill-name` to learning metadata
- [ ] Test skill by reading it in a fresh session
