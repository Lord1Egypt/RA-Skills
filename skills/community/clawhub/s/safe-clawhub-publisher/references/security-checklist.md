# Release security checklist

Apply this checklist before any ClawHub dry-run or publication.

## Blockers

- Credentials, private keys, seed phrases, session cookies, `.env` contents, auth configuration, or signed download URLs.
- File or directory symlinks that resolve outside the package root, broken symlinks, device files, sockets, FIFOs, or unexpected executables.
- Missing files referenced by instructions or manifests.
- Unreviewed lifecycle scripts, shell interpolation of metadata, or commands that download and execute mutable code.
- A target owner/slug, account, package type, or version that cannot be established from evidence.

## Review explicitly

- Hidden files, ignore rules, archives and their members, source maps, lockfiles, generated output, fixtures, and test snapshots.
- Token-like strings even when they appear fake; determine whether they are examples or live values without printing them.
- Network endpoints, telemetry, subprocess execution, filesystem writes, native modules, and requested host permissions.
- Personal paths, usernames, internal hostnames, repository remotes, and proprietary source accidentally included in reports or artifacts.
- Dependency sources outside the expected registry and mutable Git dependencies.
- Differences between the validator's publish file list or fingerprint and the ClawHub dry-run result.
- Executable bits, native binaries, archive links/path traversal, and compressed content that exceeds review limits when unpacked.

## Command safety

- Pass metadata as quoted arguments or an argument array, never as evaluated shell source.
- Prefer a known installed `clawhub` binary. Record its version.
- Keep tokens in supported credential stores or masked CI secrets. Never use `set -x` around authentication or publication.
- Dry-run first, then require a fresh confirmation for the exact mutating command.
- After confirmation, repeat local validation, dry-run, account verification, and remote version inspection. Abort when the file set, fingerprint, account, target, version, tags, or remote baseline changed.
- After an ambiguous network failure, inspect the remote version before retrying.

The bundled validator is deliberately conservative and incomplete. A clean result does not certify the package as safe.
