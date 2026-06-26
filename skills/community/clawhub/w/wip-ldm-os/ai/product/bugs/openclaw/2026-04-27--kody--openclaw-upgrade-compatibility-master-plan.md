# Master Plan: OpenClaw Upgrade Compatibility Layer

**Date:** 2026-04-27
**Author:** Kody, with Parker
**Status:** master plan; v2026.4.25 promotion completed, upstream memory-core fixes accepted post-v2026.4.26, follow-ups remain
**Area:** OpenClaw, LDM OS compatibility/update layer, Bridge, Memory Crystal, healthcheck
**Primary runbook:** `repos/ldm-os/devops/open-claw-upgrade-private/UPGRADE-RUNBOOK.md`
**Primary landmines:** `repos/ldm-os/devops/open-claw-upgrade-private/KNOWN-LANDMINES.md`

## Problem

OpenClaw upgrades are not safe to treat as normal package updates for Lēsa's production installation.

The live system is not stock OpenClaw. It includes a fork build, carried source patches, Bridge/chatCompletions behavior, Memory Crystal capture, OpenClaw memory-core, 1Password-backed secrets, iMessage routing, healthcheck, private mode, compaction indicators, session export, and local LaunchAgent service management.

When upstream OpenClaw changes auth scopes, gateway route ordering, plugin hook permissions, config schemas, memory-core internals, CLI backends, or restart behavior, the whole LDM/OpenClaw stack can regress. The recent v2026.4.23 to v2026.4.25 work exposed the pattern clearly: the upgrade was not "install latest"; it became a multi-day compatibility exercise across fork patches, memory OOM fixes, health probes, plugin hook gates, config safety, and canary promotion.

LDM OS needs an explicit compatibility/update layer around OpenClaw upgrades.

## Product Conclusion

LDM OS should not assume OpenClaw upgrades are safe. We need:

- preflight snapshots
- version pinning
- migration notes
- doctor before/after
- plugin compatibility checks
- fork patch tracking
- rollback path
- known broken upstream versions ledger
- canary promotion gates
- post-upgrade config invariant checks

The goal is to turn "why did everything break?" into a managed, repeatable upgrade flow.

## Supersedes

This ticket consolidates the active OpenClaw tickets from April 5 onward. Superseded originals should remain in `ai/product/bugs/openclaw/archive/` for forensic detail. The upstream memory-core packet remains a top-level companion ticket until WIP canaries and promotes a build containing the accepted upstream commits.

| Ticket | Disposition in this master plan |
|---|---|
| `2026-04-05--cc-mini--brainstorm-cron-exec-approval.md` | Folded into Phase 8: cost/control-plane safety and non-interactive approval policy. |
| `2026-04-05--cc-mini--chatcompletions-streaming-architecture.md` | Folded into Phase 5: Bridge/chatCompletions queue semantics and future mid-turn cancellation research. |
| `2026-04-05--cc-mini--cli-adapter-workaround-steipete.md` | Folded into Phase 7: Claude CLI backend isolation. Marked as do-not-pursue for billing workaround unless policy/behavior changes. |
| `2026-04-12--cc-mini--claude-cli-identity-contamination.md` | Folded into Phase 7: CLI backend isolation and identity boundaries. |
| `2026-04-12--cc-mini--format-error-billing-cooldown.md` | Folded into Phase 6: failover/auth-state classification. |
| `2026-04-12--cc-mini--session-amnesia-on-billing-failure.md` | Folded into Phase 7: session continuity and single-source session state. |
| `2026-04-14--cc-mini--upgrade-v4.11-to-v4.14.md` | Folded into Phase 1 and Phase 3 as the historical proof of the fork-upgrade runbook pattern. |
| `2026-04-24--cc-mini--main-sqlite-oom-artifact.md` | Folded into Phase 4: memory-core bounded read and canary gates. |
| `2026-04-24--kody--upstream-memory-core-packet.md` | Linked from Phase 9 as the upstream packet. Upstream accepted the memory-core fixes after `v2026.4.26`; do not archive until WIP canaries/promotes a build containing them and retires the fork carry. |

## Current State

As of 2026-04-28:

- Live OpenClaw: `2026.4.25` WIP fork build, merge commit `c188a3647c11fde080f8e6475e20380aa9671f35`.
- Latest stable upstream tag/npm: `v2026.4.26`, but it does not contain accepted memory-core commits `983fd775e2` and `864c4f7ff4`.
- Current upstream `main`: contains the accepted memory-core fixes and is the next canary target if we do not wait for a later stable tag.
- Promotion path used: built source from the merged WIP fork worktree, installed with `npm link`, restarted with `launchctl kickstart -k`.
- Fork carry PR: `wipcomputer/openclaw#4` (`kody/v2026-4-25-carry-memory-core`) merged into `kody/v2026-4-25-base`.
- Superseded upstream-main canary: `wipcomputer/openclaw#3`, closed after #4 replaced the mislabeled `.26` path with the real `v2026.4.25` base.
- Protected probes for `.25+`: `/healthz` and `/readyz`. Legacy `/health` can hang and should not be the promotion gate.
- Trusted external plugins using conversation-access hooks need `hooks.allowConversationAccess=true`.
- Live config now includes `hooks.allowConversationAccess=true` for `memory-crystal`, `compaction-indicator`, and `session-export`.
- Raw npm install is unsafe while production-critical patches are absent from the stable tag being installed.

Live post-promotion checks:

- `openclaw --version`: `OpenClaw 2026.4.25 (c188a36)`
- `/healthz`: green
- `/readyz`: green
- LaunchAgent: PID stable, last exit code `0`
- Main session: reports `gpt-5.5` in `openclaw sessions`
- Memory Crystal: saw post-upgrade compaction/reset activity

Open follow-ups before calling the whole compatibility layer mature:

- Clean the stale duplicate `tavily` warning that points at an older worktree.
- Add explicit `plugins.allow` provenance pins for trusted local plugins.
- Keep `listChunks()` bounded-read work open as R2.A.3 until a post-`v2026.4.26` build containing `864c4f7ff4` is canaried/promoted.
- Keep boot-payload inventory and identity-kernel work separate from this upgrade plan.

## Master Execution Plan

### Phase 0: Freeze the source of truth

1. Treat `open-claw-upgrade-private` as the operational source of truth for OpenClaw upgrades.
2. Keep `UPGRADE-RUNBOOK.md`, `KNOWN-LANDMINES.md`, `ai/notes/system-state.md`, and `ai/todos/open-items.md` current before any live promotion.
3. Add a dedicated `COMPATIBILITY-LEDGER.md` to the upgrade repo with:
   - upstream version or commit
   - status: `blocked`, `canary`, `promoted`, `rolled-back`, `safe`
   - required WIP patches
   - known upstream regressions
   - doctor/config hazards
   - plugin hook changes
   - validated probes
   - rollback target
4. Add every new landmine to the ledger and to `KNOWN-LANDMINES.md` the day it is discovered.

### Phase 1: Preflight snapshot automation

Build a scriptable preflight in the upgrade repo. It should capture:

1. `openclaw --version`
2. current global binary target (`which openclaw`, symlink target, npm link target)
3. `~/.openclaw` git status and HEAD
4. `~/.openclaw/openclaw.json` config fingerprint
5. `~/.openclaw/agents/main/agent/settings.json`
6. plugin health:
   - `op-secrets`
   - `memory-crystal`
   - `private-mode`
   - `tavily`
   - `compaction-indicator`
   - `session-export`
   - Bridge/lesa-bridge
7. memory database stats:
   - Memory Crystal `crystal.db` chunk count
   - OpenClaw memory-core `main.sqlite` size and key table row counts
8. service state:
   - LaunchAgent loaded state
   - gateway PID
   - recent gateway logs
9. current carry-patch status from the OpenClaw fork.

Output should be written to `open-claw-upgrade-private/logs/YYYY-MM-DD--preflight-<from>-to-<target>.md`.

### Phase 2: Version pin and fork strategy

Before any install:

1. Decide whether the target is:
   - latest stable tag
   - upstream main commit
   - WIP fork branch
   - rollback/pinned prior version
2. Verify the target is intentional. Do not confuse upstream main package version with a stable release tag.
3. Check whether every production-critical local patch is:
   - upstreamed
   - still fork-only and must carry
   - intentionally dropped
   - no longer needed after canary
4. If any critical patch remains fork-only, install from a built WIP fork worktree only. Do not use raw npm.

Current must-carry set:

1. chatCompletions routing via dm-scope header or `user=main`
2. next-turn queue for non-streaming chatCompletions
3. next-turn queue for streaming chatCompletions
4. runtime config boundary for OpenAI-compatible handler queue checks
5. memory-core `seedEmbeddingCache()` streaming with `.iterate()` until a promoted build contains upstream `983fd775e2`
6. memory-core cooperative yield during large seed until a promoted build contains upstream `983fd775e2`
7. memory-core bounded fallback vector scoring until a promoted build contains upstream `864c4f7ff4`

Do not reintroduce the broad final-resync fallback superseded by upstream #71293 unless a Bridge canary proves a remaining gap.

### Phase 3: Build and install discipline

The upgrade path is:

1. fetch upstream and tags
2. create an isolated worktree
3. rebase or cherry-pick the WIP patch stack
4. run `pnpm install --config.minimum-release-age=0`
5. run `pnpm build`
6. verify source invariants before install
7. install with `npm link` from the built worktree
8. verify `openclaw --version`

Do not run `npm install -g openclaw@latest` for Lēsa while latest stable lacks production-critical patches.

### Phase 4: Memory-core safety gate

Memory-core is a promotion blocker.

Required implementation:

1. Keep `seedEmbeddingCache()` bounded:
   - no `.all()` over `embedding_cache`
   - stream with `.iterate()` or move to lazy LRU
   - yield to event loop every N rows
2. Fix or track `listChunks()`:
   - no unbounded `.all()` over `chunks`
   - avoid selecting `embedding` unless required
   - stream or keyset paginate broad fallback scans
   - no `OFFSET` pagination on large tables
3. Add slow-query/large-row logging where OpenClaw patterns permit.

Promotion canary:

1. run the Day 63 style broad-memory path against a production-size copy or live-safe read path
2. verify no V8 heap OOM
3. verify no `StatementSync::All` crash signature
4. verify gateway PID stays stable
5. verify `/healthz` and `/readyz` remain responsive during seed
6. verify no healthcheck SIGKILL from one transient busy loop

### Phase 5: Bridge/chatCompletions compatibility

Bridge depends on the OpenAI-compatible chatCompletions endpoint and session routing.

Required behavior:

1. `model: "openclaw"` and `model: "openclaw/<agentId>"` work.
2. Bridge can route to the main session by supported header/user semantics.
3. Messages sent while the agent is busy are queued as next-turn work, not silently dropped.
4. Streaming and non-streaming chatCompletions share the same queue safety.
5. `x-openclaw-queued: next-turn` semantics remain honest. Do not call this true mid-turn steering.

Research, lower priority:

1. Decide whether true mid-turn interjection/cancellation is worth upstreaming.
2. If useful, file an upstream feature request separately.
3. Keep the current product contract as "next-turn queue" until true interjection exists.

### Phase 6: Failover/auth-state correctness

OpenClaw must not turn request-format errors into provider-wide billing cooldowns.

Required behavior:

1. HTTP 400 format errors are request-level failures.
2. Format errors do not set `disabledReason: "billing"`.
3. Format errors do not disable every model on the same provider.
4. Fallback should distinguish:
   - billing/quota
   - auth invalid
   - rate limit
   - payload format
   - provider transient
   - model unavailable
5. Add a regression test around `tool_use` without matching `tool_result` causing request failure but not provider cooldown.

Until fixed, the operator workaround remains clearing bad billing flags from `auth-state.json`, but this should become unnecessary.

### Phase 7: Claude CLI backend isolation

The Claude CLI backend is not safe for Lēsa until identity and session isolation are proven.

Current decision:

- Do not pursue the Apr 5 billing workaround. Parker tested it and Anthropic returned that third-party apps draw from extra usage, not plan limits.

Required before any future CLI-backend use:

1. The subprocess must not inherit CC's `~/.claude/CLAUDE.md`, memory, project rules, or identity.
2. Test whether `--bare` prevents identity contamination.
3. If not, use a separate config/home directory and separate login for Lēsa.
4. There must be one coherent session continuity model.
5. Billing or CLI subprocess failures must not rotate Lēsa into a fresh amnesic session.
6. Add an identity regression test:
   - fresh low-context Lēsa session
   - ask "who are you?"
   - must answer as Lēsa, not CC/Claude Code.

If these cannot be guaranteed, keep Lēsa on direct API/fork-supported runtime paths.

### Phase 8: Cost/control-plane safety

Non-interactive channels cannot satisfy interactive exec approvals.

Required behavior:

1. Disable or retire any cron that can fire shell exec from iMessage/webchat without approval support.
2. Replace shell exec delivery with first-class OpenClaw or Bridge tools where possible.
3. If exec is required, use a narrow allowlist with exact command/path constraints.
4. Any automated cron must have:
   - max retry count
   - cost budget
   - timeout
   - idempotency key
   - no orphan iMessage fragments on failure
5. Add an upgrade preflight check for enabled crons and their approval mode.

The brainstorm cron issue is folded here. Treat it as either retired or blocked until it can run without impossible approvals.

### Phase 9: Upstream and patch retirement

Every local patch must have a retirement path.

1. Maintain the Patch Tracking table in `UPGRADE-RUNBOOK.md`.
2. Submit upstream PRs where appropriate:
   - memory-core stream/yield
   - chatCompletions routing/next-turn queue
   - any remaining catalog pin if still needed
3. Open upstream issues where the fix is larger:
   - `listChunks()` broad recall materialization
   - restart/doctor config normalization stripping keys
   - failover/auth-state error classification
4. Stop carrying a patch only after:
   - upstream source is verified
   - fork branch is rebased past the upstream fix
   - Bridge/chatCompletions canary passes
   - memory-core canary passes where relevant
   - live config invariants survive doctor/restart.

### Phase 10: Config mutation safety

`openclaw doctor`, restart, and config normalization must be treated as mutators.

Required behavior:

1. Never run `openclaw doctor --fix` blind.
2. Always inspect `git diff` in `~/.openclaw` after doctor.
3. Prefer LaunchAgent kickstart over `openclaw gateway restart` until restart normalization is proven safe.
4. Add a config invariant checker for:
   - `memorySearch.remote` remains `{}`
   - gateway auth token or env token exists
   - Bridge queue mode is set
   - chatCompletions endpoint is enabled
   - trusted plugin `hooks.allowConversationAccess` flags are present
   - model/provider/fallback keys are preserved
   - image generation model/fallback settings are preserved
5. Longer term: move desired config into a deploy pipeline that can validate, diff, stamp writer identity, and fail closed.

### Phase 11: Promotion gates

A candidate OpenClaw build is promotable only if:

1. `pnpm build` succeeds.
2. relevant tests pass or are explicitly waived with reason.
3. `openclaw doctor` reports no critical issues.
4. `git diff` in `~/.openclaw` shows only expected changes.
5. `/healthz` and `/readyz` are healthy.
6. plugin health checks pass.
7. Bridge/chatCompletions smoke test passes.
8. next-turn queue canary passes while the agent is busy.
9. Memory Crystal capture still works.
10. private-mode state remains correct.
11. Day 63 memory-core canary passes when memory-core changed.
12. no impossible approval cron is enabled.
13. rollback command and rollback target are written before promotion.

### Phase 12: Archive the old ticket set

After this master ticket lands:

1. Move the superseded OpenClaw tickets listed above into `ai/product/bugs/openclaw/archive/`.
2. Keep `2026-04-24--kody--upstream-memory-core-packet.md` top-level as the active upstream packet.
3. Leave this master ticket as the only top-level OpenClaw upgrade-compatibility planning ticket.
4. Future focused implementation tickets may be filed only when they represent a separately owned patch/PR. Link them back here.

## Acceptance Criteria

- One top-level OpenClaw master ticket exists and references the superseded tickets.
- Superseded Apr 5+ OpenClaw tickets are archived, except the active upstream memory-core packet.
- Upgrade repo has a clear next-step plan for compatibility ledger, preflight automation, patch tracking, canary gates, and rollback.
- The plan distinguishes stock OpenClaw issues from WIP/LDM integration requirements.
- The plan states that raw npm OpenClaw upgrades are unsafe while fork-only production patches remain.
- The plan includes the memory-core OOM path, Bridge/chatCompletions queue requirements, Claude CLI identity/session risks, failover cooldown bug, cron exec approval issue, and upstream patch retirement.

## Immediate Next Actions

1. Add `COMPATIBILITY-LEDGER.md` to `open-claw-upgrade-private`.
2. Add `scripts/preflight-snapshot.sh` to `open-claw-upgrade-private`.
3. Add `scripts/verify-promotion-gates.sh` to `open-claw-upgrade-private`.
4. Update `UPGRADE-RUNBOOK.md` to call those scripts.
5. Build/canary current upstream `main` in isolation, because it contains accepted memory-core commits `983fd775e2` and `864c4f7ff4` while latest stable `v2026.4.26` does not.
6. If that canary passes, promote the post-`v2026.4.26` build and retire the redundant fork carry patches.
7. Open upstream OpenClaw issues/PRs for:
   - restart/doctor config mutation safety
   - format errors incorrectly affecting auth-state cooldown
