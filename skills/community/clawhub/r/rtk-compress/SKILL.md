---
name: "rtk-compress"
version: "1.15.2"
published: false
description: "Save 60-90% of LLM tokens on shell commands, file reads, and test outputs. Wraps rtk CLI for compressed output."
tags: rtk, token-saving, compression, cli, shell, devtools
---

**Save 60-90% of LLM tokens on shell commands, file reads, and test outputs.**

This skill wraps [rtk (Rust Token Killer)](https://github.com/rtk-ai/rtk) — a CLI proxy that filters and compresses command outputs before they reach your LLM context.

## Install

```bash
# 1. Install rtk
brew install rtk          # macOS
# or: curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh

# 2. Verify
rtk gain  # Should show token savings stats
```

Then copy this `SKILL.md` to your agent's skills directory.

## Commands Reference

### Smart File Operations
```bash
rtk ls .                                # Token-optimized directory tree
rtk read file.rs                         # Smart file reading (compressed output)
rtk read file.rs -l aggressive           # Signatures only (strips bodies)
rtk smart file.rs                      # 2-line heuristic code summary
```

### Search & Diff
```bash
rtk find "*.rs" .                        # Compact find results
rtk grep "pattern" .                    # Grouped search results
rtk diff file1 file2                    # Condensed diff
```

### Git Operations
```bash
rtk git status                         # Compact status
rtk git log -n 10                      # One-line commits
rtk git diff                           # Condensed diff
rtk git add                           # → "ok"
rtk git commit -m "msg"                    # → "ok abc1234"
rtk git push                          # → "ok main"
rtk git pull                           # → "ok 3 files +10 -2"
```

### GitHub CLI
```bash
rtk gh pr list                         # Compact PR listing
rtk gh pr view 42                       # PR details + checks
rtk gh issue list                      # Compact issue listing
rtk gh run list                        # Workflow run status
```

### Test Runners
```bash
rtk test cargo test                    # Show failures only (-90%)
rtk err npm run build                 # Errors/warnings only
rtk vitest run                         # Vitest compact (failures only)
rtk playwright test                   # E2E results (failures only)
rtk pytest                            # Python tests (-90%)
rtk go test                            # Go tests (NDJSON, -90%)
rtk cargo test                        # Cargo tests (-90%)
```

### Build & Lint
```bash
rtk lint                               # ESLint grouped by rule/file
rtk lint biome                         # Supports other linters
rtk tsc                                # TypeScript errors grouped by file
rtk next build                          # Next.js build compact
rtk prettier --check .                 # Files needing formatting
rtk cargo build                        # Cargo build (-80%)
rtk cargo clippy                        # Cargo clippy (-80%)
rtk ruff check                          # Python linting (JSON, -80%)
rtk golangci-lint run                   # Go linting (JSON, -85%)
```

### Package Managers
```bash
rtk pnpm list                          # Compact dependency tree
rtk pip list                           # Python packages (auto-detect uv)
rtk pip outdated                         # Outdated packages
rtk prisma generate                     # Schema generation (no ASCII art)
```

### Containers
```bash
rtk docker ps                           # Compact container list
rtk docker images                       # Compact image list
rtk docker logs <container>                # Deduplicated logs
rtk docker compose ps                   # Compose services
rtk kubectl pods                        # Compact pod list
rtk kubectl logs <pod>                    # Deduplicated logs
rtk kubectl services                     # Compact service list
```

### Data & Analytics
```bash
rtk json config.json                    # Structure without values
rtk deps                                # Dependencies summary
rtk env -f AWS                        # Filtered env vars
rtk log app.log                         # Deduplicated logs
rtk curl <url>                         # Auto-detect JSON + schema
rtk wget <url>                        # Download, strip progress bars
rtk summary <long command>          # Heuristic summary
rtk proxy <command>                     # Raw passthrough + tracking
```

### Token Savings Analytics
```bash
rtk gain                               # Summary stats
rtk gain --graph                       # ASCII graph (last 30 days)
rtk gain --history                     # Recent command history
rtk gain --daily                       # Day-by-day breakdown
rtk gain --all --format json            # JSON export for dashboards
rtk discover                            # Find missed savings opportunities
rtk discover --all --since 7           # All projects, last 7 days
```

## Rules for the Agent

Use `rtk <command>` instead of bare commands whenever possible:

### Always use rtk for:
- `rtk git status` / `rtk git log` / `rtk git diff`
- `rtk ls -la` / `rtk cat <file>`
- `rtk npm test` / `rtk pytest` / `rtk cargo test`
- `rtk npm run build` / `rtk ruff check`

### Don't use rtk for:
- Commands whose output is piped to other tools (e.g., `git log | grep ...`)
- Scripts that parse raw output
- Commands where you need the exact full output

### If rtk fails:
Fall back to the bare command. Never block a task because of compression.

### Check savings:
```bash
rtk gain           # current session
rtk gain --global  # all-time stats
```

## Token Savings Reference

| Operation | Without rtk | With rtk | Savings |
|-----------|------------|----------|---------|
| `git status` | ~300 | ~60 | -80% |
| `git log -20` | ~2,000 | ~400 | -80% |
| `cat file.ts` | ~2,000 | ~600 | -70% |
| `npm test` | ~5,000 | ~500 | -90% |
| `pytest` | ~2,000 | ~200 | -90% |
| **Typical session** | **~150k** | **~45k** | **-70%** |

## Links

- rtk: https://github.com/rtk-ai/rtk
- OpenClaw feature request: https://github.com/openclaw/openclaw/issues/35053
