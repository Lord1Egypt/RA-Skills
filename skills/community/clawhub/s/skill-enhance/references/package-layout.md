# Package Layout

Use this file when the user wants a standard file tree for a reusable skill.

## Canonical Layout

```text
skill-name/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── evals/
│   └── evals.json
└── references/
    ├── trigger-design.md
    ├── output-contracts.md
    ├── review-checklist.md
    ├── publish-readiness.md
    ├── artifact-matrix.md
    ├── skill-packaging.md
    ├── workflows.md
    └── package-layout.md
```

## File Responsibilities

- `SKILL.md`: the agent-facing operating instructions
- `README.md`: the human-facing overview
- `agents/openai.yaml`: display metadata and default prompt
- `evals/evals.json`: realistic test prompts for review
- `references/`: focused supporting docs loaded only when relevant

## Layout Rule

Use the full layout for reusable or published skills.
Use a lighter layout only for small local experiments.
