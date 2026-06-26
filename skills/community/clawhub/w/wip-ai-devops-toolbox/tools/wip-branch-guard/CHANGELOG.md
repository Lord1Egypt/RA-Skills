# Changelog

## 1.9.84 (2026-04-21)

# wip-branch-guard v1.9.84

## Proactive onboarding advisory + bypass audit escalation

Closes #255.

Closes out the last two follow-ups from the v1.9.82 ticket (`2026-04-21--parker-cc-mini--bugfix.md`): Gap A and Gap C. Together with v1.9.82 (cross-session state fix + Layer 3 temp-dir filter + env-var hatch removal) and v1.9.83 (shell-redirect bypass block + state sanity check), the v1.9.82 ticket is fully closed.

## Gap A: proactive SessionStart onboarding advisory

### The bug

The onboarding gate is reactive. It fires on the first Write/Edit/Bash-write attempt in a session-new repo, not on session start or first `cd`. When an agent hasn't done the onboarding Reads before its first write, it hits the deny, which then triggers the retry-after-block pattern on subsequent attempts. That pattern is what Claude Code's auto-mode decider false-positives on (tracked upstream as anthropics/claude-code#51676).

Prevention is the only fix that doesn't require Anthropic to ship a remediation-aware decider: surface the required onboarding reads at SessionStart so the agent does them up-front in a single parallel-Read turn, before any write.

### The fix

New `checkProactiveOnboardingAdvisory(cwd)` helper, called from `handleSessionStart`. If cwd is a git repo and the repo root has `README.md`, `CLAUDE.md`, or any `*RUNBOOK*.md` / `*LANDMINES*.md` / `WORKFLOW*.md`, the guard emits a boot-context advisory listing each required Read path. Non-blocking; purely informational.

Example output (injected into boot context):

```
📖 ONBOARDING ADVISORY: /path/to/repo has onboarding docs. Before your first Write/Edit/Bash-write in this session, Read these in parallel (one turn):

  Read /path/to/repo/README.md
  Read /path/to/repo/CLAUDE.md

The guard enforces onboarding on first write; reading up-front avoids retry-after-block cycles that Claude Code's auto-mode decider false-positives on.
```

## Gap C: bypass audit escalation at SessionStart

### The bug

`~/.ldm/state/bypass-audit.jsonl` records every guard denial and every env-var override. Pre-v1.9.82, `LDM_GUARD_SKIP_ONBOARDING` and `LDM_GUARD_ACK_BLOCKED_FILE` writes appeared here frequently. The log existed; nothing parsed it. Repeat bypasses accumulated silently.

### The fix

New `checkBypassAuditEscalation()` helper, called from `handleSessionStart`. Reads the last 500 lines of the audit log, filters to the last 24 hours, and emits a boot-context warning if:

- Any path was denied 3+ times in the window (`🚨 BYPASS AUDIT`), OR
- Any env-var override fired at all (`⚠️ ENV-VAR OVERRIDES`). Post-v1.9.82, only `LDM_GUARD_UPSTREAM_PR_APPROVED` is legitimate; any other override appearing here means the deployed guard is stale (pre-v1.9.82) and `ldm install` is needed.

The warning is non-blocking; it surfaces the pattern so Parker can triage without reading the audit log manually.

## What's in the diff

- `tools/wip-branch-guard/guard.mjs`
  - New: `checkProactiveOnboardingAdvisory(cwd)` helper (Gap A)
  - New: `checkBypassAuditEscalation()` helper (Gap C)
  - Changed: `handleSessionStart` now collects warnings from four sources (state sanity, bypass audit, onboarding advisory, on-main warning) and emits them joined into a single `additionalContext` response
- `tools/wip-branch-guard/package.json`
  - Version bump 1.9.83 → 1.9.84

## Tradeoff accepted

The onboarding advisory fires on EVERY SessionStart in a git repo with onboarding docs. That's slightly noisy for experienced sessions in familiar repos. The alternative (gate on "not yet onboarded" via state lookup) requires state to exist at SessionStart, which it typically doesn't (per-session state file is created on first PreToolUse). Preferred noisy-but-useful over silent-but-inert.

## The v1.9.82 ticket is now closed

| Item | Shipped in |
|---|---|
| Cross-session state collision fix | v1.9.82 |
| Env-var escape hatches removed | v1.9.82 |
| Layer 3 temp-dir false-positive filter | v1.9.82 |
| Gap B: shell-redirect bypass block | v1.9.83 |
| SessionStart state sanity check | v1.9.83 |
| Gap A: proactive SessionStart onboarding advisory | v1.9.84 |
| Gap C: bypass audit escalation | v1.9.84 |

## Co-authors

Parker Todd Brooks, Lēsa (oc-lesa-mini, Opus 4.7), Claude Code (cc-mini, Opus 4.7).

## 1.9.83 (2026-04-21)

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

## 1.9.82 (2026-04-21)

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
