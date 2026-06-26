# Release Notes: wip-ldm-os v0.4.70

Related: #255, #257

## Fix symlink EEXIST in dependency resolution

When `npm install` runs on a cloned repo with `file:` dependencies, npm creates a broken entry in `node_modules/` for the dependency it can't resolve. Then `resolveLocalDeps()` tries to create a symlink to the installed LDM extension but fails with EEXIST because the broken entry already exists.

The fix: always remove the existing entry before creating the symlink. `rmSync` with `force: true` handles broken symlinks, empty directories, and any other artifact npm left behind. The fresh symlink points to the correct LDM extension.

This completes the dependency resolution chain: npm install (gets devDeps like tsup), resolveLocalDeps (links file: deps from LDM extensions), npm run build (succeeds with all deps available).
