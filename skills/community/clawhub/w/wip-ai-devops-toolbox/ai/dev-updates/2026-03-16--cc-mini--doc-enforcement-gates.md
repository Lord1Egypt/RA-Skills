# Doc enforcement gates for wip-release

**Date:** 2026-03-16
**Closes:** #117, #128

## What changed

Two new pre-release gates in wip-release:

**Technical Docs Gate (#117):** When source code (*.mjs, *.js, *.ts) changed since the last release tag, checks that SKILL.md or TECHNICAL.md was also modified. Catches code shipping without doc updates. Warns on patch, blocks on minor/major. Skip with `--skip-tech-docs-check`.

**Interface Coverage Gate (#128):** For toolbox repos, scans each tool in tools/*/ for actual interfaces (CLI, Module, MCP, OC Plugin, Skill, CC Hook) and compares to the coverage table in README.md and SKILL.md. Reports: tools missing from table, interfaces detected but not marked Y, interfaces marked Y but not detected, tool count mismatches. Warns on patch, blocks on minor/major. Skip with `--skip-coverage-check`.

Both follow the same pattern as existing gates (checkProductDocs, checkStaleBranches). Both run in real and dry-run modes.

## Why

Source code was shipping without doc updates constantly. SKILL.md and TECHNICAL.md fell behind the code. Interface coverage tables drifted from reality. These gates catch it before release instead of after.
