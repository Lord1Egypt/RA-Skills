# Self-Optimization

`self-optimization` is a skill package for turning real work into durable improvements.

It helps an agent or team move beyond one-off note taking by capturing meaningful lessons, linking recurring incidents, promoting stable rules into guidance files, and extracting reusable skills when patterns are proven.

## What It Does

- captures corrections, knowledge gaps, and better approaches
- records non-obvious command and tool failures
- tracks missing capabilities as feature requests
- links repeated incidents with stable metadata
- promotes proven patterns into durable workspace or repo guidance
- supports extracting reusable skills from repeated learnings

## Core Loop

1. Detect meaningful signal during work.
2. Capture it in `.learnings/`.
3. De-duplicate and connect related entries.
4. Promote stable rules into guidance files.
5. Extract reusable skills when a pattern becomes portable.

## Directory Layout

```text
self-optimization/
├── .learnings/
│   ├── ERRORS.md
│   ├── FEATURE_REQUESTS.md
│   └── LEARNINGS.md
├── assets/
│   ├── LEARNINGS.md
│   └── SKILL-TEMPLATE.md
├── hooks/
│   └── openclaw/
│       ├── handler.js
│       ├── handler.ts
│       └── HOOK.md
├── references/
│   ├── examples.md
│   ├── hooks-setup.md
│   └── openclaw-integration.md
├── scripts/
│   ├── activator.sh
│   ├── error-detector.sh
│   └── extract-skill.sh
├── README.md
├── SKILL.md
└── _meta.json
```

## Key Files

- [SKILL.md](./SKILL.md): main skill definition and operating model
- [references/examples.md](./references/examples.md): concrete examples for learnings, errors, feature requests, promotion, and skill extraction
- [references/openclaw-integration.md](./references/openclaw-integration.md): OpenClaw installation and workspace integration
- [references/hooks-setup.md](./references/hooks-setup.md): hook configuration for Claude Code, Codex, and related setups
- [scripts/extract-skill.sh](./scripts/extract-skill.sh): helper for scaffolding a skill from a durable learning

## Quick Start

### Install In OpenClaw

```bash
clawdhub install self-optimization
```

Or install manually:

```bash
cp -r self-optimization ~/.openclaw/skills/
```

### Create The Learning Inbox

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Use these files:

- `LEARNINGS.md` for corrections, conventions, and better patterns
- `ERRORS.md` for non-obvious failures and debugging discoveries
- `FEATURE_REQUESTS.md` for missing capabilities worth tracking

### Optional Hook

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-optimization
openclaw hooks enable self-optimization
```

## When To Use It

Use `self-optimization` when:

- the user corrects the agent
- a command fails in a non-obvious way
- a stronger workflow or implementation pattern is discovered
- the same issue appears across multiple tasks
- the user asks for a capability that does not exist yet
- a lesson should become durable repo or workspace guidance

Do not use it for trivial one-off noise that is unlikely to matter again.

## Promotion Targets

Promote stable lessons out of `.learnings/` when they become rules:

- `CLAUDE.md` for project facts and conventions
- `AGENTS.md` for workflows and delegation patterns
- `TOOLS.md` for tool behavior and environment gotchas
- `SOUL.md` for behavioral rules in OpenClaw workspaces
- `.github/copilot-instructions.md` for Copilot-facing repo guidance

## Skill Extraction

When a pattern is repeatable and broadly useful, scaffold a new skill:

```bash
./skills/self-optimization/scripts/extract-skill.sh my-new-skill --dry-run
./skills/self-optimization/scripts/extract-skill.sh my-new-skill
```

Then fill in the generated `SKILL.md` with the stable workflow, examples, and caveats.

## Supporting Files

- [assets/LEARNINGS.md](./assets/LEARNINGS.md) provides a stronger learning template
- [assets/SKILL-TEMPLATE.md](./assets/SKILL-TEMPLATE.md) helps convert proven lessons into standalone skills
- [scripts/activator.sh](./scripts/activator.sh) emits a lightweight reminder after prompt submission
- [scripts/error-detector.sh](./scripts/error-detector.sh) emits a reminder when tool output looks like a meaningful failure

## Design Goal

This package is designed to make improvement operational:

- not just "remember this"
- but "capture it, connect it, promote it, and reuse it"
