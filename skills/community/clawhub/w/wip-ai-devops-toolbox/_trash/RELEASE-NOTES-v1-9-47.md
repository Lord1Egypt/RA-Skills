# Release Notes: wip-ai-devops-toolbox v1.9.47

**New: `wip-repos claude` command + CLAUDE.md templates.**

## What changed

### `wip-repos claude` (Phases 1-3 of the CLAUDE.md plan)

New subcommand that generates cross-repo ecosystem sections in CLAUDE.md files. When an agent opens repo-A, it can't read repo-B. This command pre-generates the context.

```bash
wip-repos claude              # regenerate all repos
wip-repos claude my-repo      # regenerate one repo
wip-repos claude --init       # create CLAUDE.md for repos missing one
wip-repos claude --dry-run    # preview changes
```

Features:
- Reads all repos from manifest, extracts metadata (package.json, SKILL.md, directory structure)
- Generates `## Ecosystem` sections with delimiter comments (`<!-- wip-repos:start/end -->`)
- Hand-written sections are never overwritten
- Relevance filtering: only related repos shown (same category + core repos)
- `--init` creates starter CLAUDE.md from template for repos missing one

### Templates

- `templates/global-claude-md.md` ... universal CLAUDE.md for ~/.claude/CLAUDE.md
- `templates/repo-claude-md.template` ... per-repo starter with ecosystem placeholder

## Why

Agents lose context across repos. They can't read sibling repos at runtime. Pre-generating cross-repo maps into CLAUDE.md solves this without requiring runtime access.

## Issues closed

- #212 (partial: Phases 1-3 of 6)

## How to verify

```bash
wip-repos claude --dry-run
```
