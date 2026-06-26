# Add wip-repo-init: scaffold the standard ai/ directory

**Date:** 2026-03-11 10:15 PST
**Author:** Claude Code (cc-mini)

## What changed

New tool: `wip-repo-init`. Scaffolds the standard `ai/` directory structure in any repo.

- New repo (no ai/ folder): creates the full structure with self-documenting READMEs
- Existing repo: confirms first, then moves old ai/ to `ai/_sort/ai_old/` so you can sort at your own pace
- Nothing is ever deleted
- Template includes: dev-updates, product bible, roadmap, plans with lifecycle stages, todos, product ideas, notes
- Every folder has `_trash/` (archive) and key folders have `_sort/` (holding pen)
- Fixed typo in template: `dev-udates` -> `dev-updates`
- All template files rewritten to be generic (removed Memory Crystal references)

## Files changed

- `tools/ai-dir-template/init.mjs` ... the CLI tool
- `tools/ai-dir-template/package.json` ... package definition
- `tools/ai-dir-template/SKILL.md` ... skill documentation
- `tools/ai-dir-template/ai/` ... all template files rewritten
- `README.md` ... added Repo Init under Repo Management
- `SKILL.md` ... added wip-repo-init section and interface coverage
