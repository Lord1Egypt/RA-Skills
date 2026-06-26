---
name: disk-hygiene
description: macOS disk cleanup, cache pruning, stale file detection, and Downloads triage. TRIGGERS - disk space, cleanup, disk usage
allowed-tools: Read, Bash, Write, Glob, Grep, AskUserQuestion
---

# Disk Hygiene

> Audit disk usage, clean developer caches, find forgotten large files, and triage Downloads on macOS.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When to Use This Skill

Use this skill when:

- User asks about disk space, storage, or cleanup
- System is running low on free space
- User wants to find old/forgotten large files
- User wants to clean developer caches (brew, uv, pip, npm, cargo)
- User wants to triage their Downloads folder
- User asks about disk analysis tools (dust, dua, gdu, ncdu)

## TodoWrite Task Templates

### Template A - Full Disk Audit

```
1. Run disk overview (df -h / and major directories)
2. Audit developer caches (uv, brew, pip, npm, cargo, rustup, Docker)
3. Scan for forgotten large files (>50MB, not accessed in 180+ days)
4. Present findings with AskUserQuestion for cleanup choices
5. Execute selected cleanups
6. Report space reclaimed
```

### Template B - Cache Cleanup Only

```
1. Measure current cache sizes
2. Run safe cache cleanups (brew, uv, pip, npm)
3. Report space reclaimed
```

### Template C - Downloads Triage

```
1. List Downloads contents with dates and sizes
2. Categorize into groups (media, dev artifacts, personal docs, misc)
3. Present AskUserQuestion multi-select for deletion/move
4. Execute selected actions
```

### Template D - Forgotten File Hunt

```
1. Scan home directory for large files not accessed in 180+ days
2. Group by location and type (media, ISOs, dev artifacts, documents)
3. Present findings sorted by size
4. Offer cleanup options via AskUserQuestion
```

---

## Phase 1 - Disk Overview

Get the lay of the land before diving into specifics.

```bash
/usr/bin/env bash << 'OVERVIEW_EOF'
echo "=== Disk Overview ==="
df -h /

echo ""
echo "=== Major Directories ==="
du -sh ~/Library/Caches ~/Library/Logs ~/Library/Application\ Support \
  ~/.Trash ~/Downloads ~/Documents ~/Desktop ~/Movies ~/Music ~/Pictures \
  2>/dev/null | sort -rh

echo ""
echo "=== Developer Tool Caches ==="
du -sh ~/.docker ~/.npm ~/.cargo ~/.rustup ~/.local ~/.cache \
  ~/.conda ~/.pyenv ~/.local/share/mise 2>/dev/null | sort -rh
OVERVIEW_EOF
```

## Phase 2 - Cache Audit & Cleanup

### Cache Size Reference

| Cache       | Location                                         | Typical Size  | Clean Command                                                           |
| ----------- | ------------------------------------------------ | ------------- | ----------------------------------------------------------------------- |
| uv          | `~/Library/Caches/uv/`                           | 5-15 GB       | `uv cache clean`                                                        |
| Homebrew    | `~/Library/Caches/Homebrew/`                     | 3-10 GB       | `brew cleanup --prune=all`                                              |
| pip         | `~/Library/Caches/pip/`                          | 0.5-2 GB      | `pip cache purge`                                                       |
| npm         | `~/.npm/_cacache/`                               | 0.5-2 GB      | `npm cache clean --force`                                               |
| cargo       | `~/.cargo/registry/cache/`                       | 1-5 GB        | `cargo cache -a` (needs cargo-cache)                                    |
| rustup      | `~/.rustup/toolchains/`                          | 2-10 GB       | `rustup toolchain uninstall <name>` (list with `rustup toolchain list`) |
| mise        | `~/.local/share/mise/installs/<tool>/<version>/` | 0.2-2 GB each | `mise uninstall <tool>@<version>` (list with `mise ls`)                 |
| Docker      | Docker.app                                       | 5-30 GB       | `docker system prune -a`                                                |
| Playwright  | `~/Library/Caches/ms-playwright/`                | 0.5-2 GB      | `npx playwright uninstall`                                              |
| sccache     | `~/Library/Caches/Mozilla.sccache/`              | 1-3 GB        | `rm -rf ~/Library/Caches/Mozilla.sccache`                               |
| go-build    | `~/Library/Caches/go-build/`                     | 5-25 GB       | `go clean -cache` (or `rm -rf` if `go` not on PATH)                     |
| huggingface | `~/.cache/huggingface/`                          | 1-10 GB       | `rm -rf ~/.cache/huggingface/hub/<model>`                               |

### Safe Cleanup Commands (Always Re-downloadable)

```bash
/usr/bin/env bash << 'CACHE_CLEAN_EOF'
set -euo pipefail

echo "=== Measuring current cache sizes ==="
echo "uv:       $(du -sh ~/Library/Caches/uv/ 2>/dev/null | cut -f1 || echo 'N/A')"
echo "Homebrew: $(du -sh ~/Library/Caches/Homebrew/ 2>/dev/null | cut -f1 || echo 'N/A')"
echo "pip:      $(du -sh ~/Library/Caches/pip/ 2>/dev/null | cut -f1 || echo 'N/A')"
echo "npm:      $(du -sh ~/.npm/_cacache/ 2>/dev/null | cut -f1 || echo 'N/A')"

echo ""
echo "=== Cleaning ==="
brew cleanup --prune=all 2>&1 | tail -3
uv cache clean --force 2>&1
pip cache purge 2>&1
npm cache clean --force 2>&1
CACHE_CLEAN_EOF
```

### Troubleshooting Cache Cleanup

| Issue                               | Cause                      | Solution                                  |
| ----------------------------------- | -------------------------- | ----------------------------------------- |
| `uv cache` lock held                | Another uv process running | Use `uv cache clean --force`              |
| `brew cleanup` skips formulae       | Linked but not latest      | Safe to ignore, or `brew reinstall <pkg>` |
| `pip cache purge` permission denied | System pip vs user pip     | Use `python -m pip cache purge`           |
| Docker not running                  | Docker Desktop not started | Start Docker.app first, or skip           |

## Phase 3 - Forgotten File Detection

Find large files that have not been accessed in 180+ days.

```bash
/usr/bin/env bash << 'STALE_EOF'
echo "=== Large forgotten files (>50MB, untouched 180+ days) ==="
echo ""

# Scan home directory (excluding Library, node_modules, .git, hidden dirs)
find "$HOME" -maxdepth 4 \
  -not -path '*/\.*' \
  -not -path '*/Library/*' \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  -type f -atime +180 -size +50M 2>/dev/null | \
while read -r f; do
  mod_date=$(stat -f '%Sm' -t '%Y-%m-%d' "$f" 2>/dev/null)
  size=$(du -sh "$f" 2>/dev/null | cut -f1)
  echo "${mod_date} ${size} ${f}"
done | sort

echo ""
echo "=== Documents & Desktop (>10MB, untouched 180+ days) ==="
find "$HOME/Documents" "$HOME/Desktop" \
  -type f -atime +180 -size +10M 2>/dev/null | \
while read -r f; do
  mod_date=$(stat -f '%Sm' -t '%Y-%m-%d' "$f" 2>/dev/null)
  size=$(du -sh "$f" 2>/dev/null | cut -f1)
  echo "${mod_date} ${size} ${f}"
done | sort
STALE_EOF
```

### Common Forgotten File Types

| Type                  | Typical Location                                                 | Example                                                                                                                                                                 |
| --------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Windows/Linux ISOs    | Documents, Downloads                                             | `.iso` files from VM setup                                                                                                                                              |
| CapCut/iMovie exports | Movies/                                                          | Large `.mp4` renders                                                                                                                                                    |
| Phone video transfers | Pictures/, DCIM/                                                 | `.MOV` files from iPhone                                                                                                                                                |
| Old Zoom recordings   | Documents/                                                       | `.aac`, `.mp4` from meetings                                                                                                                                            |
| Orphaned downloads    | Documents/                                                       | `CFNetworkDownload_*.mp4`                                                                                                                                               |
| Screen recordings     | Documents/, Desktop/                                             | Capto/QuickTime `.mov`                                                                                                                                                  |
| TTS debug WAV         | `~/.local/share/tts-debug-wav/`, `~/.local/share/kokoro-debug*/` | Debug-mode TTS audio captures — can grow 1-2 GB/day if debug mode left on. Look for a `tts-prune` mise task in your repos or set tighter retention in the pruner script |

## Phase 4 - Downloads Triage

Use AskUserQuestion with multi-select to let the user choose what to clean.

### Workflow

1. List all files in `~/Downloads` with dates and sizes
2. Categorize into logical groups
3. Present AskUserQuestion with categories as multi-select options
4. Offer personal/sensitive PDFs separately (keep, move to Documents, or delete)
5. Execute selected actions

### Categorization Pattern

```bash
/usr/bin/env bash << 'DL_LIST_EOF'
echo "=== Downloads by date and size ==="
find "$HOME/Downloads" -maxdepth 1 \( -type f -o -type d \) ! -path "$HOME/Downloads" | \
while read -r f; do
  mod_date=$(stat -f '%Sm' -t '%Y-%m-%d' "$f" 2>/dev/null)
  size=$(du -sh "$f" 2>/dev/null | cut -f1)
  echo "${mod_date} ${size} $(basename "$f")"
done | sort
DL_LIST_EOF
```

### AskUserQuestion Template

When presenting Downloads cleanup options, use this pattern:

- **Question 1** (multiSelect: true) - "Which items in ~/Downloads do you want to delete?"
  - Group by type: movie files (with total size), old PDFs/docs, dev artifacts, app exports
- **Question 2** (multiSelect: false) - "What about personal/sensitive PDFs?"
  - Options: Keep all, Move to Documents, Delete (already have copies)
- **Question 3** (multiSelect: false) - "Ongoing cleanup tool preference?"
  - Options: dust + dua-cli, Hazel automation, custom launchd script

## Disk Analysis Tools Reference

### Comparison (Benchmarked on ~632GB home directory, Apple Silicon)

| Tool        | Wall Time | CPU Usage            | Interactive Delete       | Install                |
| ----------- | --------- | -------------------- | ------------------------ | ---------------------- |
| **dust**    | **20.4s** | 637% (parallel)      | No (view only)           | `brew install dust`    |
| **gdu-go**  | 28.8s     | 845% (very parallel) | Yes (TUI)                | `brew install gdu`     |
| **dua-cli** | 37.1s     | 237% (moderate)      | Yes (staged safe delete) | `brew install dua-cli` |
| **ncdu**    | 96.6s     | 43% (single-thread)  | Yes (TUI)                | `brew install ncdu`    |

### Recommended Combo

- **`dust`** for quick "where is my space going?" - fastest scanner, tree output
- **`dua i`** or **`gdu-go`** for interactive exploration with deletion

### Quick Usage

```bash
# dust - instant tree overview
dust -d 2 ~              # depth 2
dust -r ~/Library         # reverse sort (smallest first)

# dua - interactive TUI with safe deletion
dua i ~                   # navigate, mark, delete with confirmation

# gdu-go - ncdu-like TUI, fast on SSDs
gdu-go ~                  # full TUI with delete support
gdu-go -n ~              # non-interactive (for scripting/benchmarks)
```

### Install All Tools

```bash
brew install dust dua-cli gdu
```

**Note**: gdu installs as `gdu-go` to avoid conflict with coreutils.

## Quick Wins Summary

Ordered by typical space reclaimed (highest first):

| Action                          | Typical Savings | Risk                                | Command                                                          |
| ------------------------------- | --------------- | ----------------------------------- | ---------------------------------------------------------------- |
| `go clean -cache`               | 5-25 GB         | None (re-downloads)                 | `go clean -cache`                                                |
| `uv cache clean`                | 5-15 GB         | None (re-downloads)                 | `uv cache clean --force`                                         |
| `brew cleanup --prune=all`      | 3-10 GB         | None (re-downloads)                 | `brew cleanup --prune=all`                                       |
| Delete movie files in Downloads | 2-10 GB         | Check first                         | Manual after AskUserQuestion                                     |
| Prune old rustup toolchains     | 2-5 GB          | Keep current                        | `rustup toolchain list` then `rustup toolchain uninstall <name>` |
| Prune stale mise toolchains     | 0.5-3 GB        | Cross-check `.mise.toml` pins first | `mise ls`, then `mise uninstall <tool>@<version>`                |
| `npm cache clean --force`       | 0.5-2 GB        | None (re-downloads)                 | `npm cache clean --force`                                        |
| `pip cache purge`               | 0.5-2 GB        | None (re-downloads)                 | `pip cache purge`                                                |
| Docker system prune             | 5-30 GB         | Removes stopped containers          | `docker system prune -a`                                         |
| Empty Trash                     | Variable        | Irreversible                        | `rm -rf ~/.Trash/*`                                              |

## Post-Change Checklist

After modifying this skill:

1. [ ] Cache commands tested on macOS (Apple Silicon)
2. [ ] Benchmark data still current (re-run if tools updated)
3. [ ] AskUserQuestion patterns match current tool API
4. [ ] All bash blocks use `/usr/bin/env bash << 'EOF'` wrapper
5. [ ] No hardcoded user paths (use `$HOME`)
6. [ ] Append changes to [evolution-log.md](./references/evolution-log.md)

## Troubleshooting

| Issue                                                                      | Cause                                                                                                                                  | Solution                                                                                                                                                                                                                                           |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `uv cache clean` hangs                                                     | Lock held by running uv                                                                                                                | Use `--force` flag                                                                                                                                                                                                                                 |
| `brew cleanup` frees 0 bytes                                               | Already clean or formulae linked                                                                                                       | Run `brew cleanup --prune=all`                                                                                                                                                                                                                     |
| `find` reports permission denied                                           | System Integrity Protection                                                                                                            | Add `2>/dev/null` to suppress                                                                                                                                                                                                                      |
| `gdu` command not found                                                    | Installed as `gdu-go`                                                                                                                  | Use `gdu-go` (coreutils conflict)                                                                                                                                                                                                                  |
| `dust` shows different size than `df`                                      | Counting method differs                                                                                                                | Normal - `df` includes filesystem overhead                                                                                                                                                                                                         |
| Stale file scan is slow                                                    | Deep directory tree                                                                                                                    | Limit `-maxdepth` or exclude more paths                                                                                                                                                                                                            |
| Docker not accessible                                                      | Desktop app not running                                                                                                                | Start Docker.app or skip Docker cleanup                                                                                                                                                                                                            |
| `parse error near TASK_ID=$(pueue add ...)` from heredoc with spaced paths | A user shell hook (e.g. pueue submission) re-parses the command string and breaks on `${var}/Path With Spaces/*` globs inside heredocs | Write multi-line scripts to `/tmp/<name>.sh` first via Write tool, then invoke as `bash /tmp/<name>.sh` — bypasses the inline heredoc → hook re-quote path entirely                                                                                |
| Removing a mise toolchain triggers immediate auto-reinstall                | A project's `.mise.toml` pins the version you just removed; mise restores it on next invocation from that project                      | Before `mise uninstall <tool>@<version>`, grep all reachable `.mise.toml` and `mise.toml` files for the version. If pinned, leave it alone or update the pin first. Same applies to rustup toolchains vs. `rust-toolchain.toml` files in projects. |

### Hook-safe multi-line scripts

If the user's shell environment has bash hooks that intercept tool calls (pueue, asciinema, etc.) and the heredoc pattern fails with cryptic parse errors, write the script to a temp file and invoke it:

```bash
# Instead of: bash << 'EOF'  ... EOF
# Use: Write tool → /tmp/<task>.sh, then:
bash /tmp/<task>.sh
```

Single-line bash invocations like `du -sh "$HOME/Library/Application Support"/Google/* 2>/dev/null | sort -rh | head` work fine even with hooks installed — only multi-line heredocs containing spaced-path globs are problematic.

## Post-Execution Reflection

After this skill completes, reflect before closing the task:

0. **Locate yourself.** — Find this SKILL.md's canonical path before editing.
1. **What failed?** — Fix the instruction that caused it.
2. **What worked better than expected?** — Promote to recommended practice.
3. **What drifted?** — Fix any script, reference, or dependency that no longer matches reality.
4. **Log it.** — Evolution-log entry with trigger, fix, and evidence.

Do NOT defer. The next invocation inherits whatever you leave behind.
