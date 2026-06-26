# Skill Inspector Workflow

This document guides deep analysis of candidate skills.

## Purpose

Analyze candidate skills beyond name and description to determine precise fit for the task.

## Input

- `01-intent.md` - Required capabilities and constraints
- `02-candidates.md` - List of candidate skills

## Process

For each candidate skill:

### 1. Read SKILL.md

Read the full SKILL.md file from the candidate's path.

### 2. Extract Information

Extract and record:

- **Capabilities**: What can this skill do?
- **IO Contract**: What inputs does it accept? What outputs does it produce?
- **Phase**: ingest / transform / synthesize / other
- **Dependencies**: Does it require other skills or tools?
- **Constraints**: Any limitations or requirements?

### 3. Evaluate Fit

For each required capability from `01-intent.md`:

- Does this skill provide it directly?
- Does it provide something similar that could work?
- Is there a gap?

### 4. Check Compatibility

If multiple skills are selected:

- Do their IO contracts chain properly?
- Are there conflicts in approach?

## Output

Produce `03-inspection.md` with the following structure:

```markdown
# Skill Inspection Report

## Task Summary
<Brief recap of required capabilities>

## Inspected Skills

### <skill_name>

**Path**: `<path>`

**Capabilities**
- <capability 1>
- <capability 2>

**IO Contract**
- Input: <types>
- Output: <types>

**Phase**: ingest / transform / synthesize

**Coverage**
| Required | Status | Notes |
|----------|--------|-------|
| <cap_1> | covered / partial / missing | <detail> |

**Verdict**: recommended / partial / not-recommended

---

### <skill_name>
...

## Summary

### Coverage Matrix
| Required Capability | Best Skill | Status |
|---------------------|------------|--------|
| <cap_1> | <skill> | covered |
| <cap_2> | <skill> | covered |
| <cap_3> | - | missing |

### Gaps
- <missing capability>: <recommendation>

### Recommendation
native / single-skill / orchestration / cannot-fulfill

<Explanation of recommendation>
```

## Guidelines

- Be precise about IO contracts - this determines if skills can chain
- Note any assumptions or uncertainties
- If a skill is clearly not a fit, state why briefly
- Focus on practical fit, not theoretical possibilities
