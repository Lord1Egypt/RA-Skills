# Changelog

All notable changes to this project will be documented in this file.

Format: [Semantic Versioning](https://semver.org)

---

## [1.0.1] — 2026-03-25

### Security
- **REPO-03 fix**: `TRAUMAS.md` injection now requires explicit trigger phrases
  (`"my trauma"`, `"telos trauma"`, `"traumas"`) instead of any message containing
  the word "trauma". Prevents accidental injection of sensitive personal data in
  group chats or unrelated conversations.
  - Identified by: SlowMist Agent Security Review
  - Affected file: `hooks/telos-context.js`

---

## [1.0.0] — 2026-03-24

### Added
- Initial release of TELOS skill for OpenClaw
- 20 template files covering all life dimensions (MISSION, GOALS, BELIEFS, etc.)
- `scripts/init-telos.ts` — Initialize telos directory from templates
- `scripts/update-telos.ts` — Safe update with automatic backup and changelog
- `scripts/backup-telos.ts` — Full snapshot backup and restore system
- `hooks/telos-context.js` — OpenClaw hook for automatic context injection
  - `agent:bootstrap` — Loads MISSION + GOALS + BELIEFS at session start
  - `message:preprocessed` — Injects relevant files based on topic keywords
- `references/onboarding.md` — Guided setup workflow
- `references/update-workflow.md` — Update format rules
- `evals/evals.json` — Skill evaluation test cases
- Updated `SKILL.md` with File Index table, backup triggers, hook integration docs

### Architecture
- Zero external npm dependencies (pure Node.js built-ins + bun stdlib)
- Append-only file updates — no destructive overwrites
- `.gitignore` excludes all personal telos data from version control
- Paths hardcoded to `~/clawd/telos/` — no path traversal attack surface

## [1.0.2] — 2026-03-26

### Changed
- **SKILL.md**: Add `requires` field in frontmatter declaring `bun` and `node` as
  runtime dependencies (used by scripts and hook respectively)
- **SKILL.md**: Clarify Context Loading section — explicitly distinguish between
  "with hook" (auto-inject at bootstrap) vs "without hook" (on-demand only)
- **SKILL.md**: Add opt-in warning before hook install instructions — users must
  explicitly consent to persistent automatic context injection behavior

These changes address ClawHub security scan findings:
- Missing runtime requirement declarations
- Inconsistency between "on-demand" description and hook's bootstrap auto-injection
- Missing disclosure of persistent/privilege behavior for hook installation

## [1.0.3] — 2026-03-26

### Changed
- **scripts & hook**: Replace hardcoded `~/clawd/telos` path with `$OPENCLAW_WORKSPACE/telos`
  — respects OpenClaw runtime environment variable for cross-user compatibility.
  Falls back to `~/openclaw/telos` (standard install) then `~/clawd/telos` (legacy).
- **SKILL.md**: Update Data Location to reference `$OPENCLAW_WORKSPACE/telos/`
- **`.gitignore`**: Add `*.skill` to exclude build artifacts from version control
- **Git**: Remove `telos.skill` binary from repository tracking
