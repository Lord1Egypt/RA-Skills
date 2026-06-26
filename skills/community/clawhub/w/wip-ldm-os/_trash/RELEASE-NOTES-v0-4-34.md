# Release Notes: wip-ldm-os v0.4.34

**Fix: detect updates for all npm packages, rename ghost extension dirs.**

## What changed

1. **Non-scoped packages now checked for updates (#141).** Previously, `ldm install` only checked `@wipcomputer/*` packages. Extensions like `tavily` (unscoped) were invisible to the update loop. Now all packages are checked.

2. **Ghost `ldm-install-*` dirs renamed to clean names (#141).** Extensions installed from GitHub got deployed as `ldm-install-<repo>` instead of `<repo>`. Now the cleanup renames these dirs (and their registry entries) to the correct names. Both `~/.ldm/extensions/` and `~/.openclaw/extensions/` are handled.

3. **Tavily added to catalog.** Was installed but not in catalog, so the installer couldn't manage it.

## Why

`ldm install` ran twice and didn't pick up tavily v1.0.0 -> v1.0.2 or wip-xai-grok v1.0.2 -> v1.0.3. Tavily was skipped because of the scope filter. Grok was invisible because the dir was named `ldm-install-wip-xai-grok` instead of `wip-xai-grok`.

## Issues closed

- #141

## How to verify

```bash
ldm install --dry-run
# Should show tavily update if behind
# Should NOT show ldm-install-* names
# Ghost dirs should be renamed to clean names
```
