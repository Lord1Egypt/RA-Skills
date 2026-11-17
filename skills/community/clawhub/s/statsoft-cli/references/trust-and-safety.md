# Trust & Safety

This skill performs **high-risk operations**. Understand risk levels before use:

| Risk | Level | Description |
|------|-------|-------------|
| Execute local executables | 🔴 High | Launches detected statistical software (e.g., `stats.exe`, `Rscript.exe`) |
| Download & install software | 🔴 High | Fetches R installer from CRAN, Anaconda installer from Anaconda repos |
| Modify config.json | 🟡 Medium | Writes software paths, backs up existing config |
| Execute user-provided scripts | 🔴 High | Runs `.sps` content via SPSS Python, creating temporary wrapper scripts |
| Network access | 🟡 Medium | Downloads installers from CRAN, Anaconda repositories |

> Required permissions (local file read/write / process execution / network access) are described in the "Core Permissions" section of `SKILL.md`.

**Pre-flight**: ✅ Review all scripts; ✅ Confirm config.json changes (auto-backed up); ✅ Confirm any download tasks; ✅ Check generated commands for sensitive projects.