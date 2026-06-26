# skill-distill

Merge N overlapping skills into 1 distilled skill. Input: skills. Output: skill.

## Problem

When multiple skills cover similar ground (e.g., three separate writing-improvement skills), users face routing ambiguity ("which one do I load?") and context budget waste (redundant content loaded multiple times). Distillation consolidates overlapping skills into a single entry point.

## How it works

4-phase process, each phase must complete before the next begins:

1. **Collect** -- Read all source skills, build inventory table (lines, sections, references, unique contributions)
2. **Analyze** -- Cross-reference every knowledge point across sources. Classify as intersection / unique contribution / conflict / redundant
3. **Confirm** -- Present distillation plan to user. Conflicts require human decision. NEVER auto-generate without confirmation
4. **Generate** -- Write the distilled skill, then validate via improvement-learner (accuracy >= 0.80 required)

## Directory structure

```
skill-distill/
├── SKILL.md                           # Main skill definition (workflow, rules, examples)
├── README.md                          # This file
├── references/
│   └── distillation-checklist.md      # Decision matrix and post-distillation checklist
└── .improvement-memory/               # Auto-generated quality tracking (do not edit)
```

## Key constraints

- Distilled SKILL.md body must be <= 500 lines; long-tail content goes to `references/`
- Only merge skills with >= 30% content overlap (see decision matrix in checklist)
- Every section in the output must be traceable to its source skill(s)
- Phase 4 validation via improvement-learner is mandatory, not optional

## Related skills

- `skill-creator` -- Creation spec that distilled skills must follow
- `skill-forge` -- Generate task_suite.yaml for the distilled skill
- `improvement-orchestrator` -- Post-distillation quality optimization
- `improvement-learner` -- Structural scoring (6 dimensions) used in Phase 4
- `improvement-evaluator` -- Execution-based validation via task suites

## License

MIT
