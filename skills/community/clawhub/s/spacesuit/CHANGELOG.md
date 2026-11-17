# Changelog

## [0.4.0] - Pending publication

- Add local-export Linear/Jira portfolio and operations work-graph compilation.
- Parse documented workspace flags and preserve unmarked instructions unless
  explicitly adopting them; validate markers and back up modifying upgrades.
- Preserve existing install version state; support text-only package version
  discovery and create workspace runtime directories.
- Separate release preflight/artifact staging from tagging and publication.

- Add explicit, opt-in business-operations flavor with Intel, Pipeline and Monetization snapshots, preview/apply/disable/restore and bounded local collection.
- Document Command Center as standalone and Spacesuit as its highly recommended companion, without a standalone interaction UX.

## [0.3.0] - 2026-02-04
### Added
- CONTRIBUTING.md — comprehensive contribution guide
- CODE_OF_CONDUCT.md — Contributor Covenant-based code of conduct
- `--profile` flag for multi-OpenClaw support in sync-operators.sh
- `--dev` shortcut for development profile
- `-h/--help` flag for sync-operators.sh

### Changed
- sync-operators.sh respects `OPENCLAW_PROFILE` env var
- Generated JSON includes profile metadata when set

## [0.2.0] - 2026-02-04
### Added
- `sync-operators.sh` — auto-generate operators.json from session transcripts
  - Scans OpenClaw session files for Slack users
  - Preserves manually-set roles across syncs
  - Tracks message count per operator
- Install script now copies utility scripts to workspace `scripts/`

### Changed
- Package structure documented with data layer scripts section

## [0.1.0] - 2026-02-03
### Added
- Initial extraction from openclaw-workspace
- Base files: AGENTS.md, SOUL.md, TOOLS.md, HEARTBEAT.md, SECURITY.md, MEMORY.md
- Templates for all workspace files
- Install/upgrade/diff scripts with section-based merging
- Meta-learning framework (expert-first methodology)
- Full git workflow with worktree conventions
- Parallel multi-agent workflow with merge locks
- P0-P5 priority system
- Memory commit discipline
- Security baseline with data classification
- Cross-platform handoff protocol
- Heartbeat framework with proactive checks
