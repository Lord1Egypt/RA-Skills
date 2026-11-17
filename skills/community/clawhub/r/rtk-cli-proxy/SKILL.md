---
name: rtk
description: Run shell/dev commands through the rtk CLI proxy so verbose output (ls, tree, git, gh, grep, logs, JSON, docker, tests) is compacted before it reaches the model context. Use when a command would produce long output or during exploration of large repos.
---

# rtk — output-compacting CLI proxy

rtk wraps normal commands and returns token-optimized output instead of raw text.
Binary: `/usr/local/bin/rtk` (built from source on this host; see Restore).

Check availability first: `rtk --version` (expected 0.49.x).

## When to use

- Exploring a repo or directory: prefer `rtk ls`, `rtk tree`, `rtk find`
- Reading long files: `rtk read <file>`
- Git/CI noise: `rtk git status|log|diff`, `rtk gh pr list`
- Big logs or test runs: `rtk test <cmd>`, `rtk err <cmd>`, `rtk log <file>`
- JSON dumps: `rtk json <file>` (`--keys-only` for shape only)
- Package/dependency listing: `rtk deps`, `rtk env`

Do NOT use it when exact byte-level output matters (diff patches to apply, checksums,
signatures, secrets, machine-parsed files). Call the native command instead.

## Common patterns

```sh
rtk ls /path                 # compact listing
rtk tree /path               # directory tree
rtk read /path/file.py       # filtered read
rtk git status               # short status
rtk git log -n 10            # compact log
rtk grep "pattern" src/      # grouped/truncated matches
rtk find . -name '*.ts'      # compact find tree
rtk test "npm test"          # failures only
rtk err "make build"         # errors/warnings only
rtk summary "some command"   # heuristic 1-2 line summary
```

`rtk <cmd> --help` lists flags per subcommand.

## Restore after an add-on rebuild

The binary lives in the container filesystem, so a rebuild removes it. Backups:
`/config/clawd/bin/rtk` (copy of the working binary).

1. Try the backup first: `cp /config/clawd/bin/rtk /usr/local/bin/rtk && chmod 755 /usr/local/bin/rtk`
2. If missing, rebuild from source (prebuilt ARM64 releases need GLIBC 2.39; this host is Debian 12 / 2.36, so they fail):

```sh
export CARGO_HOME=/config/.cargo RUSTUP_HOME=/config/.rustup
export PATH="$CARGO_HOME/bin:$PATH"
[ -x "$CARGO_HOME/bin/cargo" ] || { curl -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal; }
git clone --depth 1 --branch develop https://github.com/rtk-ai/rtk.git /tmp/rtk-src
cd /tmp/rtk-src && cargo build --release     # ~40 min on this box
cp target/release/rtk /usr/local/bin/rtk && cp target/release/rtk /config/clawd/bin/rtk
```

Build takes ~45 min on the HA host (rustup download is the slow part).

## Notes

- Repo: https://github.com/rtk-ai/rtk (Rust, MIT-ish licenses in repo)
- Version built here: 0.49.0
- Never pipe secrets or tokens through rtk; it summarizes text.
