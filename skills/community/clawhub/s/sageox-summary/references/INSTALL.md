# Installing `ox`

Invoked when `bash scripts/update-ox.sh` exits `2` (no install state
recorded, or `ox` is not on PATH). The deterministic install shell lives
in `scripts/install-ox-curl.sh`; this file covers the user-facing flow
and PATH recovery.

## Install

Invoke the bundled helper. It downloads the `ox` release tarball
directly from GitHub Releases at a tag pinned in the script source,
verifies it against an sha256 checksum embedded in the script, extracts
it into `$HOME/.local/bin`, and records the install state (pinned
release tag, install directory, install timestamp) in
`~/.openclaw/memory/sageox-ox-install.json`. No sudo, no shell-script
piping, no dynamic "latest" resolution.

```bash
bash scripts/install-ox-curl.sh
```

Contract:

- **Args:** none
- **Stdout:** human-readable progress (download URL, checksum
  verification, extract, install dir)
- **Stderr:** errors and PATH-configuration guidance
- **Exit:** `0` success; `3` internal (curl/tar missing, download
  failed, checksum mismatch, unsupported platform, or `ox` not
  runnable after install)

**Do not install `ox` via Homebrew or any package manager** (e.g.
`brew install sageox/tap/ox`, `apt`, `dnf`, `pacman`). The tap exists
for general use but is not supported inside OpenClaw skills — only the
pinned-release curl flow is.

If the script exits non-zero, surface its stderr to the user and stop.
Do not silently retry.

## PATH configuration

`install-ox-curl.sh` installs into `$HOME/.local/bin`. This directory
is not on `PATH` by default on every distro. If the script prints a
warning to stderr that `$HOME/.local/bin` is not on `PATH`, surface its
guidance verbatim and ask the user to add the following line to
`~/.openclaw/.env`:

```sh
PATH=$HOME/.local/bin:$PATH
```

OpenClaw loads `.env` into the skill subprocess, so the updated `PATH`
takes effect on the next invocation. After the user confirms they've
updated the file, re-run the state checker to confirm `ox` is reachable:

```bash
bash scripts/update-ox.sh
```

It should exit `0` with no stderr.

## Upgrading `ox`

The curl flow pins a specific `ox` release by tag and sha256. There is
no per-run auto-update. To pick up a newer release, re-run
`scripts/install-ox-curl.sh` from a version of this skill that pins the
newer release — typically by re-running `clawhub install` for the
skill after a new skill version publishes.
