---
name: sngs-helper
description: Search source code with the sngs sparse n-gram index. Use for fast literal or regex searches, repeated repository searches, machine-readable code-search results, index initialization, incremental Git updates, and search diagnostics.
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - sngs
    envVars:
      - name: SNGS_SYNC_TTL_SECS
        required: false
        description: Override the dirty-scan cache TTL; 0 disables the cache.
      - name: SNGS_NO_STATS
        required: false
        description: Disable local usage statistics when set.
    homepage: https://github.com/nano-harness/sparse-ngram-search
---

# sngs-helper

`sngs` builds a sparse n-gram inverted index for fast literal and regex search without rescanning every file. Use it for symbols, strings, configuration values, error messages, and repeated searches in a repository.

If `sngs` cannot find content that should exist, use `rg` as a fallback and report the discrepancy rather than assuming the content is absent.

## Install from source

Requires Rust 1.75 or newer:

```bash
git clone https://github.com/nano-harness/sparse-ngram-search.git
cd sparse-ngram-search
cargo build -p sngs --release
mkdir -p ~/.local/bin
install -m 755 ./target/release/sngs ~/.local/bin/sngs
```

Ensure `~/.local/bin` is on `PATH`, then run `sngs doctor` when diagnosing an existing installation.

## Default search workflow

1. Search with automatic index creation:

   ```bash
   sngs search --auto-init --json "ConnectionPool"
   ```

2. Use the smallest useful output format:
   - Files only: `sngs search -l "TODO"`
   - Match counts: `sngs search -c "unsafe"`
   - Grep-style lines and context: `sngs search --grep -C 2 "TODO"`
   - JSON for tools and agents: `sngs search --json "ConnectionPool"`

3. Add filters to reduce irrelevant results:

   ```bash
   sngs search --grep --glob "src/*" --exclude "*/tests/*" --type rs "ConnectionPool"
   ```

4. After changes, run `sngs sync` when the next search must observe them immediately.

## Commands

| Goal | Command |
|---|---|
| Build an index | `sngs init --path <repo>` |
| Search a literal | `sngs search "fn parse_header"` |
| Search a regex | `sngs search -e "impl\\s+Display"` |
| Limit results | `sngs search -n 20 "unsafe"` |
| Auto-build a missing index | `sngs search --auto-init "ConnectionPool"` |
| Update an index | `sngs sync --path <repo>` |
| Inspect index metadata | `sngs status --path <repo>` |
| Force a full rebuild | `sngs rebuild --path <repo>` |
| Diagnose setup and index health | `sngs doctor --path <repo>` |
| Warm the OS page cache | `sngs warmup --path <repo>` |
| Explain the current index | `sngs explain-index --path <repo>` |
| Generate completions | `sngs completion zsh` |

Global options include `--timeout <seconds>` for bounded searches and `--index-dir <dir>` for external or read-only-repository index storage.

## Freshness and platform behavior

- Git repositories use a base index plus an in-memory overlay for changed files.
- Dirty-worktree scans are cached for an adaptive TTL capped at 30 seconds. A file that changes after the cached scan may be missed temporarily.
- `sngs sync` forces a full freshness scan. Set `SNGS_SYNC_TTL_SECS=0` to disable the dirty-scan cache.
- Non-Git directories currently perform a full rebuild on `sync`.
- `--no-ignore` currently has no effect in Git repositories and produces a warning; use it only for non-Git directories.
- Search exit codes follow ripgrep: `0` means matches, `1` means no matches, and `2` means an error.

## Local state and privacy

Indexes are stored in `.sngi-store/` by default, or under the directory supplied with `--index-dir`. Usage statistics are local, not required for search, and can be disabled with `SNGS_NO_STATS=1`.

For read-only analysis or workspaces that must stay unchanged, select an index
directory outside the workspace before the first search, for example
`sngs --index-dir "$HOME/.cache/sngs" search --json "ConnectionPool"`.
Alternatively, set `SNGS_INDEX_DIR` to that external directory. Use the same
location for later commands. External indexing leaves `.gitignore` untouched;
the default in-workspace initialization adds a `.sngi-store/` ignore entry in
Git repositories. Git searches initialize a missing index even without
`--auto-init`.

Do not publish indexes, search output, or local statistics when they reveal private source code or sensitive paths.

## Agent guidelines

- Prefer `--json` for programmatic processing and `--grep` for human-readable context.
- Report whether a search used a fresh sync or could have observed the dirty-scan cache.
- Distinguish exit code `1` from an execution error.
- Never claim that no match proves a symbol does not exist; stale indexes and ignored files can hide matches.
