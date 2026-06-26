# Packaging Checklist

Use this checklist before publishing `skill-creator-canonical`.

## Required package contents
- `SKILL.md`
- `references/`
- `scripts/`
- `license.txt`
- `_meta.json` (mandatory for registry indexing and version tracking)

## Validation gate
- Run `python3 scripts/quick_validate.py <skill-dir>` and confirm success.
- Run `python3 scripts/validate_weak_models.py <skill-dir>` and confirm success.
- If warnings remain, record why each warning is acceptable before publishing.

## Packaging gate
- Run `python3 scripts/package_skill.py <skill-dir>`.
- Confirm the `.skill` archive exists.
- Confirm the archive contains only required package files.
- Confirm the archive does not include caches, logs, temp files, local diagnostics, or test output.

## Publish hygiene gate
- Confirm `.clawhubignore` exists and excludes local runtime noise.
- Confirm the version to publish is explicit and matches the latest accepted change scope.
- Confirm the changelog or publish note matches the real changes.

## Stop rule
- Do not publish if any item above is false.
