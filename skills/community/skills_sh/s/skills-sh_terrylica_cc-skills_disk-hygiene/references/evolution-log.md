# Evolution Log

Reverse chronological - newest on top.

## 2026-05-15 — Three new high-impact cache vectors discovered

**Trigger**: Second disk audit on terryli's MBP found 21GB in `~/Library/Caches/go-build` plus multi-toolchain accumulation in rustup (8.8GB, 6 versions) and mise installs (7GB) — none of which were in the skill's cache reference table. Skill incorrectly listed `cargo cache -a` as the rustup cleanup; the actual command is `rustup toolchain uninstall <name>`. Mise toolchain pruning wasn't documented at all.

**Root cause**: The skill's cache table predates heavy Go and multi-version-Rust usage. It also confuses `cargo` registry caching with `rustup` toolchain installs (they're distinct concerns at different paths).

**Fix**: Added 3 rows to the Cache Size Reference table:

- `go-build` at `~/Library/Caches/go-build/` — typical 5-25GB on active dev machines; clean with `go clean -cache` (or `rm -rf` as fallback if `go` not on PATH)
- `rustup toolchains` at `~/.rustup/toolchains/` — typical 1-2GB per installed version; list with `rustup toolchain list`, remove with `rustup toolchain uninstall <name>` (NOT `rustup toolchain remove` — that's wrong syntax)
- `mise installs` at `~/.local/share/mise/installs/<tool>/<version>/` — typical 200MB-2GB per version; list with `mise ls`, remove with `mise uninstall <tool>@<version>`

**Evidence**: 2026-05-15 audit. Round 2 reclaim breakdown: go-build 21GB, std cache regrowth 8GB (Homebrew 3.8G + uv 2.5G + sccache 1.6G + npm/pre-commit 0.4G), rustup 1.94 + 1.94.1 = 2.7GB, mise python/3.11 + node/20 = 0.6GB. Total 32GB physical reclaim in one pass.

**Two operational learnings worth surfacing**:

1. **`mise uninstall <tool>@<version>` is the correct command**, NOT `mise toolchain uninstall` or any other variant. Verified on mise 2024+.
2. **Always cross-check stale-toolchain candidates against project `.mise.toml` pins before removal.** Example: removing `node@22.21.1` would have triggered an auto-reinstall on next mise invocation from `~/.claude/` because `~/.claude/.mise.toml` pins `node = "22"`. Skipped that removal mid-cleanup based on this check.

**Bonus finding**: `~/.local/share/tts-debug-wav` accumulated to 11GB in 7 days from Kokoro TTS debug captures (~1.4GB/day generation rate). The pruner was working — retention was just generous. Worth surfacing as a separate non-cache "debug-output growth" vector in future audits.

**Action taken**: Updated Cache Size Reference table (3 new rows + corrected rustup row), updated Quick Wins Summary to include go-build, added the project-pin cross-check note to Troubleshooting.

## 2026-05-09 — pueue hook conflict with heredocs containing spaced paths

**Trigger**: Drilldown bash blocks for `~/Library/Application Support/...` failed with `parse error near TASK_ID=$(pueue add ...` and `(eval):X: unmatched '` after the pueue interception hook tried to wrap them.

**Root cause**: When a `Bash` tool call is intercepted by a pueue submission hook, the hook re-parses the command string. Heredocs that contain `${var}/Path With Spaces/*` or backslash-escaped spaces inside variable expansions break the hook's quoting layer, even though the bash itself is well-formed.

**Fix**: For multi-line drilldowns, write the script to `/tmp/<name>.sh` with the `Write` tool, then invoke as `bash /tmp/<name>.sh`. This bypasses the inline heredoc → hook re-quote path entirely. Single-line `du -sh "$VAR"/path/*` style commands still work fine.

**Evidence**: 2026-05-09 disk audit on terryli's MBP — Chrome / Claude / MacWhisper drilldowns failed twice via heredoc, succeeded immediately when scripted via `/tmp/disk-hygiene-scan.sh`. Reclaim totals were unaffected; 40GB freed across both passes (caches 19GB + selected items 20GB physical).

**Action taken**: Added "pueue hook + heredoc with spaced paths" row to Troubleshooting table in SKILL.md, plus a "Hook-safe multi-line scripts" note in Phase 2.

## 2026-02-08 - Initial creation

- Created skill from real disk audit session
- Benchmarked dust (20.4s), gdu (28.8s), dua-cli (37.1s), ncdu (96.6s) on ~632GB home dir
- Documented cache cleanup workflow: uv (10.8GB), brew (9.4GB), pip (837MB), npm (1.1GB) = ~22GB reclaimed
- Added forgotten file detection patterns (ISOs, video exports, old recordings)
- Added Downloads triage workflow with AskUserQuestion multi-select pattern
- Covers 10 cache types: uv, brew, pip, npm, cargo, rustup, Docker, Playwright, sccache, huggingface
