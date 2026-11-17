# Changelog

## [1.1.5] - 2026-08-03
### Fixed
- Parse both current `/owner/skills/slug` and legacy `/owner/slug` ClawHub URLs.
- Record bounded-scan omissions and fetch failures in the audit report.
- Return `UNKNOWN` with exit code 2 whenever the scan is incomplete.
- Avoid presenting clean-pattern assurances when files were not fully inspected.
- Add regression tests for URL parsing and file-limit handling.

## [1.1.4] - 2026-08-03
### Changed
- Added OpenClaw registry verification as the first trust signal.
- Removed the unnecessary `clawhub` binary requirement and global pip installation.
- Clarified that regex and LLM scores are heuristic evidence, not installation authorization.

## [1.1.3] - 2026-03-03
### Fixed
- Misleading binary requirements: marked `python3` as mandatory (`bins`) and `clawhub` as optional (`anyBins`).

## [1.1.2] - 2026-03-03
### Added
- Simplified installation instructions (Ask OpenClaw / CLI) to SKILL.md and README.md.

## [1.1.1] - 2026-02-23
### Fixed
- Re-submit for VirusTotal scan clearance.

## [1.1.0] - 2026-02-23
### Fixed
- Fixed prompt injection vulnerability in LLM-as-judge.

## [1.0.0] - 2026-02-23
### Initial Release
- Audit any ClawHub skill for security risks.
