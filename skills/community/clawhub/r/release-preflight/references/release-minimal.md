# release minimal

Use this as the safe minimal publish surface for the first public release.

## Keep
- `SKILL.md`
- `references/rules.md`
- `references/report-format.md`
- `references/target-types.md`
- `references/export-safety.md`
- `scripts/release_preflight.py`

## Optional
- keep only if the publish target or repo workflow truly needs them:
  - `README.md`
  - `CHANGELOG.md`

## Exclude
- workspace-private logs
- `memory/`
- `logs/audit/`
- `<openclaw-local-dir>/`
- `.venv*`
- `tmp/`
- unrelated test outputs

## Rule
Prefer publishing from the skill directory itself. Keep the first public surface minimal and let later versions expand only when real usage justifies it.
