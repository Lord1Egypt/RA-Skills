# Release Notes: Memory Crystal v0.7.5

## LDM OS Integration

Memory Crystal now works with LDM OS when it's available.

### crystal init delegates to ldm install

When the `ldm` CLI exists on PATH, `crystal init` delegates generic deployment to it. LDM OS handles the scaffold, interface detection, and extension deployment. Memory Crystal keeps its own setup: database backup, role configuration, pairing, cron jobs.

When `ldm` isn't available, `crystal init` works standalone like it always has. No new dependencies. No breaking changes.

### LDM OS tip

After install completes, Memory Crystal prints a tip: "Run `ldm install` to see more skills you can add." Helps users discover the rest of the ecosystem.

### Part of LDM OS

README now includes a "Part of LDM OS" section linking back to the LDM OS repo. Memory Crystal installs into LDM OS, the local runtime for AI agents.
