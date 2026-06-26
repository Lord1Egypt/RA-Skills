# Skill Template Generator

Generates platform-specific skill folders from a single template source of truth.

## Quick start

    python skill_template/generate.py

## How it works

The core template (`weekend-scout.template.md`) uses two mechanisms:

### Conditional blocks: `#@IF` / `#@ENDIF`

Lines between `#@IF platform-id` and `#@ENDIF` are included only for
the named platform. Use commas for OR: `#@IF claude-code,codex`.
Use `!` for NOT: `#@IF !openclaw`.

The `#@IF` and `#@ENDIF` lines themselves are consumed (never appear in output).
Nested `#@IF` is not supported.

### Variable substitution: `%%VAR_NAME%%`

Variables defined in `platforms.yaml` (per-platform or shared) are
substituted using double-percent delimiters. This avoids collision
with the skill's own `{placeholder}` syntax.

If a `%%VAR%%` has no matching key, the generator raises an error (no silent pass-through).

## Adding a new platform

1. Add a platform entry to `platforms.yaml` with `output_dir` and `vars`
2. Add `#@IF new-platform` blocks to the template where behavior differs
3. Run `python skill_template/generate.py`

## CLI options

    python skill_template/generate.py                    # generate all platforms
    python skill_template/generate.py --platform NAME    # one platform only
    python skill_template/generate.py --dry-run          # print, don't write
    python skill_template/generate.py --check            # verify files are up to date (CI)

`--check` exits with code 1 if any file is missing or differs from the template output.

## Files

- `platforms.yaml` — platform definitions and variables
- `weekend-scout.template.md` — the core orchestrator template
- `resources/common/` — bundled references/scripts copied to every generated skill
- `resources/<platform>/` — platform-specific bundled references/scripts
- `generate.py` — the generator script
- `README.md` — this file
