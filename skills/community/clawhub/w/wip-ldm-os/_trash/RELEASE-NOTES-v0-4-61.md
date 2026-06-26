# Release Notes: wip-ldm-os v0.4.61

**Fix installer: stop recursive subprocess spawning, fix tavily catalog resolution.**

## The story

Two installer bugs causing a 3.5 minute install time that should take seconds:

1. When installing catalog components, the installer spawned `execSync('ldm install <repo>')` for each one. Each subprocess ran the full installer: system state check, catalog lookup, npm check, clone, detect, deploy. For 12 toolbox sub-tools, that's 12 full installer runs. Replaced with a direct `installCatalogComponent()` function call that clones (with --depth 1) and installs in one pass.

2. `findInCatalog('wipcomputer/openclaw-tavily')` matched the `openclaw` catalog entry because `"wipcomputer/openclaw-tavily".includes("openclaw")` was true. The installer then cloned the entire OpenClaw platform repo (instead of the tiny tavily plugin). Fixed the partial match to require hyphen-aligned word boundaries. Added exact repo URL matching.

## Issues closed

- #232 (installer performance + tavily resolution)

## How to verify

```bash
time ldm install
# Should complete in seconds, not minutes
# Tavily should NOT clone openclaw/openclaw
```
