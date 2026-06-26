# Changelog

All notable changes to Sara will be documented in this file.

## [0.1.0] - 2026-04-11
### Added
- **Initial Preview Release**: SARA logic guard for OpenClaw.
- **Four Core Safety Rules**: 
  - `backup` -> `delete` (Prevent data loss)
  - `check` -> `operate` (Reduce failed retries)
  - `permission` -> `read` (Privacy guard)
  - `preview` -> `publish` (Social safety)
- **Alias System**: Support for 50+ common tool verbs across Git, DB, and social media skills.
- **Deterministic Auditor**: Zero-token local Python script for sequence validation.
- **OpenClaw Integration**: Native `SKILL.md` instruction set.

### Fixed
- Improved path discovery for robust installation in various folder structures.
