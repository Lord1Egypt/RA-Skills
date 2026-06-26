---
name: release-preflight
description: Pre-release safety and scope checker for skills, repos, and export bundles. Use before publishing or sharing a skill folder, repository, or release bundle when you need to detect private artifacts, overscoped publish surfaces, local identity leakage, missing release basics, and export-safety risks before something becomes public.
---

# Release Preflight

Check whether a skill, repo, or export bundle is clean enough to publish.

## Core workflow
1. Identify the target path and target type (`skill`, `repo`, or `bundle`).
2. Check export-safety risks first: private directories, local-only artifacts, and unnecessary publish surface.
3. Check readiness basics for the chosen target type.
4. Scan text files for obvious local identity leakage.
5. Produce a decision: `ready`, `ready_after_fixes`, or `not_ready`.

## Read references as needed
- Read `references/rules.md` for the rule set and severity model.
- Read `references/report-format.md` for the report structure and decision meanings.
- Read `references/target-types.md` for type-specific expectations and minimal publish surfaces.
- Read `references/export-safety.md` for the default private-path and local-artifact patterns.
- Read `references/release-minimal.md` before packaging or publishing so the first public surface stays minimal.

## Use scripts as needed
- Use `scripts/release_preflight.py <target-path> [--type ...] [--publish-target ...]` to run the preflight check.

## Operating rules
- Prefer blocking obvious private artifacts over guessing intent.
- Prefer suggesting a smaller public surface instead of trying to auto-fix files.
- Treat identity leakage conservatively when absolute local paths or local usernames appear in public-facing text files.
- Keep the first version focused on text reports and P0 checks; do not expand into full secret scanning or automated publishing.
