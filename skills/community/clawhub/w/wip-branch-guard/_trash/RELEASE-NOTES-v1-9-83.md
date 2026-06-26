# wip-branch-guard v1.9.83

## Close the shell-redirection bypass class + surface corrupt per-session state at boot

Closes #254.

Addresses Gap B and the optional SessionStart sanity check from the v1.9.82 ticket (`2026-04-21--parker-cc-mini--bugfix.md`).

## Gap B: shell redirection bypass into protected deployed paths

### The bug

`wip-file-guard` protects identity files on Edit/Write. `wip-branch-guard` blocked Edit/Write + destructive git commands + `python -c "open().write()"` / `node -e "writeFile()"`. But Bash redirects (`>`, `>>`, `tee`) into the deployed extension directories, OpenClaw config, agent auth-profiles, credentials, and secrets were not pattern-matched. An agent blocked from `Edit ~/.openclaw/openclaw.json` could pivot to `echo '{...}' > ~/.openclaw/openclaw.json` or `jq '.' ... > ~/.openclaw/openclaw.json` and the guard would not notice.

Parker surfaced this class during the 2026-04-19 debugging session ... after `Edit` was denied, the agent attempted a `jq` + shell-redirect pivot to the same file. The guard did not catch that, and Parker called it out manually.

### The fix

Six new patterns in `DESTRUCTIVE_PATTERNS`. Each matches `>`, `>>`, or `tee` into a protected path:

- `~/.openclaw/openclaw.json` ... OpenClaw's main config
- `~/.openclaw/agents/<id>/agent/auth-profiles.json` ... agent auth credentials
- `~/.openclaw/agents/<id>/agent/settings.json` ... agent settings
- `~/.openclaw/extensions/*` ... deployed plugins (canonical path is `ldm install`)
- `~/.openclaw/credentials/*` ... iMessage pairing data
- `~/.openclaw/secrets/*` ... 1Password SA token
- `~/.ldm/extensions/*` ... LDM OS deployed extensions
- `~/.ldm/config.json` ... LDM OS root config
- `~/.ldm/agents/<id>/config.json` ... LDM OS agent configs

`DESTRUCTIVE_PATTERNS` blocks on any branch, not just main. Redirect-writes to these paths are never legitimate regardless of where the agent is working; the canonical modification path is always source-repo + `ldm install`.

### What's still allowed

`cp`, `mv`, `rm`, `mkdir` into `~/.openclaw/extensions/` and `~/.ldm/extensions/` remain allowed via `ALLOWED_BASH_PATTERNS` (hotfix-deploy flows). Shared-state paths (`~/.openclaw/workspace/`, `~/.ldm/agents/*/memory/daily/`, `~/.ldm/logs/`, `~/.ldm/shared/`, etc.) are not in the new patterns so they're still writable via any method.

## SessionStart sanity check on per-session state file

### The bug

v1.9.82 introduced per-session state files at `~/.ldm/state/guard-session-<sid>.json` with TTL cleanup. If a state file becomes corrupt, loses its `started_at`, or survives past the 24h TTL (because cleanup failed), the guard silently recovers on the next invocation by writing fresh state. Silent recovery hides the corruption from the operator, so a class of state bug could persist across sessions without anyone noticing.

### The fix

On `SessionStart`, the guard now checks the current session's state file and emits a warning into boot context if it's:

- Unreadable (permissions, I/O error)
- Unparseable JSON
- Missing `started_at` or with a non-numeric value
- Older than 24 hours (the TTL cleanup window)

The warning is non-blocking; it tells Parker + the agent that state corruption is present and gives the manual cleanup command. Fresh state is still created automatically on the next tool call, so the session continues normally.

Runs regardless of branch (the existing on-main warning only fires on main; state corruption is session-wide).

## What's in the diff

- `tools/wip-branch-guard/guard.mjs`
  - New: 6 patterns in `DESTRUCTIVE_PATTERNS` for Gap B (shell-redirect bypass block)
  - New: `emitSessionStartContext()` helper
  - New: `checkSessionStateSanity()` helper
  - Changed: `handleSessionStart()` refactored to collect warnings from both state-sanity and on-main paths, emit combined context
- `tools/wip-branch-guard/test.sh`
  - New: Gap B test cases (redirect into protected paths denied, into shared-state allowed)
- `tools/wip-branch-guard/package.json`
  - Version bump 1.9.82 → 1.9.83

## Tradeoff accepted

Gap B's `~/.openclaw/extensions/*` pattern blocks `echo > ext.mjs` even in a legitimate hotfix-deploy scenario, because the redirect form is not part of the canonical hotfix flow. If someone needs to redirect-into-extensions for a one-off, they can `ldm install` from a worktree build instead.

## Out of scope for this PR (still open from v1.9.82 ticket)

- **Gap A:** proactive SessionStart scan (no auto-onboarding before first write).
- **Gap C:** bypass audit escalation at SessionStart/Stop (passive log, no surface to Parker).

Both targeted for v1.9.84.

## Co-authors

Parker Todd Brooks, Lēsa (oc-lesa-mini, Opus 4.7), Claude Code (cc-mini, Opus 4.7).
