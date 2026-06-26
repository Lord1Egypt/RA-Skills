# rules

## P0 checks

### 1. Private artifacts
Treat these as private or local-only by default:
- `memory/`
- `logs/audit/`
- `<openclaw-local-dir>/`
- `.venv/`, `.venv-*`
- `tmp/`
- `.DS_Store`

If these appear inside the intended publish surface, mark them as at least a warning. Escalate to blocking when the target type is `skill` or `bundle` and the path is clearly inside the shared payload.

### 2. Overscoped publish surface
Warn when the target includes files or directories that do not match the likely public surface.

For `skill`, the minimal surface is usually:
- `SKILL.md`
- `references/`
- `scripts/`
- optional `README.md`
- optional `CHANGELOG.md`

### 3. Identity leakage
Scan text-like files for:
- absolute user-home paths such as `<user-home>/...`
- obvious local host or machine references
- user-specific local paths that should not appear in public-facing examples

### 4. Readiness basics
For `skill`, require `SKILL.md`. Warn when neither `references/` nor `scripts/` exists.
For `repo`, warn when there is no obvious entry file such as `README.md`, `main` code, or a clearly named root file.
For `bundle`, warn when the bundle has no obvious explanation file or structure.

## Decision model
- `not_ready`: blocking issues exist.
- `ready_after_fixes`: no blocking issues, but warnings exist.
- `ready`: no blocking issues and no warnings worth stopping on.
