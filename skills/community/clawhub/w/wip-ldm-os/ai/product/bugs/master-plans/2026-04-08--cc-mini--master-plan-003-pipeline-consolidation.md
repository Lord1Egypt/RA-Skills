# Master Plan 003: Pipeline, Installer, and Documentation Consolidation

## Context

12 bug reports and plans filed over 2 weeks (March 26 - April 8) all describe different faces of one structural failure: **the system has no single enforcement layer.** The release pipeline has optional gates that silently skip when config is missing. The installer deploys to wrong paths after directory renames. Documentation is scattered across three locations that contradict each other.

The trigger: a subagent built `wip-x-xai-grok-private` with wrong license, no CLA, no README template, no release notes. It went through `wip-release alpha`, `deploy-public.sh`, published to npm and GitHub. Zero quality gates fired. In the same session, an API key was hardcoded in a PM2 config file committed to the repo.

This plan supersedes individual bug files for execution ordering. Bug files remain the source of truth for each item's details.

**Consolidated from:**
- `bugs/release-pipeline/2026-04-05--release-pipeline-master-plan.md` (8 phases, $900 incident)
- `bugs/release-pipeline/2026-04-06--shared-universal-config-layer.md`
- `bugs/release-pipeline/2026-04-08--silent-skip-without-license-guard-config.md` (CRITICAL)
- `bugs/installer/2026-04-03--installer-recreates-renamed-folders.md`
- `bugs/installer/2026-04-08--tools-allow-not-updated-on-plugin-install.md`
- `plans-prds/current/ldmos-core/2026-04-08--daily-workspace-audit.md`
- `plans-prds/current/ldmos-core/2026-04-08--shared-to-library-refactor.md`
- `plans-prds/current/git-init-privatize/2026-03-27--wip-privatize-pipeline.md`
- `plans-prds/current/docs/2026-03-26--docs-pipeline.md`
- `plans-prds/current/docs/2026-04-03--doc-architecture-and-update-pipeline.md`
- `bugs/master-plans/bugs-plan-04-05-2026-002.md` (Wave 2 partially shipped)

## Already Shipped (from Master Plan 002 Wave 2)

- Phase 1: Main branch check
- Phase 2: Tag collision detection
- Phase 4: Auto-PR for protected main
- Phase 6: integrate deploy-public
- Phase 7: Surface real errors
- Phase 8: Version drift errors
- Pre-commit hook bootstrap fix (Apr 8)
- Hooks deployed on every ldm install (Apr 8)

---

## WAVE 0: Emergency Gate Fix (CRITICAL, 1 session) ... SHIPPED 2026-04-08

**Repo:** `wip-ai-devops-toolbox-private`
**File:** `tools/wip-release/core.mjs`
**Bug:** Any repo without `.license-guard.json` ships with zero quality gates

Three locations need the same fix (lines ~1744, ~2594, ~2594-hotfix):

Current: `if (existsSync(configPath)) { /* run checks */ }` (silently skips if missing)
Fix: `if (!existsSync(configPath)) { /* BLOCK with clear error */ return failed; }`

Additional gates to add after existing license checks:
1. `.npmignore` must exist and exclude `ai/` if repo has `ai/` directory
2. `ai/` directory must exist for `-private` repos (scaffold check)

**Verify:** `wip-release patch --dry-run` in a repo without `.license-guard.json` must FAIL.

---

## WAVE 1: Release Pipeline Completion (1-2 sessions) ... SHIPPED 2026-04-08

**Repo:** `wip-ai-devops-toolbox-private`
**File:** `tools/wip-release/core.mjs`

### Phase 3: Publish before commit
Current order: git commit+tag -> push -> npm publish
If npm fails, git has orphan tag. Permanent divergence.
Fix: git commit+tag -> npm publish -> push. On npm failure: remove tag, reset commit.

### Phase 5: Auto-publish sub-tools
`validateSubToolVersions()` (line 1391) warns on drift but doesn't fix.
Add: auto-bump sub-tool `package.json` patch version when files changed since last tag.

**Verify:** Force npm publish failure, verify clean rollback. Change sub-tool file, verify auto-bump in `--dry-run`.

---

## WAVE 2: Installer Fixes (1-2 sessions) ... SHIPPED 2026-04-08

**Repo:** `wip-ldm-os-private`
**Files:** `bin/ldm.js`, `lib/deploy.mjs`

### Fix 1: Template deploy path
`bin/ldm.js` line ~1018: `settings/templates/` -> `library/templates/`

### Fix 2: tools.allow update on plugin install
`lib/deploy.mjs`: After deploying plugin to `~/.openclaw/extensions/`, read `openclaw.json`, add plugin to `tools.allow` if not present.

### Fix 3: Bridge deploy filter
`bin/ldm.js` `deployBridge()` line ~637: Create bridge dir if missing instead of skipping with `.filter(t => existsSync(t.dir))`.

### Fix 4: Rules deploy on every install
Extract rules deployment from `cmdInit()` (lines 947-986) into `deployRules()`. Call from both `cmdInit()` and `cmdInstallCatalog()`.

**Verify:** `ldm install --dry-run` shows no `settings/` paths. After install, `tools.allow` includes new plugins. Bridge dir created on first install.

---

## WAVE 3: Documentation Sync (2-3 sessions) ... Sessions 1+2 SHIPPED 2026-04-08, Session 3 partial

### Session 1: Fix stale path references
- `~/wipcomputerinc/CLAUDE.md`: `settings/` -> `library/` in directory tree
- All rules files: `settings/config.json` -> `~/.ldm/config.json`
- All docs referencing `settings/docs/` -> `library/documentation/`

### Session 2: ~/.ldm/shared/ -> ~/.ldm/library/ rename
- `bin/ldm.js`: All `join(LDM_ROOT, 'shared', ...)` -> `join(LDM_ROOT, 'library', ...)`
- Safety net: symlink `~/.ldm/shared -> ~/.ldm/library` for backward compat
- Update Lesa's workspace files (TOOLS.md, MEMORY.md)
- 8-phase execution per `2026-04-08--shared-to-library-refactor.md`

### Session 3: Seed repos (DONE: 2 of 13 manually)
- `.license-guard.json` in every repo missing it (~11 remaining)
- Per-repo `CLAUDE.md` for repos missing them (~8 repos)
- `CLA.md` where missing
- wip-ldm-os-private: DONE
- wip-x-xai-grok-private: DONE

### Wave 3.3: Manifest-driven compliance (replaces manual seeding)

Instead of manually seeding each repo, add compliance enforcement to `wip-repos sync`:

**Source of truth:** `~/wipcomputerinc/repos/repos-manifest.json`
- Already lists every repo and its GitHub remote (80+ entries)
- Stale: missing kaleidoscope-private, wip-x-xai-grok-private, wip-cloud-private, upgrade repo

**`wip-repos sync --compliance`** (new mode):
1. Iterate every repo in manifest that has a local path
2. Check for: `.license-guard.json`, `CLA.md`, `LICENSE` (dual MIT+AGPL), `.npmignore` (if `ai/` exists)
3. Report missing items. With `--fix`: create them using WIP Computer defaults
4. Uses `wip-license-guard check --fix` per repo for the actual file generation

**`wip-repo-init` hook:**
When `wip-repo-init` scaffolds a new repo, it must also:
1. Add the repo to `repos-manifest.json` (path + GitHub remote)
2. Create `.license-guard.json`, `CLA.md`, `LICENSE` as part of scaffold
3. This ensures no repo exists without being in the manifest

**Manifest watchdog (cron or daily audit):**
Scan `~/wipcomputerinc/repos/` recursively for git repos. Compare against `repos-manifest.json`.
- Alert if a repo exists on disk but is NOT in the manifest
- Alert if a manifest entry points to a path that doesn't exist
- Run daily or on `ldm install`

**Files to change:**
- `tools/wip-repos/core.mjs`: add `sync --compliance` mode
- `tools/wip-repo-init/core.mjs`: add manifest update step
- `repos-manifest.json`: update with missing repos
- `bin/ldm.js` or daily cron: call manifest watchdog

**Verify:** `wip-repos sync --compliance --dry-run` lists all missing configs. After `--fix`, all repos pass.

---

## WAVE 4: Operational Hygiene (2-3 sessions)

### Daily workspace audit
New cron or healthcheck extension. Checks:
- Uncommitted work in any repo worktree
- Stale worktrees (>14 days, no commits)
- Files in wrong locations
- Hardcoded keys (grep for sk-ant-api, xai-, ghp_, ops_, tvly-)
- Commits that bypassed PR
- **Repos on disk but not in repos-manifest.json** (from Wave 3.3 watchdog)

### Doc pipeline completion
- Step 5b: Replace Mintlify starter content with real docs
- Step 6: Add TECHNICAL.md gate to wip-release for minor/major releases

### Per-repo TECHNICAL.md
6 repos missing: agent-pay, markdown-viewer, xai-grok, x-platform, dream-weaver, healthcheck

---

## Dependency Order

```
WAVE 0 (must ship first, blocks everything)
  |
  +-- WAVE 1 (same file as Wave 0, ship after)
  |
  +-- WAVE 2 (independent repo, can parallel with Wave 1)
       |
       +-- WAVE 3 (depends on Wave 2 installer fixes)
            |
            +-- WAVE 4 (depends on everything being stable)
```

## Files Changed Summary

| Wave | File | What |
|------|------|------|
| 0 | `tools/wip-release/core.mjs` | Block without .license-guard.json (3 locations) |
| 1 | `tools/wip-release/core.mjs` | Publish-before-commit, auto-bump sub-tools |
| 2 | `bin/ldm.js` | Deploy paths, bridge filter, rules deploy |
| 2 | `lib/deploy.mjs` | tools.allow update |
| 3 | `~/wipcomputerinc/CLAUDE.md` | Fix stale paths |
| 3 | `bin/ldm.js` | shared/ -> library/ rename |
| 3 | Every repo | Seed .license-guard.json, CLAUDE.md, CLA.md |
| 4 | New: audit cron | Daily workspace checks |
| 4 | `tools/wip-release/core.mjs` | TECHNICAL.md gate |

## Estimated Scope

| Wave | Sessions | Time |
|------|----------|------|
| 0 | 1 | 30 min |
| 1 | 1-2 | 2 hrs |
| 2 | 1-2 | 2 hrs |
| 3 | 2-3 | 3-4 hrs |
| 4 | 2-3 | 2-3 hrs |
| **Total** | **7-11** | **~3-5 working days** |
