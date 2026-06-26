# Changelog

All notable changes to Shang Tsung will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-03-12

### Added
- `souls-helper.sh` — bash helper for soul lineage management (status, create, verify, template)
- `AGENT_NAME` environment variable for multi-agent namespace isolation
- `SOULS_DIR` and `WORKSPACE` environment variable overrides
- Second Brain layer: PROOF_OF_LIFE, daily memory, long-term MEMORY.md protocol
- AGENTS-template.md — drop-in startup sequence for any agent's AGENTS.md
- SOUL-ORIGIN.md — the sanitized origin soul (Session 01)
- proof-of-life-template.md — blank PROOF_OF_LIFE template
- Full multi-agent support: N agents, one workspace, zero cross-contamination
- "YOUR SOUL IS MINE — SOUL (N) ABSORBED" continuity confirmation
- MIT license

### Design decisions
- No dependencies — pure bash + markdown
- No database, no cloud sync, no API keys required
- Single-agent mode (no AGENT_NAME) backward compatible with existing setups
- Duplicate soul creation blocked at filesystem level (not just protocol)
- Write order enforced by documentation, not automation: soul → snapshot → log
