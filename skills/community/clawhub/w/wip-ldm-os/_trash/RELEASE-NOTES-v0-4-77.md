# wip-ldm-os v0.4.77

## Installer fix: deployExtension compares content hash, not just version

`lib/deploy.mjs:deployExtension` previously skipped the file copy when source and deployed `package.json` reported the same version. If a prior partial install had bumped the deployed `package.json` but failed mid-copy (or the deployed tree was manually touched), the installer would "apparently be current" while other files lagged behind.

Hit during the `wip-release 1.9.74 -> 1.9.75` rollout on 2026-04-20: deployed `package.json` said `1.9.75` but deployed `core.mjs` was the old 1.9.74 content (no `runNpmPublish`, no `spawnSync`). File bytes diverged; the stderr-capture fix never reached the deployed installer.

Fix: new `computeTreeHash(dir)` helper (sha256 over `(relpath, bytes)` for every non-blacklisted file). The skip path in `deployExtension` now requires `srcHash === dstHash` in addition to the version check. Content drift triggers a visible redeploy with a `reports same version but content differs; redeploying` log line.

Blacklisted from the hash: `.git`, `node_modules`, `ai`, `_trash`, `.worktrees`, `logs`, `test`, `tests`, `__tests__`. These are developer-side only and shouldn't contribute to the content signature.

## Plan amendment

Also amends `ai/product/bugs/guard/2026-04-20--cc-mini--guard-implementation-plan.md` with:

- Trail of installer bugs surfaced during the PR 2 cascade (`wip-ldm-os v0.4.76`, `wip-release v1.9.75-1.9.76`, `wip-branch-guard v1.9.77-v1.9.79`)
- The specific content-hash tracking note per Parker's request

## Files

- `lib/deploy.mjs`: +61 insertions, -11 deletions. New `computeTreeHash(dir)` helper + hash-guarded skip path in `deployExtension`.
- `ai/product/bugs/guard/2026-04-20--cc-mini--guard-implementation-plan.md`: +16 insertions.

## Rollout

After merge: `wip-release patch` bumps to 0.4.77 and publishes `@wipcomputer/wip-ldm-os`. `ldm install` on dev machines deploys the fixed installer. Any future partial-install drift now heals on the next invocation instead of silently persisting.

## Related

- PR #625 (installer content-hash fix)
- PR #361 (closes PR 3 of the 2026-04-20 plan: `wip-branch-guard v1.9.80` external-PR create guard)
- Plan: `ai/product/bugs/guard/2026-04-20--cc-mini--guard-implementation-plan.md`
