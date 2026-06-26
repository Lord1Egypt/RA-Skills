# LDM OS v0.4.4

`ldm install` finally works the way it should.

## npm version checking (per extension)

`ldm install --dry-run` now checks every installed extension against npm using its own package name. Shows real version diffs:

```
  Checking npm for updates...
  Would update 3 extension(s) from npm:
    wip-branch-guard: v1.9.30 -> v1.9.36 (@wipcomputer/wip-branch-guard)
    ldm-install-wip-xai-grok: v1.0.2 -> v1.0.3 (@wipcomputer/wip-xai-grok)
    ldm-install-wip-xai-x: v1.0.1 -> v1.0.4 (@wipcomputer/wip-xai-x)
```

No more relying on local source paths. No more stale `/tmp/` clones. npm is the source of truth. Closes #55.

## Install lockfile

Only one `ldm install` runs at a time. PID-based lock at `~/.ldm/state/.ldm-install.lock`. Stale locks (dead PID) auto-cleaned. Prevents the process swarm that was hitting 310% CPU when multiple sessions ran install simultaneously. Closes #57.

## Issues closed

- Closes #55
- Closes #57
