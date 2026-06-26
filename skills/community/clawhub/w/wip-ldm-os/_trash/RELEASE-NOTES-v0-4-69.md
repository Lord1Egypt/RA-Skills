# Release Notes: wip-ldm-os v0.4.69

Closes #257

## Fix installer deploy order for repos with file: dependencies

The installer ran `resolveLocalDeps()` before `npm install`. This meant the symlink for dream-weaver-protocol was created, then `npm install` ran and either removed it or failed trying to resolve the `file:` reference. The build tool (tsup) never got installed because `npm install` was disrupted by the unresolvable `file:` dep.

The fix: `npm install` runs first (installs devDependencies like tsup), then `resolveLocalDeps()` runs second (re-creates symlinks for `file:` deps after npm is done touching node_modules), then `npm run build` runs third.

This was caught during a live `ldm install` where memory-crystal failed with "tsup: command not found" despite the dependency resolution fix from v0.4.68 correctly linking dream-weaver-protocol. The link was created but npm install overwrote it.
