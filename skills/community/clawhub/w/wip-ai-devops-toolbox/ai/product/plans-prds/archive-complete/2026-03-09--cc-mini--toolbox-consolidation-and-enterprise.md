# Plan: Toolbox Consolidation + Enterprise Repo Manifest

**Date:** 2026-03-09
**Author:** Claude Code (cc-mini)
**Status:** Planning
**Source:** `ai/product/prodcut-ideas/dev-tools-gaps-and-roadmap--2026-03-09.md`, `ai/product/prodcut-ideas/enterprise--wip-repos--2026-03-09.md`

---

## Overview

Three workstreams for the next phase of wip-dev-tools:

1. **Fold wip-file-guard into the toolbox**
2. **Fold wip-universal-installer into the toolbox**
3. **Build wip-repos (enterprise repo manifest tool)**

All three follow the same principle: the toolbox is the product. Independent tools, one drawer.

---

## 1. Fold wip-file-guard into the toolbox

wip-file-guard is a hook that blocks destructive edits to protected identity files. Works with Claude Code CLI and OpenClaw. Currently lives as its own repo (`wipcomputer/wip-file-guard`, private: `wip-file-guard-private`). Needs to move into `tools/wip-file-guard/` inside the toolbox.

### Precedent

wip-release and wip-license-hook both started as standalone repos, proved themselves, then got folded in. The old repos got renamed to `-deprecated` and moved to `_sunsetted/`.

### Steps

1. **Copy source into toolbox.** `tools/wip-file-guard/` with all source, README, SKILL.md, package.json, LICENSE.
2. **Verify it works from the new location.** CLI, Claude Code hook, OpenClaw plugin all still function.
3. **Update the umbrella README.** Add wip-file-guard to the tools table and source code table in wip-dev-tools README.
4. **Update npm publishing.** `@wipcomputer/wip-file-guard` publishes from `tools/wip-file-guard/`. Verify `wip-release` can target subdirectories.
5. **Deprecate standalone repos.**
   - Rename `wipcomputer/wip-file-guard` to `wipcomputer/wip-file-guard-deprecated`
   - Rename `wipcomputer/wip-file-guard-private` to `wipcomputer/wip-file-guard-private-deprecated` (or just archive)
   - Move local folders to `_sunsetted/`
   - Update the deprecated repo READMEs to point to `wipcomputer/wip-dev-tools`
6. **Update org profile.** Change the `[wip-file-guard](link)` entry to point to the tools subfolder instead of a standalone repo.
7. **Update repos manifest and README.** Remove wip-file-guard from `utilities/`, note it's now inside `devops/wip-dev-tools-private/tools/`.
8. **deploy-public** to sync the updated toolbox to `wipcomputer/wip-dev-tools`.

### Location changes

- **From:** `ldm-os/utilities/wip-file-guard-private/`
- **To:** `ldm-os/devops/wip-dev-tools-private/tools/wip-file-guard/`
- **Public repo:** `wipcomputer/wip-file-guard` -> `wipcomputer/wip-file-guard-deprecated`
- **npm package:** `@wipcomputer/wip-file-guard` (unchanged, just publishes from new path)

---

## 2. Fold wip-universal-installer into the toolbox

wip-universal-installer is the Universal Interface specification for agent-native software. It defines how every tool ships six interfaces: CLI, importable module, MCP Server, OpenClaw Plugin, Skill, Claude Code Hook. Currently its own repo. Needs to move into `tools/wip-universal-installer/`.

This is also the key to the MCP roadmap item (#1 priority from the gaps doc). The installer IS the MCP layer. Folding it in means every tool in the toolbox can immediately be instrumented with all six interfaces.

### Steps

Same as wip-file-guard above, plus:

1. **Copy source into toolbox.** `tools/wip-universal-installer/` with SPEC.md, SKILL.md, REFERENCE.md, install.js, detect.mjs, examples/, package.json, LICENSE.
2. **Verify it works from the new location.**
3. **Promote SPEC.md.** Consider symlinking or copying `SPEC.md` to the toolbox root as `UNIVERSAL-INTERFACE.md` so it's visible at the top level. This is the philosophical document that defines the whole approach.
4. **Update the umbrella README.** Add universal-installer to the tools table.
5. **Update npm publishing.** `@wipcomputer/universal-installer` publishes from `tools/wip-universal-installer/`.
6. **Deprecate standalone repos.**
   - Rename `wipcomputer/wip-universal-installer` to `wipcomputer/wip-universal-installer-deprecated`
   - Same for the private repo
   - Move local folders to `_sunsetted/`
   - Update deprecated repo READMEs to point to `wipcomputer/wip-dev-tools`
7. **Update org profile.** Change the `[wip-universal-installer](link)` entry.
8. **Update repos manifest and README.** Remove from `components/`, note it's now inside `devops/wip-dev-tools-private/tools/`.
9. **deploy-public.**

### Location changes

- **From:** `ldm-os/components/wip-universal-installer-private/`
- **To:** `ldm-os/devops/wip-dev-tools-private/tools/wip-universal-installer/`
- **Public repo:** `wipcomputer/wip-universal-installer` -> `wipcomputer/wip-universal-installer-deprecated`
- **npm package:** `@wipcomputer/universal-installer` (unchanged)

### After folding in

Apply the Universal Installer to the other tools in the toolbox. This is the MCP roadmap item:

1. Instrument `wip-release` with all six interfaces
2. Instrument `wip-license-hook`
3. Instrument `wip-repo-permissions-hook`
4. Instrument `deploy-public`
5. Instrument `wip-file-guard`
6. Test: Lesa types "run wip-release minor" and it ships

---

## 3. Build wip-repos (enterprise repo manifest tool)

New tool. Lives at `tools/wip-repos/`. Makes `repos-manifest.json` the single source of truth for repo organization across a team.

### The concept

The manifest is like a code formatter. You can move folders around all day. But on sync, everything snaps back to where the manifest says it belongs. Want to change the structure? PR to the manifest. Org owner approves or rejects. Rejected? Your folders snap back on next sync.

### Commands

- `wip-repos add my-thing --category utilities` ... add a repo to the manifest (creates a PR)
- `wip-repos move my-thing --from utilities --to identity` ... propose moving a repo
- `wip-repos check` ... diff filesystem against manifest, flag drift
- `wip-repos sync` ... rearrange local folders to match the manifest
- `wip-repos readme` ... regenerate README directory tree from manifest

### Manifest schema (v2)

Current manifest is flat key-value (path -> remote). Needs to be richer:

```json
{
  "_version": "2",
  "_description": "Source of truth for repo directory structure.",
  "repos": {
    "ldm-os/devops/wip-dev-tools-private": {
      "remote": "wipcomputer/wip-dev-tools-private",
      "public": "wipcomputer/wip-dev-tools",
      "privatized": true,
      "category": "devops",
      "description": "Dev toolkit for AI-assisted development"
    }
  }
}
```

### Integration points

- `deploy-public` and `wip-release` call `wip-repos check` before running. Stale manifest blocks deploys.
- `wip-repos readme` regenerates the README. No more manual edits.
- `wip-repos claude` regenerates CLAUDE.md repo references. Agents always have correct paths.
- CI: `wip-repos check` as a PR check. Drift = blocked merge.

### Steps

1. **Design the v2 manifest schema.** Migration path from current flat format.
2. **Build `wip-repos check`.** Walk filesystem, compare to manifest, report drift.
3. **Build `wip-repos sync`.** Move folders to match manifest. Confirm before destructive moves.
4. **Build `wip-repos add` and `wip-repos move`.** Update manifest, optionally create PR.
5. **Build `wip-repos readme`.** Template-based README generation from manifest data.
6. **Hook into deploy-public and wip-release.** Pre-flight check.
7. **Apply Universal Installer.** Make it callable by agents (MCP, skill, hook).
8. **Migrate our manifest.** Convert `repos-manifest.json` to v2 format.
9. **Test end-to-end.** Move a repo, sync, verify everything updates.

### Enterprise value

This is the feature that makes wip-dev-tools relevant for teams beyond WIP.computer. Any org with 10+ repos needs this. Any org with AI agents referencing paths REALLY needs this. The pitch: "Your AI broke because someone moved a folder. That never happens again."

---

## Sequencing

1. **Fold wip-file-guard in first.** Smaller tool, simpler move. Validates the consolidation process.
2. **Fold wip-universal-installer in second.** Bigger move, but the roadmap depends on it being inside the toolbox.
3. **Build wip-repos.** New tool, builds on the manifest that already exists.
4. **Apply Universal Installer to everything.** The MCP unlock. Every tool becomes agent-callable.

Steps 1 and 2 can potentially run in parallel since they're independent moves.

---

## Files that change

Every consolidation touches these files (the maintenance rule):
- `repos-manifest.json`
- `repos/README.md`
- `.github-private/profile/README.md` (org profile)
- CLAUDE.md references (both global and project)
- Memory files that reference repo paths

This is exactly the problem wip-repos solves. Once it exists, it handles all of this automatically.

---

## What the toolbox looks like after

```
wip-dev-tools-private/
  tools/
    wip-release/                 ← release pipeline
    wip-license-hook/            ← license change detection
    wip-repo-permissions-hook/   ← repo visibility guard
    wip-file-guard/              ← identity file protection (NEW)
    wip-universal-installer/     ← Universal Interface spec (NEW)
    wip-repos/                   ← enterprise repo manifest (NEW)
    ldm-jobs/                    ← macOS scheduled jobs
  scripts/
    deploy-public.sh             ← private-to-public sync
    post-merge-rename.sh         ← merged branch renaming
  DEV-GUIDE-GENERAL-PUBLIC.md
  UNIVERSAL-INTERFACE.md         ← promoted from universal-installer SPEC.md
  README.md
  SKILL.md
```

Nine tools, one toolbox. Each self-contained. No shared dependencies. Not a monorepo. A drawer.
