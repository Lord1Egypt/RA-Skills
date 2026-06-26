---
name: skill-compiler
description: Compile SKILL.md files into runtime artifacts (SKILL.struct.json and SKILL.toon), verify freshness/health, and prepare portable publish-ready skill folders for ClawHub-style registries.
contract_version: v0
quick_cmd: skills/public/skill-compiler/scripts/compile-skill --skill skills/todoist/SKILL.md
risk_level: safe
capabilities:
  bins: [bash, mdquery, jq, toon]
  network: false
  secrets: []
dry_run_cmd: skills/public/skill-compiler/scripts/check-env
compat:
  os: [linux, macos]
  arch: [x64, arm64]
  shell: [bash]
owner: matt
last_tested: 2026-03-08
rollback: remove skills/public/skill-compiler and revert commit
category: ops
inputs_min: []
cost_hint: low
---

# skill-compiler

Compile-first workflow for skill runtime performance.

## Commands

```bash
# Check local dependencies
skills/public/skill-compiler/scripts/check-env

# Compile one skill doc
skills/public/skill-compiler/scripts/compile-skill --skill skills/todoist/SKILL.md

# Compile all SKILL.md under a root (default: ./skills)
skills/public/skill-compiler/scripts/compile-all --root skills
```

## Outputs

For each input `SKILL.md`, compiler generates sibling artifacts:
- `SKILL.struct.json` (canonical runtime structure)
- `SKILL.toon` (token-lean projection)

## Entrypoint trigger setup (`exe` / `execute`)

Preferred runtime trigger words:
- `exe <skill>`
- `execute <skill>`

Resolution order:
1. `SKILL.struct.json` / `SKILL.toon` (artifact-first)
2. `quick_cmd` from frontmatter
3. `SKILL.md` fallback

Use bundled helper:
```bash
skills/public/skill-compiler/scripts/exe skill-compiler
```

## Publish-ready shape

This folder is ClawHub-ready once versioned:
- `SKILL.md`
- `skill.yaml`
- `scripts/*`

Optional publish command:
```bash
clawhub publish ./skills/public/skill-compiler \
  --slug skill-compiler \
  --name "Skill Compiler" \
  --version 0.2.0 \
  --changelog "Add exe/execute trigger docs and artifact-first entrypoint"
```
