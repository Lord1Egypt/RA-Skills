# Release Notes: memory-crystal v0.7.32

**Date:** 2026-03-31

## What changed

### Dream Weaver is a required dependency again

Reverts PR #101 (optional Dream Weaver import). dream-weaver-protocol is back in `dependencies` instead of `optionalDependencies`. The static import in `dream-weaver.ts` is restored. The dynamic import with try/catch wrapper is removed. The null check in `cli.ts` for when DW is unavailable is removed.

## Why

PR #101 made dream-weaver-protocol optional because `file:../dream-weaver-protocol-private` failed in fresh clones where the sibling directory doesn't exist. The installer (v0.4.68+) now resolves `file:` dependencies from installed extensions at `~/.ldm/extensions/` before building, so the sibling directory is no longer needed. The build succeeds without it.

Making DW optional added complexity (dynamic imports, null checks, degraded type safety) that is no longer necessary. This revert simplifies the code back to what it was.

## How to verify

```bash
# Build should succeed (installer resolves file: deps)
cd memory-crystal-private && npm run build

# dream-weaver-protocol should be in dependencies, not optionalDependencies
node -e "const p = require('./package.json'); console.log('deps:', !!p.dependencies['dream-weaver-protocol']); console.log('optional:', !!p.optionalDependencies?.['dream-weaver-protocol'])"
# Should print: deps: true, optional: false
```
