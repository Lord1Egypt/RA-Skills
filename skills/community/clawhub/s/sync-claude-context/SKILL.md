---
name: sync-claude-context
description: >
  Sync all Claude Code project context at the start of a new session or after significant changes.
  Use this whenever: starting fresh on a project after a gap, asked to "sync", "catch up",
  "update project docs", "bring yourself up to speed", or when you suspect CLAUDE.md, skills,
  or memory might be stale. Proactively suggest it when the user says they've been away, a big
  feature landed, or the stack changed. Works for any language and project structure.
  Covers CLAUDE.md accuracy, project skills, memory consolidation, and settings review.
---

# sync-project-docs

Audits and updates Claude Code's project-level context files. Autonomous for CLAUDE.md, skills,
and memory; surfaces settings as suggestions since those require explicit user authorization.

---

## Phase 1 — Orient

If the project uses git:
```bash
git log --oneline -20
git status --short
```
Then `git diff HEAD~5 -- <key files below>` to see recent infrastructure changes.

If no git repo, read the directory structure and key files directly.

Find which of these exist:

| Look for | Examples |
|---|---|
| Package/dependency config | `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, `requirements.txt`, `Gemfile` |
| Commands | `Makefile`, `justfile`, `scripts/`, `package.json` scripts, `taskfile.yml` |
| Infrastructure | `docker-compose.yml`, `fly.toml`, `render.yaml`, `Procfile`, `vercel.json`, `k8s/` |
| App config | `config.*`, `settings.*`, `config/`, `application.yml` |
| Env template | `.env.example`, `.env.template`, `.env.sample` |

Goal: know what work landed, what's in-flight, and which key files changed.

---

## Phase 2 — Audit and update CLAUDE.md

Check for all project-level instruction files:
```bash
ls CLAUDE.md .claude/CLAUDE.md CLAUDE.local.md .claude/rules/ 2>/dev/null
```

**If no `CLAUDE.md` exists**: invoke the `init` skill at `sub-skills/init/SKILL.md`, then continue.

**If CLAUDE.md exists**, read it and cross-check each section against the sources from Phase 1:

**Commands** — compare against the actual command source. Fix changed commands, add useful new ones, remove deleted ones.

**Architecture/structure** — compare described modules and key files against what exists on disk. Add new additions; remove deleted or renamed things.

**Configuration/env vars** — compare against actual config files. Add new runtime-relevant settings; remove or correct stale ones.

**Constraints and gotchas** — check whether any documented constraints have been resolved by recent work.

**Env template**: verify it lists all vars the config requires. Missing vars here break fresh setups.

**`@import` references**: scan for `@path/to/file` lines and verify each imported file still exists. A missing import silently breaks context loading.

**Size**: if the file exceeds 200 lines, flag it — beyond that, adherence degrades and context cost rises. Suggest moving detail into `.claude/rules/` topic files.

**`.claude/rules/`**: if this directory exists, check whether any path-scoped rule files reference commands, module names, or file paths that no longer match the current codebase. Fix or flag stale ones.

**`CLAUDE.local.md`**: if this exists, give it the same pass as CLAUDE.md — it's the gitignored personal supplement and can go stale too.

Be surgical: update what's stale, leave accurate content alone. It's read by a future Claude session.

---

## Phase 3 — Audit project skills

```bash
ls .claude/skills/ 2>/dev/null
```

Read each skill. Two categories:

**Infrastructure-coupled skills** (run, deploy, migrate, CI, integration) reference concrete things — commands, services, ports, env vars, file paths. Cross-check each against Phase 1:
- Do referenced commands still exist?
- Do service names, ports, and URLs still match?
- Do env vars still exist in config?
- Are file paths and module names still valid?

Fix small divergences directly. For substantial rework of a run/startup skill (new startup sequence, major service changes), ask first:
> "The run skill looks significantly out of date. Regenerate from scratch with `/run-skill-generator` (may lose custom gotchas) or rewrite stale sections manually?"

If no run skill exists and startup is non-trivial: suggest `/run-skill-generator` if available, or `/run` as a fallback.

**Process/workflow skills** (PR templates, commit style): only check if the git log suggests the described process changed; otherwise leave alone.

---

## Phase 4 — Memory

The memory path is derived from the git repo root (or `pwd` outside a repo):
```bash
REPO=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
echo "$HOME/.claude/projects/$(echo "$REPO" | sed 's|/|-|g')/memory/"
```

**If memory exists**: invoke `consolidate-memory`.

**If none exists**: ask before creating anything —
> "No project memory exists yet. Auto-memory is already on, so Claude will build it up over time — but want me to seed it now with key facts from this codebase so your next session starts oriented right away?"

If yes: seed with non-obvious facts a future session would otherwise waste time re-deriving:
- Surprising constraints (concurrency models, version pins, unexpected defaults)
- Current in-progress work and why
- Non-obvious decisions baked into the code

Create `MEMORY.md` as a concise one-line-per-entry index. Detailed notes go in separate topic files (e.g. `architecture.md`, `constraints.md`) — `MEMORY.md` stays under 200 lines so it fits in the session context window.

---

## Phase 5 — Settings

Check `.claude/settings.json` for stale hooks referencing scripts or commands that no longer exist.

Identify read-only commands that come up constantly (test runners, linters, health checks, `git log`, `git diff`) and would be safe to allow without prompting.

Don't write to settings.json — present them as suggestions. Point to:
- **`update-config`**: to add permissions, env vars, or fix hooks
- **`fewer-permission-prompts`**: to discover permissions from actual transcript history

---

## Phase 6 — Compact

All findings are now on disk. Before wrapping up, remind the user to handle the context by running the `/compact` command to start from a fresh state.

---

## Summary

Print a summary of the changes:

```
## Project sync complete

**CLAUDE.md**: <what changed, or "no changes needed">
**Skills**: <what was updated, or "accurate">
**Memory**: <consolidated / seeded / "no changes">
**Settings suggestions**: <suggested allowances, or "nothing to add">
**Git state**: <uncommitted files + in-flight work, one sentence>

Run `git diff` to review file changes.
```
