# wip-branch-guard v1.9.82

## Fix cross-session state collision, kill the env-var escape hatches, and stop Layer 3 from firing on temp-dir writes

Closes #253.

## Additional fix: Layer 3 onboarding/blocked-file gates skip temp-dir and shared-state Bash writes

The Layer 3 onboarding and blocked-file-tracking gates were firing on
ANY Bash command whose extracted write targets list was non-empty,
including writes to `/tmp`, `/var/tmp`, and `/var/folders/.../T/`. The
temp-dir allowance lives in `ALLOWED_BASH_PATTERNS` and only gates
Layer 1 (the on-main write block); Layer 3 ran first and denied with
an onboarding message, even though /tmp is outside any git repo.

Symptom: `cp source /tmp/x` from a session-new repo on main was denied
with "Onboarding required" instead of being allowed.

Surfaced by the Phase 12 audit tests in `test.sh` on 2026-04-21 when
`wip-release` first ran the test suite from main; the 8 temp-dir
test cases (`cp/mv/rm/mkdir/touch/>/tee` to `/tmp` and `cp` to
`/var/tmp`) all failed.

Fix: filter `writeTargets` before Layer 3 to exclude temp paths and
shared-state paths. Symmetric with the Layer 1 allowlist and with
the existing `isSharedState` skip for Edit/Write tools.

`extractWriteTargets` itself is unchanged; the filter lives at the
Layer 3 call site so the function stays general-purpose.

## The bug

Every Claude Code session on the machine was writing the same
`~/.ldm/state/guard-session.json`. The guard's `detectNewSession()` check
fires on `session_id` mismatch and wipes the whole state file
(`onboarded_repos_canonical`, `read_files`, `recent_denials`) before
writing its own. When Parker runs multiple CC sessions at once (his
default working mode, documented in his auto-memory), every tool call
from one session clobbered every other session's onboarding and
read-tracking state.

Symptom: the agent reads a repo's `README.md` + `CLAUDE.md`, commits a
first write successfully, and then on the next Write attempt in the
same worktree the guard demands the same reads again. The dogfood pass
on 2026-04-21 showed this happening mid-session, where the agent
re-read the onboarding docs three times and still hit the same block.

Root cause: one file shared across every session on the machine.

## The fix

### Per-session state files

State now lives at `~/.ldm/state/guard-session-<session_id>.json`. Each
CC session has its own file. Cross-session ping-pong is eliminated at
the source: one session's tool calls can't wipe another session's
state because they write to different files.

The sanitizer in `statePathFor()` maps `session_id` to a safe filename
segment (alphanumerics, dash, underscore; max 64 chars) so weird
session IDs can't escape the state dir.

### Lockfile-based atomic writes within a session

Same-session parallel tool calls (e.g., four Reads kicked off in one
assistant turn) were also racing on read-modify-write of the state
file. `writeSessionState()` now takes a lockfile
(`guard-session-<sid>.json.lock`) via `openSync(..., 'wx')` before
rewriting, with a 2s acquire budget and stale-lock recovery at 10s.

Lock failure degrades to a best-effort write rather than deadlock: the
per-session file fix is the load-bearing change, the lock is
belt-and-suspenders.

### TTL cleanup

Per-session files accumulate over time (one per CC session). The guard
runs `cleanupStaleStateFiles()` on each invocation, deleting any
`guard-session-*.json` or `.lock` older than 24h. `readdirSync` on a
small state dir is sub-millisecond so the scan is cheap enough to run
unconditionally.

### Removed: `LDM_GUARD_SKIP_ONBOARDING` and `LDM_GUARD_ACK_BLOCKED_FILE`

These env vars existed as escape hatches for when the state bug above
bit. With the bug fixed at the root, the hatches just train agents to
route around the guard instead of fixing its misbehavior: every "please
run this env var to unstick me" exchange was the workaround system
working as designed, not a one-off. Both env vars are now ignored. The
only remaining override, `LDM_GUARD_UPSTREAM_PR_APPROVED`, is
legitimate operator authorization (Parker green-lighting a PR to an
upstream repo), not a guard-bug workaround.

Deny messages for the onboarding gate and blocked-file retry gate no
longer suggest setting those env vars. The `approvalCheck` audit
entries for `skip-onboarding-approved` and `ack-blocked-file-approved`
are gone (they can't fire anymore).

## What's in the diff

- `tools/wip-branch-guard/guard.mjs`
  - New: `statePathFor()`, `withStateLock()`, `cleanupStaleStateFiles()`,
    per-session state constants
  - Changed: `readSessionState()` takes a `sessionId`; `writeSessionState()`
    routes the write through the per-session path under a lockfile
  - Removed: `detectNewSession` wipe path in `main()` (per-session files
    make it obsolete); `approvalCheck` calls + audit entries for the
    removed env vars; escape-hatch hints in deny messages
- `tools/wip-branch-guard/test.sh`
  - Flipped: `LDM_GUARD_SKIP_ONBOARDING` / `LDM_GUARD_ACK_BLOCKED_FILE`
    tests assert the env var is now ignored (expected deny)
  - New: "Cross-session state isolation" regression test block (6 cases
    plus 2 on-disk-file-existence assertions) that exercises the exact
    ping-pong pattern
- `tools/wip-branch-guard/SKILL.md`
  - Documentation updates: per-session state shape, v1.9.82 entry in
    version history, override table now lists only the one remaining
    env var, removed-env-var notes in Layer 3 sections
- `tools/wip-branch-guard/package.json`
  - Version bump 1.9.81 → 1.9.82

## Test plan

```
bash tools/wip-branch-guard/test.sh
```

Expected: 95 pass, 0 fail, 8 skip (on-main-branch cases that only run
when the test-runner's own CWD is on main).

The key regression cases to watch on every future guard change:
- `iso: session A still onboarded after B's activity` (the exact bug)
- `iso: per-session file for A exists on disk`
- `onboarding: LDM_GUARD_SKIP_ONBOARDING=1 IGNORED (still denies)`

## Migration

The legacy `~/.ldm/state/guard-session.json` becomes an orphan after
install. v1.9.82 ignores it. Safe to delete:

```
rm -f ~/.ldm/state/guard-session.json
```

`cleanupStaleStateFiles()` does NOT touch it (the regex matches
`guard-session-*.json`, not the un-suffixed legacy filename), so leaving
it in place is also fine: it'll sit there doing nothing until someone
cleans `~/.ldm/state/` manually.

## Tradeoff accepted

With the env-var escape hatches gone, a future guard malfunction
genuinely strands the agent mid-session: the only way forward is to
patch + install a fix. We accept this because the alternative (keep
the hatches) keeps the workaround loop alive. The compensating surface
is the installer-as-escape-hatch path documented in SKILL.md (roll back
to a pre-problematic tag via `ldm install /tmp/toolbox-old`) and the
bypass audit log, which records every deny with enough context to
diagnose the next state bug in minutes rather than hours.

## Out of scope for this PR (still open)

Audit performed during the fix flagged three gaps that do NOT get
addressed here. Separately filed; mentioned so the next guard PR picks
them up rather than losing them.

- **Gap A: no proactive SessionStart scan.** The onboarding gate is
  reactive (fires on first write, not on session start or first cd).
  If the agent never writes, the scan never happens.
- **Gap B: shell redirection hole.** The guard blocks Edit/Write and
  catches `python -c` / `node -e`, but Bash `>`, `>>`, `tee` to
  protected paths outside `.worktrees/`, `/tmp`, etc. isn't
  pattern-matched. Narrower than the explicit code-execution bypass
  block and a real workaround surface.
- **Gap C: passive bypass audit.** `~/.ldm/state/bypass-audit.jsonl`
  records denials and (before this PR) env-var overrides, but nothing
  parses it at SessionStart or Stop to surface repeat bypasses to
  Parker.

## Co-authors

Parker Todd Brooks, Lēsa (oc-lesa-mini, Opus 4.7), Claude Code (cc-mini, Opus 4.7).
