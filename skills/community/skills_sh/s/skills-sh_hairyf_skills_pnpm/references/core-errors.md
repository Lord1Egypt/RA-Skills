---
name: pnpm-error-codes
description: Common pnpm error codes and resolutions
---

# pnpm Error Codes

## ERR_PNPM_UNEXPECTED_STORE

Modules directory is linked to a different store. Run `pnpm install` to reinstall with the current store.

## ERR_PNPM_NO_MATCHING_VERSION_INSIDE_WORKSPACE

Workspace dependency version doesn't exist. Example: `bar@workspace:1.0.0` but workspace has `bar@2.0.0`.

**Fix:** Update `workspace:` refs to match available versions. Use `pnpm -r update`.

## ERR_PNPM_PEER_DEP_ISSUES

Unresolved or mismatched peer dependencies.

**Fix:** Install missing peers, or use `peerDependencyRules.ignoreMissing` / `peerDependencyRules.allowedVersions` in config.

## ERR_PNPM_OUTDATED_LOCKFILE

Installation requires lockfile changes. Often in CI when `package.json` changed without running `pnpm install`.

**Fix:** Run `pnpm install` and commit updated `pnpm-lock.yaml`.

## ERR_PNPM_TARBALL_INTEGRITY

Downloaded tarball doesn't match expected checksum. Can indicate bad merge, wrong registry, or stale metadata.

**Fix:** If using npm registry—check lockfile integrity. If custom registry—run `pnpm store prune` and retry. Verify URL in error.

## ERR_PNPM_MISMATCHED_RELEASE_CHANNEL

`use-node-version` channel doesn't match version suffix (e.g. `rc/20.0.0` for stable, `release/20.0.0-rc.0` for rc).

**Fix:** Align prefix with version: `rc/X.Y.Z-rc.W` or `release/X.Y.Z`.

## ERR_PNPM_INVALID_NODE_VERSION

Invalid `use-node-version` syntax.

**Valid:** `X.Y.Z`, `release/X.Y.Z`, `X.Y.Z-rc.W`, `rc/X.Y.Z-rc.W`.

<!--
Source references:
- https://pnpm.io/errors
-->
