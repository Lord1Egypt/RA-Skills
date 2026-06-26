---
name: wip-branch-guard
description: PreToolUse hook that enforces branch discipline, blocks destructive commands, requires repo onboarding before first write, tracks blocked-file retries, and gates PR creation against external repos. Read when: a tool call was denied by the guard, or you're about to make the first write in a new repo, or an agent is setting up a new Claude Code / OpenClaw install.
---

# wip-branch-guard

Runtime enforcement of the WIP Computer development workflow. Installed as a PreToolUse hook for Claude Code and as an OpenClaw plugin. Same rules, same deny messages on both harnesses.

## Layer 1 ... write gate

| Context | Writes (Write/Edit/NotebookEdit/Bash-write) |
|---|---|
| On main branch of a git repo | Denied |
| On a feature branch, NOT in a linked worktree | Denied |
| On a feature branch, IN a linked worktree | Allowed |
| Shared-state paths (see below) | Always allowed |
| Not in any git repo | Allowed |

**Shared-state paths (always allowed):** `~/.claude/plans/`, `~/.claude/projects/*/memory/`, `~/.claude/rules/`, `~/.openclaw/workspace/`, `~/.openclaw/extensions/`, `~/.ldm/shared/`, `~/.ldm/messages/`, `~/.ldm/templates/`, `~/.ldm/extensions/`, `~/.ldm/logs/`, `~/.ldm/agents/*/memory/daily/*.md`, `~/.ldm/memory/shared-log.jsonl`, `~/.ldm/memory/daily/*.md`, `workspace/SHARED-CONTEXT.md`, `workspace/TOOLS.md`, `workspace/MEMORY.md`, `workspace/IDENTITY.md`, `workspace/SOUL.md`, `workspace/WHERE-TO-WRITE.md`, `workspace/HEARTBEAT.md`, `workspace/memory/*.md`, `CLAUDE.md`.

Worktree convention: `.worktrees/<repo>--<branch>/`. Bootstrap compound (`git worktree add .worktrees/... && mkdir -p .../ai/... && cp src dest`) is explicitly allowed.

## Layer 2 ... destructive-command block (any branch)

Always denied regardless of branch:

- `git clean -f*` (deletes untracked)
- `git checkout -- <path>` (reverts files)
- `git checkout .` (reverts everything)
- `git stash drop` / `pop` / `clear` (destroys stashed work)
- `git reset --hard` (nukes uncommitted changes)
- `git restore <path>` (reverts files; `--staged` is safe and allowed)
- `python -c "open().write()"` / `node -e "writeFile()"` (scripting-language write bypass)
- `--no-verify` (skips git hooks)
- `git push --force` without `--force-with-lease`

Quoted content is stripped before matching so `gh issue create --body 'use git checkout -- to fix'` is allowed.

## Layer 3 ... session-level gates (new in 1.9.77)

### 1. Onboarding-before-first-write

Before the first write to any git repo in a session, the guard requires the agent to have Read specific onboarding docs at the repo root. The check auto-populates from Read tool calls on the hook matcher (`Read|Glob|Write|Edit|NotebookEdit|Bash`).

Required reads: `README.md`, `CLAUDE.md`, and anything matching `*RUNBOOK*.md`, `*LANDMINES*.md`, `WORKFLOW*.md` at repo root.

TTL: 2 hours of activity once onboarded. Fresh session or inactivity expires the cache.

**Expected ritual for any repo new to your session:**

```
1. git rev-parse --show-toplevel   # confirm the repo
2. Read README.md                  # via Read tool, not cat
3. Read CLAUDE.md                  # if present
4. Read RUNBOOK / LANDMINES / WORKFLOW  # if present at root
5. Proceed with Write/Edit
```

**No override.** Pre-v1.9.82 an `LDM_GUARD_SKIP_ONBOARDING` env var could bypass this gate. It was removed in v1.9.82 along with the cross-session state-file bug that made it necessary. Actually reading the docs is the only path through.

### 2. Recently-blocked-file tracking

Every time the guard denies a write to a specific file, it records `{ts, path, tool, command_stripped}` to the session's recent-denials tail (last 20 entries, 1-hour window). If a subsequent file-writing tool call targets the same path, the guard denies again with prior-block context.

This catches the pattern: `Edit X` → denied → agent retries with `cat > X` via Bash. The second attempt is caught as "equivalent-action bypass" even if the Bash command itself would otherwise be allowed.

**No override.** Pre-v1.9.82 an `LDM_GUARD_ACK_BLOCKED_FILE` env var could acknowledge-and-continue on a blocked-file retry. Removed in v1.9.82. If the original block was wrong, fix the underlying cause (not the block).

### 3. External-PR create guard (new in 1.9.80)

Denied:
- `gh pr create --repo <non-wipcomputer>/<repo>`
- `gh pr create --repo <non-wipcomputer>/<repo> --head <fork>:<branch>` (cross-fork)
- `gh pr create [--web]` when the cwd's git origin is `<non-wipcomputer>/<repo>`
- `gh api repos/<non-wipcomputer>/<repo>/pulls ... -X POST`

Allowed:
- Same commands when owner is `wipcomputer/`
- `gh pr view`, `gh pr list`, `gh pr merge`, `gh pr edit` against any repo (read/interact, not create)
- `gh api repos/<owner>/<repo>/issues ... -X POST` (issues, not pulls)

Triggered by the 2026-04-18 PR #89 incident where an agent opened a PR directly against `steipete/imsg` without approval.

Override: `LDM_GUARD_UPSTREAM_PR_APPROVED=<owner>/<repo>` (target-specific) or `=1` (blanket for the current process).

## Override env vars

Overrides are routed through the inlined approval backend. Every use is recorded in the bypass audit log.

| Env var | Applies to | Value shape |
|---|---|---|
| `LDM_GUARD_UPSTREAM_PR_APPROVED` | External-PR guard | `<owner>/<repo>` or `1` |
| `LDM_GUARD_APPROVAL_BACKEND` | Backend selector | `env` (default). Future: `bridge`, `kaleidoscope-biometric`. |
| `LDM_GUARD_STATE_DIR` | State file redirect | dir path. Tests only. |

**Removed in v1.9.82:** `LDM_GUARD_SKIP_ONBOARDING` and `LDM_GUARD_ACK_BLOCKED_FILE`. Both existed as escape hatches for a cross-session state-collision bug that v1.9.82 fixes at the root. With the bug gone, the escape hatches just train agents to route around the guard instead of fixing its misbehavior. If either env var is set now, the guard ignores it.

**Default stance: don't bypass.** The block message tells you exactly what to do. The one remaining override (`LDM_GUARD_UPSTREAM_PR_APPROVED`) exists for scope-specific operator authorization of a specific external PR, not routine workaround.

## Bypass audit log

`~/.ldm/state/bypass-audit.jsonl`, append-only JSON Lines:

```json
{"kind":"deny","ts":1776780123456,"session_id":"...","tool":"Edit","path":"/abs/path","command_stripped":"...","reason":"BLOCKED: ..."}
{"kind":"skip-onboarding-approved","ts":...,"session_id":"...","path":"<repo>","via":"env","reason":"LDM_GUARD_SKIP_ONBOARDING set"}
{"kind":"external-pr-create-approved","ts":...,"session_id":"...","target":"owner/repo","via":"env","reason":"..."}
```

Rotates to `bypass-audit.jsonl.YYYY-MM-DD` at 50 MB. Keep last 10 archives.

## Session state

**Per-session file (v1.9.82+):** `~/.ldm/state/guard-session-<session_id>.json`. One file per CC session. Pruned after 24 hours of inactivity.

```json
{
  "session_id": "...",
  "started_at": 1776700000000,
  "last_touch_ts": 1776700500000,
  "read_files": ["/abs/path/README.md", "/abs/path/CLAUDE.md"],
  "onboarded_repos": {
    "/abs/repo/path": { "onboarded_at_ts": ..., "last_touch_ts": ... }
  },
  "recent_denials": [
    { "ts": ..., "path": "...", "tool": "Edit", "command_stripped": "..." }
  ]
}
```

Each session's state is independent of every other session's. Writes are serialized within a session via a lockfile (`guard-session-<sid>.json.lock`) to prevent parallel tool calls from clobbering each other. Atomic tmp-file + rename. Never edit directly; the guard owns this file.

**Pre-v1.9.82 legacy:** the guard used a single global `~/.ldm/state/guard-session.json`. Every CC session wrote to it with its own `session_id`, triggering a full state reset on every session switch. That file is ignored by v1.9.82+ and can be deleted safely.

## SessionStart warning

Separate hook event. When a session starts in the main working tree of a protected repo, the guard injects a warning into boot context listing available worktrees + the stash escape-hatch. Non-blocking; just informational.

## When the guard errors on import (fail-open)

If guard.mjs fails to load (missing module, syntax error), Claude Code treats the hook as fail-open ... tools proceed unguarded. This is a safety failure mode and should be caught by:

1. The matcher-containing static test (`bash test.sh`).
2. Smoke-tests after every `ldm install`.

If you suspect fail-open, probe directly:

```
echo '{"tool_name":"Bash","tool_input":{"command":"echo test"}}' | node ~/.ldm/extensions/wip-branch-guard/guard.mjs
```

Empty output = allow (fine). Any error = broken guard (file an issue + roll back to a prior version via `ldm install /tmp/toolbox-at-old-tag`).

## Recovery: installer-as-escape-hatch

The guard can cliff-block its own fix. When that happens, roll back via the installer:

```
git -C <wip-ai-devops-toolbox-private> worktree add /tmp/toolbox-old <pre-problematic-tag>
ldm install /tmp/toolbox-old --yes
```

The installer writes a pre-fix guard to `~/.ldm/extensions/`. Source edits are then unblocked. Fix the underlying issue, ship the new version, reinstall.

## Version history (today)

- 1.9.76: worktree-bootstrap allowlist
- 1.9.77: Layer 3 core (shipped with a dead-code bug; the Read handler never fired because the matcher omitted `Read`)
- 1.9.78: hotfix, inlined `lib/*.mjs` into `guard.mjs` after an installer bug dropped the lib/ subdir
- 1.9.79: added `Read|Glob` to the matcher so the Read handler actually runs
- 1.9.80: external-PR create guard
- 1.9.81: canonical repo key (onboarding shared across worktrees)
- 1.9.82: per-session state files (fix cross-session state wipe), lockfile-based atomic writes, removed `LDM_GUARD_SKIP_ONBOARDING` + `LDM_GUARD_ACK_BLOCKED_FILE` env-var bypasses

## Related

- Plan: `wip-ldm-os-private/ai/product/bugs/guard/2026-04-20--cc-mini--guard-implementation-plan.md`
- Spec (onboarding): `wip-ldm-os-private/ai/product/bugs/guard/2026-04-19--cc-mini--guard-onboarding-and-blocked-file-tracking.md`
- Spec (external-PR): `wip-ldm-os-private/ai/product/bugs/guard/2026-04-19--cc-mini--external-pr-guard.md`
- Triggering incident: `wip-ldm-os-private/ai/product/bugs/code/lesa/2026-04-19--cc-mini--pr-89-process-violation-postmortem.md`
