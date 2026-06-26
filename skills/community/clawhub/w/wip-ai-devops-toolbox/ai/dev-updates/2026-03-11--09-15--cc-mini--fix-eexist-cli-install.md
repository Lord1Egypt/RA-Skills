# Fix CLI install EEXIST when package name changed

**Date:** 2026-03-11 09:15 PST
**Author:** Claude Code (cc-mini)

## Problem

`wip-install` failed to install `wip-license-hook` CLI because a stale symlink existed at `/opt/homebrew/bin/wip-license-hook` from the old package name (`@wipcomputer/license-hook`). The new package name is `@wipcomputer/wip-license-hook`. npm refuses to overwrite a binary created by a different package (EEXIST).

## Fix

In `installCLI()`: when `npm install -g` fails with EEXIST, check each binary. If it's a symlink pointing to a different package, remove it and retry. Only removes symlinks (not regular files), and only if the target doesn't match the package being installed.

## Files changed

- `tools/wip-universal-installer/install.js` ... EEXIST recovery in `installCLI()`

Closes #85
