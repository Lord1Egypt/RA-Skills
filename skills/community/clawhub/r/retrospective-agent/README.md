# retrospective-agent

Structured retrospectives and execution-memory hygiene for OpenClaw agents.

## Goal

Capture reusable execution lessons without creating hidden memory, duplicate truth, or fake autonomy.

## What belongs here

- repeated corrections
- workflow improvements
- tool failure patterns
- success patterns worth repeating
- scoped project or domain lessons

## What does not belong here

- factual continuity already covered by `memory/YYYY-MM-DD.md` or `MEMORY.md`
- identity or values
- secrets or credentials
- silent behavior changes

## Data location

Operational notes for this skill live under:

- `workspace/ops/retrospective-agent/`

Suggested structure:

```text
workspace/ops/retrospective-agent/
├── corrections.md
├── weekly/
│   └── README.md
├── domains/
│   ├── communication.md
│   ├── ops.md
│   ├── research.md
│   └── writing.md
├── projects/
│   └── README.md
└── templates/
    ├── post-task-retro.md
    ├── weekly-retro.md
    └── lesson-entry.md
```

## Modes

### Post-task retro
Short review after meaningful work.

### Correction logging
Capture explicit reusable corrections.

### Weekly retro
Summarize recurring wins, misses, and candidate improvements.

## Promotion model

- observed
- repeated
- candidate rule
- confirmed rule

Conservative by design. Recommend promotions, do not silently enforce them.

## Guardrails

- never rewrite persona files
- never patch config
- never send messages
- never infer preferences from silence
- never create hidden memory

## First-pass references

- `references/workflow.md`
- `references/promotion-rules.md`
- `references/boundaries.md`

## Templates

Skill templates:
- `assets/templates/post-task-retro.md`
- `assets/templates/weekly-retro.md`
- `assets/templates/lesson-entry.md`

Operational templates:
- `workspace/ops/retrospective-agent/templates/post-task-retro.md`
- `workspace/ops/retrospective-agent/templates/weekly-retro.md`
- `workspace/ops/retrospective-agent/templates/lesson-entry.md`
es/lesson-entry.md`
