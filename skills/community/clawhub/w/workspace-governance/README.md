# workspace-governance

[中文文档](README.zh-CN.md)

A methodology-first workspace governance skill for AI agents.  
The goal is safe, reversible, and traceable workspace management without forcing a fixed folder scaffold.

## Document Metadata

- Author: Mars
- GitHub: Mars2003
- Date: 2026-04-28

## Core Principles (Short)

- Boundary before structure
- Plan before action
- Reversible before optimized
- Explicit confirmation for delete and bulk move
- Protect sensitive files and VCS metadata by default

## Quick Start

### 1) Install the skill

```bash
# Claude Code (global)
mkdir -p ~/.claude/skills/workspace-governance
cp SKILL.md ~/.claude/skills/workspace-governance/

# Cursor (project-level)
mkdir -p .cursor/skills/workspace-governance
cp SKILL.md .cursor/skills/workspace-governance/
```

### 2) Project-level adaptation (optional but recommended)

This repository includes `SKILL_ADAPT.yaml` for boundary, protection, batch execution, and logging preferences.  
The skill works without it, but with it, behavior is more stable and consistent across sessions.

### 3) Recommended trigger intents

- "organize workspace"
- "audit first, then cleanup"
- "archive project xxx"
- "create project yyy with boundaries"

### 4) One-command validation (recommended)

```bash
make check
```

## Suggested Directories

Beyond `SKILL.md`, you can optionally maintain:

- `references/`: manuals, process notes, strategy examples
- `assets/`: diagrams, screenshots, and visual resources
- `scripts/`: helper scripts for checks, batch operations, exports
- `tools/`: tool configs and integration notes

## Detailed Docs

- English governance manual (detailed): `references/Governance-Manual.md`
- Chinese governance manual (detailed): `references/治理手册.zh-CN.md`
- Minimal run example: `examples/minimal-governance-run.md`

## Project Meta

- Changelog: `CHANGELOG.md`
- Contributing guide: `CONTRIBUTING.md`

## License

MIT
