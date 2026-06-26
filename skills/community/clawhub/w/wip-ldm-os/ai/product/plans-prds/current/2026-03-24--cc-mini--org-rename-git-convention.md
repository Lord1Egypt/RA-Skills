# Plan: Org Rename + Git Naming Convention + Variable Paths

**Date:** 2026-03-24
**Author:** cc-mini (with Parker)
**Issue:** #117

## Context

The workspace folder is `~/wipcomputer/`. The GitHub org is `wipcomputer`. The company is WIP Computer. But when another company installs LDMOS, their folder should be their name (e.g. `~/acmeinc/`). The folder name needs to be a variable in config, not hardcoded in 43+ places.

Also: system git repos need a naming convention so they're recognizable across orgs. And the `.ldm/` repo (currently `ldm-home`) needs to follow the same convention.

## The Convention

**Git repo naming for system repos:**
- `wipcomputer-ldmos-{orgname}-home-private` = workspace folder (`~/{orgname}/`)
- `wipcomputer-ldmos-{orgname}-system-private` = runtime folder (`~/.ldm/`)

**For us (org = wipcomputerinc):**
- Folder: `~/wipcomputerinc/` (renamed from `~/wipcomputer/`)
- Home repo: `wipcomputer/wipcomputer-ldmos-wipcomputerinc-home-private` (renamed from `wipcomputer/wipcomputer`)
- System repo: `wipcomputer/wipcomputer-ldmos-wipcomputerinc-system-private` (renamed from `wipcomputer/ldm-home`)

**GitHub org stays `wipcomputer`.** That's the developer/publisher identity. `wipcomputerinc` is the local install name.

## What Changes

### Phase 1: Make the path a variable (do this FIRST)

The workspace path is hardcoded as `~/wipcomputer/` in 43+ places across 12 files. Before renaming anything, make it read from config.

**Source of truth:** `~/.ldm/config.json` gets a `workspace` field:
```json
{
  "workspace": "/Users/lesa/wipcomputerinc",
  "org": "wipcomputerinc"
}
```

All docs and config files should reference `{workspace}/` or `settings/config.json paths.workspace` instead of a literal path. The literal path appears ONLY in `~/.ldm/config.json` and `settings/config.json`.

**Files to update (43 occurrences across 12 files in ~/wipcomputer/settings/):**
- `config.json` (7 refs) ... update `org` to `wipcomputerinc`, `paths.workspace` to `~/wipcomputerinc`
- `config-dependencies.json` (5 refs) ... update target paths
- `system-working-directories/README.md` (4 refs)
- `docs/system-directories.md` (8 refs)
- `docs/how-backup-works.md` (9 refs)
- `docs/directory-map.md` (2 refs)
- `docs/how-install-works.md` (2 refs)
- `docs/acknowledgements.md` (2 refs)
- `docs/how-worktrees-work.md` (1 ref)
- `docs/local-first-principle.md` (1 ref)
- `templates/claude-md/workspace-claude-md-placeholder.md` (1 ref)
- `templates/dev-guide-private-placeholder.md` (1 ref)

**Files outside the workspace:**
- `~/.ldm/config.json` ... add `workspace` and `org` fields
- `~/.claude/projects/-Users-lesa--openclaw/memory/repo-locations.md` (3 refs)
- `~/.claude/projects/-Users-lesa--openclaw/memory/` other files (5 refs across 4 files)

### Phase 2: Rename the folder

```bash
mv ~/wipcomputer ~/wipcomputerinc
```

Then update the two source-of-truth files:
- `~/.ldm/config.json` ... `"workspace": "/Users/lesa/wipcomputerinc"`
- `~/wipcomputerinc/settings/config.json` ... `"org": "wipcomputerinc"`, `"paths.workspace": "~/wipcomputerinc"`

### Phase 3: Rename GitHub repos

| Current | New |
|---------|-----|
| `wipcomputer/wipcomputer` | `wipcomputer/wipcomputer-ldmos-wipcomputerinc-home-private` |
| `wipcomputer/ldm-home` | `wipcomputer/wipcomputer-ldmos-wipcomputerinc-system-private` |

```bash
gh repo rename wipcomputer-ldmos-wipcomputerinc-home-private --repo wipcomputer/wipcomputer
gh repo rename wipcomputer-ldmos-wipcomputerinc-system-private --repo wipcomputer/ldm-home
```

Then update git remotes in both repos:
```bash
cd ~/wipcomputerinc && git remote set-url origin git@github.com:wipcomputer/wipcomputer-ldmos-wipcomputerinc-home-private.git
cd ~/.ldm && git remote set-url origin git@github.com:wipcomputer/wipcomputer-ldmos-wipcomputerinc-system-private.git
```

### Phase 4: Update all references

Replace `~/wipcomputer/` with `~/wipcomputerinc/` in every file from Phase 1 list. Also replace `wipcomputer` (the folder name, not the GitHub org) with `wipcomputerinc` where it refers to the local install.

**Important distinction:**
- `wipcomputer` as GitHub org ... stays `wipcomputer`
- `wipcomputer` as npm scope ... stays `@wipcomputer`
- `wipcomputer` as the local folder name ... becomes `wipcomputerinc`
- `wipcomputer` as the org name in config.json ... becomes `wipcomputerinc`
- `wipcomputer` as the co-author line ... stays (GitHub org identity)

### Phase 5: Update LDM OS installer

**File:** `wip-ldm-os-private/bin/ldm.js`

The `cmdInit()` function needs to:
1. Ask for org name (default: read from existing `~/.ldm/config.json`, or prompt)
2. Store `workspace` path and `org` in `~/.ldm/config.json`
3. All path resolution uses the config, not hardcoded `~/wipcomputer`

Add a `loadWorkspace()` helper that other tools can import:
```javascript
function loadWorkspace() {
  const config = JSON.parse(readFileSync(join(LDM_ROOT, 'config.json')));
  return config.workspace || join(HOME, config.org || 'ldmos');
}
```

### Phase 6: Update wip-ldm-os-private plans

20+ plan files in `ai/` reference `~/wipcomputer/`. These are historical documents. Update the active plans (in `current/` and `upcoming/`). Archive plans can stay as-is (they reflect what was true when written).

**Active plans to update:**
- `current/2026-03-22--cc-mini--workspace-migration.md`
- `current/2026-03-21--cc-mini--ldmos-workspace-root.md`
- `current/2026-03-18--unified-backup-system.md`
- `upcoming/2026-03-23--obsidian-as-ldmos-ui-layer.md`
- `upcoming/2026-03-23--cc-mini--memory-crystal-augmentations.md`

### Phase 7: Commit everything

1. Commit changes to `~/wipcomputerinc/` repo (home-private)
2. Commit changes to `~/.ldm/` repo (system-private)
3. Worktree + PR + merge for wip-ldm-os-private plan updates
4. Update CC auto-memory files

## Verification

```bash
# Folder exists at new path
ls ~/wipcomputerinc/settings/config.json

# Old path gone
ls ~/wipcomputer/ 2>&1 | grep "No such file"

# Git remotes correct
cd ~/wipcomputerinc && git remote -v | grep "home-private"
cd ~/.ldm && git remote -v | grep "system-private"

# Config points to right place
cat ~/.ldm/config.json | grep wipcomputerinc

# No stale references in active config
grep -r "~/wipcomputer/" ~/wipcomputerinc/settings/ | grep -v wipcomputerinc  # should be empty

# GitHub repos renamed
gh repo view wipcomputer/wipcomputer-ldmos-wipcomputerinc-home-private --json name
gh repo view wipcomputer/wipcomputer-ldmos-wipcomputerinc-system-private --json name
```

## Note: iCloud migration still in progress

Files are still being moved from `/Users/lesa/Documents/wipcomputer--mac-mini-01/` to the workspace. `~/.openclaw/CLAUDE.md` and `~/.claude/CLAUDE.md` still reference the iCloud paths because repos haven't moved yet. That's a separate task (the original migration plan). This plan only covers:
1. Making the workspace path a variable
2. Renaming the folder from `wipcomputer` to `wipcomputerinc`
3. Establishing the git naming convention
4. Renaming GitHub repos

The CLAUDE.md iCloud path updates happen when Parker moves the repos.

## What NOT to update

- Historical plan files in `archive/` (they reflect what was true when written)
- Session exports in `~/.ldm/agents/cc-mini/memory/sessions/` (historical)
- Crystal chunks with old paths (historical, search still works)
- `~/.openclaw/CLAUDE.md` and `~/.claude/CLAUDE.md` iCloud paths (separate repo migration task)
