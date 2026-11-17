# Public Guard Issue Reconciliation

**Date:** 2026-05-01
**Filed by:** Claude Code (cc-mini)
**Area:** guard
**Status:** closed
**Priority:** low
**Implementation repo:** `wip-ai-devops-toolbox-private` for any code changes; `wipcomputer/wip-ldm-os` for the public issue closures.

## Summary

Four public `wipcomputer/wip-ldm-os` issues for the branch guard remained `OPEN` after the 2026-04-29 guard closeout. The 2026-04-30 raw-session review at `team/parker/repos/raw-terminal-sessions-private-only/raw-sessions/guard--cody--04-27-2026--01--open.md` noted that these issues "appear partially or fully covered by the shipped guard rollout, but closing them should be a separate issue reconciliation pass."

This ticket tracks that pass. For each issue, the work is to verify shipped guard behavior against the issue's acceptance criteria, then either close the issue on GitHub with a reference to the closing PR or version, or file a private follow-up that documents the remaining gap.

Reference guard version for the pass: `@wipcomputer/wip-branch-guard@1.9.91` (current published `latest`).

## Resolution

Closed 2026-05-01 after the reconciliation pass landed and shipped:

- Source fix: `wip-ai-devops-toolbox-private` PR `#405`, merged as `992956e`.
- Release: `@wipcomputer/wip-ai-devops-toolbox@1.9.73-alpha.9` and `@wipcomputer/wip-branch-guard@1.9.91`.
- Source version sync: `wip-ai-devops-toolbox-private` PR `#407`, merged as `9d41ef1`.
- Deployed validation: CLI, LDM runtime, and OpenClaw runtime all reported `wip-branch-guard` `1.9.91`.
- OpenClaw plugin validation: `/Users/lesa/.openclaw/extensions/wip-branch-guard/openclaw.plugin.json` exists and points `before_tool_use` to `./guard.mjs`.

Public issue disposition:

- `#127`: left open. Guard simulation blocks `git commit` in `~/.ldm` when invoked, but the full issue also covers dirty ldm-home cleanup and durable install coverage. Follow-up filed at `ai/product/bugs/guard/2026-05-01--codex--ldm-home-guard-install-and-drift.md`.
- `#131`: closed. Shared-main protections and the OpenClaw plugin manifest now cover the no-direct-main-write invariant across the guarded surfaces.
- `#215`: closed. Release cooldown is now session-scoped, not machine-wide.
- `#241`: closed. Nested `bash -c` write targets and Python script-file write targets are now parsed and tested.

Validation evidence:

```text
node --check tools/wip-branch-guard/guard.mjs
git diff --check
em dash scan over changed toolbox files
bash tools/wip-branch-guard/test.sh
Result: 126 passed, 0 failed, 8 skipped
```

Deployed OpenClaw hook probes used `LDM_GUARD_STATE_DIR=/tmp/guard-openclaw-validate-*` so this Codex sandbox could write session state:

```text
main create before onboarding: denied with onboarding requirement
main create after onboarding: denied as main Write
main edit after onboarding: denied as main Edit
feature worktree create after onboarding: allowed
audit log: records onboarding, main Write, and main Edit denials with session identity
```

## Issues To Reconcile

### `wipcomputer/wip-ldm-os#127`: Add branch guard to `~/.ldm/`

What it asks: extend guard protection to the `~/.ldm/` directory, which is itself a tracked private repo.

Likely shipped state: the guard operates against any tracked private repo via standard protections, but it is unclear whether `~/.ldm/` is recognized as a protected repo path and whether shared-main protections (commit, merge, push, dirty pull) apply there. Worth checking explicitly because `~/.ldm/` is the deployed-extensions root and a write there could clobber the live runtime.

Verification:

1. From `~/.ldm/` on `main`, attempt the actions in the shared-main protection list and confirm each is denied.
2. Confirm `wip-branch-guard onboard ~/.ldm/` succeeds.
3. If any protection is missing, file a guard scope ticket in `ai/product/bugs/guard/`. Otherwise close `#127` with a comment linking to the 1.9.88 shared-main protections and the verification transcript.

### `wipcomputer/wip-ldm-os#131`: Enforce branch/PR workflow: agents must never write on main

What it asks: agents must not commit, merge, push, or otherwise write on `main` without going through a branch and PR.

Likely shipped state: shared-main protections in `wip-branch-guard@1.9.88` already block commit, merge, rebase, push to `origin main`, non-`--ff-only` pull, and `--ff-only` pull when the tree is dirty or ahead. This appears fully covered.

Verification:

1. Read the issue body line for line against the `Shared-Main Protections` section in the archived `2026-04-24--codex--guard-dev-update.md`.
2. If every action listed in `#131` is in the protection list, close `#131` with a comment linking the relevant guard version and the dev update.
3. If any action is missing, file a guard ticket for the gap.

### `wipcomputer/wip-ldm-os#215`: Dogfood guard blocks wrong sessions: should be per-session, not machine-wide

What it asks: the guard's denial state (recently-blocked-file tracker, approval state) should be scoped per session, not machine-wide.

Likely shipped state: partially covered. The 04-29 cp regression fix landed acceptance criterion 7 ("recently-blocked-file tracker does not turn a known false-positive class into a dead end after the parser is fixed"). That addressed cache poisoning specifically, but it is unclear whether the tracker is now session-scoped or still machine-wide.

Verification:

1. Read `tools/wip-branch-guard/` source for how the recently-blocked-file tracker keys its state (process id, session id, machine path, etc.).
2. Run two concurrent CC sessions, induce a denial in one, confirm the other is unaffected.
3. If session-scoped, close `#215` with a reference to the 1.9.89 fix. If still machine-wide, file a guard scope ticket for per-session state.

### `wipcomputer/wip-ldm-os#241`: Branch guard: catch python/bash file write bypasses

What it asks: the guard should catch write attempts via interpreter scripts (python, bash) that route around direct Bash tool calls.

Likely shipped state: unclear. The 1.9.88 destination-aware Bash parser covers `cp`, `mv`, `rm`, `mkdir`, `touch`, redirects, and `tee`. It does not obviously cover `python -c 'open(...,"w")...'` or `bash -c '...'` invocations that perform writes through the interpreter rather than via a recognized shell command. This is a real bypass class if not handled.

Verification:

1. Try `python -c "open('/path/to/protected', 'w').write('x')"` with the protected path inside a shared-main checkout.
2. Try `bash -c 'echo x > /path/to/protected'` against the same path.
3. Try a script file invocation: `python /tmp/write.py`.
4. If any of these succeed against shared-main, file a guard parser-extension ticket in `ai/product/bugs/guard/`. The fix likely belongs alongside the destination-aware parser work in `wip-ai-devops-toolbox-private`.
5. If all are blocked, close `#241` with a comment showing the verification transcript.

## Acceptance Criteria

1. Each of the four public issues is read against the current guard implementation in `repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-branch-guard/`.
2. For each issue: either close it on GitHub with a comment linking to the closing PR or version, or file a follow-up private ticket in `ai/product/bugs/guard/` that documents the remaining gap.
3. Reconciliation pass uses `wip-branch-guard@1.9.91` as the reference version.
4. Once all four issues are decided, this ticket is moved to `ai/product/bugs/guard/archive/` with a short resolution note pointing to each closure or follow-up.

## Related

- Raw session review: `team/parker/repos/raw-terminal-sessions-private-only/raw-sessions/guard--cody--04-27-2026--01--open.md`
- Guard closeout: `ai/product/bugs/guard/archive/2026-04-24--codex--guard-dev-update.md`
- cp regression closure: `ai/product/bugs/guard/archive/2026-04-29--codex--guard-cp-source-regression.md`
- Biometric backend follow-up: `ai/product/bugs/guard/2026-04-29--codex--guard-biometric-approval-backend.md`
- Current published guard version: `@wipcomputer/wip-branch-guard@1.9.91`
