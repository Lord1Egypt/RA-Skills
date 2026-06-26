# Dev Conventions — Notes from cc-air

**Date:** 2026-02-25
**Agent:** cc-air

## Existing Convention Sources

Two repos define how WIP.computer projects are managed:

### 1. `wip-dev-resources` (private)
- **DEVELOPMENT-PROCESS.md** — the main best practices doc
- Covers: repo structure, architecture (4-piece pattern), release process, branch conventions, branch protection, review flow, license compliance, public/private repo pattern
- **Key rules:**
  - Every change goes through a PR. No direct pushes to main. `enforce_admins=true` on all repos.
  - Branch prefixes by agent/machine: `lesa/`, `mini/`, `mba/`
  - Architecture: `core.ts` + `cli.ts` + `mcp-server.ts` + (optional) `openclaw.ts`
  - Public repos stay clean — no todos, no dev noise
  - Private dev stuff goes in `wip-dev-resources/repos/<project>/`
- Has a `repos/` subfolder for per-project todos, conversations, notes

### 2. `wip-dev-updates` (private)
- Centralized dev update repo — one folder per project, updates accumulate
- **Naming convention:** `{who}-dev-update-{MM-DD-YYYY}--{HH-MM-SS}.md`
- **who:** `cc` (Claude Code), `lesa` (Lesa), `parker` (Parker)
- Also has a `cc-session-export/` folder with auto-generated session exports
- Has a repo index table in README.md

### 3. Per-repo `ai/` folders (newer pattern)
- `wip-agent-pay` has `ai/dev-update/` with both date-only and timestamped files
- `memory-crystal` now has `ai/` with `dev-updates/`, `plan/`, `todos/parker/`

## Branch Prefix Update

The existing DEVELOPMENT-PROCESS.md says `lesa/`, `mini/`, `mba/`. Parker has updated the convention:

| Agent | Machine | Branch Prefix | Notes |
|-------|---------|---------------|-------|
| cc-air | MacBook Air | `cc-air/` | Claude Code on Air |
| cc-mini | Mac Mini | `cc-mini/` or `mini/` | Claude Code on Mini |
| lesa-mini | Mac Mini | `lesa/` | Lesa on Mini via OpenClaw |

## File Naming Convention (updated)

All files authored by an agent must include the agent name:

```
YYYY-MM-DD--{agent}--{description}.md
```

Examples:
- `2026-02-25--cc-air--phase2-worker-build.md`
- `2026-02-25--cc-air--setup-checklist.md`
- `2026-02-25--lesa-mini--weekly-tuning-report.md`

This differs from the older `wip-dev-updates` convention (`{who}-dev-update-{MM-DD-YYYY}--{HH-MM-SS}.md`) — the new format uses ISO dates and puts the agent name after the date with double-dash separators.

## Decision: `ai/` folder per repo (2026-02-25)

**The `ai/` folder is the standard going forward.** Every repo gets one. It holds all the thinking between Parker and agents — plans, dev updates, todos, conversations. It's scoped to the repo it belongs to.

```
ai/
  dev-updates/       ← what was built, session logs
  plan/              ← architecture plans, convention notes
  todos/
    parker/          ← manual tasks for Parker
```

- `wip-dev-updates` (centralized repo) is legacy. Leave it as-is, don't add to it.
- `wip-dev-resources/DEVELOPMENT-PROCESS.md` still holds the engineering best practices (branch protection, release process, architecture pattern). Update it when branch prefixes and file naming are finalized across all agents.
