# Changelog

All notable changes to SPM will be documented in this file.

## [3.0.0] — 2026-05-13

### Added
- **WBS Hash Attestation**: SHA-256 integrity protection (`scripts/attest-wbs.sh`, `scripts/verify-wbs.sh`)
- **Hook Auto-Injection**: Active tasks auto-injected into context via `scripts/inject-wbs-context.py`
- **Session Recovery**: Auto-generated recovery reports from `scripts/session-recovery.py`
- **Parallel Task Pointers**: `.active_ledger` symlink + `scripts/switch-ledger.sh` for multi-task isolation
- **SPM Minimal Mode**: 5-rule lightweight mode for <10 task projects (`docs/spm-minimal-mode.md`)
- **Template/Script Physical Separation**: Clear `templates/` → project copy mapping
- **UPGRADE.md**: Version migration guide
- **COMMUNITY.md**: Community showcase and extension registry
- **---BEGIN/END WBS DATA---**: Standardized delimiters for safe context injection

### Changed
- SKILL.md: Updated to v3.0.0 with new features documentation
- Task Ledger Template: Added hash attestation notice and Resume Point column
- README: Added v3.0 features to core capabilities list

### Security
- WBS Ledger now protected by hash attestation
- Tampered ledgers auto-detected with clear warnings
- Injection blocked when hash mismatch detected

## [2.0.0] — 2026-05-09

### Added
- **Cold-Start Context Briefs**: Every WBS task now includes self-contained context for cold-start agent execution
- **Adversarial Plan Review**: Phase 2 dispatches a reviewer subagent against a 5-dimension checklist before showing plan to user
- **Plan Mutation Protocol**: Formalized split/insert/skip/reorder/abandon operations with audit trail (`references/plan-mutation.md`)
- **Model Tier Routing**: Three-tier model routing (fast/standard/strong) across different providers to avoid rate-limit contention
- **Eval Delta**: Baseline vs current test comparison required before marking tasks `done`
- **Standardized Verification Report**: 7-phase YES/NO grid replacing narrative verification (`templates/verification-report.md`)
- **External Research Workflow**: Phase 1 optional sub-flow for analyzing external codebases/skills (`workflows/external-research.md`)
- **Non-Code Project Support**: `project_type` config (code|docs|config) with format validation replacing TDD for non-code projects
- **QUICKSTART.md**: 5-minute onboarding guide
- **Complete Example Project**: `examples/jwt-auth/` with filled spec, WBS ledger, plan review, and verification report
- **CI Workflow**: `.github/workflows/ci.yml` (shell/python syntax + schema validation + runtime checkpoint test)
- **Plan Reviewer Subagent**: `subagents/plan-reviewer-prompt.md`
- **LICENSE**: MIT
- **manifest.json**: Skill metadata

### Changed
- **SKILL.md**: Complete rewrite with mode architecture, template index, reading guide, model routing
- **Config system**: Rewrote `config/default.yaml` + `src/config/` from StockPulse-specific to SPM project management
- **All subagent prompts**: Strengthened with concrete checklists, anti-patterns, and output formats
- **WBS ledger**: Added Context Brief column, Mutation Log section, aligned `Dependencies` naming across all files
- **Workflows**: Unified to 14 workflows, writing-plans adds adversarial review step, subagent-driven-development adds cold-start + model routing
- **README**: Updated project structure, workflow count, `Dependencies` alignment
- **`.gitignore`**: Expanded

### Fixed
- `checkpoint.sh`: Template path mapping bug, sed delimiter conflict (values containing `/`), task count off-by-one, dead code removal, hard stop enforcement added
- `validate_contract.sh`: Directory `-nt` unreliability, missing client file check
- `verify_checklists.py`: `package.json` absence guard
- `quality-check.sh`: Fragile pipe with `set -e`
- `setup-checkpoints.sh`: Duplicate npm script blocks merged
- OpenAPI spec: `/projects` path duplication fixed
- SKILL.md: `sessions_yield` added to allowed-tools
- All files: StockPulse artifacts removed (financial config, candle data, collector references)
- Naming: `Depends` → `Dependencies` unified across all files

## [1.0.0] — 2026-05-04

### Added
- Initial release: 5-phase lifecycle, 13 workflows, WBS ledger, 3-tier quality gates
- Subagent dispatch with WBS binding
- Git worktree isolation
- Heartbeat-based interruption recovery
- Checkpoint templates (Phase 1/2/3/5)
- Code completion + deployment readiness checklists
- OpenAPI project management API contract
