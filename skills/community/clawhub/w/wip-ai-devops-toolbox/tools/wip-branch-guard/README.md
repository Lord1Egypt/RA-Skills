###### WIP Computer

# Branch Guard

PreToolUse hook that enforces branch discipline, blocks destructive commands, requires repo onboarding before first write, tracks blocked-file retries, and gates PR creation against external repos. Same logic ships as a Claude Code hook and as an OpenClaw plugin.

## Install

See [INSTALL.md](INSTALL.md) for hook registration in `~/.claude/settings.json` (PreToolUse + SessionStart entries).

## What it does

- **Layer 1 ... write gate.** Blocks Write/Edit/NotebookEdit/Bash-write on main branch or non-worktree feature branches. Shared-state paths (`~/.claude/plans/`, `~/.openclaw/workspace/`, `~/.ldm/extensions/`, etc.) are always allowed.
- **Layer 2 ... destructive-command block.** Always denies `git clean -f`, `git reset --hard`, `git stash drop/pop/clear`, `git checkout -- <path>`, `python -c "open().write()"`, `node -e "writeFile()"`, `--no-verify`, and `git push --force` without `--force-with-lease`.
- **Layer 3 ... session-level gates.**
  - Onboarding-before-first-write: requires Read of `README.md`, `CLAUDE.md`, and any `*RUNBOOK*.md` / `*LANDMINES*.md` / `WORKFLOW*.md` at repo root before the first write.
  - Recently-blocked-file tracking: catches `Edit X` denied → `cat > X` via Bash as an equivalent-action bypass.
  - External-PR create guard: denies `gh pr create` against non-wipcomputer repos without explicit `LDM_GUARD_UPSTREAM_PR_APPROVED` operator authorization.

See [SKILL.md](SKILL.md) for full layer details, override semantics, per-session state shape, and the installer-as-escape-hatch recovery path.

## Test

```bash
bash test.sh
```

Expected: 95 pass, 0 fail, 8 skip (on-main-branch cases that only run when the test-runner CWD is on main).

## Source

- `guard.mjs` ... PreToolUse + SessionStart handler, all logic inlined (zero runtime dependencies)
- `test.sh` ... 95+ regression cases including cross-session state isolation
- `package.json` ... npm metadata + hook registration manifest

## Interfaces

- **Claude Code Hook** ... PreToolUse + SessionStart, registered via `~/.claude/settings.json`
- **OpenClaw Plugin** ... same logic, same deny messages

## License

MIT for tool usage; AGPLv3 for commercial redistribution, marketplace listings, or bundling into paid services. See [LICENSE](LICENSE) and [CLA.md](CLA.md) in this directory, and the parent repo's [dual-license model](../../README.md#license) for full context.

## Part of [AI DevOps Toolbox](https://github.com/wipcomputer/wip-ai-devops-toolbox)

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.7), Claude Code (Claude Opus 4.7).
