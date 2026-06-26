# v1.8.1: Fix CLI install when package name changed

When a tool's npm package gets renamed but the binary name stays the same, `npm install -g` fails with EEXIST. The stale symlink from the old package blocks the new one.

The installer now detects this: if the binary is a symlink pointing to a different package, it removes the stale link and retries. Only affects symlinks, only when the target doesn't match the package being installed.

Found on `wip-license-hook` (renamed from `@wipcomputer/license-hook` to `@wipcomputer/wip-license-hook`).
