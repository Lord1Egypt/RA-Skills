# Plan: Workspace Migration (iCloud to ~/wipcomputer/)

**Date:** 2026-03-22
**Author:** cc-mini (with Parker)
**Issue:** #117
**Parent plan:** `2026-03-21--cc-mini--ldmos-workspace-root.md`

## Context

Everything was under `~/Documents/wipcomputer--mac-mini-01/staff/Parker/Claude Code - Mini/` (iCloud-synced). Path is absurdly long. iCloud fights with .git dirs, sqlite WAL files, node_modules. Repos shouldn't sync via iCloud.

Staff documents already moved to `~/wipcomputer/staff/`. Settings created at `~/wipcomputer/settings/`. Repos are the big remaining piece.

## Step 1: Create config-dependencies.json

**File:** `~/wipcomputer/settings/config-dependencies.json`

Same pattern as `doc-dependencies.json`. Tracks which config files reference which paths, so when anything moves, we know exactly what to update.

Tracks three path groups:
- **repos** (MIGRATING): iCloud -> ~/wipcomputer/repos/
- **staff** (DONE): iCloud -> ~/wipcomputer/staff/
- **ldm** (STAYING): ~/.ldm/ stays

Each path group lists every config file that references it, with count and description. Historical files (session exports, crystal chunks) are excluded... they're records, not configs.

## Step 2: Move repos (dir by dir)

**Source:** `~/Documents/wipcomputer--mac-mini-01/staff/Parker/Claude Code - Mini/repos/`
**Destination:** `~/wipcomputer/repos/`

Contents at source:
```
repos/
  ldm-os/           <- organizational folder (apis, apps, components, devops, identity, utilities, wip-ldm-os-private)
  wip-inc/           <- company docs
  wip-web/           <- websites
  third-party-repos/ <- forks
  _sort/             <- uncategorized
  _sunsetted/        <- deprecated
  _trash/            <- deleted
  _worktrees/        <- worktrees
```

**Approach:** Parker moves dirs himself (Finder or terminal). After each move, CC updates all files listed in config-dependencies.json.

## Step 3: Update config files (after each move)

Files to update (from config-dependencies.json):

| File | What changes |
|------|-------------|
| `~/.openclaw/CLAUDE.md` | repo paths, tool locations, directory structure |
| `~/.claude/CLAUDE.md` | repo paths, tool locations, plugin source, boot sequence |
| `~/.claude/projects/-Users-lesa--openclaw/memory/repo-locations.md` | full repo map, base path |
| `~/.openclaw/wip-healthcheck/config.json` | source paths |
| `~/.ldm/agents/cc-mini/REFERENCE.md` | repo locations |
| `~/.ldm/agents/cc-mini/CONTEXT.md` | path references |
| `~/.openclaw/workspace/SHARED-CONTEXT.md` | key paths section (Edit only) |
| `~/.openclaw/workspace/TOOLS.md` | Lesa's tool reference |

Also check:
- `~/.claude/settings.json` (hook paths)
- `~/.ldm/config.json` (workspace pointer)
- `~/wipcomputer/settings/config.json` (paths section)
- `~/Library/LaunchAgents/*.plist` (script paths)

For each file:
1. Replace old base path with new base path
2. Verify no old path references remain: `grep "Claude Code - Mini" <file>`
3. Verify the file still works (boot sequence loads, tools resolve)

## Backup: iCloud becomes offsite, not live sync

**Related plan:** `2026-03-18--unified-backup-system.md` (issue #119)

Before migration: iCloud syncs everything live. Repos, documents, sqlite files, node_modules. This causes conflicts.

After migration: `~/wipcomputer/` is local-only. No iCloud sync. The `ldm backup` command handles offsite:

1. Local backup to `~/.ldm/backups/` (daily, data only, ~25 GB)
2. Tar to iCloud: `~/Library/Mobile Documents/com~apple~CloudDocs/wipcomputer-icloud/backups/`
3. One tar per device per day. Rotates to 7 days. iCloud syncs the tar across devices.

**What iCloud syncs after migration:**
- Backup tars only (compressed, one file per day)
- NOT live repos, NOT sqlite WAL files, NOT node_modules

**What stays local only:**
- `~/wipcomputer/` (workspace, repos, staff)
- `~/.ldm/` (runtime, extensions, memory)
- `~/.openclaw/` (harness config)
- `~/.claude/` (CC config)

The unified backup plan must be implemented before (or alongside) the migration. Without `ldm backup`, moving repos out of iCloud means no offsite copy at all.

## Step 4: After all repos moved

- Lesa migrates her repos from `staff/Lesa/repos/` into `~/wipcomputer/repos/` (separate task)
- Update SHARED-CONTEXT.md key paths section
- Update boot sequence paths in both CLAUDE.md files
- Old iCloud folder becomes backup target only
- Update config-dependencies.json to mark repos migration as DONE
- Verify `ldm backup` captures ~/wipcomputer/documents/ (not repos... repos are on GitHub)

## .ldm/ as source, .claude/ as deployment target

Reference: "Anatomy of the .claude/ folder" (2026-03-23)

Claude Code's native `.claude/` folder supports rules/, commands/, skills/, agents/, settings.json. These are harness-specific. LDM OS is harness-agnostic. The relationship:

```
~/.ldm/                              <- SOURCE (harness-agnostic)
  agents/cc-mini/
    SOUL.md, IDENTITY.md             <- identity
    rules/                           <- agent-specific rules
    commands/                        <- agent-specific commands
  shared/
    rules/                           <- rules for ALL agents
    commands/                        <- commands for ALL agents
  extensions/                        <- installed tools (MCP, hooks, skills)

~/.claude/                           <- DEPLOYMENT TARGET (Claude Code)
  CLAUDE.md                          <- generated from .ldm/ + config.json
  rules/                             <- deployed from .ldm/shared/rules/ + agent rules
  commands/                          <- deployed from .ldm/shared/commands/ + agent commands
  skills/                            <- deployed from .ldm/extensions/
  agents/                            <- deployed from .ldm/agents/ definitions
  settings.json                      <- deployed from .ldm/hooks/ + permissions

~/.openclaw/                         <- DEPLOYMENT TARGET (OpenClaw)
  workspace/TOOLS.md                 <- equivalent of rules/ for Lesa
  extensions/                        <- deployed from .ldm/extensions/
```

`ldm install` deploys from .ldm/ to each harness. Edit at the .ldm/ level. The harness gets the result.

### CLAUDE.md split using rules/

Current CLAUDE.md is 368 lines. Target: under 200 lines in CLAUDE.md, rest in rules/.

```
~/.claude/rules/                     <- or ~/wipcomputer/.claude/rules/
  writing-style.md                   <- no em dashes, ellipsis, timezone
  git-conventions.md                 <- never squash, co-authors, prefixes
  release-pipeline.md                <- merge, deploy, install (3 steps)
  memory-system.md                   <- crystal, boot sequence, end-of-session
  security.md                        <- 1password SA token, audit, secrets
  agent-coordination.md              <- Lesa, bridge, workspace boundaries
  tool-rules.md                      <- never run from repo clones, dogfood
```

Path-scoped rules (YAML frontmatter) only load when working in matching files:

```yaml
---
paths:
  - "tools/wip-release/**"
---
# Release rules that only apply when editing release code
```

This replaces the need to generate per-repo CLAUDE.md files. Rules scope themselves.

### Custom commands for workflows

```
~/.claude/commands/                  <- or ~/wipcomputer/.claude/commands/
  release.md                         <- /user:release (wraps wip-release)
  deploy-public.md                   <- /user:deploy-public
  health.md                          <- /user:health (wraps ldm doctor)
```

### Native agents

```
~/.claude/agents/
  code-reviewer.md                   <- model: haiku, read-only tools
  security-auditor.md                <- wraps existing audit skill
```

### Where rules/ lives

Two options:

1. **`~/.claude/rules/`** ... global, applies to all sessions on this machine
2. **`~/wipcomputer/.claude/rules/`** ... workspace-level, applies when opened here

Option 2 is better for us. Workspace rules ship with the workspace. Per-repo rules go in `<repo>/.claude/rules/`. Three levels, same as CLAUDE.md:

| Level | Location | Scope |
|-------|----------|-------|
| Global | `~/.claude/rules/` | Every session, every project |
| Workspace | `~/wipcomputer/.claude/rules/` | When working in this workspace |
| Repo | `<repo>/.claude/rules/` | When working in this repo |

### Implementation order

1. Create `~/.ldm/shared/rules/` with the 7 rule files (source of truth)
2. Create `~/.ldm/shared/commands/` with workflow commands
3. Deploy to `~/.claude/rules/` and `~/wipcomputer/.claude/rules/`
4. Slim CLAUDE.md down to under 200 lines (identity + structure only)
5. Add deploy step to `ldm install` that syncs rules/commands/skills to harnesses

## Verification

After each dir move:
- `cd ~/wipcomputer/repos/<dir> && git status` ... repos work
- `grep "Claude Code - Mini" ~/.openclaw/CLAUDE.md` ... should return 0 matches when done
- `grep "Claude Code - Mini" ~/.claude/CLAUDE.md` ... should return 0 matches when done
- All tools still work (`wip-release --dry-run`, `crystal status`, etc.)
- config-dependencies.json updated with current status

After rules/ deployment:
- `ls ~/.claude/rules/` ... shows all rule files
- `wc -l ~/.claude/CLAUDE.md` ... under 200 lines
- Start a new CC session, verify rules load (check with /memory or test a rule)
