# v1.9.1: Release gates ... product docs and release notes quality enforcement

Agents read the Dev Guide, say "got it," and then release with garbage one-liner notes anyway. Documentation doesn't change behavior. Tools do. This release adds two new gates to `wip-release` that block bad releases before they happen.

## Product docs gate

Every PR is supposed to include updated product docs: a dev update, roadmap changes, and readme-first updates. This was documented in the Dev Guide as a manual checklist. Nobody followed it.

`wip-release` now checks three things before publishing:

1. **Dev update exists.** Looks in `ai/dev-updates/` for a file from the last 3 days. If you did work worth releasing, you should have written about it.
2. **Roadmap was updated.** Checks `ai/product/plans-prds/roadmap.md` via `git diff` against the last tag. If the roadmap doesn't reflect what just shipped, it's stale.
3. **Readme-first was updated.** Same check on `ai/product/readme-first-product.md`. The product bible should always describe what's actually built.

Repos without an `ai/` directory are skipped silently. This only applies to repos that have adopted the `ai/` folder standard.

For **patch** releases: warns but doesn't block. Hotfixes shouldn't be held up by docs.
For **minor/major** releases: blocks the release. You can't ship a meaningful feature with stale product docs.

`--skip-product-check` overrides for exceptional cases.

## Release notes quality gate

On 2026-03-11, the other CC session released memory-crystal v0.7.4. It read the Dev Guide (which now explicitly says "write a RELEASE-NOTES file on the branch"). It said it understood. Then it ran `wip-release patch --notes="MCP fix and agent ID config"` and published a one-liner to GitHub. The old `warnIfNotesAreThin()` function printed a warning to console. The agent ignored it.

The root cause was architectural, not behavioral. The warning ran at step 8 of the pipeline, AFTER the version was already bumped, committed, tagged, and pushed. By the time the warning appeared, the damage was done. And it was a warning, not a gate. Agents don't read warnings.

The fix:
- `checkReleaseNotes()` replaces `warnIfNotesAreThin()`. It runs before the version bump, not after.
- The CLI now tracks `notesSource`: where the notes came from (`file`, `dev-update`, `flag`, or `none`).
- For minor/major releases: if notes came from a bare `--notes` flag instead of a `RELEASE-NOTES-v{version}.md` file, the release is **blocked**. The agent gets explicit instructions: "Write RELEASE-NOTES-v{version}.md (dashes not dots), commit it, then release."
- For patch releases: warns if notes are short, but doesn't block.

## Both gates follow the same pattern

The existing license compliance gate (step 0) checks `.license-guard.json` and blocks if licensing is wrong. The new product docs gate (step 0.5) and release notes gate (step 0.75) work the same way: check early, block before any changes, show status in `--dry-run`, give clear instructions on how to fix it.

The MCP server was also updated with `skipProductCheck` and `notesSource` passthrough so agents calling wip-release via MCP get the same enforcement.
