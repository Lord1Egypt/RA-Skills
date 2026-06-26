# v1.9.1: Release gates (product docs + release notes quality)

**Date:** 2026-03-11
**Author:** cc-mini
**Branch:** cc-mini/release-gates

## What changed

### Product docs gate in wip-release
- `checkProductDocs()` and `fileModifiedSinceLastTag()` added to core.mjs
- Checks: dev update exists (last 3 days), roadmap modified since last tag, readme-first modified since last tag
- Repos without `ai/` directory are skipped silently
- Patches: warn. Minor/major: block.
- `--skip-product-check` flag to override

### Release notes quality gate in wip-release
- `checkReleaseNotes()` replaces the old `warnIfNotesAreThin()` warning
- Tracks `notesSource` (file, dev-update, flag, none) through CLI to core
- Minor/major releases with bare `--notes` flag are BLOCKED
- Agent gets explicit instructions: write RELEASE-NOTES-v{version}.md, commit, release
- Gate runs BEFORE version bump (old warning ran at step 8, after damage was done)
- MCP server updated with `skipProductCheck` parameter and `notesSource` passthrough

### Incident that triggered this
memory-crystal v0.7.4 released with garbage one-liner notes. Other CC session read the Dev Guide, said "got it," and still used `--notes="short string"`. Documentation doesn't change behavior. Tools do.

## Files modified
- `tools/wip-release/core.mjs` (+99 lines: two new functions, two gate integrations, dry-run output)
- `tools/wip-release/cli.js` (+6 lines: notesSource tracking, --skip-product-check flag)
- `tools/wip-release/mcp-server.mjs` (+2 lines: skipProductCheck, notesSource)
- `tools/wip-release/SKILL.md` (product docs gate documentation)
- `tools/wip-release/README.md` (one-liner about the feature)
- `ai/product/plans-prds/upcoming/2026-03-11--cc-mini--product-doc-enforcement.md` (plan)
