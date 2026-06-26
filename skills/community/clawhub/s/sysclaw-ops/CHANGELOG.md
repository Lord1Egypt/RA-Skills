# Changelog

## v1.6.1 — 2026-03-17

### Fixed
- **db-schema.md:** Replaced all "virus" / "Virus" references with "human operator" (consistent with v1.2.0 rename)
  - `issues.resolved_by` column note
  - `agent_requests.resolved_by` column note
  - `agent_requests.escalated` column note
  - Status flow diagram
- **SKILL.md:** Removed orphaned duplicate line in escalation section
- **SKILL.md:** Added note that SQL examples are illustrative patterns, not for copy-paste

### Added
- CHANGELOG.md

## v1.6.0 — 2026-03-17

Simplified execution model. SysClaw executes all approved requests — agents only ask because they can't do it themselves.

## v1.5.0 — 2026-03-17

Added worklog table for tracking executed actions. Added hybrid execution model.

## v1.4.0 — 2026-03-17

Added SysClaw escalation handling section documenting heartbeat-based escalation checks.

## v1.3.0 — 2026-03-17

Clarified Telegram escalation is manual (SysClaw handles it, not cron job).

## v1.2.0 — 2026-03-17

Replaced operator name with generic 'human operator' for portability.

## v1.1.0 — 2026-03-17

Added declared credentials with minimal privileges, clarified OpenClaw cron job (not system crontab).

## v1.0.0 — 2026-03-17

Server-side operations for cross-agent communication. Processing workflow, decision guidelines, escalation handling.
