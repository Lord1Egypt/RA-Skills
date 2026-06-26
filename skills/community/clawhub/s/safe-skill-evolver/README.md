# Skill Evolver

A safe, diff-based skill builder and optimizer for OpenClaw.

## What It Does

**NEVER applies changes automatically. Always suggests diffs and waits for explicit user confirmation.**

Three operating modes:

1. **Builder Mode** — Create new skills from scratch or templates
2. **Evolver Mode** — Analyze and improve existing skills
3. **Audit Mode** — Read-only safety and quality review

## Why Safe?

Every operation follows:

```
ANALYZE → SUGGEST → REVIEW → CONFIRM → APPLY
```

- ❌ No automatic writes
- ❌ No silent changes
- ❌ No command execution without approval
- ✅ Always shows diff first
- ✅ Always explains why
- ✅ Always waits for confirmation

## Installation

```bash
clawhub install skill-evolver --registry "https://clawhub.ai"
```

Or copy to your workspace `skills/` directory.

## Usage

### Create a New Skill

> "Create a skill for [task]"

Skill Evolver will:
1. Gather requirements
2. Pick the right template (basic / tool / workflow)
3. Generate a draft SKILL.md
4. **Show you the complete draft**
5. Wait for your "yes" before creating any files

### Improve an Existing Skill

> "Improve the [skill-name] skill" or "[skill] has errors"

Skill Evolver will:
1. Read the existing skill
2. Analyze for gaps, safety issues, unclear triggers
3. Generate a structured diff
4. **Show you exactly what would change and why**
5. Wait for your "yes" before applying

### Audit a Skill (Read-Only)

> "Audit the [skill-name] skill"

Skill Evolver will:
1. Read everything
2. Output a structured quality report
3. **Make zero changes** — completely safe

## Templates Included

| Template | Use Case |
|----------|----------|
| `basic_skill.md` | Knowledge/pattern skills (no scripts) |
| `tool_skill.md` | Skills wrapping external tools |
| `workflow_skill.md` | Multi-step decision-tree skills |
| `evolver_task.md` | Track improvement opportunities |

## Scripts Included

| Script | Purpose |
|--------|---------|
| `validate_skill.py` | Score any skill 0-100 against quality checklist |
| `analyze_skill.py` | Deep analysis with improvement suggestions |
| `generate_diff.py` | Readable before/after diffs |

## Safety

See `SKILL.md` → "Safety & Boundaries" for complete rules.

Short version: **We don't touch your files without asking.**

## License

MIT-0 — Free to use, modify, redistribute. No attribution required.
