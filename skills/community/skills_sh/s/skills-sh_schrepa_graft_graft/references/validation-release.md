# Validation and Release Hygiene

Use this reference when the task is docs cleanup, release readiness, contributor experience, or validating that a Graft change matches the current package behavior.

## What to inspect first

- Public exports and top-level docs
- CLI command sources and help text
- Scaffold templates if the project ships generators
- Tests that define transport, auth, and example behavior

## Validation loop

If shell or repo tools are available:

1. Run the narrowest relevant validation first.
2. For package changes, use the package-local checks such as:
- `pnpm --filter graft test`
- `pnpm --filter graft typecheck`
- `pnpm --filter graft lint`
3. For example or transport docs, compare against tests before finalizing the wording.
4. For app or proxy docs, use `graft check` and `graft studio` when that materially validates the documented workflow.

If tools are not available:

- State the exact files or tests that should be checked before publishing.
- Call out any assumption that could invalidate the docs or skill content.

## Drift prevention

- Add lightweight docs contract tests for claims that are easy to regress:
  - public API example shapes
  - auth forms
  - transport method claims
  - required skill packaging artifacts
- Prefer string or contract assertions over large snapshots.

## Release checklist

- README examples compile conceptually against the current public API.
- Skill instructions match the current package behavior and CLI.
- No unsupported registry or publishing metadata is documented unless the repo actually contains it.
- Examples and guidance reflect the current scaffold or recommended project structure.
