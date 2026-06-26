---
name: skillforge
description: Generate and audit OpenClaw agent skills from natural language. Use when the operator asks to create a skill, build a skill, generate a skill, audit a skill, or check skill quality. Provides both free template-based generation and Pro AI-powered generation with quality assessment. Triggers on phrases like "create a skill", "generate a skill", "build a skill", "audit a skill", "check this skill", "make a skill for", "skillforge".
---

# SkillForge — Skill Generator & Auditor

Generate complete, publish-ready OpenClaw agent skills from natural language descriptions. Audit existing skills for quality, safety, and completeness.

## Prerequisites

SkillForge CLI must be installed globally:
```bash
npm install -g @shadoprizm/skillforge@latest
```

Check version: `skillforge --version` (requires 0.3.2+)

## Commands

### Generate a Skill

**Free tier** (template scaffold, no API key):
```bash
skillforge "<description>" --output <path> --lang <typescript|javascript|python>
```

**Pro tier** (AI-powered, requires API key):
```bash
skillforge "<description>" --pro --output <path> --lang <typescript|javascript|python>
```

### Audit a Skill

```bash
skillforge audit <path> --format <table|json|markdown>
```

Pro audit with AI analysis:
```bash
skillforge audit <path> --pro --format markdown
```

### Publish to ClawHub

First-time auth:
```bash
clawhub login
```

Then publish:
```bash
skillforge "<description>" --output <path> --publish
```

Or publish an existing skill:
```bash
clawhub publish <path> --slug <slug> --name "<name>" --version <semver>
```

## Workflow

### When asked to create/generate a skill:

1. Clarify the skill purpose if the description is vague
2. Run `skillforge "<description>" --pro --output /tmp/skillforge-gen --lang typescript`
3. Read the generated files to verify quality
4. Run `skillforge audit /tmp/skillforge-gen --pro` to score it
5. If score is B+ or above, offer to publish to ClawHub
6. If score is below B+, improve the SKILL.md and scripts manually, then re-audit
7. On operator approval, publish: `clawhub publish /tmp/skillforge-gen --slug <slug> --name "<name>" --version 1.0.0`

### When asked to audit a skill:

1. Run `skillforge audit <path> --pro --format markdown`
2. Present the report to the operator
3. Offer specific fixes for any issues found
4. Re-audit after fixes

## API Key Configuration

SkillForge Pro uses the operator's own API key (BYOK model). Supported providers:

| Env Variable | Provider |
|---|---|
| `ZAI_API_KEY` | Z.AI (GLM-5) |
| `OPENAI_API_KEY` | OpenAI |
| `OPENROUTER_API_KEY` | OpenRouter |
| `QWEN_API_KEY` | Qwen |

Keys can also be stored via: `skillforge config:set-api-key <key>`

## Audit Categories

| Category | Weight | What It Checks |
|---|---|---|
| Structure | 20% | SKILL.md, skill.json, file organization |
| Completeness | 25% | Required sections, fields, tags |
| Quality | 25% | Description depth, workflow detail, examples |
| Safety | 20% | Dangerous patterns, hardcoded secrets |
| Compatibility | 10% | Category validity, tool references |

## Constraints

- Always use `--pro` when an API key is available for best quality
- **WARNING: Pro mode sends skill contents to your chosen AI provider.** Do not audit directories containing secrets, .env files, private keys, or credentials. Point audits only at skill directories.
- Verify generated skills actually work before publishing
- Never publish without operator approval
- Use `--format json` for CI/CD contexts, `--format table` for chat
- Slug must be unique on ClawHub — if taken, try variations
- Never pass production API keys to untrusted skill content for auditing
