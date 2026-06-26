# Dev Update: LDM OS Public Launch Prep

**Date:** 2026-03-12
**Author:** cc-mini
**Branch:** cc-mini/public-launch
**PR:** #22

## What changed

### SKILL.md (new)
Wrote the full "Teach Your AI" spec for LDM OS. Follows the same pattern as Memory Crystal and DevOps Toolbox SKILL.md files. Covers: what LDM OS is, platform compatibility, operating rules (dry-run first, never touch sacred data), install steps, component catalog table, interface detection table, update flow.

### catalog.json (new)
Static component catalog that ships with the npm package. Three components:
- Memory Crystal (recommended, stable)
- AI DevOps Toolbox (stable)
- Agent Pay (coming soon)

### Interactive catalog picker in `ldm init`
After scaffolding `~/.ldm/`, `ldm init` now reads catalog.json and shows available components with an interactive prompt. Supports:
- Number selection (1, 2)
- `all` to install everything
- `none` to skip
- `--yes` flag installs recommended components automatically
- `--none` flag skips the picker entirely
- Non-TTY environments skip the prompt silently

### Catalog ID resolution in `ldm install`
`ldm install memory-crystal` now resolves via catalog.json to the GitHub repo and clones it. No need to know the full org/repo path or npm package name. Falls through to existing GitHub/local path logic for non-catalog targets.

### Bare `ldm install` shows catalog status
Running `ldm install` with no arguments now shows installed components (with versions) and available components, with an interactive prompt to install more.

### npx compatibility
Added `wip-ldm-os` as a second bin entry pointing to the same `bin/ldm.mjs`. This means `npx @wipcomputer/wip-ldm-os init` works as a one-liner. `ldm init` remains the short daily-use command.

### README update
Added Components section with links to Memory Crystal, DevOps Toolbox, and Agent Pay.

### Release notes
Wrote RELEASE-NOTES-v0-2-0.md covering: ldm CLI, interface detection, safe deployment, catalog, SKILL.md.

### Full plan
Saved public launch plan to `ai/products/plans-prds/ldm-os-public-launch-plan.md` covering all phases: LDM OS prep, npm publish, public repo, MC cross-link, Toolbox cross-link, crystal init delegation, wip-install delegation, verification.

## What's next
- Merge PR #22
- npm publish as @wipcomputer/wip-ldm-os (requires Parker approval)
- Sync to public repo via deploy-public.sh (requires Parker approval)
- crystal init: delegate to ldm install (#41)
- wip-install: delegate to ldm install (#77)
