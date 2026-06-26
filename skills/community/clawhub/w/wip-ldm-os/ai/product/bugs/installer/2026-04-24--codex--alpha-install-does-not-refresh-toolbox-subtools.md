# Alpha install does not refresh toolbox sub-tools

Status: Fixed in branch. Close after merge and release.
Public issue: https://github.com/wipcomputer/wip-ldm-os/issues/272
Owner repo: `wip-ldm-os-private`
Discovered: 2026-04-24

## Summary

After the guard/repo-tools alpha release, the npm global commands updated but the LDM-deployed extension copies did not.

Observed after `@wipcomputer/wip-ai-devops-toolbox@1.9.73-alpha.3`:

- `wip-branch-guard --version` returned `1.9.88`
- `wip-repos --version` returned `1.9.69`
- `node ~/.ldm/extensions/wip-branch-guard/guard.mjs --version` returned `1.9.86`
- `node ~/.ldm/extensions/wip-repos/cli.mjs --version` returned `1.9.68`

`ldm install --alpha --yes` reported everything up to date, so the installer did not redeploy the extension runtime that agents actually use.

## Impact

Agents can believe alpha validation passed because the global CLI is current while Codex, Claude Code, and OpenClaw still load older extension files from `~/.ldm/extensions`. For guard/repo-tools this means the exact runtime that should prevent workflow mistakes is not the runtime being tested.

## Required fix

- Make alpha/beta update detection refresh toolbox-style parent packages when any deployed sub-tool is stale.
- Redeploy sub-tools from the updated parent package into `~/.ldm/extensions`.
- Preserve the rule that stable/latest installs are Lēsa dogfood unless she explicitly asks an agent to run them.
- Add regression coverage for stale deployed sub-tools under a newer parent package.

## Acceptance criteria

- `ldm install --alpha --yes` updates the deployed `wip-branch-guard` extension to `1.9.88`.
- `ldm install --alpha --yes` updates the deployed `wip-repos` extension to `1.9.69`.
- A regression test fails before the fix and passes after it.
- The public issue is closed after the fix ships.

## Resolution

Implemented in this branch:

- Parent-package update detection now honors `--alpha` and `--beta` by querying the requested npm dist-tag instead of always querying the stable `version`.
- Parent-package post-install bookkeeping no longer stamps the aggregate toolbox version onto sub-tool registry entries. Each sub-tool keeps its own package version.
- Added `scripts/test-installer-update-tracks.mjs` and `npm run test:installer-update-tracks`.

Local validation:

- Before the fix, `ldm install --alpha --yes` reported everything up to date while deployed extension files stayed stale.
- After the fix, `node bin/ldm.js install --dry-run --alpha` reports `wip-ai-devops-toolbox v1.9.72 -> v1.9.73-alpha.3`.
- Running the fixed installer deployed `wip-branch-guard 1.9.88` and `wip-repos 1.9.69`.
- Registry entries now agree: `wip-branch-guard 1.9.88`, `wip-repos 1.9.69`.
