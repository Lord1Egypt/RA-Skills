# Release Notes: wip-ldm-os v0.4.63

Closes #244, #245, #247

## Bridge fix, config merge, OpenClaw pin, cc-watcher disable

The lesa-bridge MCP tool (`lesa_send_message`) was broken since Mar 29 when `ldm install` silently upgraded OpenClaw from v2026.2.22-2 to v2026.3.28. The new gateway changed its model validation: it requires `openclaw/main` instead of just `main`. The bridge was sending the old format.

This release fixes that and addresses three related issues discovered during the investigation.

### What changed

**Bridge model param fix.** `src/bridge/core.ts` now sends `model: "openclaw/main"` instead of `model: "main"`. The original code (Feb 10) sent `"openclaw:main"` with a colon. At some point during the bridge absorption into LDM OS (Mar 15), the prefix was dropped. The gateway later changed from colon to slash separator. Neither side was updated to match.

**Config merge.** `config-from-home.json` is merged into `config.json` on install. The backup script reads iCloud path and keep days from the unified config at `~/.ldm/config.json` instead of the deleted `$WORKSPACE/settings/config.json`.

**OpenClaw pinned in catalog.** `ldm install` no longer auto-upgrades OpenClaw. Upgrades overwrite three dist patches (EMFILE, walkDir, cron catch-up) documented in KNOWN-LANDMINES.md. OpenClaw upgrades must be explicit.

**cc-watcher disabled.** The broken LaunchAgent (old iCloud path, wrong node path, exit 78 since Mar 24) is disabled on install. Renamed to `.disabled`, not deleted.

**Hardcoded org name removed.** Backup tar filename reads from config instead of hardcoded "wipcomputerinc".

**CI fix.** Added package-lock.json and reverted to `npm ci` for reproducible builds.
