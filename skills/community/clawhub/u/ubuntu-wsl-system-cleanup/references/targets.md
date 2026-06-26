# Cleanup Targets

## Default safe targets

### APT caches
- `/var/cache/apt`
- `/var/lib/apt/lists`
Safe to clean and will be regenerated.

### Journald logs
- inspect with `journalctl --disk-usage`
- safe vacuum examples:
  - `journalctl --vacuum-time=7d`
  - `journalctl --vacuum-size=200M`

### Temporary directories
- `/tmp`
- `/var/tmp`
Only remove stale files, not very recent ones.

### User caches
- `/root/.npm`
- `/root/.cache`
- pip/npx caches inside them
These are usually rebuildable.

## Usually preserve
- `/root/.openclaw`
- `/root/.local/share/pipx/venvs/crawl4ai`
- `/root/.local/share/pipx/venvs/agent-reach`
- project directories
- Docker volumes unless explicitly requested
- shared runtimes such as `uv`, `npm`, Python, and browser binaries still needed by active tools

## Second-round cleanup targets
When the user wants deeper cleanup after uninstalling tools, also inspect:
- broken symlinks in `~/.local/bin`
- stale tool caches in `~/.cache`
- stale tool configs in `~/.config`
- stale tool data in `~/.local/share`
- old workspace `_trash` entries already approved for permanent deletion

## High-impact but risky targets
- `/var/lib/docker`
- old tool installations under `/root/.local/share` if still referenced by active commands
- model files, browser binaries, or crawlers the user actively uses

## WSL / Ubuntu notes
- Stay on Linux filesystem only.
- Exclude `/mnt` entirely.
- Prefer reclaiming caches/logs before removing installed tools.
