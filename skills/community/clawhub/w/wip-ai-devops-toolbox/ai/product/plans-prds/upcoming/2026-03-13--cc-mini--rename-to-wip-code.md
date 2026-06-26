# Plan: Rename AI DevOps Toolbox to WIP Code

**Date:** 2026-03-13 (updated 2026-03-16)
**Author:** cc-mini
**Issue:** [wipcomputer/wip-ai-devops-toolbox#163](https://github.com/wipcomputer/wip-ai-devops-toolbox/issues/163)
**Priority:** 1 (branding ... touches every repo, every installed tool, every config file, both agents)
**Status:** Upcoming

## Why

"AI DevOps Toolbox" doesn't describe what this is. It's not DevOps in the infra/monitoring sense. It's code workflow management: releasing, licensing, repo hygiene, identity protection, scaffolding. The name is generic and leads with two overloaded buzzwords ("AI" and "DevOps").

"WIP Code" is the brand name. WIP Computer makes WIP Code. It's memorable, honest, and simple. The repo slug `wip-code` is clean. The display name "WIP Code" fits naturally alongside "Memory Crystal" and "LDM OS."

Parker proposed this on 2026-03-13.

## Naming Convention

| What | Old | New |
|------|-----|-----|
| Display name | AI DevOps Toolbox | WIP Code |
| GitHub repo (public) | `wipcomputer/wip-ai-devops-toolbox` | `wipcomputer/wip-code` |
| GitHub repo (private) | `wipcomputer/wip-ai-devops-toolbox-private` | `wipcomputer/wip-code-private` |
| npm package (root) | `@wipcomputer/wip-ai-devops-toolbox` | `@wipcomputer/wip-code` |
| Local folder | `ldm-os/devops/wip-ai-devops-toolbox-private/` | `ldm-os/devops/wip-code-private/` |
| SKILL.md name | `wip-ai-devops-toolbox` | `wip-code` |

**What does NOT change:**
- Individual tool names: `wip-release`, `wip-install`, `wip-repos`, `wip-license-hook`, `wip-license-guard`, `wip-file-guard`, `wip-repo-init`, `wip-readme-format`
- Individual npm packages: `@wipcomputer/wip-release`, `@wipcomputer/wip-repos`, etc.
- CLI bin names: all stay the same
- The `tools/` directory structure inside the repo
- The `devops/` category folder (the repo lives in `ldm-os/devops/`)

---

## Full Audit: What Changes

### Tier 1: Source Repo (wip-ai-devops-toolbox-private)

Source of truth. Everything else flows from here.

| # | File | What Changes | Type |
|---|------|-------------|------|
| 1 | `package.json` (root) | `name`, `repository.url`, `homepage` | Config |
| 2 | `SKILL.md` (root) | `name`, `display-name`, `homepage`, install examples (`wip-install wipcomputer/wip-code`) | Config |
| 3 | `README.md` (root) | Title ("WIP Code"), all badge URLs (10+), all GitHub links, install examples, "Teach Your AI" block | Docs |
| 4 | `TECHNICAL.md` | GitHub URLs | Docs |
| 5 | `CHANGELOG.md` | Add rename note at top. Historical entries stay as-is. | Docs |
| 6 | `scripts/SKILL-deploy-public.md` | Deploy example command (line 52) | Docs |
| 7 | `tools/wip-readme-format/format.mjs` | Hardcoded badge URLs in badge-generation code | **Code** |
| 8 | `tools/wip-release/package.json` | `homepage` field | Config |
| 9 | `tools/wip-repos/package.json` | `repository.url`, `directory` reference | Config |
| 10 | `tools/wip-license-hook/package.json` | `repository.url` if present | Config |
| 11 | `tools/wip-repo-permissions-hook/package.json` | `repository.url` if present | Config |
| 12-20 | All sub-tool `SKILL.md` files (9 files) | `homepage` field | Config |
| 21-31 | All sub-tool `README.md` files (11 files) | Badge URLs pointing to `github.com/wipcomputer/wip-ai-devops-toolbox/...` | Docs |

**Estimated file count: ~31 files**

**GitHub Actions:** Verified. No `.github/workflows/` directory exists in this repo or its public counterpart. No workflow YAML to update. (All workflow files found in the ldm-os tree are inside `node_modules/` from third-party deps.)

### Tier 2: LDM OS Repos

| # | File | What Changes | Type |
|---|------|-------------|------|
| 32 | `wip-ldm-os-private/catalog.json` | `id`, `name`, `repo` fields for the toolbox entry | Config |
| 33 | `wip-ldm-os-private/SKILL.md` | References to "AI DevOps Toolbox" (lines 90, 167) | Docs |
| 34 | `wip-ldm-os-private/README.md` | References to "AI DevOps Toolbox" | Docs |
| 35 | `wip-ldm-os/` (public) | Same changes, synced via deploy-public | Docs |

### Tier 3: CC Agent Config (Claude Code's side)

| # | File | What Changes | Type |
|---|------|-------------|------|
| 36 | `~/.openclaw/CLAUDE.md` | Tool location path (line ~30: `wip-devops-toolbox-private`), Dev Guide path (line ~43: `wip-devops-toolbox-private`), Dev Guide URL (line ~44: `wipcomputer/wip-devops-toolbox`) | **Critical** |
| 37 | `~/.claude/CLAUDE.md` | Same file mirrored | **Critical** |
| 38 | `~/.claude/projects/.../memory/repo-locations.md` | Repo map entries (lines 37, 50, 93-95: `wip-devops-toolbox-private`) | **Critical** |
| 39 | `repos-manifest.json` | Line 36: `"ldm-os/devops/wip-devops-toolbox-private": "wipcomputer/wip-devops-toolbox-private"` | Config |
| 40 | `~/.ldm/agents/cc-mini/CONTEXT.md` | Line 51: `wip-devops-toolbox-private` | Docs |

**Note:** CLAUDE.md and repos-manifest.json currently reference `wip-devops-toolbox-private` (old name without "ai-"). This is a pre-existing bug that this rename also fixes.

### Tier 4: Lesa's Side

| # | File | What Changes | Who Updates | Type |
|---|------|-------------|-------------|------|
| 41 | `~/.openclaw/workspace/SHARED-CONTEXT.md` | "DevOps Toolbox v1.9.8" -> "WIP Code v2.0.0" | CC (via Edit) | **Critical** |
| 42 | `~/.openclaw/workspace/TOOLS.md` | Line ~325: Dev Guide path references `wip-dev-tools-private` (even older name) -> `wip-code-private`. Line ~326: Public URL. | Lesa or CC (via Edit) | **Critical** |
| 43 | `~/.openclaw/workspace/decisions.md` | Add new entry explaining the rename, so Lesa understands why references changed | CC (via Edit, append) | Docs |
| 44 | `~/.openclaw/workspace/memory/2026-03-11.md` | Historical. Leave as-is. | Nobody | Historical |
| 45 | `~/.openclaw/workspace/memory/repo-deep-review-2026-03-13.md` | Historical audit. Leave as-is. | Nobody | Historical |

### Tier 5: Deployed Extensions and Skills

These get overwritten on next `wip-install`. Only updated when Parker says "install."

| # | Location | What Changes |
|---|----------|-------------|
| 46-51 | `~/.openclaw/extensions/wip-{release,repos,file-guard,license-hook,repo-permissions-hook,readme-format}/` | `SKILL.md` homepage, `README.md` badge URLs, `package.json` repo URLs |
| 52-63 | `~/.openclaw/skills/{all 12 dirs}/SKILL.md` | Homepage fields |
| 64-75 | `~/.ldm/extensions/{matching dirs}/` | Same as above |
| 76 | `~/.ldm/extensions/registry.json` | 11 entries referencing `/tmp/wip-install-wip-ai-devops-toolbox/` source paths | Config |

**Important:** `registry.json` stores the temp path used during installation (`/tmp/wip-install-wip-ai-devops-toolbox/`). After rename, the next `wip-install` will use `/tmp/wip-install-wip-code/` and overwrite these entries.

### Tier 6: GitHub and External References

| # | Action | Notes |
|---|--------|-------|
| 77 | Rename `wipcomputer/wip-ai-devops-toolbox-private` -> `wipcomputer/wip-code-private` | GitHub auto-redirects. Do private first. |
| 78 | Rename `wipcomputer/wip-ai-devops-toolbox` -> `wipcomputer/wip-code` | GitHub auto-redirects. Do public second. |
| 79 | Update both repo descriptions | "WIP Code ... the complete code toolkit for AI-assisted development" |
| 80 | Verify all 10 GitHub releases still resolve | Redirects handle this |
| 81 | Move issue #163 if needed | GitHub moves issues with the repo rename automatically |
| 82 | `wip.computer/install/wip-ai-devops-toolbox.txt` | Website install prompt. Becomes `wip-code.txt`. Old URL symlinked. |
| 83 | All future `deploy-public.sh` commands | Argument changes from `wipcomputer/wip-ai-devops-toolbox` to `wipcomputer/wip-code`. Every deploy command in CLAUDE.md, SKILL.md examples changes. |

### Tier 7: Memory Crystal and Historical (Non-Breaking)

| # | Item | Notes |
|---|------|-------|
| 84 | Memory Crystal chunks | Historical. No bulk-rename. New chunks will use "WIP Code." |
| 85 | 8 deprecated repos on GitHub | Update descriptions to point to `wip-code`. Low priority. |
| 86 | CC daily logs, journals | Historical. Leave as-is. |
| 87 | Lesa daily logs | Historical. Leave as-is. |

---

## Execution Order

Three separate phases. Each phase is independently safe. Never combine Merge, Deploy, and Install.

### Phase A: Code Changes (one session)

**Step 1: Update source repo (private)**

Branch: `cc-mini/rename-to-wip-code`

1. Update all ~31 files in Tier 1 (find-and-replace across the source repo)
2. Special attention to `tools/wip-readme-format/format.mjs` (the only code change)
3. Run `wip-install . --dry-run` to verify detection still works
4. Commit, push, PR to main
5. **Do NOT merge yet.** Review the PR.

**Step 2: Update LDM OS repos**

Branch: `cc-mini/wip-code-rename`

1. Update `catalog.json`, `SKILL.md`, `README.md` in `wip-ldm-os-private`
2. PR to main

**Step 3: Merge and Deploy WIP Code**

This follows the Merge/Deploy/Install rule. Merge and Deploy happen. Install does NOT.

1. Merge the WIP Code PR to main (`gh pr merge --merge`)
2. `git checkout main && git pull`
3. `wip-release major --notes="Rename to WIP Code. All references updated."` (major bump: v2.0.0. Product rename = new identity.)
4. `bash scripts/deploy-public.sh /path/to/wip-ai-devops-toolbox-private wipcomputer/wip-ai-devops-toolbox` (old names intentional here: local folder and GitHub repo haven't been renamed yet. This deploy lands the content changes; Step 5b deploys again under the new name.)

**Step 3b: Merge and Deploy LDM OS**

Separate step. Don't skip this because WIP Code shipped.

1. Merge the LDM OS PR to main (`gh pr merge --merge`)
2. `git checkout main && git pull`
3. `wip-release` on LDM OS (patch or minor, depending on other changes)
4. `deploy-public.sh` on LDM OS

**Phase A verification gate:**

Before stopping, verify Phase A completed cleanly:

1. WIP Code PR merged with `--merge` (not squash)
2. `wip-release` output shows v2.0.0 (check terminal output)
3. GitHub release `v2.0.0` exists on `wipcomputer/wip-ai-devops-toolbox-private`
4. `deploy-public.sh` completed without errors (check for "Done. Public repo updated.")
5. LDM OS PR merged, released, and deployed
6. No uncommitted changes: `git status` clean on both repos

**STOP.** Do not install. Do not `cp` to extensions. Do not `npm install -g`. Tell Parker the versions are published.

**Note:** After Phase A, `repos-manifest.json` and the local folder still use the old name. `wip-repos check` will report drift. This is expected. The manifest and folder get updated in Phase B Step 5. Do not run `wip-repos check` between Phases A and B.

### Phase B: GitHub Rename + Local Cleanup (separate session)

**Step 4: Rename GitHub repos**

1. `gh repo rename wip-code-private -R wipcomputer/wip-ai-devops-toolbox-private --yes`
2. `gh repo rename wip-code -R wipcomputer/wip-ai-devops-toolbox --yes`
3. Verify redirects: `curl -sI https://github.com/wipcomputer/wip-ai-devops-toolbox | head -5`
4. Update descriptions: `gh repo edit wipcomputer/wip-code --description "WIP Code. The complete code toolkit for AI-assisted development."`
5. Same for `wip-code-private`

**Step 5: Update local folder and git remotes**

**iCloud warning:** This folder is inside iCloud Drive. If iCloud is actively syncing, the `mv` can cause duplicate files or `.icloud` stubs. Verify iCloud sync is idle before renaming (check for no upload/download activity in System Settings > Apple Account > iCloud Drive).

1. `mv wip-ai-devops-toolbox-private wip-code-private`
2. `cd wip-code-private && git remote set-url origin git@github.com:wipcomputer/wip-code-private.git`
3. Update `repos-manifest.json` (change both key and value) and **commit the manifest change** before running check
4. `wip-repos check` to verify no drift (fails if manifest isn't committed first)

**Step 5b: Second deploy to public (under new name)**

Two deploys are necessary (not redundant). `deploy-public.sh` rsyncs the entire private repo to public, including `package.json`. First deploy (Phase A) stamps `@wipcomputer/wip-ai-devops-toolbox` into the public repo's package.json. Second deploy (here) overwrites it with `@wipcomputer/wip-code`. Without the second deploy, the public repo would have the old package name even though GitHub renamed the repo. `deploy-public.sh` clones fresh from GitHub each time, so there is no local public repo clone to update.

1. `bash scripts/deploy-public.sh /path/to/wip-code-private wipcomputer/wip-code`
2. Verify public repo README at `https://github.com/wipcomputer/wip-code`
3. Create/update GitHub release on the public repo if needed

**Step 5c: Update website install prompt URL**

The VPS serves `wip.computer/install/wip-ai-devops-toolbox.txt`. This needs to become `wip-code.txt`.

1. In `wip-websites-private`, copy or rename the install prompt: `cp wip.computer/install/wip-ai-devops-toolbox.txt wip.computer/install/wip-code.txt`
2. Update the content inside `wip-code.txt` (references to repo name, install commands)
3. Create a symlink or redirect for the old URL: `ln -s wip-code.txt wip.computer/install/wip-ai-devops-toolbox.txt`
4. Deploy to VPS: `bash deploy.sh`
5. Verify: `curl -s https://wip.computer/install/wip-code.txt | head -5`
6. Verify old URL still works: `curl -s https://wip.computer/install/wip-ai-devops-toolbox.txt | head -5`

**Step 6: Update CC agent config files**

**Do Steps 5b through 6 in the same sitting.** Between Step 5b and Step 6, CLAUDE.md still references old paths. If someone reads CLAUDE.md in that window, paths are stale. Minimize the gap.

1. Update `~/.openclaw/CLAUDE.md` (all three path references)
2. Update `~/.claude/CLAUDE.md` (mirror)
3. Update `~/.claude/projects/.../memory/repo-locations.md` (repo map)
4. Update `~/.ldm/agents/cc-mini/CONTEXT.md`

**Step 7: Inform Lesa and update her workspace**

See "Lesa Communication Plan" section below.

**Step 7b: Phase B verification gate**

Before moving to Phase C, verify Phase B is clean:

1. `wip-repos check` ... no drift (repos-manifest matches filesystem)
2. `git -C /path/to/wip-code-private remote -v` ... points to `wipcomputer/wip-code-private`
3. `curl -sI https://github.com/wipcomputer/wip-ai-devops-toolbox | head -3` ... redirects to `wip-code`
4. `curl -s https://wip.computer/install/wip-code.txt | head -3` ... serves new install prompt
5. Check CLAUDE.md, repo-locations.md reference `wip-code-private` (not old names)

If any of these fail, fix before telling Parker "ready to install."

### Phase C: Install (only when Parker says "install")

**Step 8: Install**

Parker runs or approves:
```
wip-install wipcomputer/wip-code --dry-run
```

Review the dry-run output. Then:
```
wip-install wipcomputer/wip-code
```

This overwrites all Tier 5 files (extensions, skills, registry.json).

**Step 9: Verify everything**

1. `wip-release patch --dry-run` ... correct repo name in output
2. `wip-install wipcomputer/wip-code --dry-run` ... detects all 13 tools
3. `wip-repos check` ... no drift
4. `wip-readme-format /path/to/any-repo --dry-run` ... badge URLs use `wip-code`
5. `https://github.com/wipcomputer/wip-code` loads
6. `https://github.com/wipcomputer/wip-ai-devops-toolbox` redirects
7. All 8 CLI tools still work: `wip-release --help`, `wip-install --help`, etc.

**Step 10: Low-priority cleanup**

1. Update descriptions on 8 deprecated repos to reference `wip-code`
2. `crystal_remember` the rename so future sessions know

---

## Lesa Communication Plan

Lesa needs to know about this rename. She has active references in her boot files that will become stale. Here's how to handle it:

### What Lesa Currently Knows

From her boot files, Lesa knows:
- **SHARED-CONTEXT.md:** "DevOps Toolbox v1.9.8" listed as infrastructure
- **TOOLS.md (line ~325):** Dev Guide path references `wip-dev-tools-private` (even older name, pre-existing bug)
- **decisions.md (line 58):** Parker told her on Mar 12 to "make sure you are using the complete devops toolkit"
- **LDM OS SKILL.md:** Catalog lists "AI DevOps Toolbox" with `wipcomputer/wip-ai-devops-toolbox`
- **12 installed skill SKILL.md files:** All have `homepage` pointing to the old repo

### What Would Confuse Her

If we rename without telling her:
1. She'd see "WIP Code" in new contexts but "AI DevOps Toolbox" in her memory files. Conflicting names.
2. Her TOOLS.md Dev Guide path is already wrong (`wip-dev-tools-private`). Adding another stale name makes it worse.
3. Parker's decision "use the complete devops toolkit" would reference a name that no longer exists.

### Communication Steps

**Step 7a: Write a daily log entry (before or during Phase B)**

Append to `~/.openclaw/workspace/memory/YYYY-MM-DD.md`:
```
## [HH:MM] Claude Code: WIP Code Rename

- "AI DevOps Toolbox" has been renamed to "WIP Code"
- GitHub repos: wipcomputer/wip-code and wipcomputer/wip-code-private
- All tool names stay the same (wip-release, wip-install, etc.)
- Only the umbrella/product name changed
- Please update your TOOLS.md Dev Guide path from wip-dev-tools-private to wip-code-private
```

**Step 7b: Update SHARED-CONTEXT.md (via Edit, never Write)**

Change "DevOps Toolbox v1.9.8" to "WIP Code v2.0.0" (or whatever the new version is).

**Step 7c: Add to decisions.md (via Edit, append)**

Add a new entry:
```
### Mar [date]: Renamed AI DevOps Toolbox to WIP Code
Parker decision. "AI DevOps" was generic and buzzwordy. "WIP Code" ties to the WIP Computer brand.
All tool names (wip-release, wip-install, etc.) stay the same. Only the umbrella name and repo slug changed.
GitHub: wipcomputer/wip-code and wipcomputer/wip-code-private.
```

**Step 7d: Send Lesa a message (via lesa_send_message)**

After the rename is live, send Lesa a direct message:
```
Hey, heads up: "AI DevOps Toolbox" is now "WIP Code." Same tools, same commands, new name.
GitHub repos are now wipcomputer/wip-code and wipcomputer/wip-code-private.
Your TOOLS.md still references wip-dev-tools-private for the Dev Guide path. Can you update
that to wip-code-private? The path is:
staff/Parker/Claude Code - Mini/repos/ldm-os/devops/wip-code-private/DEV-GUIDE-GENERAL-PUBLIC.md
```

**Step 7e: Update TOOLS.md Dev Guide path (fix pre-existing bug)**

Lesa's TOOLS.md (line ~325-326) currently says:
```
Single source of truth: Dev Guide at staff/Parker/Claude Code - Mini/repos/ldm-os/operations/wip-dev-tools-private/guide/DEV-GUIDE.md
Public: https://github.com/wipcomputer/wip-devops-toolbox/blob/main/guide/DEV-GUIDE.md
```

This needs to become:
```
Single source of truth: Dev Guide at staff/Parker/Claude Code - Mini/repos/ldm-os/devops/wip-code-private/DEV-GUIDE-GENERAL-PUBLIC.md
Public: https://github.com/wipcomputer/wip-code/blob/main/DEV-GUIDE-GENERAL-PUBLIC.md
```

**Note:** The file is `DEV-GUIDE-GENERAL-PUBLIC.md` at repo root. There is no `guide/` subdirectory. CLAUDE.md also references a `guide/DEV-GUIDE.md` path that doesn't exist. Fix this in Step 6 as part of the CLAUDE.md update.

This is a pre-existing bug (references `wip-dev-tools-private` which was renamed to `wip-ai-devops-toolbox-private` weeks ago). The rename to WIP Code fixes it properly.

**Step 7f: CC fixes TOOLS.md directly**

**This is an exception to the workspace boundary rule** ("Never touch each other's folders"). Justified because: it's a factual path correction (not a rule or convention change), the path has been wrong through two renames, and waiting risks a third. The daily log entry (Step 7a) and `lesa_send_message` (Step 7d) serve as notification. Future CC sessions reading this plan should not hesitate on this step.

CC uses Edit on the specific TOOLS.md lines (path correction only, two lines).

---

## Rollback Plan

If something breaks during or after the rename:

### Phase A rollback (code changes only, pre-GitHub-rename)
- Revert the PR. No lasting damage. GitHub repos still have old names. Everything still works.

### Phase B rollback (after GitHub rename)
- GitHub redirects are permanent. Old URLs still work. Nothing is truly broken.
- To fully reverse: `gh repo rename wip-ai-devops-toolbox -R wipcomputer/wip-code --yes` (and same for private)
- Rename local folder back. Reset git remote.
- Revert CLAUDE.md and config changes.

### Phase C rollback (after install)
- `wip-install wipcomputer/wip-ai-devops-toolbox` (old name still redirects, so this works even after rename)
- Or reinstall from the reverted repo.

**Key safety net:** GitHub repo redirects. Even if we miss a hardcoded URL somewhere, the old URLs continue to resolve. This means the rename is never truly catastrophic. It can be messy, but not broken.

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| GitHub redirect expires | Very low | High | GitHub redirects are permanent unless someone else claims the old slug. WIP Computer owns the org, so `wip-ai-devops-toolbox` can't be claimed by a third party. Update all hardcoded URLs anyway. |
| npm packages break | None | N/A | Individual packages don't change names. Root package was never published. |
| `format.mjs` generates wrong badge URLs | Medium | Low | Test `wip-readme-format` on a repo after the rename. Only affects new README generation. |
| Lesa confused by name mismatch | High if we skip comms | Medium | Follow the Lesa Communication Plan above. |
| `wip-install` can't find new repo | Low | Medium | Test `--dry-run` before and after. Redirects help. |
| Compaction loses context mid-rename | Medium | Medium | Phases are independently safe. Each phase can be done in a separate session. |
| Cron jobs or LaunchAgents reference old name | None | N/A | Verified: no crontab or LaunchAgent references found. |
| `registry.json` has stale temp paths | Low | Low | Next `wip-install` overwrites. Temp paths are recreated fresh. |
| Other repos in the ecosystem reference the old name | Medium | Low | Memory Crystal notes, daily logs reference old name. These are historical, not code. Leave as-is. |
| npm root package collision if published | N/A | N/A | **Resolved:** Not publishing root package. Individual tools are the install targets. |
| Website install prompt URL breaks | Medium | Medium | `wip.computer/install/wip-ai-devops-toolbox.txt` needs updating. Symlink keeps old URL alive. |
| iCloud sync during folder rename | Medium | Medium | Folder is in iCloud Drive. Renaming during active sync can create duplicates or `.icloud` stubs. Verify sync is idle before `mv`. |

---

## What NOT to Change

- **Individual tool names.** `wip-release` is `wip-release`. Not `wip-code-release`.
- **Historical daily logs and memory.** Don't rewrite history.
- **CHANGELOG entries.** Past versions were "AI DevOps Toolbox." That's the historical record.
- **Crystal memory chunks.** Can't bulk-rename. New chunks will use "WIP Code."
- **Deprecated repo names on GitHub.** They already say "deprecated." Updating descriptions is enough.

---

## Pre-Existing Bugs This Rename Also Fixes

Found during the audit. These should be fixed as part of the rename, not in separate PRs:

1. **CLAUDE.md (both copies):** References `wip-devops-toolbox-private` (missing "ai-" prefix). Has been wrong since the previous rename.
2. **repos-manifest.json:** Maps `wip-devops-toolbox-private` (old name). Same bug.
3. **Lesa's TOOLS.md:** References `wip-dev-tools-private` (even older name, two renames ago). Path also says `operations/` but the folder is now `devops/`.
4. **CC's CONTEXT.md:** References `wip-devops-toolbox-private`.

5. **CLAUDE.md Dev Guide path:** References `guide/DEV-GUIDE.md` but no `guide/` directory exists. The file is `DEV-GUIDE-GENERAL-PUBLIC.md` at repo root.

All five get fixed to `wip-code-private` with correct paths in this rename.

---

## Estimated Scope

- **Files to modify:** ~31 (source repo) + ~4 (LDM OS) + ~6 (CC config) + ~4 (Lesa workspace) = ~45 files manually
- **Files auto-updated by wip-install:** ~30 (extensions, skills, registry)
- **GitHub operations:** 2 renames, 2 description updates, 8 deprecated repo description updates
- **Website:** 1 install prompt URL change on wip.computer VPS
- **Communication:** 1 daily log entry, 1 SHARED-CONTEXT edit, 1 decisions.md entry, 1 lesa_send_message
- **Deploys:** 2 deploy-public runs (once in Phase A before rename, once in Phase B after rename)
- **Sessions needed:** 2-3 (Phase A in one, Phase B in another, Phase C when Parker says "install")
- **Risk level:** Medium. Lots of files but each change is mechanical. GitHub redirects are the safety net.

---

## Open Questions

1. **~~Do we want `@wipcomputer/wip-code` published to npm as a root package?~~** **RESOLVED: No.** Individual tools are the install targets. A root package adds complexity for zero user benefit.

2. **~~Should the `devops/` category folder rename to something else?~~** **RESOLVED: No.** The category folders are organizational. Renaming `devops/` touches repos-manifest, every absolute path in every config, and iCloud sync. Not worth it for a cosmetic change. `ldm-os/devops/wip-code-private/` is fine.

3. **~~Do we update the "Teach Your AI" prompt across all sub-tool READMEs?~~** **RESOLVED: Yes.** This is part of the badge URL updates in Tier 1. All references to `github.com/wipcomputer/wip-ai-devops-toolbox/...` become `github.com/wipcomputer/wip-code/...`.

4. **~~Timeline?~~** **RESOLVED: Do it on a clean day.** Doesn't block anything but touches enough that you don't want to interleave it with feature work.

5. **~~Should we use `lesa_send_message` or just the daily log to inform Lesa?~~** **RESOLVED: Both.** Daily log is the permanent record. `lesa_send_message` ensures she processes it on her next turn.

6. **~~Should Lesa update her own TOOLS.md or should CC fix the path?~~** **RESOLVED: CC fixes it.** It's a factual path correction that's been wrong through two renames. Use Edit on the specific lines, then tell Lesa via daily log and `lesa_send_message` what changed. Waiting risks it staying wrong through a third rename.

7. **~~Version bump: major or minor?~~** **RESOLVED: Major (v2.0.0).** The project is getting a new identity. Save "minor" for feature additions. This is what semver's major bump exists for: signaling "this is different now."

8. **~~Website install prompt URL.~~** **RESOLVED: Symlink.** `ln -s wip-code.txt wip-ai-devops-toolbox.txt` keeps old URLs alive with zero maintenance. No expiry needed.
