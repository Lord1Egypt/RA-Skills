# PMA Delivery Rules

## Table of Contents

- [Shell And Process Management](#shell-and-process-management)
- [Repository Hygiene](#repository-hygiene)
- [Git Conventions](#git-conventions)
- [Pull Request Workflow](#pull-request-workflow)
- [PR Review Checklist](#pr-review-checklist)
- [CI Pipeline](#ci-pipeline)
- [GitHub Actions Conventions](#github-actions-conventions)
- [Database Migrations](#database-migrations)
- [Tools And Security](#tools-and-security)

## Shell And Process Management

- Prefer `bash` for all command execution. Do not use `zsh` unless explicitly requested.
- When a tool supports explicit shell selection, set it to `bash`.
- Never use `kill $(lsof -ti:PORT)` without `-sTCP:LISTEN`.

### Tmux Persistent Sessions

Always use tmux for dev servers, test servers, and long-running processes.

**Session naming:**

```bash
SESSION=$(basename "$PWD" | tr '.' '-')-$(echo -n "$PWD" | md5sum | cut -c1-6)
```

`tr '.' '-'` is required because tmux session names cannot contain dots.
Worktrees of the same project get distinct names automatically.

**Creating sessions — always use a persistent shell:**

```bash
# WRONG: process exit kills the session
tmux new-session -d -s $SESSION 'bun run dev'

# CORRECT: persistent shell survives process restarts
tmux new-session -d -s $SESSION /bin/bash
tmux send-keys -t $SESSION 'bun run dev' Enter
```

**Before starting:** check for existing sessions first, reuse or restart.

```bash
tmux has-session -t $SESSION 2>/dev/null && echo "exists" || echo "not found"
```

**If session exists:** send keys to restart the process.

```bash
tmux send-keys -t $SESSION C-c
tmux send-keys -t $SESSION 'bun run dev' Enter
```

**If session does not exist:** create with persistent shell.

```bash
tmux new-session -d -s $SESSION /bin/bash
tmux send-keys -t $SESSION 'bun run dev' Enter
```

**Checking output:**

```bash
tmux capture-pane -t $SESSION -p
```

**Stopping:**

```bash
tmux send-keys -t $SESSION C-c
# Or kill the entire session:
tmux kill-session -t $SESSION
```

**Rules:**

- Never kill ports as the first approach — manage process lifecycle through tmux.
- Always check for an existing session before creating a new one.
- One tmux session per service — do not multiplex unrelated services.

## Repository Hygiene

Each PMA-managed repository should establish a baseline set of project-level configuration files before substantive feature work. These describe the project to humans and tooling, and they prevent build artifacts, environment variables, and editor metadata from leaking into git.

### Required (every repo)

| File | Purpose | How to populate |
|---|---|---|
| `.gitignore` | Exclude build artifacts, dependency caches, secrets, IDE/OS files | Start from <https://github.com/github/gitignore> for the stack (`Rust.gitignore`, `Node.gitignore`, `Go.gitignore`), then append global ignores (`Global/macOS.gitignore`, `Global/Linux.gitignore`, `Global/JetBrains.gitignore`, `Global/VisualStudioCode.gitignore`). Always include `.env`, `*.key`, `*.pem`, `*.log`, coverage outputs, and DB dump paths. |
| `.gitattributes` | Normalize line endings, mark binaries, mark generated files | Minimum: `* text=auto eol=lf`. Mark generated/vendored files with `<path> linguist-generated=true` so they do not pollute the language stats and review diff. |
| `.editorconfig` | Editor-agnostic indentation, charset, trailing whitespace | One root file matching the stack's formatter (rustfmt / gofmt / Prettier-equivalent width). |
| `LICENSE` | Make license explicit | OSI identifier (MIT / Apache-2.0 / BSL-1.1 / etc.) with year and copyright holder; commercial-only projects state "All rights reserved" explicitly. Never leave the project unlicensed by accident. |
| `README.md` | Project entry point | What it is, why it exists, quick-start command, the one-line quality-gates command. Update when the quick-start command changes. |
| `.env.example` | Document required environment variables without leaking secrets | Every key consumed by runtime config; placeholder values only. Real `.env` files are git-ignored. |

### Required when applicable

| File | When |
|---|---|
| `docs/changelog.md` | Once the project has releases or shipped behavior changes (Keep a Changelog format). |
| `docs/decisions/` | Once any default has been relaxed (e.g. a Hard Lock exception) or a non-default design decision needs to outlive a PR description. |
| `.github/CODEOWNERS` | Once review ownership is non-trivial (multiple maintainers or teams). |
| `.github/PULL_REQUEST_TEMPLATE.md` | Once the PR Summary / Test plan format below is used consistently. |
| `.github/dependabot.yml` or `renovate.json` | When automated dependency updates are wanted — pairs with `workflow.md` *Dependency Freshness*. Group routine bumps to keep noise low. |
| `SECURITY.md` | Once the project has external users or is internet-exposed. |

### Stack-pinned toolchain files

The runtime / language version must be declared in the project, not assumed:

- Rust: `rust-version` in `[workspace.package]`; optional `rust-toolchain.toml` for pinned channel (vector pattern).
- Node / Bun: `engines.node` and `engines.bun` in `package.json`; `.nvmrc` / `.node-version` when contributors use nvm / fnm / asdf.
- Go: `go` and `toolchain` directives in `go.mod`.

### Anti-patterns

- A `.gitignore` that lists only `node_modules/` while `dist/`, `target/`, `*.log`, coverage outputs, or local DB files leak into commits.
- A committed `.env` containing real secrets — when discovered: rotate the secret first, then scrub history and add `.env` to `.gitignore`.
- `.vscode/settings.json` checked in with personal editor preferences. Check in only project-wide tooling (debugger configs, recommended extensions list); cross-editor formatting goes in `.editorconfig`.
- A `README.md` that documents how the project worked six months ago — treat the quick-start command as a tested artifact.
- `LICENSE` missing or "TBD" — block at PR review.

### Verification

When starting a new repo, or when auditing an existing one, confirm:

- [ ] `.gitignore` covers the stack's build outputs, dependency caches, OS/editor files, and secret-bearing files
- [ ] `.gitattributes` sets `eol=lf` and marks generated files
- [ ] `.editorconfig` matches the stack's formatter
- [ ] `LICENSE` is present and explicit
- [ ] `README.md` documents the current quick-start and quality-gates commands
- [ ] `.env.example` is complete and contains no real secrets
- [ ] Toolchain version is pinned in the stack-native file (Cargo / package.json / go.mod)

If any item is missing on a non-trivial repo, surface it in the Phase 2 proposal as a separate hygiene task rather than fixing it silently inside a feature commit.

## Git Conventions

- Use English for commits, PR titles, PR descriptions, and all remote-visible metadata.
- Do not mention AI assistants, agents, or model names (Claude, Codex, ChatGPT, OpenAI, Anthropic, etc.) in commits, PR text, comments, or any remote-visible content.
- Use conventional commits: `<type>: <description>`.
- Chinese must not appear in code or documentation unless the user explicitly requests it.

## Pull Request Workflow

Before creating or updating a PR:

1. Review the full diff from the branch point.
2. Run code review focused on correctness, regressions, and missing tests.
3. Run a security review.
4. Ensure build passes.
5. Ensure lint passes.
6. Ensure tests pass.

PR body format:

```markdown
## Summary
- ...

## Test plan
- [ ] ...
```

## PR Review Checklist

- all review and security checks pass
- build, lint, and tests pass
- commit history is clean
- task and plan state are synced
- changelog updated if required

## CI Pipeline

Standard stages:

```text
format/lint -> static checks -> build -> test -> security review
```

CI commands come from the active stack skill or existing project scripts.

## GitHub Actions Conventions

- workflows live in `.github/workflows/`
- pin actions to full SHAs
- run on `pull_request` and `push`
- align cache and toolchain setup with the active project stack

## Database Migrations

Migration files are **generated by the project's migration tool, never written or restructured by hand.** Hand-made migrations diverge from the tool's tracked state (checksums / version table / schema snapshot), so the next generated migration errors, emits a corrupt diff, or silently drops changes.

- **Identify the mechanism before any schema change.** The data layer owns it: SQLx (`sqlx migrate add` + checksummed files), SeaORM (`sea-orm-migration`), Diesel (`diesel migration generate`), Drizzle (`drizzle-kit generate`), Prisma (`prisma migrate dev`), Alembic (`alembic revision --autogenerate`), etc. **If an ORM is in use, the ORM's own migration command produces the file — do not bypass it.**
- **Schema source of truth is the model / declared schema, not the SQL files.** Change the model, then let the tool emit the migration. Never create a migration from scratch, copy-and-rename one, or rewrite a generated file's structure.
- **Allowed manual edits, only inside an already-generated file:** operations the generator cannot express (data backfill, `CREATE INDEX CONCURRENTLY`, a custom `down`). After editing, re-run the tool's consistency step (e.g. `cargo sqlx prepare`, `drizzle-kit` snapshot regenerate) so checksums/state stay aligned.
- **Never edit, reorder, or delete a migration already applied to any shared environment.** Forward-fix with a new generated migration.
- **Verify before marking the task done:** run the tool's apply + consistency check (e.g. `sqlx migrate run` + `cargo sqlx prepare --check`, or `drizzle-kit check`).

## Tools And Security

- Never skip checks with `--no-verify`.
- Stop and escalate when a serious security issue is found.
- Review auth, secrets, outbound HTTP, and config changes with extra scrutiny.
