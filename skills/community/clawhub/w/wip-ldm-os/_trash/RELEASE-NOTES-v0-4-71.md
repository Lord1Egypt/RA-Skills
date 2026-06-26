# Release Notes: wip-ldm-os v0.4.71

Related: #255, #257, #262

## Registry as source of truth + backup fixes

The installer was broken in a fundamental way: it checked a catalog baked into the npm package to know what exists, then compared against the registry to know what's installed. Every CLI update got a fresh catalog, which triggered unnecessary reinstalls. Private repos and third-party extensions were invisible to the update checker because they weren't in the catalog.

This release fixes that. The registry is now the single source of truth. When you install anything (your repos, someone else's, local paths), the registry records where it came from. `ldm install` checks every registry entry for updates. Private repos work via SSH. Third-party repos are tracked forever. The catalog becomes a discovery tool for new users, not the authority for updates.

Also fixes the backup script deployment (reads iCloud path from the unified config instead of a deleted settings file) and the installer build order (npm install before resolveLocalDeps before build). The OpenClaw backup-verify cron that was creating duplicate 23GB backups every night has been removed.

**Registry as source of truth (#262).** The installer now checks the registry for updates, not the catalog. Install anything from anywhere (your repos, other people's repos, local paths). The registry tracks where each extension came from and checks for updates there. Private repos work via SSH. Third-party repos are tracked. No more unnecessary reinstalls when the CLI updates. The catalog becomes a "featured" list for discovery, not the authority for updates.

**Installer deploy order fix (#257).** npm install runs first (gets devDependencies), resolveLocalDeps runs second (symlinks file: deps from installed extensions), npm run build runs third. Also fixes EEXIST error when symlink target already exists from a previous npm install attempt.

**Backup script reads from unified config.** The deployed backup script now reads iCloud path and keep days from `~/.ldm/config.json` instead of the deleted `$WORKSPACE/settings/config.json`. Also reads org name from config for the tar filename instead of hardcoded "wipcomputerinc". OpenClaw backup-verify cron removed (was creating duplicate 23GB backups every night).
