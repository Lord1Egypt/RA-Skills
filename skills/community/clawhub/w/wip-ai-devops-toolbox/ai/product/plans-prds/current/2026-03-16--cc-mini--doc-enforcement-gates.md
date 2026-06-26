# Plan: Doc Enforcement Gates (#117 + #128)

**Date:** 2026-03-16
**Author:** cc-mini
**Status:** In Progress

## Goal

Two new wip-release gates that enforce documentation stays in sync with code.

## Gate 1: Technical Docs (#117)

When source code (*.mjs, *.js, *.ts) changes since last release tag, require that SKILL.md or TECHNICAL.md was also modified. Prevents shipping code without updating docs.

- [x] `checkTechnicalDocs()` function in core.mjs
- [x] Integrated into real + dry-run release paths
- [x] `--skip-tech-docs-check` flag in cli.js and mcp-server.mjs
- [x] Warn on patch, block on minor/major

## Gate 2: Interface Coverage (#128)

Verify the interface coverage table in README.md and SKILL.md matches actual interfaces detected in tools/*/.

- [x] `checkInterfaceCoverage()` function in core.mjs
- [x] `parseInterfaceCoverageTable()` helper
- [x] `getToolDisplayName()` helper (reads SKILL.md frontmatter)
- [x] Detects: tool missing from table, interface mismatch (Y vs detected), tool count mismatch
- [x] Checks both README.md and SKILL.md tables
- [x] Integrated into real + dry-run release paths
- [x] `--skip-coverage-check` flag in cli.js and mcp-server.mjs
- [x] Warn on patch, block on minor/major

## Files Modified

| File | Change |
|------|--------|
| `tools/wip-release/core.mjs` | checkTechnicalDocs, checkInterfaceCoverage, helpers, release flow integration |
| `tools/wip-release/cli.js` | --skip-tech-docs-check, --skip-coverage-check flags |
| `tools/wip-release/mcp-server.mjs` | Skip flags in MCP schema + handler |
