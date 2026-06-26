---
name: skill-quality-auditor
description: Audit another Codex skill for structural compliance, trigger quality, instruction clarity, reuse of scripts or references, and overall maintainability. Use when Codex is given a skill folder and needs to judge whether the skill is qualified, explain why it passes or fails, and summarize strengths, weaknesses, blockers, and improvement ideas across multiple dimensions.
---

# Skill Quality Auditor

## Overview

Evaluate a target skill with a consistent rubric and return a clear pass/fail-style verdict plus a multi-dimensional review.
Prefer the bundled script for the first pass, then turn the raw findings into a concise human-readable assessment.

## Workflow

1. Identify the target skill folder.
2. Run `scripts/evaluate_skill.py <path-to-skill>`.
3. Read the report and group findings into:
   - final verdict
   - strengths
   - weaknesses
   - critical blockers
   - recommended fixes
4. If the script reports missing context or borderline results, inspect the target skill's `SKILL.md` and any referenced resources before writing the final judgment.
5. Keep the final answer decisive: say whether the skill is currently qualified, conditionally qualified, or not qualified.

## Rubric

Score the skill across these dimensions:

- `structure`: required files, frontmatter validity, naming, obvious TODO placeholders
- `triggering`: whether `description` clearly explains what the skill does and when to use it
- `workflow`: whether the body gives actionable steps instead of vague guidance
- `progressive_disclosure`: whether detailed material is kept in scripts or references instead of bloating `SKILL.md`
- `resources`: whether scripts, references, and assets are included only when useful and are mentioned in the body
- `examples_and_outputs`: whether the skill helps the agent understand expected usage or output shape
- `maintainability`: clarity, concision, stale metadata checks, and overall ease of iteration

Use [references/rubric.md](./references/rubric.md) when you need the detailed scoring logic and interpretation rules.

## Verdict Rules

Use these labels:

- `Qualified`: no critical blockers and score is strong enough for immediate use
- `Borderline`: usable but needs material fixes soon
- `Not Qualified`: missing required structure or too weak to trust in repeated use

Treat these as critical blockers:

- missing `SKILL.md`
- invalid or missing YAML frontmatter
- missing `name` or `description`
- unresolved template placeholders such as `TODO`
- description too weak to trigger reliably
- instructions too incomplete to execute the core task safely

## Output Shape

Prefer this response shape:

### Verdict

State `Qualified`, `Borderline`, or `Not Qualified` in the first sentence and explain the main reason.

### Score Summary

Include the total score and 3-5 highest-signal dimension notes.

### What Works Well

List concrete strengths tied to files or sections.

### What Needs Work

List concrete weaknesses tied to files or sections.

### Next Fixes

List the smallest set of changes most likely to move the skill to `Qualified`.

## Script

Run:

```bash
python3 scripts/evaluate_skill.py /absolute/path/to/skill
```

Optional JSON mode:

```bash
python3 scripts/evaluate_skill.py /absolute/path/to/skill --json
```

The script is dependency-free and performs a deterministic first-pass audit. It is intentionally conservative: if a skill barely explains its trigger conditions or still contains template leftovers, the script should flag it instead of assuming good intent.

## Review Rules

- Prefer evidence over taste.
- Praise strengths explicitly; do not only list problems.
- Distinguish hard failures from improvement opportunities.
- If the target skill intentionally omits scripts, references, or agents metadata, do not penalize that by itself.
- Penalize unused or stale directories when they add confusion.
- When inferring quality from wording, cite the exact section or file that led to the conclusion.

## Trigger Examples

- "Check whether this skill is规范合格."
- "Review this skill and tell me if it passes."
- "Audit this skill folder and summarize the good and bad."
- "Evaluate this skill against best practices and give me a verdict."
