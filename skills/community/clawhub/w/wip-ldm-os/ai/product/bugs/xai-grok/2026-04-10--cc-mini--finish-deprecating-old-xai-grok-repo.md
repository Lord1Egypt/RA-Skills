# Bug: `wip-xai-grok-private-deprecated` is only half-deprecated

**Date:** 2026-04-10
**Filed by:** cc-mini + Parker
**Component:** wip-xai-grok-private-deprecated repo cleanup
**Severity:** Medium (naming lies about state, causes confusion)

## Summary

The repo at `ldm-os/apis/wip-xai-grok-private-deprecated` has `-deprecated` in its name, but it is still the version that's:

- Installed globally at `/opt/homebrew/bin/wip-xai-grok`
- Deployed as an OpenClaw extension at `~/.openclaw/extensions/wip-xai-grok/`
- Being called by agents (both Lēsa and CC)
- Referenced in skills and documentation

The rename to "deprecated" implied the migration to `wip-x-xai-grok-private` was complete. It wasn't. Half the work got done (new repo created, auth layer rewritten using the SDK helper) but the other half (actually retiring the old one) never happened.

## What "deprecation" requires

A real deprecation of this repo needs:

1. **Archive the GitHub repo** (if it's not already)
2. **Unpublish or mark as deprecated on npm** (whoever owns the `@wipcomputer/wip-xai-grok` package)
3. **Uninstall the global binary** (`npm uninstall -g @wipcomputer/wip-xai-grok`)
4. **Remove the extension** (`rm -rf ~/.openclaw/extensions/wip-xai-grok/`)
5. **Remove from `tools.allow` / `plugins.entries` / any skill manifests** that reference `wip-xai-grok`
6. **Update docs** that say "use wip-xai-grok" to point at the new package
7. **Move the source folder** from `ldm-os/apis/wip-xai-grok-private-deprecated` to `ldm-os/_trash/` or archive

## Decision needed: naming

There are two options for what replaces it:

### Option A: Rename the new one back to `wip-xai-grok`

- New source: `ldm-os/apis/wip-xai-grok-private` (rename from `wip-x-xai-grok-private`)
- Keep the binary name `wip-xai-grok`
- Keep the extension folder `~/.openclaw/extensions/wip-xai-grok/`
- Existing scripts and TOOLS.md references Just Work
- **Downside:** the new package includes X Platform (Twitter) features, so "wip-xai-grok" is a lie ... it's not just Grok anymore

### Option B: Keep the new name `wip-x-xai-grok`

- Install binary as `/opt/homebrew/bin/wip-x-xai-grok`
- Extension folder `~/.openclaw/extensions/wip-x-xai-grok/`
- Update all scripts and docs to use the new name
- **Downside:** breaking change for everything that calls `wip-xai-grok`

**Parker's call.** Either is technically fine. Option A is less breaking. Option B is more honest about what the tool is.

## Related

- Ticket 1: `wip-xai-grok` deprecated version still deployed
- Ticket 3: Installer needs to deploy the new version
