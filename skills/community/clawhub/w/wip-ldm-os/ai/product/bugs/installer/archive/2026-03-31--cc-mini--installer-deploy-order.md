# Bug: Installer deploy order causes build failures

**Date:** 2026-03-31
**Filed by:** cc-mini
**Priority:** high
**GitHub issue:** wipcomputer/wip-ldm-os#257

## What broke

In `lib/deploy.mjs`, the `runBuildIfNeeded()` function runs `resolveLocalDeps()` BEFORE `npm install`. This is backwards.

The sequence was:
1. `resolveLocalDeps(repoPath)` ... creates symlinks in `node_modules/` for `file:` deps
2. `npm install` ... installs everything, but overwrites or removes the symlinks from step 1
3. `npm run build` ... fails because the symlinks are gone and `file:` paths don't resolve

The result: `tsup` (a devDependency) may not get installed properly, and `dream-weaver-protocol` (a `file:` dep) doesn't resolve. Build fails with "tsup: command not found" or missing module errors.

## Why tests didn't catch it

There are no installer tests. The installer is tested manually. Ticket #245 tracks adding test coverage, but it hasn't been done yet. There's no CI that runs the installer against a fresh clone with `file:` dependencies.

## Why dry-run didn't catch it

Dry-run skips all build steps entirely. It checks whether a build *would* run, but never executes `npm install`, `resolveLocalDeps`, or `npm run build`. The ordering bug is invisible in dry-run mode because the code path that contains the bug is never entered.

## The fix

Swap the order inside `runBuildIfNeeded()`:

1. First: `npm install` (installs devDependencies like tsup; may warn about unresolvable `file:` deps but still installs everything else)
2. Second: `resolveLocalDeps(repoPath)` (re-creates symlinks for `file:` deps AFTER npm is done touching `node_modules/`)
3. Third: `npm run build`

This works because:
- `npm install` with a `file:` dep pointing to a nonexistent path warns but doesn't fail. It installs all other deps (including tsup).
- `resolveLocalDeps` then creates the symlinks that `npm install` couldn't resolve.
- By running after npm, the symlinks survive. npm isn't going to touch `node_modules/` again.

## Three questions Parker asked, honest answers

**Q: Why was the order wrong in the first place?**
A: PR #272 added `resolveLocalDeps` to fix the `file:` dependency problem. The thinking was "resolve deps first so npm install sees them." That logic makes sense in isolation, but ignores that npm install rewrites `node_modules/` and can clobber the symlinks. The PR was correct about the problem but wrong about the solution ordering.

**Q: Could npm install --ignore-scripts be safer here?**
A: It's an option, but unnecessary. Regular `npm install` already handles this case. When it encounters a `file:` dep pointing to a nonexistent path, it warns but still installs everything else. Adding `--ignore-scripts` would prevent postinstall scripts from running, which could break other packages that depend on them. The simpler fix is just: let npm do its thing, then fix up what it couldn't resolve.

**Q: How do we prevent this class of bug going forward?**
A: Installer tests (ticket #245). Specifically: a test that clones memory-crystal to a temp dir (no sibling repos), runs `runBuildIfNeeded()`, and verifies that both tsup and dream-weaver-protocol resolve before `npm run build` executes. Until that test exists, ordering bugs in the build pipeline are invisible until someone hits them in production.

## Files changed

- `lib/deploy.mjs`: Swapped `resolveLocalDeps()` to run AFTER `npm install` instead of before.
