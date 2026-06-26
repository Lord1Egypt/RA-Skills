# Plan: Registry as Source of Truth

**Date:** 2026-03-31
**Author:** cc-mini (with Parker)
**Issue:** wipcomputer/wip-ldm-os#262

## Context

`ldm install` is a package manager. It should install from anywhere, track everything, and update everything. Today the catalog (baked into npm) controls what the installer knows about. Private repos, third-party repos, anything not in the catalog is invisible. The catalog changes on every CLI update, causing unnecessary reinstalls.

## The principle

The registry is the single source of truth. If it's installed, the registry knows about it. If the registry knows about it, the installer can update it. Doesn't matter where it came from.

## Current architecture (broken)

```
catalog.json (baked in npm package)
  |
  v  installer reads this to know what exists
~/.ldm/extensions/registry.json
  |
  v  installer reads this to know what's installed
comparison -> reinstall if different
```

Problems:
- Catalog changes on every CLI update (triggers reinstalls)
- Private repos not in catalog (can't auto-update)
- Third-party repos not in catalog (can't track)
- Two files that should be one

## New architecture

```
~/.ldm/extensions/registry.json (the ONE source of truth)
  |
  |  Contains: everything installed, where it came from, what version
  |
  v  ldm install reads this, checks sources for updates
"3 updates available" -> install if user says yes
```

### Registry entry (new format)

```json
{
  "memory-crystal": {
    "source": {
      "type": "github",
      "repo": "wipcomputer/memory-crystal",
      "npm": "@wipcomputer/memory-crystal"
    },
    "installed": {
      "version": "0.7.33",
      "installedAt": "2026-03-31T19:00:00Z",
      "updatedAt": "2026-03-31T19:00:00Z"
    },
    "paths": {
      "ldm": "~/.ldm/extensions/memory-crystal",
      "openclaw": "~/.openclaw/extensions/memory-crystal"
    },
    "interfaces": ["cli", "mcp", "ocPlugin", "skill"],
    "origin": "catalog"
  },
  "gstack": {
    "source": {
      "type": "github",
      "repo": "garrytan/gstack"
    },
    "installed": {
      "version": "1.2.0",
      "installedAt": "2026-04-01T10:00:00Z"
    },
    "paths": {
      "ldm": "~/.ldm/extensions/gstack"
    },
    "interfaces": ["skill"],
    "origin": "manual"
  }
}
```

`origin` tracks how it got there: `"catalog"` (from the featured list), `"manual"` (user ran `ldm install repo`), `"dependency"` (installed as a dep of another extension).

### Update checking

`ldm install` (bare, no args):

1. Read registry
2. For each entry:
   - If `source.npm` exists: `npm view {pkg} version` (fast, one HTTP call)
   - If `source.repo` exists and no npm: `git ls-remote` for latest tag (works for private repos with SSH access)
   - Compare against `installed.version`
3. Show table: "N updates available"
4. Install updates (clone/npm, detect interfaces, deploy)

### First-time install

`ldm install garrytan/gstack`:

1. Clone the repo
2. Detect interfaces (the universal installer already does this)
3. Deploy to harnesses
4. Add to registry with `origin: "manual"` and `source.repo: "garrytan/gstack"`
5. Now `ldm install` tracks it forever

### The catalog becomes optional

`~/.ldm/catalog.json` (NOT baked into npm):
- A "featured" or "recommended" list
- Shown during `ldm setup` or `ldm catalog list`
- NOT used for update checking (the registry does that)
- NOT required (you can install things without it)
- Updated via `ldm catalog update` (pulls latest from wip.computer)

### Stacks still work

Stacks are bundles of catalog entries:
- `ldm stack install core` installs memory-crystal + toolbox + 1password + mdview
- Each one gets a registry entry with `origin: "catalog"`
- After install, the registry tracks them individually

## Migration

1. Read existing `registry.json` entries
2. For each entry, check the catalog for source info (repo URL, npm package)
3. Write new format entries with source info populated
4. Extensions installed manually (not in catalog) get `origin: "manual"` and we try to detect the source from `package.json` repository field
5. Old catalog check code removed from the update loop
6. New update loop reads registry only

## What this enables

- Install anything from anywhere: your repos, other people's repos, local paths
- Track everything: the registry knows what's installed and where it came from
- Update everything: one command checks all sources
- Private repos work: SSH access to GitHub, `git ls-remote` checks tags
- No reinstalls on CLI update: the catalog isn't involved in update checking anymore
- User can edit the registry: add, remove, pin versions

## Files to change

| File | Change |
|------|--------|
| `bin/ldm.js` | Remove catalog-based update checking. Registry-based update loop. |
| `bin/ldm.js` | `ldm install {repo}` writes to registry with source info |
| `bin/ldm.js` | `ldm install` (bare) checks all registry entries |
| `lib/deploy.mjs` | Return source info after deploy for registry write |
| `catalog.json` | Move to `~/.ldm/catalog.json` on init. Optional. |

## What NOT to change

- Interface detection (already works)
- Deploy logic (already works)
- Harness wiring (already works)
- The universal installer pattern (detect, deploy, wire)
