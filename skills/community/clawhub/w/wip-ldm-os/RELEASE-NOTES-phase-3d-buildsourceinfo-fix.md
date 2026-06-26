# Installer: buildSourceInfo no longer walks up into parent git repos (Phase 3d)

## What changed

`lib/deploy.mjs::buildSourceInfo` only consults `git remote get-url origin` when `repoPath` itself has a `.git` entry. Previously it ran the command unconditionally and trusted whatever git returned.

```js
// before
if (!source.repo) {
  try { execSync('git remote ...', { cwd: repoPath }) } catch {}
}

// after
if (!source.repo && existsSync(join(repoPath, '.git'))) {
  try { execSync('git remote ...', { cwd: repoPath }) } catch {}
}
```

## Why

Git walks up the directory tree looking for `.git`. When the installer extracts an npm tarball to `~/.ldm/tmp/npm-<ts>/package/`, that path lives inside the `~/.ldm` working tree. `~/.ldm` is itself a tracked git repo pointing at `wipcomputer/wipcomputer-ldmos-wipcomputerinc-system-private.git`. Git happily returned the parent remote for every npm-sourced extension, and the registry faithfully recorded it.

Result: `~/.ldm/extensions/registry.json` entries for most installed extensions had `source.repo = "wipcomputer/wipcomputer-ldmos-wipcomputerinc-system-private"`, which is the LDM system tracking repo, not the extension's source. The field was quietly wrong.

Phase 3b (stale-entry cleanup on deploy) was written to be path-based precisely because this bug made the source field unreliable. With this fix, future installs record the correct source.repo or nothing, never the parent's remote.

## Scope

- Fixes the capture-the-parent problem for every future install.
- Does NOT rewrite existing registry entries. Old entries carry old values. They are harmless because nothing branches on `source.repo` after Phase 3b's path-based logic landed. Running `ldm install <repo>` on an existing entry will overwrite it with the correct source next time the extension updates.

## Verification

- `node --check lib/deploy.mjs` passes.
- A quick manual trace: extract a tarball to a temp dir outside any git tree, call `buildSourceInfo` with `pkg.repository` missing, confirm `source.repo` is undefined (not filled from an ancestor).

## Tracking

Closes the open question from:
`ai/product/bugs/1password/2026-04-21--cc-mini--mcp-server-missing-from-install.md`

Specifically section 5, question 1 (registry source.repo anomaly) and question 4 (buildSourceInfo accuracy gating Phase 3b). Phase 3b shipped with path-based matching so this fix is a cleanup rather than a prerequisite.
