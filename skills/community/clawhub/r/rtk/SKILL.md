---
name: rtk
description: RTK (Rust Token Kit) - CLI proxy that reduces LLM token consumption by 60-90% on common dev commands. Use rtk to wrap commands like git, ls, cat, grep, test runners, linters, docker, kubectl, and more. Single Rust binary, zero dependencies, minimal overhead. Always prefer rtk wrappers when available for shell commands that produce verbose output.
---

# RTK - Token-Optimized Command Wrapper

RTK filters and compresses command outputs before they reach context. Use it to reduce token consumption by 60-90% on common dev operations.

## Quick Reference

**Core principle:** Prefix supported commands with `rtk` for compressed output.

### Most Common Usage

```bash
# Git operations (80-92% savings)
rtk git status
rtk git diff
rtk git log -n 10
rtk git add .
rtk git commit -m "msg"
rtk git push

# File operations
rtk ls .           # Token-optimized tree
rtk read file.rs   # Smart file reading
rtk grep "pattern" .

# Testing (90% savings on failures)
rtk test cargo test
rtk test npm test
rtk vitest run
rtk playwright test
rtk pytest
rtk go test

# Linting (80-85% savings)
rtk lint           # ESLint grouped by rule
rtk tsc            # TypeScript errors by file
rtk cargo clippy
rtk ruff check
rtk golangci-lint run

# Build tools (75-80% savings)
rtk cargo build
rtk next build
rtk pnpm list

# Container ops (80% savings)
rtk docker ps
rtk docker logs <container>
rtk kubectl get pods
rtk kubectl logs <pod>
```

## When to Use RTK

**Use rtk for:**
- Commands that produce >100 lines of output
- Repeated operations (git status, test runs, lint checks)
- Any command in the supported command list below

**Skip rtk for:**
- Interactive commands (vim, nano)
- Commands already producing minimal output
- Heredocs or pipes (rtk auto-skips these)

## Supported Commands

### Version Control
- `git` - status, diff, log, add, commit, push, pull
- `gh` - pr list/view, issue list, run list

### File Operations
- `ls` - directory listing
- `cat/head/tail` - file reading (rewritten to `rtk read`)
- `rg/grep` - search (rewritten to `rtk grep`)
- `find` - file search

### Testing
- `cargo test`, `npm test`, `vitest`, `jest`, `playwright`, `pytest`, `go test`
- Shows failures only, collapses passing tests

### Linting & Type Checking
- `eslint`, `biome`, `tsc`, `prettier`, `ruff`, `golangci-lint`, `cargo clippy`
- Groups errors by file/rule

### Build Tools
- `cargo build`, `next build`, `prisma generate`
- Removes progress bars, focuses on errors

### Package Management
- `pnpm list`, `pip list`, `npm list`
- Compact dependency trees

### Containers & Orchestration
- `docker ps/images/logs`, `docker compose ps`
- `kubectl get/logs`
- Deduplicated logs, compact lists

### Network & Logs
- `curl` - auto-detects JSON
- `wget` - strips progress bars
- `docker logs`, `kubectl logs` - deduplicates repeated lines

## Output Compression Strategies

RTK applies four strategies per command type:

1. **Smart Filtering** - Removes comments, whitespace, boilerplate
2. **Grouping** - Aggregates similar items (files by dir, errors by type)
3. **Truncation** - Keeps relevant context, cuts redundancy
4. **Deduplication** - Collapses repeated log lines with counts

## Reading Levels

```bash
rtk read file.rs                    # Default: smart filtering
rtk read file.rs -l aggressive      # Signatures only (strips bodies)
rtk smart file.rs                   # 2-line heuristic summary
```

## Error Handling

When a command fails, RTK saves the full unfiltered output:

```
FAILED: 2/15 tests
[full output: ~/.local/share/rtk/tee/1707753600_cargo_test.log]
```

Read the tee log file if you need the complete unfiltered output.

## Token Savings Examples

### Directory Listing
```bash
# Standard ls -la (45 lines, ~800 tokens)
drwxr-xr-x 15 user staff 480 ... my-project/
-rw-r--r-- 1 user staff 1234 ...
...

# rtk ls (12 lines, ~150 tokens)
+-- src/ (8 files)
|   +-- main.rs
+-- Cargo.toml
```

### Git Push
```bash
# Standard git push (15 lines, ~200 tokens)
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
...

# rtk git push (1 line, ~10 tokens)
ok main
```

### Test Failures
```bash
# Standard cargo test (200+ lines on failure)
running 15 tests
test utils::test_parse ... ok
...

# rtk test cargo test (~20 lines)
FAILED: 2/15 tests
test_edge_case: assertion failed
test_overflow: panic at utils.rs:18
```

## Installation Verification

RTK binary should already be installed. Verify:

```bash
rtk --version          # Should show version
rtk gain              # Show token savings stats
```

If not found, the binary needs to be installed in the container.

## Advanced Usage

### Ultra-compact mode
```bash
rtk -u git status     # ASCII icons, inline format
```

### Filtering
```bash
rtk env -f AWS        # Show only AWS env vars
```

### Summary mode
```bash
rtk summary <long-command>  # Heuristic summary for unknown commands
```

### Raw passthrough (with tracking)
```bash
rtk proxy <command>   # Track usage without filtering
```

## Configuration

RTK config file (if needed): `~/.config/rtk/config.toml`

```toml
[tracking]
database_path = "/path/to/custom.db"

[hooks]
exclude_commands = ["curl", "playwright"]  # Skip rewrite

[tee]
enabled = true           # Save raw output on failure
mode = "failures"        # "failures", "always", or "never"
max_files = 20          # Rotation limit
```

## Auto-Rewrite Hook (Optional)

RTK supports auto-rewriting Bash commands via hooks (for Claude Code, OpenCode, Gemini CLI). This is optional and not required for manual usage.

If the hook is installed, commands like `git status` are automatically rewritten to `rtk git status` before execution.

**Not applicable for this deployment** - manual `rtk` prefixing is the expected pattern.

## Analytics

Check token savings:

```bash
rtk gain               # Summary stats
rtk gain --graph       # ASCII graph (last 30 days)
rtk gain --history     # Recent command history
rtk gain --daily       # Day-by-day breakdown
```

## Troubleshooting

**"rtk: command not found"**
- Binary not in PATH or not installed
- Check: `which rtk`

**Output still verbose**
- Command not supported by rtk
- Use `rtk proxy <command>` to track unsupported commands

**Need full output**
- Read tee log file (shown in failure message)
- Or run command without rtk prefix

## Reference

- GitHub: https://github.com/rtk-ai/rtk
- Documentation: https://www.rtk-ai.app
- Troubleshooting: https://github.com/rtk-ai/rtk/blob/master/docs/TROUBLESHOOTING.md