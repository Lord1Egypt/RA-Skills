# AI DevOps Toolbox ... Roadmap

**Last updated:** 2026-04-21
**Current version:** v1.9.72

Items are either **Upcoming**, **Done**, or **Deprecated**. Never delete. Always move.

---

## What This File Is

The prioritized roadmap for this product. Three sections:

- **Upcoming** ... work that's planned, ordered by priority. Top = most important.
- **Done** ... shipped work. Moved here with a date when it's released.
- **Deprecated** ... planned work that's no longer needed. Strikethrough, add the reason and date. Not the same as Done. Done means it shipped. Deprecated means the plan changed.

**Keep it honest.** If something isn't going to happen, deprecate it. Don't leave dead items in Upcoming.

**Keep it prioritized.** Upcoming items have priority numbers. When priorities shift, renumber them. The order is the strategy.

---

## Vision

Every AI tool you build ships with the right interfaces, the right documentation, and the right compliance. One toolbox, one install command, one release command. The AI does the devops. You do the product.

---

## Upcoming

### Priority 1 ... Public Launch Materials

Demo and template repo so people can try the tools without reading docs.

- [ ] Record 2-minute demo video of wip-release in action
- [ ] Create example template repo for cloning and testing

### Priority 2 ... Daily Dev Summary

Scan all repos' `ai/dev-updates/` for today's updates, aggregate into one daily summary, save to `wip-inc/operations/daily/`. Parker reads one file, knows everything that happened across the org.

- [ ] Core scanner using repos-manifest.json to find repos
- [ ] Summary writer (grouped by repo, agent, time)
- [ ] Scheduled automation (LaunchAgent or LDM Dev Tools.app)
- [ ] Notification via Lesa

### Priority 3 ... GitHub Actions Pack

CI/CD integration. Run license checks, release pipeline, and visibility audits in GitHub Actions.

- [ ] GitHub Action for wip-license-hook (scan on PR)
- [ ] GitHub Action for wip-release (release on merge to main)
- [ ] GitHub Action for repo visibility audit

### Priority 4 ... Security Suite

SBOM generation, CVE scanning, dependency auditing beyond license changes.

- [ ] SBOM generator
- [ ] CVE scanning integration
- [ ] Security audit automation

---

## Done

### License Guard CC Hook (2026-03-16)

- [x] guard.mjs wired as PreToolUse hook (blocks git commit/push on license failures)
- [x] claudeCode.hook config in package.json (auto-registers on ldm install)
- [x] wip-release gate (blocks release on license failures)
- [x] `--from-standard` for WIP Computer defaults
- [x] Plan: `plans-prds/current/2026-03-10--cc-mini--license-guard-hooks.md`

### npm Publish Unblocked (2026-03-16)

- [x] npm token working (all 12 sub-tools publishing to npm)
- [x] GitHub Packages publishing from public repos via deploy-public.sh
- [x] Old packages deleted from org packages page, republished from public

### Branch Guard + Safety Flags (2026-03-16)

- [x] Branch guard blocks Write, Edit, NotebookEdit, Bash on main
- [x] `--no-verify` blocked on any branch (prevents hook bypass)
- [x] `git push --force` blocked (--force-with-lease still allowed)
- [x] Global git pre-commit hook blocks commits on main/master

### SKILL.md Install Experience (2026-03-14 - 2026-03-16)

- [x] Rewritten to use `ldm install` (replaces deprecated wip-install)
- [x] Conversational, Memory Crystal-style install flow
- [x] Transparency block (explains what will change)
- [x] Dry run, install, verify steps
- [x] All 17 tools listed with descriptions
- [x] Dogfooded 20+ iterations
- [x] Plan: `plans-prds/current/2026-03-14--cc-mini--skill-ldm-install.md`

### Bootstrap LDM OS (2026-03-16)

- [x] wip-install auto-installs LDM OS when not on PATH
- [x] Falls back to standalone installer if bootstrap fails
- [x] Plan: `plans-prds/current/bootstrap-ldm-os.md`

### Release Notes Quality Gate Upgrade (2026-03-15 - 2026-03-16)

- [x] --notes flag blocked entirely (notes must come from file on disk)
- [x] Release notes must reference issues (#XX)
- [x] Auto-close referenced issues after GitHub release
- [x] scaffoldReleaseNotes() creates template with auto-detected issues
- [x] Skill publish to website on every release (.publish-skill.json)

### deploy-public.sh Improvements (2026-03-16)

- [x] --dry-run support
- [x] GitHub Packages publish from public repo clone
- [x] Co-author lines on sync commits
- [x] wip-release no longer publishes to GitHub Packages (deploy-public.sh handles it)

### --version Flags (2026-03-15)

- [x] All 12 CLI tools now support --version flag

### Interface Coverage Reorder (2026-03-16)

- [x] Tables reordered: Setup, Infrastructure, Repo Management, License, Release
- [x] Updated across SKILL.md, README.md, TECHNICAL.md

### Release Gates: Product Docs + Release Notes Quality (2026-03-11)

- [x] Product docs gate: checks dev update, roadmap, readme-first before release
- [x] Release notes quality gate: blocks minor/major when notes come from bare --notes flag
- [x] Both gates run before version bump (early in pipeline, no damage if blocked)
- [x] Patches warn, minor/major block. --skip-product-check override.
- [x] MCP server updated with skipProductCheck parameter
- [x] Plan: `plans-prds/upcoming/2026-03-11--cc-mini--product-doc-enforcement.md`

### README Formatter (2026-03-11)

- [x] Build `wip-readme-format` CLI tool
- [x] Section-based staging files (README-init-badges.md, README-init-features.md, etc.)
- [x] Deploy mode assembles sections into README.md, backs up old files to ai/_trash/
- [x] Validation mode (`--check` validates existing README against the standard)
- [x] Toolbox mode: aggregates sub-tool interfaces, generates interface coverage table
- [x] SKILL.md `name:` frontmatter for human-readable names in the table
- [x] Fixed all 8 existing SKILL.md files with correct name fields

### Dev Guide Overhaul (2026-03-11)

- [x] Added release notes workflow to public Dev Guide (RELEASE-NOTES-v{version}.md on the branch)
- [x] Added release notes workflow to private Dev Guide
- [x] Cross-references between both guides ("you must read both")

### Repo Init Tool (2026-03-11)

- [x] `wip-repo-init` CLI scaffolds standard ai/ directory in any repo
- [x] Safe handling of existing ai/ folders (moves to `ai/_sort/ai_old/`)
- [x] Confirmation prompt, `--dry-run`, `--yes` flags
- [x] Generic, self-documenting template with READMEs in every folder

### Interface System Correction (2026-03-11)

- [x] Fixed interface coverage table (License Guard: CLI only, not Module+CC Hook)
- [x] Renamed "OpenClaw" column to "OC Plugin"
- [x] Added skill deployment to wip-install (`~/.openclaw/skills/<tool>/`)
- [x] Amalgamated interface system, README standard, installer vision into one reference note

### Release Notes Cleanup (2026-03-11)

- [x] `trashReleaseNotes()` moves consumed RELEASE-NOTES files to `_trash/` during release
- [x] `_trash/` excluded from public deploy

### EEXIST Fix (2026-03-11)

- [x] Universal Installer handles stale symlinks from renamed npm packages

### CLA + Licensing + Branch Cleanup (2026-03-10)

- [x] CLA.md contributor license agreement
- [x] Dual MIT+AGPL license clarification in README
- [x] Post-merge branch renaming and pruning integrated into wip-release
- [x] Plan: `archive-complete/2026-03-10--cc-mini--cla-licensing-branch-cleanup.md`

### Toolbox Consolidation (2026-03-09 - 2026-03-10)

- [x] Universal Installer with toolbox mode
- [x] All tools moved to `tools/` with package.json
- [x] MCP servers for release, license, permissions, repos
- [x] CC Hooks for file-guard and repo-permissions
- [x] OC Plugins for file-guard and repo-permissions
- [x] README rewrite to agent-first standard
- [x] SKILL.md as the comprehensive tool documentation
- [x] Dogfooded: `wip-install wipcomputer/wip-ai-devops-toolbox` works end-to-end

---

## Deprecated

_(nothing yet)_

---

## How to Update This File

- **Shipped a feature?** Move it from Upcoming to Done. Add the date. Check the boxes.
- **Dropped a plan?** Move it to Deprecated. Strikethrough, add the reason and date.
- **New idea that's ready to plan?** Add to Upcoming with a priority number. Renumber if needed.
- **Idea that's NOT ready to plan?** Put it in `../product-ideas/` instead. The roadmap is for committed work.
- **Priorities shifted?** Renumber the Upcoming section. The order matters.
- **Always update** "Last updated" and "Current version" at the top.
