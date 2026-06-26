# Workflow Patterns

Systematic task implementation using TDD, phase checkpoints, and structured commits. Ensures quality through red-green-refactor cycles, 80% coverage gates, and verification protocols before proceeding.

## What's Inside

- The TDD task lifecycle (11 steps: select → mark in progress → RED → GREEN → REFACTOR → verify coverage → document deviations → commit → update plan → commit plan → repeat)
- Phase completion protocol (identify changes, ensure coverage, run full suite, generate checklist, wait for approval, checkpoint commit)
- Quality gates (tests, coverage, linting, types, security)
- Git commit format with task traceability
- Handling deviations (scope addition, reduction, technical changes)
- Error recovery patterns
- Task status symbols

## When to Use

- Implementing features from a plan
- Following TDD methodology
- Tasks requiring quality verification
- Projects with coverage requirements
- Team workflows needing traceability

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/meta/workflow-patterns
```

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install workflow-patterns
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/meta/workflow-patterns .cursor/skills/workflow-patterns
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/meta/workflow-patterns ~/.cursor/skills/workflow-patterns
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/meta/workflow-patterns .claude/skills/workflow-patterns
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/meta/workflow-patterns ~/.claude/skills/workflow-patterns
```

---

Part of the [Meta](..) skill category.
