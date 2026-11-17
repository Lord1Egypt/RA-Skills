# Changelog

## [3.1.1] - 2026-02-28

### Added
- **README Sync step (10.5):** After all quality gates pass, orchestrator regenerates README from the actual shipped skill — commands from skill.yml, pipeline from SKILL.md, file layout from filesystem, Known Issues from Tester non-blocking report. Ensures README always reflects the real implementation, not the original design brief.
- README sync checklist: version match, trigger coverage, OPSEC clean, Known Issues section, quality scorecard present.
- README structure template for shipped skills (commands, pipeline, setup, config, data layout, known issues, scorecard, license).
- Version Control update: README sync commit added before push; push only happens after README sync is complete.

### Changed
- Orchestrator step 10 → 10.5 inserted between "add scorecard" and "push to GitHub"
- Step 11 (was "Track iteration") renumbered to 12; new step 11 is "Push to GitHub"
- Version Control section: added README sync commit, clarified push timing


### Added
- **Mandatory skill naming step** in Designer workflow (Step 2)
  - Present 3-5 name candidates to user before writing artifacts
  - Naming criteria table: action-clear, scope-obvious, trigger-friendly, kebab-case
  - Step-by-step name generation process with worked example
- Naming step callout in SKILL.md Designer quick reference

### Removed
- Redundant "Separation of Concerns Rule" section (already covered by ARCH-1 in reviewer rubric)

# Changelog

All notable changes to the skill-engineer skill will be documented in this file.

## [2.0.0] - 2026-02-16

### Fixed
- Removed OPSEC violations (GitHub usernames, organization references)
- Replaced sensitive identifiers with generic placeholders

### Added
- skill.yml with triggers and metadata
- Comprehensive test suite (tests/test-triggers.json)
- CHANGELOG.md for version tracking
- Progressive disclosure design based on Anthropic guide

### Features
- Full skill lifecycle management (design, test, review, maintain, audit)
- Pre-execution tool validation checklist
- Tool selection decision tree
- Self-play validation workflow
- Git submodule publishing workflow
- Skill interaction mapping
- Quality scoring system (structure + OPSEC)

## [1.0.0] - Initial Release

### Added
- Initial skill-engineer implementation
- SKILL.md with comprehensive workflow documentation
- Reference materials for skill design patterns
- Workspace configuration
