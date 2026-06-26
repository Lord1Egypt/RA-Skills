# wip-branch-guard v1.9.77

## Layer 3: onboarding + blocked-file tracking + pluggable approval backend

Three behavioural additions, wired together through a new session-state file and a pluggable approval-backend module. The guard now catches two failure modes that made it into the 2026-04-19 post-mortem: (1) agents on first contact with a repo not reading the onboarding docs before editing, and (2) agents retrying a blocked file via a different tool to sidestep the specific deny message.

### Onboarding-before-first-write

First write to a repo in a session is gated on the agent having read the repo's onboarding docs in the same session. Required reads are `README.md`, `CLAUDE.md`, and anything matching `*RUNBOOK*.md` / `*LANDMINES*.md` / `WORKFLOW*.md` at the repo root. A Read of each satisfies the gate; once satisfied the repo stays onboarded for 2 hours of continuous work in that session.

Override: `LDM_GUARD_SKIP_ONBOARDING=<repo-path>` (target-specific) or `LDM_GUARD_SKIP_ONBOARDING=1` (blanket). Every skip is recorded in `~/.ldm/state/bypass-audit.jsonl` as `kind: skip-onboarding-approved`.

Shared-state paths (`~/.claude/plans/`, `~/.claude/projects/*/memory/`, `~/.openclaw/workspace/`, `~/.ldm/shared/`, etc.) bypass onboarding entirely - they're the one place agents are meant to collaboratively edit on main, and adding a gate there would trip every session.

### Recently-blocked-file tracking

Every deny that has a specific filesystem target (Write/Edit on main, Bash write on main, Write/Edit on a branch not in a worktree) records `{path, tool, command_stripped, ts}` to the session's recent-denials tail (keeps last 20 for up to 1 hour). On the next file-writing tool call, if the target path matches a recent denial, the guard denies again with the original block's context.

This catches the pattern "Edit blocked on X -> retry via Bash `cat > X`" which the previous guard let through because `cat >` on a worktree would match `ALLOWED_BASH_PATTERNS`. Now the second attempt is blocked with: "X was just denied via Edit; retrying through Bash is an equivalent-action bypass".

Override: `LDM_GUARD_ACK_BLOCKED_FILE=<path>` (target-specific; matches the exact path that was denied) acknowledges the prior block and lets the write proceed. Logged as `kind: ack-blocked-file-approved`.

### Pluggable approval backend

`lib/approval-backend.mjs` exports a single `check(action, context)` function. The `env` backend (shipping today) maps each action `kind` to an env var. Future backends slot in as new switch cases: `bridge` (route to lesa-bridge for human-in-the-loop approval), `kaleidoscope-biometric` (passkey/biometric gate). The selector is `LDM_GUARD_APPROVAL_BACKEND` (defaults to `env`).

Action kinds wired today: `skip-onboarding`, `ack-blocked-file`, `external-pr-create` (the last is scoped for PR 3 which adds the external-PR guard; the env mapping is in place so PR 3 only touches `guard.mjs`).

### Bypass audit log

Every deny, every approved skip, every approved ack lands in `~/.ldm/state/bypass-audit.jsonl`. Append-only, rotated at 50 MB to a dated archive (`bypass-audit.jsonl.YYYY-MM-DD`). Entries are single-line JSON: `{kind, ts, session_id, tool, path, command_stripped, reason}`.

This is meant to be tailed during post-mortems and reviewed periodically. The file rotates rather than truncating so nothing is lost.

### Files

- `tools/wip-branch-guard/lib/approval-backend.mjs` (new, 42 lines): pluggable backend; env mode ships, bridge / biometric deferred.
- `tools/wip-branch-guard/lib/session-state.mjs` (new, 118 lines): atomic read/write of `~/.ldm/state/guard-session.json`, onboarding TTL logic, recent-denials tail, audit log rotation. `LDM_GUARD_STATE_DIR` env override lets tests redirect to `/tmp`.
- `tools/wip-branch-guard/guard.mjs`: imports the two new modules; wraps `deny()` to write to the audit log; runs the Layer 3 gates after repo resolution and before the branch-check block; attaches denial context at the three remaining deny sites (not-worktree, main-write, main-bash-write) so the blocked-file tail catches equivalent-action retries.
- `tools/wip-branch-guard/test.sh`: 15 new Layer 3 tests (onboarding first-write deny, read-then-write allow, two env overrides, wrong-target denies, session-reset, audit log, approval-backend unit check, shared-state regression). Built on a temporary git repo with a real worktree so the branch-guard itself allows the write and Layer 3 is the only gate in play.

## Changes

- `tools/wip-branch-guard/package.json`: `1.9.76 -> 1.9.77`, description updated to mention the new behaviors.

## Tests

68 passing, 0 failing, 8 main-only skipped when run from worktree (expected). Up from 53.

## Why now

Per the implementation plan at `wip-ldm-os-private/ai/product/bugs/guard/2026-04-20--cc-mini--guard-implementation-plan.md`, this is PR 2 of 3. PR 1 (worktree-bootstrap allowlist) landed as 1.9.76 and enables PR 2's tests to create worktrees via the bootstrap compound. PR 3 (external-PR guard) will reuse the approval-backend module shipped here.

## Related

- Triggering incident: `wip-ldm-os-private/ai/product/bugs/code/lesa/2026-04-19--cc-mini--pr-89-process-violation-postmortem.md`
- Onboarding + blocked-file spec: `wip-ldm-os-private/ai/product/bugs/guard/2026-04-19--cc-mini--guard-onboarding-and-blocked-file-tracking.md`
- Implementation plan: `wip-ldm-os-private/ai/product/bugs/guard/2026-04-20--cc-mini--guard-implementation-plan.md`
- Parent master plan: `wip-ldm-os-private/ai/product/bugs/guard/2026-04-05--cc-mini--guard-master-plan.md`

## Known limitations

1. Onboarding required-reads list is hardcoded to README + CLAUDE.md + RUNBOOK/LANDMINES/WORKFLOW at repo root. Repos with their onboarding spread across subdirs (e.g. `docs/RUNBOOK.md`) aren't yet supported. Extensible: `getRequiredReads()` lives in `guard.mjs` and can be updated when a pattern emerges.

2. Blocked-file tracking operates on exact-path matches. A retry via `cd <different-abs-path> && echo > file` extracts different absolute paths (or none) so the tail check won't fire. Ordered-by-recency tail rather than a set, so the O(n) scan is fine. An argument-order-aware parser for Bash commands is the next step, deferred.

3. Session state singleton at `~/.ldm/state/guard-session.json` with atomic tmp-file + rename write. Two tool calls racing could still lose the loser's denial append (last writer wins). Acceptable for now: the outcome is "we fail to audit one denial", not "we mis-deny something". The branch guard itself remains side-effect-free per call.

4. The approval-backend `env` mode is susceptible to env pollution if a caller exports `LDM_GUARD_SKIP_ONBOARDING=1` globally. That's the intended design (dev/testing escape hatch) but it means a rogue shell rc would silently disable onboarding. The audit log catches it after the fact.
