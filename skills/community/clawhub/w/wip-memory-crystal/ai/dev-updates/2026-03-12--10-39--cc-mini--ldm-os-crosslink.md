# Dev Update: LDM OS Cross-Link

**Date:** 2026-03-12
**Author:** cc-mini
**Branch:** cc-mini/ldm-os-crosslink
**PR:** #42

## What changed

Added "Part of LDM OS" section to the README, placed above the License section. One sentence explaining that Memory Crystal installs into LDM OS, one line pointing to `ldm install` for other components.

This is part of the cross-linking effort (wip-ldm-os-private #20) to make all three products aware of each other. Same section added to the DevOps Toolbox README in a parallel PR.

## What's next
- Merge PR #42
- crystal init: add LDM tip at end of install output
- crystal init: delegate to ldm install when available (#41)
