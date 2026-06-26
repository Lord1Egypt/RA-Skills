# Release Notes: wip-ldm-os v0.4.30

**Fix installer: catalog name lookup, private repo redirect, staging dir.**

## What changed

Three installer bugs fixed:

1. **Catalog name lookup (#133):** `ldm install xai-grok` now works. `findInCatalog` matches partial IDs (e.g. "xai-grok" finds "wip-xai-grok"), display names (e.g. "xAI Grok"), and registryMatches. Previously only exact ID match worked.

2. **Private repo redirect (#134):** `ldm install wipcomputer/foo-private` now auto-redirects to the public repo (`wipcomputer/foo`). Extensions should come from public repos (code only), not private repos (which contain ai/ folders with internal plans and notes).

3. **Staging dir moved from /tmp/ to ~/.ldm/tmp/ (#135):** macOS clears /tmp/ on reboot. Install staging clones were lost after restart, and MCP configs pointing to /tmp/ paths would break. Now uses ~/.ldm/tmp/ which persists. Doctor cleanup checks both old and new locations.

## Why

Users couldn't install catalog components by name. Private repos leaked internal content into installed extensions. /tmp/ staging caused ghost directories and broken MCP configs after reboots.

## Issues closed

- #133
- #134
- #135

## How to verify

```bash
npm install -g @wipcomputer/wip-ldm-os@0.4.30
ldm install xai-grok --dry-run     # should resolve via catalog
ldm install --dry-run               # staging uses ~/.ldm/tmp/
```
