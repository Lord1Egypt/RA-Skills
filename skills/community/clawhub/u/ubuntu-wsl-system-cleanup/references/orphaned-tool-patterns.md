# Orphaned Tool Patterns

Focus on leftovers from tools that have already been removed.

## Common leftover categories

### 1. Removed CLI, data still present
Examples:
- command removed from `~/.local/bin`
- pipx/uv/npm package removed
- but related directories still exist under:
  - `~/.cache`
  - `~/.local/share`
  - `~/.config`
  - workspace `_trash`

### 2. Deleted MCP/tool wrappers, package caches remain
Examples:
- npm/npx package removed, but cache remains in `~/.npm`
- temporary downloaded server packages remain in `_npx`
- browser automation tool removed, but browser profile or cache remains

### 3. Moved tool out of active path, dangling launcher remains
Examples:
- broken symlink in `~/.local/bin`
- config entry still references removed command

## Detection checklist

### A. Broken links in `~/.local/bin`
Use:
```bash
find ~/.local/bin -xtype l -print
```

### B. pipx venvs without active launchers
Compare:
- directories under `~/.local/share/pipx/venvs`
- symlink targets from `~/.local/bin`
If a venv has no active launcher and the user confirms it is unused, mark as candidate.

### C. Tool-named leftover directories
Search for removed tool names in:
- `~/.cache`
- `~/.config`
- `~/.local/share`
- workspace `_trash`

### D. Config references to removed tools
Search config files for removed command names and paths.

## Safe second-round actions

- Remove broken symlinks in `~/.local/bin`
- Remove `_trash` entries older than or explicitly confirmed unused
- Remove caches tied to removed tools
- Remove stale config references only when obvious and isolated

## Preserve by default

Do not delete shared runtimes only because one tool was removed, for example:
- Python interpreters used by other tools
- Node/npm globally used cache roots unless the user requested cache cleanup
- shared browser runtimes still required by Crawl4AI or active tools

## Good examples

### Example: browser-use removed
Safe follow-up checks:
- broken symlinks for `browser-use`, `browser`, `browseruse`, `bu`
- `~/.cache` directories named `browser-use` or similar
- config references to `browser-use`

### Example: brew removed
Safe follow-up checks:
- shell init lines referencing brew
- leftover `/home/linuxbrew` paths
- broken PATH shims if any
