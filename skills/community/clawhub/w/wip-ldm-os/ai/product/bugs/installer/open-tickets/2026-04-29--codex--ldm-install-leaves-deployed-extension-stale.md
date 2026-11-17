# Bug: `ldm install` can leave deployed extension module stale after npm install

Status: Closed
Owner: Codex
Target: `ldm install` / universal installer
Reported: 2026-04-29
Fixed: 2026-04-29 in `@wipcomputer/wip-ldm-os@0.4.85-alpha.2`

## Summary

`ldm install --yes @wipcomputer/wip-branch-guard@1.9.90` installed the npm CLI package at `1.9.90`, but the deployed LDM extension module under `~/.ldm/extensions/wip-branch-guard/` remained at `1.9.89`.

This is the same stale-deployed-extension shape that made `wip-branch-guard@1.9.89` appear installed while the runtime module was still older. The guard fix was present in the global CLI, but the hook runtime would still execute the stale deployed extension until the files were copied manually.

2026-04-29 fix note: the root cause is that npm-packed packages extract into a generic `package/` directory. `installSingleTool()` derived the correct tool name from `package.json`, but the Claude Code hook deploy path recomputed it from `basename(repoPath)`, so `guard.mjs` could be copied to `~/.ldm/extensions/package/` while `~/.ldm/extensions/wip-branch-guard/` stayed stale. PR #751 fixed the hook deploy path to pass the package-derived tool name through, and `0.4.85-alpha.2` published the fix.

## Evidence

Commands run after publishing `@wipcomputer/wip-branch-guard@1.9.90`:

```bash
ldm install --yes @wipcomputer/wip-branch-guard@1.9.90
wip-branch-guard --version
node /Users/lesa/.ldm/extensions/wip-branch-guard/guard.mjs --version
node -p "require('/Users/lesa/.ldm/extensions/wip-branch-guard/package.json').version"
```

Observed result:

```text
wip-branch-guard --version                                      -> 1.9.90
~/.ldm/extensions/wip-branch-guard/guard.mjs --version           -> 1.9.89
~/.ldm/extensions/wip-branch-guard/package.json version           -> 1.9.89
```

Manual deployment of the global npm package files fixed the local runtime:

```bash
install -m 755 /opt/homebrew/lib/node_modules/@wipcomputer/wip-branch-guard/guard.mjs /Users/lesa/.ldm/extensions/wip-branch-guard/guard.mjs
install -m 755 /opt/homebrew/lib/node_modules/@wipcomputer/wip-branch-guard/package.json /Users/lesa/.ldm/extensions/wip-branch-guard/package.json
install -m 755 /opt/homebrew/lib/node_modules/@wipcomputer/wip-branch-guard/SKILL.md /Users/lesa/.ldm/extensions/wip-branch-guard/SKILL.md
```

After manual deployment:

```text
wip-branch-guard --version                                      -> 1.9.90
~/.ldm/extensions/wip-branch-guard/guard.mjs --version           -> 1.9.90
~/.ldm/extensions/wip-branch-guard/package.json version           -> 1.9.90
```

## Reproduction

1. Publish or select a package version where the installed global CLI is newer than the deployed extension module.
2. Run `ldm install --yes @wipcomputer/wip-branch-guard@<new-version>`.
3. Compare the global CLI version to the deployed extension module version.

Expected:

```text
wip-branch-guard --version == ~/.ldm/extensions/wip-branch-guard/guard.mjs --version
```

Actual:

```text
wip-branch-guard --version > ~/.ldm/extensions/wip-branch-guard/guard.mjs --version
```

## Related Catalog Issue

During the same release validation, `ldm install --alpha --yes wip-ai-devops-toolbox` and local path attempts resolved through the public toolbox catalog instead of installing the newly published alpha package content. That may be the same root cause or a neighboring bug:

- The requested alpha package was not the source of truth for deployed sub-tools.
- Existing deployed sub-tools could be left stale or redeployed from older catalog metadata.
- The install output looked successful, but the runtime hook version needed separate verification.

## Acceptance Criteria

1. Installing an explicit npm package spec such as `@wipcomputer/wip-branch-guard@1.9.90` deploys the module, package metadata, and skill from that exact resolved package.
2. After install, CLI version and deployed module version match.
3. `ldm install --alpha --yes wip-ai-devops-toolbox` installs from the alpha package or clearly refuses if that form is not supported. It must not silently fall back to stale public catalog content.
4. The installer prints the source package, resolved version, deployed extension path, CLI version, and deployed runtime version side by side for each extension-style interface.
5. A post-install verification step fails the install if the deployed module version does not match the resolved package version or global CLI version.
6. Alpha and beta validation runbooks include the same side-by-side check and treat divergence as a failed validation, even when the CLI reports the expected version.
7. Regression tests cover the stale-extension shape with a newer package replacing an older deployed extension.

## Notes

The manual deployment above was only used to unblock local dogfooding of `wip-branch-guard@1.9.90`. The installer should own this update path.

## Closure Validation

After installing `@wipcomputer/wip-ldm-os@0.4.85-alpha.2`, the package install path was re-run:

```bash
ldm install --yes @wipcomputer/wip-branch-guard@1.9.90
wip-branch-guard --version
node /Users/lesa/.ldm/extensions/wip-branch-guard/guard.mjs --version
node -p "require('/Users/lesa/.ldm/extensions/wip-branch-guard/package.json').version"
```

Observed result:

```text
wip-branch-guard --version                                      -> 1.9.90
~/.ldm/extensions/wip-branch-guard/guard.mjs --version           -> 1.9.90
~/.ldm/extensions/wip-branch-guard/package.json version           -> 1.9.90
```
