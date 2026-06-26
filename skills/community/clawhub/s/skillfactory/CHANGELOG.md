# Changelog — skill-factory

All notable changes to skill-factory will be documented in this file.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

---

## [Unreleased]

No unreleased changes yet.

---

## [2.4.0] — 2026-05-13

### Summary

**End-to-end ClawHub CLI publishing workflow.** Phase 3 now includes a full, battle-tested SOP for publishing skill updates to ClawHub via CLI — covering login, publish, verify, and local sync. Lessons from earlier failures (proxy issues, requirement creep, device flow) are captured.

### Added
- Phase 3 → ClawHub CLI Publishing: device flow login, publish command, verify, local sync steps
- Phase 3 → Windows proxy notes: HTTPS vs SSH guidance
- Lessons Learned table: LRN-005 (ClawHub device flow background), LRN-006 (SSH/proxy), LRN-007 (requirement creep)

### Changed
- SKILL.md version bumped from v2.3.0 to v2.4.0
- README.md / README_zh.md version badges updated to v2.4.0

### Fixed
- CLAWHUB.md version updated from v2.1.0 to v2.3.0 (was out of sync)
- SKILL.md Workspace Layout: corrected `D:/WorkBuddy/` → `D:/Agent/WorkBuddy/skills/` for skill repo paths
- SKILL.md Legacy section: `D:/WorkBuddy/<skill-name>/` → `D:/Agent/WorkBuddy/skills/<skill-name>/`
- README_zh.md: OpenAI URL changed from Chinese-localized to canonical English URL
- README.md / README_zh.md: manual install path from `~/.claw/skills/` → `~/.workbuddy/skills/`
- .workspace-index.md: directory structure comment updated from v2.2.0 to v2.3.0

## [2.3.0] — 2026-05-12

### Summary

**First-class upgrade workflow for existing skills.** Skill Factory now explicitly supports 1→N maintenance alongside 0→1 creation.

### Added
- `Upgrade skill:` as a first-class entry point alongside `New skill:`
- Upgrade Workflow section in SKILL.md: Inspect → Classify → Propose → Apply → Summary
- Version bump decision framework: skill's "public API" defined (use cases, input/output, workflow phases, safety boundaries, file structure)
- Upgrade plan template: current version, proposed version, change type, files to modify, risk level, changelog entry, commit message, tag
- Enhanced trigger words covering upgrade and maintenance scenarios

### Changed
- SKILL.md: `[Unreleased]` section added to CHANGELOG guidance per Keep a Changelog standard
- CHANGELOG discipline: now requires grouped changes (Added / Changed / Fixed / Deprecated / Removed / Security) and user-readable summaries
- README.md: added "Maintaining Existing Skills (1→N)" section
- README_zh.md: updated quick start with skill upgrade example
- Legacy "Skill Iteration" section renamed to "Skill Iteration (Legacy)" with redirect to Upgrade Workflow

### Fixed
- Workspace layout path in SKILL.md now consistent with actual directory structure

---

## [2.2.2] — 2026-04-27

### Summary

**Version sync: local repo aligned with ClawHub v2.2.2 release.**

### Changed
- `SKILL.md`: version field updated to `2.2.2`
- `README.md` / `README_zh.md`: version badges updated to `2.2.2`

### Notes
- ClawHub listing had advanced to v2.2.2; this commit brings the GitHub repo in sync
- Submitted false-positive appeal to openclaw/clawhub for suspicious flag on this skill

---

## [2.2.1] — 2026-04-21

### Summary

**ClawHub distribution ready + clean publish structure.**

### Added
- `README.md`: ClawHub installation instructions (`claw skill install skillfactory`)
- `README_zh.md`: 中文安装说明
- `README.md` & `README_zh.md`: Tags section for discoverability
- `CLAWHUB.md`: Dedicated ClawHub listing page with one-line pitch
- `PUBLISH.md`: Release command reference for future updates

### Changed
- Slug finalized: `skillfactory` (GitHub: PandaBro666/skillfactory)
- `.gitignore` updated: excludes `inbox/`, `wip/`, `promo/` from public repo

### Notes
- Minimum ClawHub requirement: `SKILL.md` only
- Recommended: `SKILL.md` + `README.md` + `LICENSE` for professional presentation
- Clean publish workflow: copy core files to separate directory to avoid uploading WIP content

---

## [2.2.0] — 2026-04-20

### Summary

**Bilingual README split + clean publish structure.**

### Added
- `README_zh.md` — dedicated Chinese README with bilingual badge linking between versions
- `.gitignore` — excludes `inbox/` and `wip/` from public repo (personal work area)

### Changed
- `README.md` (English): completely purged of Chinese text; "Skills Built With This Factory" section replaced with a concrete end-to-end example using the `harness` skill
- `README.md` now includes badge linking to `README_zh.md`
- `README_zh.md` likewise links back to English version via badge

### Fixed
- SKILL.md Phase 3 bilingual spec updated: README is now two separate files, not two sections in one

---

## [2.1.0] — 2026-04-20

### Summary

**GitHub release ready.** Full bilingual README, version management SOP, and LICENSE added.

### Added
- `LICENSE` (MIT) — required for ClawHub distribution
- Semantic versioning guide in `SKILL.md`: MAJOR / MINOR / PATCH semantics with decision criteria
- Commit message convention (`feat:` / `fix:` / `refactor:` / `release:`)
- Changelog discipline rules (every release must update CHANGELOG)

### Changed
- `README.md` rewritten as bilingual (EN + ZH), "industrial revolution" analogy as lead hook
- `SKILL.md` v2.1: extended version management section, bilingual README spec in Phase 3
- Trigger words expanded: added `skill版本管理`, `skill如何发行`, `skill生产`, `skill自动化`

---

## [2.0.0] — 2026-04-20

### Summary

**From SOP document to meta-skill.**

Skill Factory is now itself a publishable WorkBuddy skill. v2.0 restructures the project so it can be distributed via GitHub/ClawHub and loaded by any Claw instance, just like any other skill.

### Changed
- `SKILL.md` completely rewritten as a proper skill entry point with YAML frontmatter, trigger words, and self-contained SOP
- Added Phase 3 publishing specs: README format, ClawHub distribution checklist, version semantics
- Added skill iteration workflow (1→N upgrades)
- `README.md` rewritten as human-facing project page with selling points

### Added
- `CHANGELOG.md` (this file)
- ClawHub distribution spec in Phase 3
- Skill upgrade triggers and process
- Workspace layout reference

---

## [1.0.0] — 2026-04-18

### Summary

**Initial creation.**

Built during the harness skill development cycle as a response to 4 accumulated learnings (LRN-001 through LRN-004). Established the four-phase SOP and workspace directory structure.

### Added
- `SKILL-SOP.md` — four-phase workflow (Phase 0-3)
- `inbox/` directory — idea drop zone
- `wip/` directory — active skill workspace
- `D:/WorkBuddy/.workspace-index.md` — master skill status board
- 4 lessons from harness creation embedded into SOP
