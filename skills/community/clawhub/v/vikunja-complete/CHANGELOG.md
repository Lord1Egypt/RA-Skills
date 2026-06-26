# Changelog

All notable changes to the Vikunja skill-dev project are documented here.

## [0.4.0] - 2026-03-11

### Added
- V0.4 command groups in `skills/vikunja/scripts/vikunja.sh`:
  - attachments (`list|upload|download|delete`)
  - relations (`add|remove`)
  - filters (`list|create|get|update|delete`)
  - notifications (`list|mark`)
  - subscriptions (`subscribe|unsubscribe`)
  - tokens (`list|create|delete`)
- Help/usage coverage and SKILL examples for all new command groups.

### Changed
- Bumped CLI and project version to `0.4.0`.
- Updated roadmap and smoke-test run notes for V0.4 verification.

## [0.3.0] - 2026-03-11

### Added
- V2 command groups in `skills/vikunja/scripts/vikunja.sh`:
  - comments (`list|add|update|delete`)
  - labels (`list|create|add|remove`)
  - assignees (`list|add|remove`)
  - views (`list|create`)
  - buckets (`list|create`)
  - webhooks (`list|create|delete`)
  - bulk-update (`--ids ...`)
- Reminder support via `update --reminder DATE`
- Repeatable smoke harness coverage for V2

### Changed
- Improved deterministic routing with exact-name resolution for project/view/bucket.
- Added quickstart/onboarding examples in `skills/vikunja/SKILL.md`.
- Added release-readiness and API coverage docs.

### Fixed
- Due date normalization (`YYYY-MM-DD` -> RFC3339) for create/update.
- Safe merge-update flow to prevent field wipe on task POST updates.
- Help/version now work without env vars.
- Corrected endpoint coverage mapping to strict matching.

## [0.2.0] - 2026-03-11

### Added
- Retry/backoff controls:
  - `VIKUNJA_API_RETRIES`
  - `VIKUNJA_API_RETRY_DELAY`
- Error classification and deterministic exit codes.
- `skills/vikunja/scripts/test-smoke.sh` harness.

## [0.1.0] - 2026-03-11

### Added
- Core command set:
  - `health`
  - `list`
  - `create`
  - `complete`
  - `move`
  - `update`
- Initial skill docs and project scaffolding.
