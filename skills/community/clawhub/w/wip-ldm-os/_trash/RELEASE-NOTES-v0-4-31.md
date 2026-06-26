# Release Notes: wip-ldm-os v0.4.31

**Fix ldm install: detect CLI updates, parent package updates, and clean ghost entries.**

## What changed

Three bugs fixed in `ldm install --dry-run` and `ldm install`:

1. **CLI self-update detection.** `ldm install --dry-run` now shows when LDM OS CLI itself is behind. Previously the CLI version check was display-only in dry-run and silently updated during real installs. Now it's part of the update plan.

2. **Parent package detection.** Toolbox-style repos (like wip-ai-devops-toolbox with 12 sub-tools) now report updates under the parent name. Previously only individual sub-tools were checked, so "wip-release v1.9.44 -> v1.9.45" showed instead of "wip-ai-devops-toolbox v1.9.44 -> v1.9.45". The other 11 sub-tools were invisible.

3. **Ghost registry cleanup.** Entries with `-private` suffix or `ldm-install-` prefix (from pre-v0.4.30 installs) are automatically cleaned from the registry. No more phantom "wip-xai-grok-private" showing as a separate extension.

## Why

After releasing three packages (memory-crystal v0.7.28, LDM OS v0.4.30, wip-ai-devops-toolbox v1.9.45), `ldm install --dry-run` couldn't detect any of its own updates. The installer was blind to its own releases. Broke when universal installer was moved internally in v0.4.29.

## Issues closed

- #132

## How to verify

```bash
# Install, then immediately check:
ldm install --dry-run
# Should show CLI update if behind
# Should show parent package names (not sub-tool names)
# Should NOT show -private or ldm-install- ghost entries
```
