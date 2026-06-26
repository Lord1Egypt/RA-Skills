# Changelog - Remember When Skill

## [2.0.0] - 2026-04-12
### Added
- Cross Collections section: `create-cross`, `add-to-cross`, `list-cross`, `show-cross` commands and interview protocol.
- Group Rules section: `set-rule`, `list-rules` commands and rule evaluation protocol.
- Contextual Enrichment section: `set-daily-context` and `enrich-entry` commands with deduplication protocol.
- Enrichment Decision Guide: topic-based recommendations for what contextual info to search.
- Enrichment Configuration documentation in `rules.json`.

## [1.2.0] - 2026-04-11
### Added
- Proactive Archiving mode: agent detects and offers archival of valuable content autonomously.
- Archiving Context Buffer: uses last active group as default context.
- Pre-flight Check (Interview Workflow): verifies group context before archiving.
- Post-action Validation: presents summary and asks for optional metadata after every `add`.
- `interest_point` entry type for places, locations, and geographic points of interest.
- Validation Questions API: explicit permission for confirmation questions before bulk or major operations.
- Agent Configuration Requirements section: instructions for internal `AGENTS.md`, `TOOLS.md`, and `HEARTBEAT.md`.
- Multimedia Capture Workflow: explicit save → `add --file` → confirm pipeline.

## [1.1.4] - 2026-04-10
### Added
- Standardized YAML metadata for Clawhub.
- Enhanced English instructions for the agent.
- Protocol for autonomous group auditing.
- Support for `openclaw install` command.

## [1.0.0] - 2026-04-10
- Initial release.
