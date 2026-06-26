# Skill Starter

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> A scaffolding CLI for OpenClaw skills that creates a clean project shell with security-minded defaults.

| Item | Value |
| --- | --- |
| Package | `@mike007jd/openclaw-skill-starter` |
| Runtime | Node.js 18+ |
| Interface | CLI + project generator |
| Templates | `standard`, `strict-security` |

## Why this exists

The first version of a skill usually decides whether the project stays clean or accumulates ad hoc files and missing guardrails. Skill Starter gives you a repeatable project layout with a ready-to-edit `SKILL.md`, test stub, changelog, fixture data, and optional CI workflow.

## What it generates

- A normalized package layout for new OpenClaw skills
- `SKILL.md` with frontmatter and safety guidance
- `docs/`, `scripts/`, `.env.example`, and `CHANGELOG.md`
- A smoke test scaffold under `tests/`
- A profiling fixture and helper script
- Optional GitHub Actions security scan workflow
- A stricter template with `.openclaw-tools/safe-install.policy.json`

## Primary workflow

1. Pick a skill name and template.
2. Generate the project with or without prompts.
3. Fill in business logic, policy, and docs.
4. Run the included smoke test and wire in real linting.

## Quick start

```bash
git clone https://github.com/mike007jd/openclaw-skills.git
cd openclaw-skills/skill-starter
npm install
node ./bin/create-openclaw-skill.js review-assistant --no-prompts --template strict-security --ci --out /tmp
```

## Command

| Command | Purpose |
| --- | --- |
| `create-openclaw-skill <name> [--template <standard|strict-security>] [--ci] [--no-prompts] [--force] [--out <dir>]` | Generate a new skill project |

## Generated shape

```text
<skill-name>/
├── SKILL.md
├── docs/README.md
├── scripts/README.md
├── fixtures/profile-input.json
├── tests/smoke.test.js
├── .env.example
└── CHANGELOG.md
```

## Template choice

| Template | When to use it |
| --- | --- |
| `standard` | Fast internal prototypes and general-purpose skills |
| `strict-security` | Skills that need safer defaults, CI scanning, and policy scaffolding |

## Project layout

```text
skill-starter/
├── bin/
├── src/
├── test.js
└── SKILL.md
```

## Status

Skill Starter is intentionally opinionated but lightweight. It focuses on getting a new skill into a reviewable shape quickly rather than generating a complete production system.
