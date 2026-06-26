# Skill Architecture Levels

Not every skill needs every folder. Choose the smallest architecture that reliably supports the work.

## Level 1 — Documentation Skill

Use when the skill is mostly guidance.

```text
my-skill/
└── SKILL.md
```

Good for:
- decision frameworks
- writing guidance
- troubleshooting heuristics

## Level 2 — Reference-Backed Skill

Use when the skill needs conditional or heavy docs.

```text
my-skill/
├── SKILL.md
├── project.skill.template.md
└── references/
```

Good for:
- API or schema guidance
- multiple variants/frameworks
- local setup that differs by repo

## Level 3 — Operational Skill

Use when deterministic repeated operations should be scripted.

```text
my-skill/
├── SKILL.md
├── project.skill.template.md
├── references/
├── scripts/
└── tests/
```

Good for:
- file generation
- formatting/export steps
- repeatable CLI workflows

## Level 4 — Resilient Operational Skill

Use when a narrow class of common failures can be remediated safely.

```text
my-skill/
├── SKILL.md
├── project.skill.template.md
├── references/
├── scripts/
├── tests/
└── self-healing/
```

Good for:
- creating a missing output directory
- generating a harmless config stub
- repairing a known local setup precondition

## Escalation rule

Start small. Add the next level only when it eliminates repeated failure, repeated code writing, or repeated confusion.

## Warning

Self-healing is not a license for broad mutation. If the fix is risky, ambiguous, or project-sensitive, stop and ask instead of auto-healing.
