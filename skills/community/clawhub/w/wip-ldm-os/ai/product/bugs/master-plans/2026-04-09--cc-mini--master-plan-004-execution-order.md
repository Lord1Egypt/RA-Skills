# Master Plan 004: Execution Order

**Date:** 2026-04-09
**Author:** cc-mini (with Parker)
**Status:** execution checklist. Run these in order. One at a time. No skipping.
**Supersedes:** Master Plan 003 (which was incomplete and marked things as shipped that weren't)

## Source files (read ALL of these before executing ANYTHING)

1. `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/release-pipeline/2026-04-05--cc-mini--release-pipeline-master-plan.md`
2. `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/release-pipeline/2026-04-06--cc-mini--shared-universal-config-layer.md`
3. `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/release-pipeline/2026-04-08--cc-mini--silent-skip-without-license-guard-config.md`
4. `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/installer/2026-04-03--cc-mini--installer-recreates-renamed-folders.md`
5. `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/installer/2026-04-08--cc-mini--tools-allow-not-updated-on-plugin-install.md`
6. `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/docs/2026-04-03--cc-mini--doc-architecture-and-update-pipeline.md`
7. `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/docs/2026-03-26--cc-mini--docs-pipeline.md`
8. `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/release-pipeline/2026-04-06--cc-mini--shared-universal-config-layer.md`
9. `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/ldmos-core/2026-04-08--cc-mini--shared-to-library-refactor.md`
10. `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/ldmos-core/2026-04-08--cc-mini--daily-workspace-audit.md`
11. `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/git-init-privatize/2026-03-27--cc-mini--wip-privatize-pipeline.md`

---

## What was actually shipped in Master Plan 003 (Apr 8-9)

These are real, verified, in production:

- [x] wip-release blocks if .license-guard.json missing (all 3 paths)
- [x] wip-release .npmignore ai/ leak check
- [x] wip-release publish-before-commit with rollback on npm failure
- [x] wip-release autoFixSubToolVersions() auto-bumps patch versions
- [x] Installer template deploy path: settings/templates/ -> library/templates/
- [x] Installer updateToolsAllow() adds plugin to openclaw.json on deploy
- [x] Installer deployBridge() creates dirs if missing
- [x] Installer deployRules() extracted, called from cmdInit + cmdInstallCatalog
- [x] Template path references fixed: settings/config.json -> ~/.ldm/config.json
- [x] Template path references fixed: settings/docs/ -> library/documentation/
- [x] Template path references fixed: _worktrees/ -> .worktrees/
- [x] Installer deploy destinations: ~/.ldm/shared/ -> ~/.ldm/library/
- [x] Backward-compat symlink: ~/.ldm/shared -> ~/.ldm/library
- [x] wip-repos compliance command (check + fix)
- [x] wip-repos watchdog command (find unmanifested repos)
- [x] workspace-audit.sh script (6 checks)
- [x] deploy-public.sh blocks alpha versions
- [x] .license-guard.json added to wip-ldm-os-private
- [x] .license-guard.json added to wip-x-xai-grok-private

## What was NOT shipped but claimed as shipped or left incomplete

- [ ] ~/.ldm/library/documentation/ is EMPTY. No agent docs deployed.
- [ ] ~/wipcomputerinc/CLAUDE.md NOT updated (only templates in repo updated)
- [ ] ~/.claude/rules/ still has stale settings/config.json references (installer hasn't run)
- [ ] Lesa's workspace files (TOOLS.md, MEMORY.md) NOT updated for library/ rename
- [ ] how-we-work.md rule never written (from Apr 6 shared-universal-config plan)
- [ ] Core tool groups (group:fs, group:runtime, etc.) not ensured by installer on every run
- [ ] ldm doctor doesn't audit plugins vs tools.allow
- [ ] Per-repo CLAUDE.md missing on ALL repos except wip-ldm-os-private
- [ ] TECHNICAL.md missing on 6 repos
- [ ] Doc dependency guard not built (Step 6 from docs pipeline)
- [ ] Mintlify starter content not replaced (Step 5b from docs pipeline)
- [ ] Release notes gate doesn't block (warns only)
- [ ] wip-release doesn't regenerate home docs or agent docs
- [ ] repos-manifest.json stale (134 repos on disk not in manifest)
- [ ] 11 repos still missing .license-guard.json
- [ ] wip-repo-init doesn't update repos-manifest.json
- [ ] wip-x-xai-grok public repo has alpha release and v1.0.0 with wrong license

---

## Execution order

### Step 1: Release and install to deploy what was built

Nothing built in this session has been installed yet. The installer changes, rules deploy, library rename... none of it is live.

**Repo:** wip-ai-devops-toolbox-private
- [ ] `wip-release alpha` (includes Waves 0, 1, deploy-public gate, compliance tools, audit script)

**Repo:** wip-ldm-os-private
- [ ] `wip-release alpha` (includes Wave 2 installer fixes, Wave 3 template/path fixes, library rename)

**Then:**
- [ ] `npm install -g @wipcomputer/wip-ldm-os@alpha`
- [ ] `npm install -g @wipcomputer/wip-ai-devops-toolbox@alpha`
- [ ] `ldm install`
- [ ] Verify: `~/.ldm/library/rules/` has current rules
- [ ] Verify: `~/.ldm/library/` exists, `~/.ldm/shared` is symlink
- [ ] Verify: `~/.claude/rules/` no longer references settings/config.json
- [ ] Verify: `~/.openclaw/openclaw.json` tools.allow has all plugins

### Step 2: Fix the deployed CLAUDE.md and rules

The templates in the repo are fixed but the deployed files are not.

**Source:** Plan #6 (doc architecture, Apr 3), Bug #4 (installer recreates folders, Apr 3)

- [ ] Update `~/wipcomputerinc/CLAUDE.md`: settings/ -> library/ in directory tree
- [ ] Update `~/.claude/CLAUDE.md`: settings/config.json -> ~/.ldm/config.json
- [ ] Verify deployed `~/.claude/rules/` match source `~/.ldm/library/rules/` (ldm install should have done this)
- [ ] Remove `~/wipcomputerinc/settings/docs/` if installer didn't recreate it

### Step 3: Write how-we-work.md

The full workflow mental model. This is the single most important rule file. Every agent reads it.

**Source:** Plan #2 (shared-universal-config, Apr 6), lines 79-99

- [ ] Write `shared/rules/how-we-work.md` in wip-ldm-os-private
- [ ] Content: worktrees -> PR -> merge -> pull -> alpha -> beta -> stable -> deploy-public -> install
- [ ] Include: "always pull main after merge", "alpha never goes to public", "beta goes to public as prerelease", "release notes on the branch"
- [ ] Commit, merge, release alpha, ldm install to deploy

### Step 4: Installer ensures core tool groups on every run

**Source:** Bug #5 (tools.allow, Apr 8), items 2 and 3

- [ ] `bin/ldm.js`: On every `ldm install`, verify group:fs, group:runtime, group:sessions, group:memory are in tools.allow (if the list exists)
- [ ] `ldm doctor`: Add check comparing plugins.entries against tools.allow. Warn if mismatch.

### Step 5: Update Lesa's workspace for library/ rename

**Source:** Plan #9 (shared-to-library refactor, Apr 8), Phase 5

- [ ] Update `~/.openclaw/workspace/TOOLS.md`: any references to ~/.ldm/shared/ -> ~/.ldm/library/
- [ ] Update `~/.openclaw/workspace/MEMORY.md`: same
- [ ] Tell Lesa about the change via lesa_send_message

### Step 6: Populate ~/.ldm/library/documentation/ with agent docs

**Source:** Plan #6 (doc architecture, Apr 3), Level 3 agent docs

- [ ] Installer should deploy doc templates to `~/.ldm/library/documentation/` (not just home library/)
- [ ] Update `deployDocs()` in `bin/ldm.js` to also write to `~/.ldm/library/documentation/`
- [ ] Verify after install: `~/.ldm/library/documentation/` has all 14 doc files

### Step 7: Doc dependency guard in wip-release

**Source:** Plan #7 (docs pipeline, Mar 26), Step 6

- [ ] Add to `tools/wip-release/core.mjs`: before publishing, check what code changed since last tag
- [ ] Compare against change-dependencies.json
- [ ] Warn if corresponding docs weren't updated
- [ ] This is Option B from the plan (runs at release time, not every commit)

### Step 8: Release notes gate blocks (not warns)

**Source:** Plan #1 (release pipeline, Apr 5), current behavior is warn-only for alpha

- [ ] Alpha: require release notes file (RELEASE-NOTES-v*.md) or block
- [ ] Remove the `--notes="inline"` escape hatch for alpha (file only)
- [ ] Keep `--notes` for hotfix (convenience)

### Step 9: Seed all repos with .license-guard.json via manifest

**Source:** Wave 3.3 from Master Plan 003

- [ ] Update repos-manifest.json with missing repos (134 unmanifested)
- [ ] Run `wip-repos compliance --fix` across all repos
- [ ] Each repo needs commit + PR + merge (or build into wip-repo-init)
- [ ] Add manifest update to wip-repo-init scaffold

### Step 10: Per-repo CLAUDE.md

**Source:** Plan #6 (doc architecture, Apr 3), content inventory

- [ ] Write CLAUDE.md for: memory-crystal-private, wip-ai-devops-toolbox-private, wip-agent-pay-private, wip-1password-private, wip-markdown-viewer-private, dream-weaver-protocol-private, wip-healthcheck-private, wip-x-xai-grok-private
- [ ] Each follows the Level 3 template from wip-ldm-os-private/CLAUDE.md
- [ ] Commit per repo, PR, merge

### Step 11: Per-repo TECHNICAL.md

**Source:** Plan #6 (doc architecture, Apr 3), Plan #7 (docs pipeline, Mar 26)

- [ ] Write TECHNICAL.md for: agent-pay, markdown-viewer, xai-grok, x-platform, dream-weaver, healthcheck
- [ ] Commit per repo, PR, merge

### Step 12: Clean up wip-x-xai-grok public repo

- [ ] Delete the alpha release (v1.0.1-alpha.2) from public
- [ ] Delete or update the v1.0.0 release (had wrong license)
- [ ] Do a proper stable release with release notes through the full pipeline
- [ ] Verify public repo has correct LICENSE, CLA, README

### Step 13: Mintlify docs site

**Source:** Plan #7 (docs pipeline, Mar 26), Step 5b

- [ ] Replace starter content at wip.computer/docs/ with real docs
- [ ] Navigation structure from the plan
- [ ] All README + TECHNICAL from all repos

### Step 14: Daily audit as cron

**Source:** Plan #10 (daily workspace audit, Apr 8)

- [ ] Set up workspace-audit.sh as LaunchAgent (daily at 06:00)
- [ ] Or add to wip-healthcheck
- [ ] Reports to Parker via iMessage or TUI

### Step 15: wip-privatize orchestration

**Source:** Plan #11 (privatize pipeline, Mar 27)

- [ ] Single command for the 7-step privatization workflow
- [ ] Connects templates, docs, config, scaffold
- [ ] 26 repos in _to-privatize/ queues

---

## Rules for execution

1. Read the source plan file before executing any step
2. Write release notes on the branch before merging
3. After every merge, pull to main
4. Alpha never goes to public
5. After every release, run ldm install and verify
6. Update documentation in ALL THREE locations: repo, home, agent
7. One step at a time. Verify before moving to next.
