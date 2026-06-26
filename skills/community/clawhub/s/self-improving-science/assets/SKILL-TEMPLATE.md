# Skill Template (Science)

Template for creating skills extracted from research learnings. Copy and customize.

---

## SKILL.md Template

```markdown
---
name: skill-name-here
description: "Concise description of when and why to use this skill. Include trigger conditions."
---

# Skill Name

Brief introduction explaining the research problem this skill solves and its origin.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Trigger 1] | [Action 1] |
| [Trigger 2] | [Action 2] |

## Background

Why this knowledge matters. What methodology mistakes it prevents. Context from the original learning or experiment.

## Solution

### Step-by-Step

1. First step with code or command
2. Second step
3. Verification step (include expected metric ranges)

### Code Example

\`\`\`python
# Example code demonstrating the solution
# Include library versions in comments
import pandas as pd  # >= 2.0
import sklearn  # >= 1.3
\`\`\`

## Common Variations

- **Variation A**: Different dataset type or scale
- **Variation B**: Different ML framework or statistical test

## Gotchas

- Warning or common mistake #1 (include metric impact if known)
- Warning or common mistake #2

## Related

- Link to related methodology documentation
- Link to related skill or experiment checklist

## Source

Extracted from learning entry.
- **Learning ID**: LRN-YYYYMMDD-XXX
- **Original Category**: methodology_flaw | data_quality | statistical_error | etc.
- **Dataset**: dataset_name (if applicable)
- **Extraction Date**: YYYY-MM-DD
```

---

## Minimal Template

For simple skills that don't need all sections:

```markdown
---
name: skill-name-here
description: "What this skill does and when to use it."
---

# Skill Name

[Problem statement in one sentence]

## Solution

[Direct solution with code/commands, including library versions]

## Source

- Learning ID: LRN-YYYYMMDD-XXX
```

---

## Template with Scripts

For skills that include executable helpers (data validation, leakage detection, etc.):

```markdown
---
name: skill-name-here
description: "What this skill does and when to use it."
---

# Skill Name

[Introduction]

## Quick Reference

| Command | Purpose |
|---------|---------|
| `./scripts/validate-data.sh` | [What it checks] |
| `./scripts/check-leakage.py` | [What it detects] |

## Usage

### Automated (Recommended)

\`\`\`bash
./skills/skill-name/scripts/validate-data.sh path/to/dataset.csv
\`\`\`

### Manual Steps

1. Step one
2. Step two

## Scripts

| Script | Description |
|--------|-------------|
| `scripts/validate-data.sh` | Data quality checks |
| `scripts/check-leakage.py` | Feature-target leakage detection |

## Source

- Learning ID: LRN-YYYYMMDD-XXX
```

---

## Naming Conventions

- **Skill name**: lowercase, hyphens for spaces
  - Good: `leakage-detection`, `normality-checks`, `model-card-template`
  - Bad: `Leakage_Detection`, `NormalityChecks`

- **Description**: Start with action verb, mention trigger
  - Good: "Detects data leakage in train/test splits. Use when feature-target correlation is suspiciously high."
  - Bad: "Data stuff"

- **Files**:
  - `SKILL.md` — Required, main documentation
  - `scripts/` — Optional, executable code (validation, detection)
  - `references/` — Optional, detailed methodology docs
  - `assets/` — Optional, templates and data schemas

---

## Extraction Checklist

Before creating a skill from a learning:

- [ ] Learning is verified (status: resolved, fix validated with data)
- [ ] Solution is broadly applicable (not dataset-specific)
- [ ] Content is complete (has all needed context and metrics)
- [ ] Statistical claims include sample sizes and effect sizes
- [ ] Name follows conventions
- [ ] Description is concise but informative
- [ ] Quick Reference table is actionable
- [ ] Code examples include library version requirements

After creating:

- [ ] Update original learning with `promoted_to_skill` status
- [ ] Add `Skill-Path: skills/skill-name` to learning metadata
- [ ] Test skill by reading it in a fresh session
