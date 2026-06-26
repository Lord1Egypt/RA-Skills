# Release Notes: wip-ldm-os v0.4.72

Related: #262, #288, #289

## Installer deploys scripts, docs, and checks backup health on every update

Previously, scripts and docs were only deployed during `ldm init`. This meant fixes to the backup script, library documentation, and other deployed files never reached the user's machine until they manually ran init. Most users never run init after the first install.

Now `ldm install` deploys scripts to `~/.ldm/bin/` and personalized docs to `~/wipcomputerinc/library/documentation/` on every run. The backup health check runs too: verifies iCloud offsite is configured, the LaunchAgent is loaded, the last backup is recent, and the script exists. Creates the iCloud directory if missing.

Also includes backup docs at `docs/backup/` (README.md + TECHNICAL.md) and the updated library doc that matches the current backup architecture (3 AM LaunchAgent, unified config at `~/.ldm/config.json`).
