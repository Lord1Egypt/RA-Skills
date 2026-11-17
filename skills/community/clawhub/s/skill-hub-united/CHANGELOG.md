# Changelog — skill-hub-united

All notable changes to this skill are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/); versioning follows [SemVer](https://semver.org/).

## v1.0.7 (2026-10-17)

- **Security hardening**: reject symlink/hardlink/device/FIFO tar members and
  symlink zip entries on **all** Python versions (write-outside-target defense).
  Extraction no longer relies on the availability of version-dependent extract
  filters.

## v1.0.6 (2026-06-22)

- Version-sync release: align the SKILL.md version with the latest published
  on clawhub (v1.0.4 / v1.0.5 were intermediate registry publishes; no
  functional changes).

## v1.0.5 (2026-06-22)

- Registry sync release (see v1.0.6).

## v1.0.4 (2026-06-22)

- Registry sync release (see v1.0.6).

## v1.0.3 (2026-06-22)

- **New source `skillhub_cn`**: install from [skillhub.cn](https://skillhub.cn)
  (SkillHub, a China-optimized public hub) via its public REST download API.
  No auth required. Endpoint contract verified end-to-end.

## v1.0.2 (2026-06-22)

- Docs: full self-hosted `custom` hub guide — server-side contract (exact
  request URL, accepted zip/tar response, 404/403/JSON-error semantics, archive
  layout), limitations (no auth headers; gate by network), and a minimal
  reference server example. No code changes.

## v1.0.1 (2026-06-21)

- Docs: correct the suite stages table (the comprehensive auditor is
  `skill-deep-audit`, and `skill-release-audit` was added as a third audit
  tool). No code changes.

## v1.0.0 (2026-06-21)

- Initial open-source release
- Four sources: clawhub (default), skills.sh, anthropic, and a configurable self-hosted `custom` hub
- Structured exit codes for conflict / license / multi-skill / missing-config handling
- Path-traversal-safe extraction and slug validation
