# LDM OS v0.4.3

`ldm install` actually works as an updater now.

## The fix

Before: `ldm install` (bare) only re-copied from saved source paths. Most were dead `/tmp/` clones. If Memory Crystal shipped v0.7.25, you'd never know. The dry-run lied ("18 would refresh" when they were stale copies).

After: `ldm install` checks npm for each extension via catalog.json. Shows real version diffs in dry-run. Installs from GitHub when a newer version exists.

```
  Would update 3 extension(s) from npm:
    memory-crystal: v0.7.24 -> v0.7.25 (@wipcomputer/memory-crystal)
    wip-xai-grok: v1.0.2 -> v1.0.3 (@wipcomputer/wip-xai-grok)
    wip-xai-x: v1.0.3 -> v1.0.4 (@wipcomputer/wip-xai-x)
```

Also includes: /tmp/ registry cleanup (#54), skills TECHNICAL.md merged into universal-installer, README link fixes, co-author fix for deploy-public.sh.

## Issues closed

- Closes #55 (ldm install checks npm for updates)
- Closes #54 (/tmp/ registry cleanup)
