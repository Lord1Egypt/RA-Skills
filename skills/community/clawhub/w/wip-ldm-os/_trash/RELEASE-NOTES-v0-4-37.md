# Release Notes: wip-ldm-os v0.4.37

**TECHNICAL.md audit: CLI reference, installation system, operations all documented.**

## What changed

Full TECHNICAL.md audit covering v0.4.5 through v0.4.36. The file was an architecture/philosophy document with zero operational docs. Now includes:

- **CLI Reference:** All ldm commands (init, install, doctor, status, worktree, updates, enable/disable, uninstall) with usage and flags.
- **Installation System:** Catalog, registry, interface detection, self-update, parent package detection, ghost cleanup, private repo redirect, staging directory.
- **Operations:** Process monitor, debug logger (LDM_DEBUG=1), CI pipeline, Prettier config.
- **Updated architecture diagram:** Now shows extensions/, logs/, tmp/, state/, actual agent names (cc-mini, oc-lesa-mini).

## Why

32 releases shipped with only the philosophical architecture doc. Agents and users had no reference for how `ldm install` works, what `ldm doctor` checks, or what the catalog system does.

## Issues closed

- #155

## How to verify

```bash
grep "ldm install" TECHNICAL.md       # CLI reference
grep "catalog" TECHNICAL.md           # installation system
grep "LDM_DEBUG" TECHNICAL.md         # debug logger
```
