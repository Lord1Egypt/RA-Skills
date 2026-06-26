# RTK Command Reference

Full list of RTK commands organized by category. Always prefer these over raw commands.

## Files

| Raw command | RTK equivalent | Savings |
|-------------|---------------|---------|
| `ls .` / `tree .` | `rtk ls .` | -80% |
| `cat file` / `head` / `tail` | `rtk read file` | -70% |
| `cat file` (signatures only) | `rtk read file -l aggressive` | -90% |
| `grep "pat" .` / `rg "pat"` | `rtk grep "pat" .` | -80% |
| `find . -name "*.ts"` | `rtk find "*.ts" .` | -80% |
| `diff file1 file2` | `rtk diff file1 file2` | -75% |
| `cat file` (2-line summary) | `rtk smart file` | -95% |

## Git

| Raw command | RTK equivalent | Savings |
|-------------|---------------|---------|
| `git status` | `rtk git status` | -80% |
| `git diff` | `rtk git diff` | -75% |
| `git log -n 10` | `rtk git log -n 10` | -80% |
| `git add .` | `rtk git add .` → "ok" | -92% |
| `git commit -m "msg"` | `rtk git commit -m "msg"` → "ok abc1234" | -92% |
| `git push` | `rtk git push` → "ok main" | -92% |
| `git pull` | `rtk git pull` → "ok 3 files +10 -2" | -90% |
| `git branch` | `rtk git branch` | -80% |
| `git stash list` | `rtk git stash list` | -80% |
| `git show HEAD` | `rtk git show HEAD` | -75% |

## GitHub CLI (gh)

| Raw command | RTK equivalent | Savings |
|-------------|---------------|---------|
| `gh pr list` | `rtk gh pr list` | -80% |
| `gh pr view 42` | `rtk gh pr view 42` | -75% |
| `gh issue list` | `rtk gh issue list` | -80% |
| `gh run list` | `rtk gh run list` | -75% |

## Test Runners

| Raw command | RTK equivalent | Savings |
|-------------|---------------|---------|
| `npm test` | `rtk test npm test` | -90% |
| `npx jest` | `rtk test npx jest` | -90% |
| `npx vitest run` | `rtk vitest run` | -90% |
| `npx playwright test` | `rtk playwright test` | -90% |
| `pytest` | `rtk pytest` | -90% |
| `go test ./...` | `rtk go test ./...` | -90% |
| `cargo test` | `rtk cargo test` | -90% |

> `rtk test <cmd>` — generic wrapper for any test runner (shows failures only)
> `rtk err <cmd>` — generic wrapper for errors/warnings only

## Build & Lint

| Raw command | RTK equivalent | Savings |
|-------------|---------------|---------|
| `npx tsc` / `tsc` | `rtk tsc` | -80% |
| `next build` | `rtk next build` | -80% |
| `npx eslint .` | `rtk lint` | -80% |
| `npx biome check .` | `rtk lint biome` | -80% |
| `npx prettier --check .` | `rtk prettier --check .` | -75% |
| `cargo build` | `rtk cargo build` | -80% |
| `cargo clippy` | `rtk cargo clippy` | -80% |
| `ruff check .` | `rtk ruff check .` | -80% |
| `golangci-lint run` | `rtk golangci-lint run` | -85% |

## Package Managers

| Raw command | RTK equivalent | Savings |
|-------------|---------------|---------|
| `npm install` | `rtk npm install` | -85% |
| `yarn install` | `rtk yarn install` | -85% |
| `pnpm install` | `rtk pnpm install` | -85% |
| `bun install` | `rtk bun install` | -85% |
| `npm run build` | `rtk err npm run build` | -80% |
| `pnpm build` | `rtk err pnpm build` | -80% |

## Docker

| Raw command | RTK equivalent | Savings |
|-------------|---------------|---------|
| `docker ps` | `rtk docker ps` | -80% |
| `docker ps -a` | `rtk docker ps -a` | -80% |
| `docker logs <id>` | `rtk docker logs <id>` | -80% |
| `docker compose ps` | `rtk docker ps` | -80% |

## Generic Wrappers

Use these for commands without a dedicated RTK handler:

```bash
rtk err <any-command>   # Errors and warnings only
rtk test <any-command>  # Test output (failures only)
```

Examples:
```bash
rtk err make build
rtk err gradle build
rtk test mvn test
rtk test dotnet test
```

## React Native / Mobile (most relevant for RN projects)

```bash
# Build output filtering
rtk err npx react-native run-android
rtk err npx react-native run-ios
rtk err expo build

# Metro bundler logs
rtk err npx react-native start

# Tests
rtk test npx jest --watchAll=false

# Type checking
rtk tsc

# Lint
rtk lint                    # ESLint
rtk err npx eslint . --ext .ts,.tsx
```
