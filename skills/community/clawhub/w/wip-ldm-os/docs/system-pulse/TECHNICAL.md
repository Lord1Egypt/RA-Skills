# System Pulse ... Technical Reference

## Commands

### ldm doctor

Checks system health across all components:

1. `~/.ldm/` exists
2. `version.json` valid and version matches CLI
3. Full system state scan (extensions, MCP, CLIs, skills)
4. Reconciliation (registry vs deployed vs MCP registered)
5. Sacred directories exist (memory/, agents/, state/, sessions/, messages/)
6. Claude Code hooks configured (checks for stale paths)
7. MCP servers registered
8. CLI binaries on PATH

With `--fix`:
- Removes stale registry entries (registered but not deployed)
- Removes stale hook paths from `~/.claude/settings.json` (missing files, `/tmp/` paths)

### ldm status

Quick overview: version, install date, extension count, extension list with versions.

### ldm updates

Shows cached update check results. Use `--check` to re-scan npm for newer versions of installed extensions.

## State Detection

`lib/state.mjs` scans the real system:

| Source | What it finds |
|--------|--------------|
| `~/.claude.json` | MCP servers (user scope) |
| `~/.ldm/extensions/` | Deployed extensions (LDM) |
| `~/.openclaw/extensions/` | Deployed extensions (OpenClaw) |
| `~/.ldm/extensions/registry.json` | Registry metadata |
| PATH | CLI binaries (with 5s timeout per binary) |
| `~/.openclaw/skills/` | Deployed skills |

Reconciliation compares all sources and determines status:
- `healthy`: registered + deployed + source available
- `installed-unlinked`: registered + deployed, no source repo
- `registered-missing`: in registry but not deployed
- `deployed-unregistered`: deployed but not in registry
- `mcp-only`: MCP server without LDM management

## Key Files

| File | What |
|------|------|
| `bin/ldm.js` | `cmdDoctor()`, `cmdStatus()`, `cmdUpdates()` |
| `lib/state.mjs` | `detectSystemState()`, `reconcileState()`, `formatReconciliation()` |
| `lib/updates.mjs` | npm version checking, manifest caching |
