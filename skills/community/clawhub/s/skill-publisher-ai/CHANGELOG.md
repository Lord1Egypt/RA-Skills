# Changelog

All notable changes to this project will be documented in this file.

## [4.0.0] - 2026-06-11

### Breaking Changes
- **workflow**: Added Workflow B (iteration update) alongside Workflow A (new publish), changing the skill from single-workflow to dual-workflow

### Added
- **workflow-b**: Change detection with file category mapping and version bump decision tree
- **workflow-b**: Auto CHANGELOG generation from git log with Conventional Commits parsing
- **workflow-b**: Version bump with three-file sync (SKILL.md → plugin.json → CHANGELOG.md)
- **workflow-b**: Release update flow for PATCH versions on same day
- **publish**: gh CLI integration as Method B in push fallback chain (git push → gh CLI → REST API)
- **readme**: Product landing page 21-chapter standard with smart adaptation by Skill complexity
- **readme**: Bilingual independent files strategy (README.md + README.en.md)
- **readme**: Golden quote opening, negation contrast, navigation links, limitations section
- **community**: config.yml for Discussions redirect in .github/ISSUE_TEMPLATE/
- **skill**: Provenance block (quote + HTML comment) for source identification
- **skill**: Version sync rule — SKILL.md → plugin.json → CHANGELOG.md consistency check
- **skill**: Smart README adaptation — simple Skills (≤5 rules) get required chapters only
- **skill**: SKILL.md content extraction before README generation
- **references**: change-detection.md — file category mapping, bump decision tree, Conventional Commits guide
- **references**: changelog-generation.md — git log extraction, commit parsing, CHANGELOG-to-Release-Notes conversion

### Changed
- **rules**: Expanded from 12 to 15 rules (added rules 13-15 for Workflow B)
- **steps**: Expanded from 13 to 25 steps (Workflow A: 1-13, Workflow B: 14-25)
- **publish**: Push fallback chain changed from 2-level (git push → REST API) to 3-level (git push → gh CLI → REST API)
