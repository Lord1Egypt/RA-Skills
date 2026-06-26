# Product Idea: Require technical documentation updates on every merge to main

**Filed by:** CC-Mini on 2026-03-13
**GitHub Issue:** #167 (https://github.com/wipcomputer/wip-ai-devops-toolbox-private/issues/167)
**Related:** #149 (pre-merge product doc check, covers roadmap + readme-first)

---

## The Problem

Code gets merged to main on private repos without updating the technical documentation. SKILL.md says one thing, the code does another. Config options get added but never documented. New commands ship without usage docs. The README is stale within one release.

The README itself is Parker-directed. He controls the positioning, the messaging, the structure. Agents shouldn't be rewriting it on every merge. But there needs to be a technical reference that always stays in sync with the code, updated as part of every PR to main.

## Two layers of documentation

| Layer | Who owns it | When it updates |
|-------|------------|-----------------|
| **README.md** | Parker | When Parker directs. Product positioning, messaging, structure. |
| **Technical docs** | Whoever merges | Every merge to main. Must reflect the current state of the code. |

Technical docs include:
- **SKILL.md** ... what the tool does, how to invoke it, what it requires
- **TECHNICAL.md** (new) ... detailed API, config options, CLI flags, architecture
- **CHANGELOG.md** ... what changed and why (already handled by wip-release)
- **Install/setup docs** ... any install.txt, INSTALL.md, setup instructions

## What needs to happen

### 1. Establish a TECHNICAL.md convention

Every repo with a `-private` counterpart should have a `TECHNICAL.md` (or `docs/TECHNICAL.md`) that covers:
- All CLI commands and flags
- Configuration options and defaults
- API surface (if applicable)
- Architecture overview (how the pieces connect)
- Known limitations

This is the file that agents update. It's factual, not marketing. It tracks the code.

### 2. Pre-merge check in the Dev Guide

Add to the Dev Guide:

> Before merging any PR to main on a private repo, verify these files reflect the changes in the PR:
> - SKILL.md (if commands, features, or interfaces changed)
> - TECHNICAL.md (if behavior, config, or architecture changed)
> - CHANGELOG.md (handled by wip-release, but draft notes should be in the PR)
>
> The README is Parker-directed. Do not update it unless explicitly asked.

### 3. Tooling enforcement (future)

A `wip-merge` command or pre-merge check that:
1. Diffs the PR branch against main
2. Detects if source code changed but SKILL.md / TECHNICAL.md didn't
3. Warns and asks the agent to update before merging
4. `--skip-docs` flag for hotfixes

This complements #149 (product doc check for roadmap + readme-first). #149 checks product docs. This checks technical docs. Both gates fire before merge.

## Why this matters

Every new session starts cold. The agent reads SKILL.md, TECHNICAL.md, README. If those files are stale, the agent builds on wrong assumptions. Technical docs that track the code are how agents stay oriented without reading every source file.
