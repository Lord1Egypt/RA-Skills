# --version on all CLIs + issue cleanup

**Date:** 2026-03-15
**Closes:** #190, #191, #169, #123, #119

## What changed

All 7 CLI tools now support `--version` and `-v`. Each reads its own `package.json` and prints the version. Previously, `wip-release --version` printed the help text instead of a version number.

Tools updated: wip-release, wip-repos, wip-license-guard, wip-repo-permissions, wip-repo-init, wip-readme-format, wip-file-guard, wip-branch-guard.

wip-license-guard also got a proper README (#169) with all commands, config format, and integration docs.

## Issues closed

- #190: wip-release --version should work
- #191: enforce --version on all CLI tools
- #169: wip-license-guard needs its own README
- #123: Merge/Deploy/Install conflated (enforced across v1.9.25-v1.9.30)
- #119: All destructive tools must have --dry-run (all confirmed)
