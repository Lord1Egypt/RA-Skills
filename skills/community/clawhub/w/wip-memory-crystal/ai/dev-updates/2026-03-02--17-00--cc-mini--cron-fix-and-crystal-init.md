# Dev Update: Cron Fix, op Popup Fix, crystal init Deployment

**Date:** 2026-03-02 17:00 PST
**Author:** CC-Mini
**Session:** Continuation from capture-crisis session

---

## What Was Done

### 1. Cron Path Fixed

Replaced `open -W ~/Applications/LDMDevTools.app --args crystal-capture` with `~/.ldm/bin/crystal-capture.sh` in crontab. The app approach failed with error -1712 at every-minute frequency. `~/.ldm/bin/` is a local path (not iCloud), so no Full Disk Access needed.

### 2. op Popup Bug Found and Fixed

`crystal-capture.sh` was calling `op item get "OpenAI" --fields label=credential` every minute. Two problems:
- Service accounts require `--vault` flag. Without it, `op` falls back to interactive auth.
- macOS TCC pops a consent dialog for `op` accessing files from cron context.

The fix: removed the `op` call from the shell script entirely. The Node poller already has `opRead()` in `core.ts:1346` that correctly uses `op read "op://Agent Secrets/OpenAI API/api key"` with the SA token via environment variable. No popup, no redundant call.

Updated all three copies: repo source, `~/.ldm/bin/`, and LDM Dev Tools app bundle.

### 3. crystal-capture.sh Moved to Memory Crystal Repo

Source of truth is now `memory-crystal-private/scripts/crystal-capture.sh`. The dev tools copy at `wip-dev-tools-private/tools/ldm-jobs/crystal-capture.sh` is a downstream consumer with a pointer comment.

**Dependency direction:** Memory Crystal never depends on Dev Tools. Dev Tools can pull from Memory Crystal if it wants a copy.

### 4. crystal init Now Deploys Script + Cron

`crystal init` now does three things:
1. Scaffolds `~/.ldm/` directory tree (existing behavior)
2. Copies `crystal-capture.sh` to `~/.ldm/bin/` (new)
3. Installs cron entry for every-minute capture (new)

The build pipeline copies `scripts/crystal-capture.sh` into `dist/` so the deployed package includes it. `deployCaptureScript()` in `ldm.ts` resolves the script from the package's dist/ directory.

### 5. LdmPaths Interface Updated

Added `bin: string` (`~/.ldm/bin`) to the `LdmPaths` interface and scaffolding.

---

## Files Changed

| File | Change |
|------|--------|
| `scripts/crystal-capture.sh` | NEW. Source of truth for the capture script. |
| `src/ldm.ts` | Added `bin` to paths, `deployCaptureScript()`, `installCron()`, `removeCron()` |
| `src/cli.ts` | `crystal init` now deploys script + cron |
| `package.json` | Build copies crystal-capture.sh to dist/ |
| `~/.ldm/bin/crystal-capture.sh` | Updated (removed op call) |
| `wip-dev-tools-private/.../crystal-capture.sh` | Downgraded to downstream copy with pointer |
| `LDMDevTools.app/.../crystal-capture.sh` | Updated (removed op call) |

## Verified

- `crystal init` scaffolds, deploys script, installs cron
- Manual run: 16 chunks captured, 0 errors
- No macOS popup from op
- Cron running every minute from `~/.ldm/bin/`

## Still Pending

- Update install docs (SKILL.md, TECHNICAL.md, README) to reflect new install flow
- Commit all Phase 1 changes to git
- Dev Tools pattern idea (auto-update docs on install-related commits)
