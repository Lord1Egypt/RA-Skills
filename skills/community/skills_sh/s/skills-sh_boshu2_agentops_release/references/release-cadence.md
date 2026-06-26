# Release Timing Guidance

AgentOps does not enforce a minimum wait between releases. Ship when the repo
state, release notes, and validation results are good enough for the version
you want to cut.

## Guidance

- Keep `[Unreleased]` current in `CHANGELOG.md` so release prep stays
  mechanical.
- Prefer coherent release notes over arbitrary schedules.
- Draft releases do not notify watchers and can be used freely for CI testing.

## Curated Release Notes

Every published release should have curated notes at
`docs/releases/YYYY-MM-DD-v<version>-notes.md`. The CI pipeline
(`scripts/extract-release-notes.sh`) uses these as the GitHub Release page
highlights, with the full CHANGELOG in a collapsible `<details>` block.

See `references/release-notes.md` for the notes format and quality bar.
