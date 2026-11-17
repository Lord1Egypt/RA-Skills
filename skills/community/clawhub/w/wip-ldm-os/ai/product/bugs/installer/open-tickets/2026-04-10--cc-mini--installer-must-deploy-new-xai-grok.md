# Bug: LDM OS installer does not deploy `wip-x-xai-grok`

**Date:** 2026-04-10
**Filed by:** cc-mini + Parker
**Component:** LDM OS installer (`wip-ldm-os-private/src/boot/installer.mjs`)
**Severity:** High (new correct version can't replace old broken version)

## Summary

`ldm install` has no deploy path for `@wipcomputer/wip-x-xai-grok`. This is why the deprecated `wip-xai-grok` is still the one installed: nothing in the install pipeline knows to replace it.

## Why it matters

The proper migration from `wip-xai-grok` to `wip-x-xai-grok` requires the installer to:

1. Detect that `~/.openclaw/extensions/wip-xai-grok/` is the old deprecated version (by checking version, source repo, or manifest)
2. Uninstall it cleanly (remove the folder, deregister from `plugins.entries` and `tools.allow`)
3. Install the new `@wipcomputer/wip-x-xai-grok` package
4. Deploy it to the right extension folder (naming decision pending; see xai-grok ticket 2)
5. Register it in `plugins.entries` and `tools.allow`
6. Verify by calling `wip-x-xai-grok imagine --help` or similar

The installer currently does none of this. It doesn't even know `wip-x-xai-grok` exists.

## Root cause: no source-of-truth manifest

More broadly, the installer does not have a canonical list of "tools that should be deployed to each runtime." It seems to walk a catalog or registry but without explicit rules for:

- Which version is canonical
- What to uninstall when replacing a tool
- How to handle renames (old extension folder vs new extension folder)
- How to update `tools.allow` after deploy (see existing ticket: `ai/product/bugs/installer/2026-04-08--cc-mini--tools-allow-not-updated-on-plugin-install.md`)

## Fix steps

### Short-term: add `wip-x-xai-grok` to the catalog

1. Add an entry to the LDM OS catalog/registry for `@wipcomputer/wip-x-xai-grok`
2. Add uninstall logic for `wip-xai-grok` (the old extension) as a prerequisite
3. Run `ldm install` and verify the old extension is removed and the new one deployed

### Long-term: proper deploy manifest

See Ticket 4 for the broader audit, but the installer should have:

- A declarative manifest of tools to deploy
- Version tracking per tool
- Migration support (rename, replace, remove)
- Verification step after each install

This becomes part of the post-upgrade smoke test plan filed earlier today:
`ai/product/plans-prds/current/openclaw-upgrade/2026-04-08--cc-mini--post-upgrade-smoke-test.md`

## Files involved

- `wip-ldm-os-private/src/boot/installer.mjs` (or wherever the deploy logic lives)
- Catalog/registry file (needs locating ... might be `catalog.json` or similar)
- `wip-x-xai-grok-private/package.json` (source of the package to install)

## Related

- Ticket 1: Deprecated xai-grok still deployed
- Ticket 2: Finish deprecating the old repo
- Ticket 4: Audit all tools that shell out to `op`
- Existing ticket: `2026-04-08--cc-mini--tools-allow-not-updated-on-plugin-install.md`
- Plan: `2026-04-08--cc-mini--post-upgrade-smoke-test.md`
