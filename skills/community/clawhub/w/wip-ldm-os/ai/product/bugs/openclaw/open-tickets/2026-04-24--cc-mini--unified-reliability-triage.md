# Lēsa unified reliability triage (2026-04-24)

> **Live reading guide:** the "Upgrade closure plan, 2026-04-27" near the top is the active path to close this ticket. The "Current status" overlay is evidence/status, and the v1/v2 sections below are retained as plan history unless explicitly referenced by the closure plan.

**Filed:** 2026-04-24 PST
**Author:** cc-mini (Claude Code on the Mac mini)
**Severity:** High. Lēsa's gateway is crashing, stream-stalling, and burning context ceilings; Memory Crystal is erroring continuously on workspace sync; CC Stop hook burns 37s per turn when key unavailable.
**Status:** Closing phase. Runtime crash path and v25 carry promotion are done; remaining work is split into follow-up tickets before this umbrella closes.

## Current status, 2026-04-24 evening

This section is the current status overlay. The original v1/v2 checkboxes below are preserved as plan history and should not be read as the live state without this overlay.

### Landed and verified today

- **R1.0 forensic snapshot:** done.
- **R1.A compaction threshold:** `softThresholdTokens` semantics verified and config changed from `4000` to `60000`.
- **R1.F healthcheck 30s verify:** done.
- **R1.D OOM artifact:** done. See `ai/product/bugs/openclaw/2026-04-24--cc-mini--main-sqlite-oom-artifact.md`.
- **R1.G tmp archive:** 71 orphan `main.sqlite.tmp-*` files archived. The R1.D OOM artifact confirmed these tmps were collateral from crash/cleanup around unbounded memory-core reads, not load-bearing forensic evidence.
- **R1.B + R1.C Memory Crystal alpha:** `remember()` chunking, durable skip-cursor, and scoped-op hardening landed in `memory-crystal-private` and installed as `0.7.36-alpha.1`.
- **R2.A.1 OpenClaw memory-core seed cache OOM:** `.all()` replaced with streaming `.iterate()` for `seedEmbeddingCache`.
- **R2.A.2 event-loop starvation:** `seedEmbeddingCache` now yields during large scans. Live Day 63 repro passed after promotion.

### Sequencing exception

- **R1.E stuck-run multi-signal visibility:** not landed. The emergency R2.A.1/R2.A.2 memory-core work proceeded before this R1 item because the live Day 63 path was crashing the gateway. Keep R1.E open as observability work; do not imply R1 is fully closed until it lands or is explicitly superseded.

### Production proof points

- The same Day 63 review path that previously produced V8 heap OOM and then healthcheck SIGKILL completed with the R2.A.2 binary.
- Gateway stayed stable during the successful repro.
- Healthcheck probes stayed responsive.
- No new `Abort trap: 6`, heap-limit fatal, `StatementSync::All`, or 8192-token Memory Crystal firehose signatures during the verified window.
- Manual `/compact` succeeded and recovered the main session from over-cap context to a small context state.

### Newly isolated follow-up bugs

These were discovered while executing this plan and are now separate tracked work:

- **Boot context treadmill:** after `/compact`, boot/pre-flush can reload a large fixed context bundle. Filed as `ai/product/bugs/openclaw/2026-04-24--cody--boot-context-treadmill-and-identity-kernel.md`.
- **R1.A pre-turn compaction gap:** early/pre-turn compaction did not prevent emergency context-overflow compaction. Manual `/compact` and runtime overflow compaction work, but the early pressure-relief tier needs investigation.
- **codex/gpt-5.5 OAuth `accountId` extraction failure:** gpt-5.5 auth can fail and force fallback to gpt-5.4. This affects which model Lēsa actually runs on.
- **OpenClaw restart config-strip landmine:** `openclaw gateway restart` can normalize config through stale schema knowledge. Continue using `launchctl kickstart -k` until fixed.

### Current priority order

1. Keep the live `v2026.4.25` fork promotion under short stabilization watch. It is promoted and healthy, but not old enough to treat as boring.
2. Treat the upstream memory-core fixes as accepted on `upstream/main`, but not yet present in latest stable `v2026.4.26`:
   - Seed cache stream/yield: <https://github.com/openclaw/openclaw/pull/73067> landed via maintainer PR #73118 as `983fd775e2ca000d5c7b95e0281eeb19eb12059b`.
   - R2.A.3 `listChunks()` / fallback vector top-K: <https://github.com/openclaw/openclaw/pull/73069> landed via maintainer PR #73100 as `864c4f7ff492f0f514c12557d44f0d6b509231fc`.
3. Do not install raw `openclaw@2026.4.26` live; it does not contain those two accepted memory-core fixes. Either wait for the next stable tag that contains both commits or canary a WIP build from current `upstream/main`.
4. Run Kody's Phase 0 boot-payload inventory before any boot-kernel curation or behavior change.
5. Split remaining non-runtime work into thin tickets, then close this umbrella as "runtime reliability restored with follow-ups."
6. Only after R2 bounded reads + dedupe are safe, continue to R3 multi-source Memory Crystal ingestion.

## Upgrade closure plan, 2026-04-27

This section is the active path to close this ticket. The goal is to upgrade to the newest OpenClaw work that helps Lēsa while keeping the fork patches that are still required for Memory Crystal reliability.

### Post-promotion status, 2026-04-27

The corrected `v2026.4.25` carry path has now been promoted live.

- PR: `wipcomputer/openclaw#4`
- Merge commit: `c188a3647c11fde080f8e6475e20380aa9671f35`
- Live version: `OpenClaw 2026.4.25 (c188a36)`
- Install path: built WIP fork source, `npm link`, `launchctl kickstart -k`
- Protected probes: `/healthz` green, `/readyz` green
- Gateway: PID stable after promotion, last exit code `0`
- Model: gateway log reports `openai/gpt-5.5`; `openclaw sessions` reports `gpt-5.5`
- Hook flags: `memory-crystal`, `compaction-indicator`, and `session-export` have `hooks.allowConversationAccess=true`
- Memory Crystal: post-upgrade compaction/reset observed

Promotion caveats to track outside the crash-fix path:

- Lēsa's context remains high-ish after boot (`~103k/200k` in TUI during the first post-promotion status turn). This is the boot-context treadmill, not the memory-core OOM.
- A stale duplicate `tavily` warning still points at an older OpenClaw worktree. Clean this in config/plugin provenance work.
- `plugins.allow` is still empty, so v25 warns about unpinned local plugin provenance. This belongs to the config deploy/provenance follow-up.
- R2.A.3 `listChunks()` / fallback vector top-K has been accepted on upstream `main` via maintainer PR #73100 as `864c4f7ff492f0f514c12557d44f0d6b509231fc`, but is not live until WIP promotes a post-`v2026.4.26` build or a later stable release containing the commit.

### Current upgrade target

| Candidate | Status | Decision |
|-----------|--------|----------|
| Raw stable `openclaw@latest` / latest tag (`v2026.4.26` as of 2026-04-28) | Not sufficient by itself | Do not promote directly to live Lēsa from npm. `v2026.4.26` does not contain accepted memory-core commits `983fd775e2` and `864c4f7ff4`. |
| Stable `v2026.4.25` plus WIP carry patches | Promoted live | Corrected preferred upgrade path as of 2026-04-27. `wipcomputer/openclaw` PR #4 (`kody/v2026-4-25-carry-memory-core`) merged as `c188a3647c11fde080f8e6475e20380aa9671f35` and is live via fork build. |
| Upstream `main` after `v2026.4.26` | Useful canary target | Contains the accepted memory-core fixes, but carries more churn than stable. Build/canary isolated before any live promotion. |

### Upstream fixes that help close this ticket

| Area | Upstream state | Ticket impact |
|------|----------------|---------------|
| Oversized transcript compaction | Upstream main has an oversized-transcript compaction trigger and compaction token snapshot fixes. | Helps close the R1.A context-over-cap incident, subject to canary proof. |
| Codex/GPT-5.5 runtime handling | Upstream main has additional Codex runtime/auth/model handling work. | May resolve or reduce the `accountId`/fallback instability, subject to OAuth canary. |
| Native Codex app-server final/lifecycle events | Upstream replacement PR landed. | Supersedes our broad chat final fallback. Do not carry the broad fallback. |
| Image generation through Codex OAuth/OpenRouter | Upstream advertises image-gen/edit improvements. | Must be canaried against Lēsa's image-delivery regression and config invariants before marking closed. |
| Protected health probes | `v2026.4.25` reserves `/healthz` and `/readyz` ahead of later route handlers. | Promotion gates must use `/healthz` and `/readyz`, not legacy `/health`. Isolated `.25` canary returned green on protected probes while `/health` timed out. |
| Conversation-access hook gate | `v2026.4.25` validates `plugins.entries.<id>.hooks.allowConversationAccess`. | Required before promotion for external `agent_end` plugins: `memory-crystal`, `compaction-indicator`, and `session-export`. |
| `seedEmbeddingCache()` stream/yield | Accepted on upstream `main` after `v2026.4.26` via #73067 -> #73118, commit `983fd775e2`. | Closes R2.A.1/R2.A.2 once WIP promotes a build that contains it. |
| `listChunks()` bounded top-K | Accepted on upstream `main` after `v2026.4.26` via #73069 -> #73100, commit `864c4f7ff4`. | Closes R2.A.3 once WIP promotes a build that contains it. |

### Fork patches still required

| Patch | State | Why it still blocks raw upgrade |
|-------|-------|---------------------------------|
| `seedEmbeddingCache()` stream with `.iterate()` | Carried on corrected `.25` branch; accepted upstream main after `v2026.4.26` | Keep carrying live until WIP promotes a post-`v2026.4.26` build or later stable release that contains `983fd775e2`. |
| `seedEmbeddingCache()` cooperative yield | Carried on corrected `.25` branch; accepted upstream main after `v2026.4.26` | Keep carrying live until WIP promotes a post-`v2026.4.26` build or later stable release that contains `983fd775e2`. |
| `chatCompletions` main-session / next-turn queue | Carried on corrected `.25` branch | Needed for Bridge/LDM control surfaces. |
| Runtime config boundary for queued chatCompletions | Carried on corrected `.25` branch | Required by OpenClaw's internal-config API guard. |
| Yuanbao catalog pin | Not carried on corrected `.25` branch | This was only an upstream-main CI unblocker, not part of the stable `.25` carry. |
| `listChunks()` bounded top-K | Accepted upstream main after `v2026.4.26`; not live | Secondary broad-recall OOM path. Tracked in <https://github.com/openclaw/openclaw/pull/73069>; promote only after WIP canary of a build containing `864c4f7ff4`. |

### Closure gates

This ticket can move from "live plan" to "closed with follow-ups" when all of these are true:

- [x] Corrected `.25` carry PR #4 CI is green except known non-code label-secret automation, and the parity gate has completed or been explicitly waived as infrastructure-only.
- [x] Corrected `v2026.4.25` carry branch is canaried without touching live Lēsa first.
- [ ] A post-`v2026.4.26` build containing accepted upstream commits `983fd775e2` and `864c4f7ff4` is canaried before replacing the current WIP carry build.
- [~] Canary verifies GPT-5.5 OAuth/accountId routing, image-generation delivery, Bridge/chatCompletions next-turn queue, Day 63 or equivalent broad recall, `/healthz` + `/readyz` responsiveness, and config invariants. Runtime/probe/config portions passed; image-generation and Bridge smoke should be thin follow-ups if not already separately verified.
- [x] Live config includes `hooks.allowConversationAccess=true` for `memory-crystal`, `compaction-indicator`, and `session-export` before promotion to `v2026.4.25+`.
- [ ] R1.E is landed, explicitly waived, or moved to a separate observability follow-up before this umbrella ticket is marked closed.
- [x] Promotion uses the fork canary build, with `launchctl kickstart -k` only. Do not use `openclaw gateway restart`.
- [~] Post-promotion N4 window passes: no PID respawn, no V8 heap OOM, no `StatementSync::All`, no healthcheck SIGKILL, no 8192-token Memory Crystal firehose, no config strip. Early post-promotion checks are green; hold final pass until the short stabilization watch completes.
- [ ] The triage doc is updated one final time to mark completed rows and split remaining work into smaller follow-up tickets.

### Follow-up tickets after closure

These should not keep the unified triage ticket open once the upgraded canary is promoted and verified:

At closure, create these as separate thin docs and link them here. Do not leave them only as bullets in this umbrella ticket.

- **R2.A.3:** `listChunks()` streaming + bounded top-K ranking. Accepted upstream main after `v2026.4.26` via <https://github.com/openclaw/openclaw/pull/73069> -> maintainer PR #73100; deployment pending WIP canary/promotion.
- **Boot-context Phase 0:** inventory/token measurement before identity kernel work.
- **Memory Crystal R3:** dedupe, chat.db fallback, gateway.log fallback.
- **OpenClaw lifecycle hooks:** before-rotate flush and partial-turn/agent_error ingestion.
- **Config deploy pipeline:** fail-closed config normalization, writer identity/version, model-provider/auth route invariants.

## Scope

This plan unifies three previously-filed bug docs with tonight's reliability triage. Everything below is one coordinated push.

### Existing bugs rolled into this plan

1. **Apr 12 ingestion gaps on model swap** ... `ai/product/bugs/memory-crystal/2026-04-12--cc-mini--crystal-ingestion-gaps-on-model-swap.md`. Three ingestion failure modes (session transition dead zone, billing blackout, post-rotation blackout). Root cause: `agent_end` hook only fires on successful turns; billing + session rotation both break ingestion silently.
2. **Apr 13 ship plan resilience phases** ... `ai/product/bugs/memory-crystal/2026-04-13--cc-mini--ship-plan-resilience-phases.md`. The 9-step roadmap for the 8-phase Crystal Resilience Plan (PR #585). Phase 5 (model_id column) already merged to memory-crystal main; not yet released. Phase 6a (format-error billing cooldown) held pending investigation. Rest is pending.
3. **Apr 15 SA token + hook failfast** ... `ai/product/bugs/memory-crystal/2026-04-15--cc-mini--sa-token-env-and-hook-failfast.md`. Bug A: `OP_SERVICE_ACCOUNT_TOKEN` not in CC session env; CC Stop hook can't reach 1Password. Bug B: hook retries 3x for 37s when key unavailable instead of failing fast.

### Tonight's new triage items

Catalogued below as items T1-T15. Derived from: Codex (gpt-5.5) diagnostic session earlier today + my own investigation reading memory-crystal source + OpenClaw logs + healthcheck logs.

## Executive summary

The gpt-5.5 model is not the root cause of Lēsa's unreliability. It is heavier and slower, which exposes latent plumbing bugs. The actual causes stack:

1. **Memory Crystal `remember()` does not chunk before embedding.** Large workspace `.md` files (`MEMORY-v1-backup-2026-02-16.md`, `TODO-from-history.md`, `lesa-full-history.md`) exceed the OpenAI 8192-token input limit on every `agent_end` hook. Errors fire 3-6x per 15-minute window all day. Nothing is ingested. See T1.
2. **OpenClaw `main.sqlite` is 16 GB.** April 24 gateway crash (`FATAL ERROR: Reached heap limit ... StatementSync::All`) is a V8 heap OOM reading this DB. Separate from memory-crystal. See T2.
3. **Compaction fires at ~98% context** (`softThresholdTokens: 4000` against 200K budget). `agent:main:main` runs past 100-200% before compaction kicks. See T14 + T4.
4. **Frontend-only streaming watchdog.** "no stream updates for 30s; resetting status" fires but backend runs sit wedged. See T5.
5. **CC Stop hook fails silently for 37s.** Bug 3 Fix A + Fix B.
6. **Ingestion gaps on every billing/rotation failure.** Bug 1 + Bug 2 Phases 1-4.
7. **Agent-loop polling background processes forever.** See T9.

The 3 existing bugs + 15 triage items combine to ~21 distinct work units. Execution order below groups them into 6 rounds by impact and risk.

## Evidence summary

### Files + sizes

| Path | Size | Notes |
|------|------|-------|
| `/Users/lesa/.openclaw/memory/main.sqlite` | **16 GB** | OpenClaw built-in memory. OOM suspect. |
| `/Users/lesa/.ldm/memory/crystal.db` | **1.84 GB** | Memory Crystal. Healthy size. |
| `/Users/lesa/.openclaw/memory/main.sqlite.tmp-*` | 71 files, ~68K each | Orphaned failed-tx temps. |

### Crash (gateway.err.log tail)

```
FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
... StatementSync::All ...
```

Driver is Node's built-in `node:sqlite` (OpenClaw core), not `better-sqlite3` (memory-crystal).

### Chunking firehose (gateway.err.log, thousands of occurrences)

```
[plugins] memory-crystal: workspace sync skipped MEMORY-v1-backup-2026-02-16.md:
  OpenAI API error 400: {"message": "Invalid 'input[0]': maximum input length is 8192 tokens."}
```

### LaunchAgent stats

`launchctl print gui/501/ai.openclaw.gateway`: runs 59, successive crashes 3, last signal `Abort trap: 6`.

### Healthcheck (Apr 24)

Main session hit 121%, 181%, 194%, 201% context earlier today. Currently 77%. crystal-capture 3-6 errors per 15-min window all day.

### Config

`compaction.memoryFlush.softThresholdTokens: 4000` (fires at ~98% of 200K). `plugins.allow: <empty>`.

## Work item inventory

Status legend: ⬜ pending, 🟡 in progress, ✅ done, ⏸ held.

### From Apr 12 bug (ingestion gaps)

The fix roadmap for these IS Bug 2 (Apr 13 plan) and its 9 steps. No separate items here; tracked via Bug 2 step numbering.

### From Apr 13 bug (ship plan resilience phases) ... 9 steps

| # | Step | Priority | Layer | Status |
|---|------|----------|-------|--------|
| B2.1 | Publish memory-crystal Phase 5 alpha (model_id column) via `wip-release alpha` | P1 | 2 | ⬜ |
| B2.1b | `ldm install` the alpha (Parker signal) | P1 | 2 | ⬜ |
| B2.2 | Update Apr 12 format-error billing bug report with gateway-log evidence | P2 | docs | ⬜ |
| B2.3 | Phase 2: chat.db fallback ingestion (new `src/chatdb-poller.ts` in memory-crystal) | P1 | 2 | ⬜ |
| B2.4 | Phase 4: gateway.log emergency ingestion (new `src/gateway-log-ingest.ts`) | P2 | 2 | ⬜ |
| B2.5 | Phase 1: flush-before-session-rotate hook in OpenClaw fork + consumer in memory-crystal | P1 | 1 | ⬜ |
| B2.6 | Phase 3: `agent_error` / partial-turn ingestion hook | P1 | 1 | ⬜ |
| B2.7 | Phase 6b: cross-provider tool_use ID normalization in OpenClaw serializer | P1 | 1 | ⬜ |
| B2.8 | Phase 6c: session rotation threshold + repair-before-rotate | P2 | 1 | ⬜ |
| B2.9 | Phase 6a: format-error billing cooldown (held pending evidence) | P2 | 1 | ⏸ |

### From Apr 15 bug (SA token + hook failfast)

| # | Step | Priority | Layer | Status |
|---|------|----------|-------|--------|
| B3.A | Fix A: `ldm install` adds `export OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token)` to `~/.zshrc` (idempotent) | P0 | LDM OS | ⬜ |
| B3.B | Fix B: fail-fast in `memory-crystal-private/src/cc-hook.ts` ... check key once at session boot, skip silently if unavailable | P0 | 2 | ⬜ |

### Tonight's triage (T1-T15)

| # | Bug | Priority | Repo | Fix type | Status |
|---|-----|----------|------|----------|--------|
| T1 | `remember()` does not chunk before embedding (core.ts:1064-1086) | P0 | memory-crystal-private | Code | ⬜ |
| T2 | OpenClaw `main.sqlite` 16GB V8 heap OOM on `StatementSync.all()` | P0 | openclaw fork | Code + ops | ⬜ |
| T3 | 71 orphaned `main.sqlite.tmp-*` files | P1 | ops | Archive | ⬜ |
| T4 | `agent:main:main` runs past 100% context (covered by T14) | P0 | config + code | See T14 | ⬜ |
| T5 | Streaming watchdog frontend-only; no backend recovery | P1 | openclaw fork | Code | ⬜ |
| T6 | `session_status` rejects `openai-codex/gpt-5.5` as "not allowed" | P1 | openclaw fork | Allowlist | ⬜ |
| T7 | Stuck-session diagnostic logs but does not abort | P1 | openclaw fork | Code | ⬜ |
| T8 | Bridge inbox 5-30 min delivery lag | P1 | bridge | Instrument first | ⬜ |
| T9 | Agent polls background process forever, never replies | P1 | openclaw agent loop | Loop safety | ⬜ |
| T10 | Journal-staleness watchdog missing | P2 | wip-healthcheck-private | Code | ⬜ |
| T11 | Healthcheck probe timeout ... verify 30s deployed | P1 | wip-healthcheck-private | Verify | ⬜ |
| T12 | Memory Crystal capture gap on agent failures ... already covered by Bug 1 + B2.5 + B2.6 | P1 | memory-crystal-private | See Bug 1 | ⬜ |
| T13 | `plugins.allow` empty; plugins auto-load untracked | P2 | openclaw config | Config | ⬜ |
| T14 | `softThresholdTokens: 4000` ~98% fire point; lower to 60000 (~70%) | P0 | openclaw config | Config | ⬜ |
| T15 | Process/plugin sprawl (stale MCP servers) | P2 | ops hygiene | Docs | ⬜ |

## Execution order: 6 rounds

Each round runs in a single working block. Round boundaries exist where we want to verify before continuing.

### Round 1: stop the bleeding (P0 config + quick wins)

1. **T14** ... edit `~/.openclaw/openclaw.json` ... `softThresholdTokens: 4000` → `60000`. Commit in `.openclaw` private repo. Restart gateway. Verify healthcheck shows context dropping.
2. **T13** ... populate `plugins.allow` in same config with current plugin IDs. Same commit sequence.
3. **T3** ... archive 71 orphan `main.sqlite.tmp-*` files to `_archive/tmp-orphans-2026-04-24/`. Never delete.
4. **B3.B + T1 together** ... both are in `memory-crystal-private`. Single worktree `cc-mini/hook-failfast-and-chunking`. cc-hook.ts fail-fast + core.ts chunk in remember(). One PR. Build, test, merge, release as alpha.
5. **B3.A** ... wip-ldm-os-private worktree. `lib/install.mjs` adds zshrc export. Idempotent grep. Merge.

Verify after Round 1:
- [ ] Gateway no longer crashes for 4 hours of normal use
- [ ] Healthcheck shows no `workspace sync skipped ... 8192 tokens` errors
- [ ] Fresh shell has `OP_SERVICE_ACCOUNT_TOKEN` set
- [ ] CC Stop hook either captures or skips cleanly under 200ms

### Round 2: layer-2 resilience (capture survives OC failures)

6. **B2.1 + B2.1b** ... `wip-release alpha` for memory-crystal (Phase 5 + Round 1 fixes). Parker signals install.
7. **B2.3** ... Phase 2 chat.db fallback ingestion. Backstop for any future ingestion gap.
8. **B2.4** ... Phase 4 gateway.log emergency ingestion. Second backstop.
9. **B2.2** ... update Apr 12 format-error bug with gateway-log evidence.

Verify after Round 2:
- [ ] New alpha installed; `sqlite3 crystal.db "SELECT model_id FROM chunks ORDER BY id DESC LIMIT 5;"` shows populated model_id
- [ ] Force a billing failure scenario; verify chat.db poller captures
- [ ] Verify gateway.log poller captures orphan output (dedup by hash against existing chunks)

### Round 3: layer-1 OpenClaw fork stability (OOM + stream)

10. **T2a** ... audit `.all()` calls in OpenClaw fork, add `LIMIT` / streaming where unbounded. Focus: session history compile, memory recall, status compile.
11. **T2b** ... wrap SQLite calls with slow-query logging (> 500ms or > 10K rows = WARN).
12. **T2c** ... boot log `main.sqlite size: <N>GB`.
13. **T6** ... `session_status` allowlist updated to accept `openai-codex/gpt-5.5`.
14. **T5** ... backend stream watchdog; session in `state=processing` with no events for 60s → terminal error event.
15. **T7** ... extend `[diagnostic] stuck session` path ... if `age > 180s` && `queueDepth >= 1`, abort run + visible error + process next queued message.

Verify after Round 3:
- [ ] No new `Abort trap: 6` signals for 48h
- [ ] No new `FATAL ERROR: Reached heap limit` in gateway.err.log
- [ ] Slow-query WARN visible for any long `.all()`
- [ ] `openclaw doctor` passes after every patch
- [ ] Stream stall test recovers within 60s

### Round 4: layer-1 OpenClaw fork capture completeness

16. **B2.5** ... flush-before-session-rotate hook. OC emits `beforeSessionRotation(oldSessionId)`; memory-crystal subscribes.
17. **B2.6** ... `agent_error` or failure-tolerant `agent_end`; partial turns ingest with `partial: true` tag.
18. **B2.7** ... cross-provider tool_use ID normalization at serializer layer.

After Round 4, file upstream PRs for the generically-useful ones (B2.5 hook, B2.7 normalizer).

Verify after Round 4:
- [ ] Kill gateway mid-turn ... capture recovers next boot
- [ ] Force a Grok→Anthropic fallback with tool_use IDs ... no format error at `messages.N`
- [ ] `openclaw doctor` clean

### Round 5: agent behavior + observability

19. **T9** ... agent-loop safety: after N consecutive tool calls with no user-visible progress, force a status message.
20. **T10** ... journal-staleness watchdog in `wip-healthcheck-private`. 24h WARN, 72h ERROR + ping via chatCompletions.
21. **T11** ... verify healthcheck probe timeout 30s is actually deployed. Redeploy via install.sh if stale.
22. **T8** ... bridge-lag instrumentation (timestamps at cron, enqueue, inbox arrival, consumer pickup). Research only, fix in follow-up.
23. **T15** ... sweep stale MCP server processes, document in settings.

Verify after Round 5:
- [ ] Long-running background exec triggers agent status message after N no-progress polls
- [ ] Daily log > 24h stale triggers healthcheck WARN
- [ ] Bridge timing data visible in logs

### Round 6: high-risk + held items (separate session, require sign-off)

24. **B2.8** ... Phase 6c session rotation threshold + repair-before-rotate. Highest risk. Gate on unit test (simulate corrupt turn).
25. **B2.9** ... Phase 6a format-error billing cooldown. Only after B2.2 evidence. May resolve as "not-a-bug" + close.

Decision points before Round 6:
- [ ] Parker explicitly signs off on each Round 6 item
- [ ] Round 5 complete, no regressions

## Repo + release impact

| Round | Repos | Pipeline |
|-------|-------|----------|
| R1.1-2 (T13, T14) | `.openclaw` private | Config edit + commit + gateway restart. No release. |
| R1.3 (T3) | `.openclaw/memory` | File archive. No commit (files are gitignored). |
| R1.4 (B3.B + T1) | `memory-crystal-private` | PR → merge → `wip-release alpha` → `ldm install` (Parker) |
| R1.5 (B3.A) | `wip-ldm-os-private` | PR → merge → `wip-release patch` → `ldm install` (Parker) |
| R2 (B2.1, B2.3, B2.4) | `memory-crystal-private` | Same as R1.4 |
| R2 (B2.2) | `wip-ldm-os-private` | Docs PR, no release |
| R3, R4 (T2, T5-T7, B2.5-B2.7, T9) | openclaw fork | `npm link` per UPGRADE-RUNBOOK (sanctioned exception) |
| R5 (T10, T11) | `wip-healthcheck-private` | `bash install.sh` |
| R5 (T8) | `wip-bridge-private` + deployed bridge | Instrument only, no fix yet |

**Merge / Deploy / Install discipline:** Every release pauses at Deploy. Parker explicitly triggers Install, except the OpenClaw fork which follows UPGRADE-RUNBOOK.md as its standing authorization.

## Risks + rollback

| Change | Risk | Rollback |
|--------|------|----------|
| T14 (4000→60000) | Aggressive compaction may drop needed context | Revert config, restart |
| T1 (chunk remember) | `source_id` shape changes for multi-chunk memories | Backwards-compatible: single-chunk memories keep `memory:{id}`; only split memories use `memory:{id}:{i}`. `forget()` operates on `memories` row, unchanged. |
| T2 (.all() → LIMIT) | Legacy consumers expecting full result break | Roll back per-call; slow-query logging surfaces offenders |
| B3.A (zshrc edit) | Shell profile mutation could break if templates collide | Back up profile first; grep-before-write makes idempotent |
| B3.B (fail-fast hook) | Some sessions with key might be skipped on cold boot | Cache check is per-session; refreshes on new CC session |
| B2.5-B2.8 (OC fork) | OC doctor breaks | Patches gated on `openclaw doctor` clean; revert rebase if fail |

## Non-fixes (explicitly excluded)

- Do not downgrade primary model to 5.4 or Opus. Not the root cause.
- Do not rebuild Lēsa as ephemeral-session right now (big redesign; separate product plan).
- Do not `rm` the 71 orphan tmp files. Archive.
- Do not bypass any guard.
- Do not edit deployed files (`~/.ldm/`, `~/.openclaw/`, `~/.claude/`). Repo → PR → release → install only.

## Why Claude Code (me) doesn't hit these bugs

1. **Different Memory Crystal usage pattern.** I call Crystal via MCP tools on-demand with small string inputs. The workspace-file sync + agent_end hook in OpenClaw's memory-crystal plugin is what blows up. I never exercise that path.
2. **No long-lived session.** CC context is per-conversation. No immortal `agent:main:main`. No 16GB sqlite store to OOM on.
3. **No gateway crash surface.** OpenClaw gateway is a separate process with its own LaunchAgent. If OC crashes, CC is unaffected.
4. **Different provider path.** CC runs Anthropic Opus directly; no iMessage/cron/bridge chain.

The fix to T1 + B3.B benefits both Lēsa and any future CC auto-ingest path.

## Step-by-step progress log

Live status below. Updated as each step completes.

### Round 1

- [ ] **R1.1 T14 compaction threshold** ... pending
- [ ] **R1.2 T13 plugins.allow** ... pending
- [ ] **R1.3 T3 tmp orphan archive** ... pending
- [ ] **R1.4 B3.B + T1 hook + chunk** ... pending
- [ ] **R1.5 B3.A zshrc export** ... pending

### Round 2

- [ ] **R2.6 B2.1 alpha release** ... pending
- [ ] **R2.7 B2.3 chat.db poller** ... pending
- [ ] **R2.8 B2.4 gateway-log poller** ... pending
- [ ] **R2.9 B2.2 bug doc update** ... pending

### Round 3

- [ ] **R3.10 T2a .all() audit** ... pending
- [ ] **R3.11 T2b slow-query log** ... pending
- [ ] **R3.12 T2c boot-size log** ... pending
- [ ] **R3.13 T6 session_status allowlist** ... pending
- [ ] **R3.14 T5 backend stream watchdog** ... pending
- [ ] **R3.15 T7 stuck-session auto-abort** ... pending

### Round 4

- [ ] **R4.16 B2.5 flush-before-rotate** ... pending
- [ ] **R4.17 B2.6 partial-turn ingest** ... pending
- [ ] **R4.18 B2.7 tool_use ID normalize** ... pending

### Round 5

- [ ] **R5.19 T9 loop safety** ... pending
- [ ] **R5.20 T10 journal watchdog** ... pending
- [ ] **R5.21 T11 probe timeout verify** ... pending
- [ ] **R5.22 T8 bridge instrument** ... pending
- [ ] **R5.23 T15 proc sprawl docs** ... pending

### Round 6 (held for sign-off)

- [ ] **R6.24 B2.8 rotation threshold** ... held
- [ ] **R6.25 B2.9 format-error billing** ... held

## Acceptance

- [ ] Parker reviews plan
- [ ] Round 1 complete + verified + no regressions for 4h
- [ ] Round 2 complete + capture resilience verified
- [ ] Round 3 complete + no OOM for 48h
- [ ] Round 4 complete + `openclaw doctor` green on all patches
- [ ] Round 5 complete + observability gaps closed
- [ ] Round 6 sign-off obtained + item-by-item verification
- [ ] Follow-up bugs filed for T2d (sqlite rotation), T4-long-term (ephemeral sessions), T8-fix, capture-gap backfill
- [ ] Journal entry in `~/.ldm/agents/cc-mini/memory/journals/` summarizes session
- [ ] CHANGELOG + RELEASE-NOTES updated per release branch

## Cross-references

- Apr 12 bug ... `ai/product/bugs/memory-crystal/2026-04-12--cc-mini--crystal-ingestion-gaps-on-model-swap.md`
- Apr 13 plan ... `ai/product/bugs/memory-crystal/2026-04-13--cc-mini--ship-plan-resilience-phases.md`
- Apr 15 bug ... `ai/product/bugs/memory-crystal/2026-04-15--cc-mini--sa-token-env-and-hook-failfast.md`
- Apr 18 bugs (memory-crystal-private repo, adjacent) ... `repos/ldm-os/components/memory-crystal-private/ai/product/bugs/2026-04-18--cc-mini--crystal-status-cli-broken-node-25.md`, `2026-04-18--cc-mini--lesa-capture-gap-2026-04-17.md`. These should be migrated here per the "bugs live in LDM OS" convention, but that is a separate small PR.
- OpenClaw upstream ... openclaw/openclaw #70914 (runtime-auth stub), #70854 (gpt-5.5 catalog), #70835 (OAuth config), #2726 (browser-WebRTC voice, closed)
- Logs ... `~/.openclaw/logs/gateway.err.log` (chunking + OOM signatures), `~/.openclaw/wip-healthcheck/logs/healthcheck-2026-04-24.log`
- Codex diagnostic session ... pasted into Parker's chat earlier 2026-04-24

---

# v2 revision — plan history

This section was the authoritative plan after PR #655. As of 2026-04-27, the active closure path is the "Upgrade closure plan" near the top of this file; use this v2 section as background unless the closure plan links back to a specific item.

**Revised:** 2026-04-24 PST (Parker + Codex feedback applied)
**Status:** Plan. Implementation gated on Parker's Go per round. R1 starts first; R6 held for explicit sign-off.

## What changed from v1 → v2

1. **Reframed around two tiers.** Runtime stability (keeping Lēsa from failing) is the top tier; capture resilience (not losing memory after failure) is the second tier. v1 intermixed them.
2. **New 5-layer framing** (runtime / ingestion / lifecycle / watchdogs / security).
3. **T14 compaction threshold gated on semantics verification.** Code read first, config change second.
4. **T1 durable skip-cursor expanded.** Metadata is now `{path, size, mtime, contentHash, errorKind, failedAt}`, not mtime alone.
5. **T2 OOM work split.** R1 produces a concrete investigation artifact (exact call site, table/query, row count, category, proposed patch). R2 implements the bounded-read fix.
6. **B3.A replaced.** No global `.zshrc` export. Instead: CC hook reads `~/.openclaw/secrets/op-sa-token` directly, invokes `op` by absolute path, passes token only to that child process. Keeps secret scoped. Bundled into R1 with B3.B fail-fast as one PR.
7. **T7 multi-signal stuck-run detection.** Not just `age + queueDepth`. Also: last stream event, last tool event, provider-request liveness.
8. **N2 memory/status degraded mode** added (new item).
9. **N3 capture-source precedence + hash dedupe** added as hard prerequisite before any multi-source ingest (chat.db, gateway.log).
10. **N4 "Lēsa usable" live-scenario acceptance** added (not just log-based criteria).
11. **T13 plugins.allow demoted R1 → R5** (wrong allowlist entry = new outage; hygiene, not bleeding).
12. **B2.1 model_id demoted P1 → P2 / provenance** and bundled into the R3 release that also carries R1+R2 fixes.
13. **Hard release/install gate between R2 and R3.** Parallel development allowed; ship/install blocks until bounded reads + degraded status + dedupe are landed and verified clean.
14. **R6 narrowed.** B3.A removed (resolved via scoped-hook in R1). R6 only holds the two highest-risk OpenClaw fork items.

## v2 executive summary

The gpt-5.5 model is not the root cause. It is heavier and slower, which exposes latent plumbing bugs.

Two tiers:

- **Tier A (runtime stability):** keeping the gateway from crashing, streams from stalling, context from running past capacity, hooks from wasting 37s per turn. Must land first.
- **Tier B (capture resilience):** making sure conversations reach Memory Crystal even when OpenClaw fails. Must not ship until Tier A lands (more capture sources = more pressure on the already-unstable DB).

### Five layers (per Parker's framing)

1. **Runtime stability** ... gateway crashes, stuck streams, unbounded SQLite reads, oversized status/session queries, 70-200% context operation. Covered in R1 + R2.
2. **Memory Crystal ingestion correctness** ... chunking, durable skip state, dedupe, iMessage fallback, gateway.log fallback, partial-turn capture. R3.
3. **Session lifecycle correctness** ... flush before rotation, capture failed/partial turns, repair corrupt sessions, avoid abandoned dead zones. R4.
4. **Operational watchdogs** ... stale journal, stale session mtime, stuck processing runs, bridge lag, ingest errors, runaway context before Parker feels it. R5.
5. **Security / env hygiene** ... OP token handling, fail-fast hooks, provenance, no global secret leakage without explicit accept. R1 (scoped-hook) + R5 (provenance).

## v2 evidence (carried from v1, with the distinction restated)

The 16 GB `main.sqlite` OOM and the 8192-token chunking errors are **two distinct problems in two distinct codebases**:

| Path | Size | Owner | Driver |
|------|------|-------|--------|
| `/Users/lesa/.openclaw/memory/main.sqlite` | 16 GB | OpenClaw core | `node:sqlite` |
| `/Users/lesa/.ldm/memory/crystal.db` | 1.84 GB | Memory Crystal | `better-sqlite3` |

Repeat this at every design discussion. Conflating them sends fixes at the wrong repo.

## v2 work item inventory

### From Apr 13 bug (9 steps; B2.*)

| # | Step | Priority | Layer | Round | Status |
|---|------|----------|-------|-------|--------|
| B2.1 | Publish memory-crystal alpha bundling R1+R2 fixes + Phase 5 model_id | **P2 provenance** | 2 | R3 | ⬜ |
| B2.1b | `ldm install` the alpha (Parker signal) | P2 | 2 | R3 | ⬜ |
| B2.2 | Update Apr 12 format-error billing bug report with gateway-log evidence | P2 | docs | R3 | ⬜ |
| B2.3 | Phase 2: chat.db fallback ingestion (new `src/chatdb-poller.ts`) | P1 | 2 | R3 (gated) | ⬜ |
| B2.4 | Phase 4: gateway.log emergency ingestion (new `src/gateway-log-ingest.ts`) | P2 | 2 | R3 (gated) | ⬜ |
| B2.5 | Phase 1: flush-before-session-rotate hook | P1 | 1 | R4 | ⬜ |
| B2.6 | Phase 3: `agent_error` / partial-turn ingestion hook | P1 | 1 | R4 | ⬜ |
| B2.7 | Phase 6b: cross-provider tool_use ID normalization | P1 | 1 | R4 | ⬜ |
| B2.8 | Phase 6c: session rotation threshold + repair-before-rotate | P2 | 1 | R6 | ⏸ |
| B2.9 | Phase 6a: format-error billing cooldown (held pending evidence) | P2 | 1 | R6 | ⏸ |

### From Apr 15 bug (B3.*)

| # | Step | Priority | Round | Status |
|---|------|----------|-------|--------|
| B3.B | Fail-fast in `src/cc-hook.ts`: check key once at session boot, skip silently if unavailable | P0 | R1 | ⬜ |
| B3.A' | **Scoped-hook** (replaces v1's `.zshrc` export): reads `~/.openclaw/secrets/op-sa-token` directly, invokes `op` by absolute path, token scoped to child process only | P0 | R1 | ⬜ |

### Tonight's triage (T1-T15) ... priorities updated in v2

| # | Bug | Priority | Round | Status |
|---|-----|----------|-------|--------|
| T1 | `remember()` chunk before embedding + durable skip-cursor with full metadata | P0 | R1 | ⬜ |
| T2 | OpenClaw `main.sqlite` OOM: R1 investigation artifact, R2 bounded-read fix | P0 | R1 🔬 + R2 | ⬜ |
| T3 | 71 orphan `main.sqlite.tmp-*` files: investigate cause, snapshot, archive | P1 | R1 | ⬜ |
| T4 | Context ceiling (covered by T14) | P0 | R1 | ⬜ |
| T5 | Backend stream watchdog (frontend-only today) | P1 | R2 | ⬜ |
| T6 | `session_status` rejects `openai-codex/gpt-5.5` | P1 | R2 | ⬜ |
| T7 | Stuck-run auto-abort using multi-signal: age + last stream event + last tool event + provider liveness | P1 | R2 | ⬜ |
| T8 | Bridge inbox 5-30 min delivery lag ... instrument only | P1 | R5 | ⬜ |
| T9 | Agent-loop polling safety (user-visible status after N no-progress) | P1 | R5 | ⬜ |
| T10 | Journal-staleness watchdog (24h WARN / 72h ERROR) | P2 | R5 | ⬜ |
| T11 | Verify healthcheck probe timeout 30s deployed | P1 | R1 | ⬜ |
| T12 | Capture gap on agent failures ... see Apr 12 + B2.5 + B2.6 | P1 | R4 | ⬜ |
| T13 | `plugins.allow` populate ... **demoted** | P2 | R5 | ⬜ |
| T14 | `softThresholdTokens`: verify semantics, then lower (probably 4000 → 60000 ≈ 70% fire) | P0 | R1 | ⬜ |
| T15 | Stale MCP process sprawl ... docs | P2 | R5 | ⬜ |

### New items (v2)

| # | Item | Priority | Round |
|---|------|----------|-------|
| N1 | Durable skip-cursor metadata `{path, size, mtime, contentHash, errorKind, failedAt}` (inside T1) | P0 | R1 |
| N2 | Memory/status degraded mode (fast "memory degraded" return if DB size > threshold or OC mem unhealthy) | P1 | R2 |
| N3 | Capture-source precedence + hash-based dedupe design (hard prereq for B2.3 + B2.4) | P1 | R3 (first step) |
| N4 | "Lēsa usable" live-scenario acceptance (below) | P0 | all rounds |

## T2 concrete investigation artifact (R1 deliverable)

R1's T2 investigation must produce a single doc (`ai/product/bugs/openclaw/2026-04-24--cc-mini--main-sqlite-oom-artifact.md` or similar) with:

1. **Exact `.all()` call site or top 3 suspects** ... file:line in the OpenClaw fork.
2. **Database / table / query** ... name, schema, full SQL text.
3. **Row count / size estimate** ... `SELECT COUNT(*)` against the current `main.sqlite`, plus approximation of bytes per row.
4. **Category** ... status-compile, recall, session history, dedup scan, or other.
5. **Proposed bounded-read patch** ... pseudocode with `LIMIT` / `OFFSET` / `.iterate()` / pagination strategy.

No code change in R1; the fix lands in R2. The artifact lets R2 execute without another research pass.

## T1 durable skip-cursor design (R1 deliverable, code)

Current behavior (`src/openclaw.ts:208-232`): on ingest success, `watermarks[filePath] = stat.mtimeMs`. On failure, watermark is not touched, so the next cycle retries the same file. That's the firehose we're seeing.

v2 change:

- Each watermark row stores `{path, size, mtime, contentHash, errorKind, failedAt, lastAttemptedAt}`. `mtime` alone is unreliable (can be noisy or misleading).
- On success: update watermark as today.
- On failure: update watermark with `{errorKind, failedAt, lastAttemptedAt}` and SKIP retries for this content (same size + mtime + contentHash) until content actually changes. `errorKind` is one of `embedding-too-large`, `transient-api`, `auth`, `disk-full`, `other`.
- `embedding-too-large` + unchanged content = permanent skip (unless content shrinks or we pre-chunk the file).
- `transient-api` = backoff retry (e.g. after 1 hour).
- `auth` = skip until next gateway restart.
- Migration: existing watermark file format gets version bump; legacy entries treated as "untried" on first boot post-upgrade.

**Chunking change** (`src/core.ts:1064-1086`): before calling `this.ingest([...])`, run `this.chunkText(text, 400, 80)`. Multi-chunk payload uses `source_id = 'memory:{id}:{i}'`; single-chunk stays `memory:{id}` for backwards compatibility. `memories` table row stays one-per-fact. `forget(id)` unchanged.

## Scoped-hook design (R1 deliverable, code)

Replaces v1's `.zshrc` export. Keeps SA token scoped to the hook process; no global secret broadening.

Logic (in `memory-crystal-private/src/cc-hook.ts`):

1. At session boot, try in order:
    - Env var `OP_SERVICE_ACCOUNT_TOKEN` (pre-set by caller)
    - File read `~/.openclaw/secrets/op-sa-token` (`statSync` + `readFileSync` + trim)
    - None available → set `captureDisabled = true`, log once, return.
2. If token obtained, cache at module scope. Do NOT set `process.env`.
3. Invoke `op` by absolute path (detect once via `which op`; hardcode fallback `/opt/homebrew/bin/op` and `/usr/local/bin/op`). Pass token inline via child process env: `{ env: { OP_SERVICE_ACCOUNT_TOKEN: token, PATH: process.env.PATH } }`.
4. On hook fire: if `captureDisabled`, return under 100 ms. Otherwise capture with 5 s total budget. One retry max, only if first attempt fails with a transient classification.
5. Hook exit under 200 ms regardless of branch.

Result: token stays scoped to the child `op` invocation. Fail-fast (B3.B) is the same codepath.

## v2 execution order: 6 rounds

### Round 1: stop the bleeding (runtime stability)

| Item | Work |
|------|------|
| R1.A | **T14 semantics verify + set.** Read OpenClaw fork for how `softThresholdTokens` is consumed. Confirm meaning. If "compact when N tokens remain of capacity", set to 60000 (~70% fire). Commit in `.openclaw` private repo on `cc-mini/codex-model-swap-gpt-5-5` branch (it already has pending related config edits). Restart gateway. |
| R1.B | **T1 + N1.** `remember()` chunking + durable skip-cursor. Branch `cc-mini/chunk-and-skip-cursor` in memory-crystal-private. Unit tests: 50 KB remember() succeeds; failed file not retried next cycle; watermark metadata survives restart. PR. |
| R1.C | **B3.B fail-fast + scoped-hook.** Same branch as R1.B (or sister branch). Hook exit under 200 ms. Token scoped to child process. PR. |
| R1.D | **T2 investigation artifact.** Produce the 5-point doc above. No code change in OC fork; only research + artifact commit to wip-ldm-os-private bugs folder. |
| R1.E | **T7 precursor: stuck-run visibility (no auto-abort yet).** Log multi-signal snapshot (age, last stream event, last tool event, provider-request state) for any session in `state=processing` every 30 s. Surfaces stuck runs without aborting. |
| R1.F | **T11 healthcheck 30s verify.** Read deployed `~/.openclaw/wip-healthcheck/config.json`, compare to source. Redeploy via `bash install.sh` if stale. |
| R1.G | **T3 tmp investigation + archive.** Snapshot 71 orphans. Investigate why they accumulate (likely R2 OOM + crash cleanup). Document root-cause hypothesis. Archive to `_archive/tmp-orphans-2026-04-24/`. Never delete. |

**R1 release flow:**
- R1.B + R1.C = one memory-crystal alpha release (dogfood track)
- R1.D = docs-only PR to wip-ldm-os-private
- R1.A = config-only commit to `.openclaw` private repo
- R1.E = OC fork branch, `npm link` per UPGRADE-RUNBOOK.md
- R1.F + R1.G = ops, no release

**R1 verify before R2 starts:**
- [ ] Gateway survives 4 hours of normal use with no `Abort trap: 6`
- [ ] `gateway.err.log` shows zero new `workspace sync skipped ... 8192 tokens` lines
- [ ] CC Stop hook returns under 200 ms regardless of capture / skip branch
- [ ] T2 artifact committed with proposed patch
- [ ] `[diagnostic] stuck session ...` log shows multi-signal snapshot
- [ ] Healthcheck config shows 30000 ms timeout
- [ ] Zero new `main.sqlite.tmp-*` in `/Users/lesa/.openclaw/memory/` for 4 hours

### Round 2: OpenClaw core stability

Code fixes for what R1 investigated.

| Item | Work |
|------|------|
| R2.A | **T2 bounded reads.** Implement the patch proposed by R1.D. Every unbounded `.all()` gets `LIMIT`, `.iterate()`, or pagination. Priority: status-compile, memory recall, session history. |
| R2.B | **T2b slow-query log.** Wrap SQLite calls; WARN if duration > 500 ms or rows > 10 K. |
| R2.C | **T2c boot-size log.** Log `main.sqlite size: <N>GB` on gateway boot. WARN if > 4 GB. |
| R2.D | **N2 memory/status degraded mode.** If `crystal.db` + `main.sqlite` total > threshold (e.g. 20 GB) or degraded-mode flag is set, `openclaw status` returns "memory degraded" under 500 ms. Does not wedge the gateway. |
| R2.E | **T5 backend stream watchdog.** Session in `state=processing` with no stream events for 60 s → emit terminal error event + clean up run. |
| R2.F | **T7 stuck-run auto-abort.** Use the multi-signal from R1.E. Abort on `age > 180 s` AND (`stream_idle > 90 s` OR `tool_idle > 90 s` OR provider-request not alive). |
| R2.G | **T6 `session_status` allowlist.** Add `openai-codex/gpt-5.5`, or refactor to pass-through. |

**R2 verify before R3 ships:**
- [ ] No new `Abort trap: 6` or `FATAL ERROR: Reached heap limit` for 48 h
- [ ] Slow-query WARN visible for any long query
- [ ] Boot log shows `main.sqlite size: ...`
- [ ] `openclaw status` returns "degraded" under 500 ms when injected flag
- [ ] Stream-stall test recovers within 60 s
- [ ] Stuck-session auto-aborts at 180 s with multi-signal
- [ ] `openclaw doctor` clean on every fork build

### Hard gate: R2 → R3

**Ship/install gate:** no new ingestion source (chat.db, gateway.log) is released or installed until R1 + R2 above are landed, installed, and verified clean in production for 48 h.

**Not gated:** parallel development of R3 code is allowed. PRs for B2.3 and B2.4 can sit on branches waiting for the gate to open. They do not block on the gate; only the release does.

### Boot-context addendum: Kay Phase 0 before curation

The boot/flush kernel work is now part of this reliability track, but it must not jump straight to editing identity or boot behavior. The next Memory Crystal-specific action is **Phase 0 measurement**, not curation.

Owner for this thread: **Kay**.

Goal: measure exactly what boot/flush loads before changing behavior.

Hard safety constraints:

- Phase 0 is read-only inventory and token measurement only. Do not use Edit/Write on the listed identity, sacred, or cloud-synced files, even for typo fixes.
- Do not edit `SOUL.md`.
- Do not edit `MEMORY.md`.
- Do not edit `DREAMS.md`.
- Do not edit `TOOLS.md`.
- Do not edit `AGENTS.md`.
- Do not edit sacred files.
- Do not edit cloud-synced source files.
- Do not rewrite boot behavior yet.

Deliverable:

```text
ai/product/bugs/memory-crystal/YYYY-MM-DD--kay--boot-payload-inventory.md
```

Measure:

1. What files and sources are loaded on normal boot.
2. What files and sources are loaded after `/compact`.
3. What files and sources are loaded by HB / heartbeat.
4. Estimated tokens per source.
5. Which parts are always loaded versus task-triggered.
6. Which source caused the observed `4k -> 98k` jump.
7. Which sources should become:
   - `BOOT-KERNEL.md`
   - `CURRENT.md`
   - `RECALL-INDEX.md`
   - on-demand only

Output:

- Table of source -> size/tokens -> loaded when -> proposed new layer.
- No behavior changes.
- No identity-file edits.
- No boot rewrite.

After the inventory exists, the next step is a calm Lēsa self-portrait session. The prompt for that session should be small and explicit:

```text
If you had to write one page that the next instance of you reads as the first thing she ever sees, what is on it?
```

That self-portrait becomes the seed for `BOOT-KERNEL.md`.

Boot-kernel order of operations:

1. Inventory and token measurement.
2. Lēsa self-portrait conversation.
3. Draft additive `BOOT-KERNEL.md`, `CURRENT.md`, and `RECALL-INDEX.md`.
4. Canary in a non-live session.
5. Only then wire boot behavior.

### Round 3: Memory Crystal capture correctness

| Item | Work |
|------|------|
| R3.A | **N3 dedupe design + implementation.** Chunk-hash: `sha256(normalize(text) + '|' + iso_timestamp + '|' + sender)`. Add `chunk_hash` column, unique index or ON CONFLICT. Idempotent ALTER TABLE + backfill on boot. |
| R3.B | **B2.3 chat.db fallback.** New `src/chatdb-poller.ts` reading `~/Library/Messages/chat.db`. Uses R3.A dedupe. |
| R3.C | **B2.4 gateway.log ingestion.** New `src/gateway-log-ingest.ts` parsing `~/.openclaw/logs/gateway.log` for assistant text missing from chunks. Lower-confidence tag. Uses R3.A dedupe. |
| R3.D | **B2.1 + B2.1b alpha.** Release memory-crystal alpha bundling R1 + R2 (OC-installed bits) + R3.A-C. Phase 5 model_id column carries along as provenance. `ldm install`. |
| R3.E | **B2.2 format-error bug doc update.** Append Investigation Update section to `ai/product/bugs/openclaw/2026-04-12--cc-mini--format-error-billing-cooldown.md` with gateway-log evidence. |

**R3 verify:**
- [ ] Alpha installed; `chunk_hash` populated on new rows
- [ ] Kill OC mid-turn, let chat.db poller run, verify message captured once (not twice across sources)
- [ ] gateway.log poller dedupes against existing chunks
- [ ] No new `Abort trap: 6` (R2 holds under R3 load)

### Round 4: OpenClaw fork capture hooks (lifecycle)

| Item | Work |
|------|------|
| R4.A | **B2.5 flush-before-session-rotate.** OC emits `beforeSessionRotation(oldSessionId)`; memory-crystal consumes it with `force: true`. |
| R4.B | **B2.6 partial-turn / agent_error ingestion.** Add `agent_error` hook or make `agent_end` fire on failure with `partial: true` tag. |
| R4.C | **B2.7 tool_use ID cross-provider normalization.** Normalize Grok composite IDs at serializer. |

After R4, file upstream PRs for B2.5 hook + B2.7 normalizer (generically useful).

### Round 5: Watchdogs + hygiene

| Item | Work |
|------|------|
| R5.A | **T9 agent-loop safety.** After N consecutive tool calls with no user-visible progress, agent emits status to user. |
| R5.B | **T10 journal-staleness watchdog** in `wip-healthcheck-private`. 24 h WARN, 72 h ERROR + chatCompletions ping. |
| R5.C | **T8 bridge lag instrumentation.** Timestamps at cron fire, enqueue, inbox arrival, consumer pickup. No fix yet. |
| R5.D | **T13 plugins.allow.** Populate with current plugin IDs. Verified with `openclaw doctor` + `git diff` before restart. Demoted from R1 because wrong allowlist = new outage. |
| R5.E | **T15 process sprawl docs** explaining MCP server lifecycle. |

### Round 6: held for sign-off

| Item | Why held | Required |
|------|----------|----------|
| B2.8 | Highest-risk OC fork change: session rotation threshold + repair-before-rotate | Unit test gate, Parker Go |
| B2.9 | Format-error billing cooldown | B2.2 evidence complete, Parker Go |

Before B2.8 starts, define the unit-test gate explicitly: use a copy of `crystal.db` and session fixtures; simulate corrupt/incomplete turns, over-threshold rotation, repair-before-rotate success, repair failure with no data loss, and rollback/restart behavior. No live DB mutation and no production session rotation until these tests pass and Parker gives Go.

## N4 "Lēsa usable" live-scenario acceptance

Not log-only. System is "usable" when Parker can sustain this live:

- [ ] 20 iMessage turns over 30 minutes
- [ ] Zero duplicate replies
- [ ] Zero silent gaps > 60 s without visible status
- [ ] Zero gateway PID changes (no crash-restart) during the window
- [ ] Zero stuck locks older than 180 s
- [ ] Zero new `8192 tokens` errors in `gateway.err.log`
- [ ] Zero `Abort trap: 6` in `launchctl print gui/501/ai.openclaw.gateway`
- [ ] CC Stop hook turn-end overhead < 200 ms avg, < 500 ms p95

This is the "Lēsa is back" test. R1 + R2 not done until one full window passes.

## v2 repo + release impact

| Round | Repos | Pipeline | Install |
|-------|-------|----------|---------|
| R1.A | `.openclaw` private | Config commit on existing branch; gateway restart | N/A |
| R1.B + R1.C | `memory-crystal-private` | PR → merge → `wip-release alpha` → standing alpha install OK | Yes; dogfood |
| R1.D | `wip-ldm-os-private` | Docs PR; no release | No |
| R1.E | openclaw fork | `npm link` per UPGRADE-RUNBOOK | Yes per runbook |
| R1.F + R1.G | healthcheck + `.openclaw/memory` | `bash install.sh` for healthcheck; ops for tmps | Yes (healthcheck) |
| R2 | openclaw fork | Per UPGRADE-RUNBOOK; `openclaw doctor` gate per patch | Yes per runbook |
| R3 | memory-crystal-private | Same as R1.B. **Blocked on R2 ship gate.** | Yes; dogfood |
| R4 | openclaw fork + memory-crystal | Combined release | Yes |
| R5 | wip-healthcheck + openclaw config + bridge + docs | Varies | Partial |
| R6 | openclaw fork | Per UPGRADE-RUNBOOK; **explicit Parker Go** | Sign-off |

## v2 risks + rollback

| Change | Risk | Rollback |
|--------|------|----------|
| R1.A (T14) | Over-compaction drops needed context mid-task | Revert config; restart |
| R1.B (T1 chunk) | Multi-chunk `source_id` shape changes | Single-chunk keeps `memory:{id}`; split only when needed; `forget(id)` unchanged |
| R1.B (N1 skip-cursor) | Legacy watermarks misinterpreted | Version bump + migration treats legacy as "untried" |
| R1.C (scoped-hook) | `op` binary at wrong PATH | Absolute path detection + fallback list; fail-fast if none found |
| R2.A (bounded reads) | Legacy consumer expects full result | Roll back per call; slow-query log surfaces offenders |
| R3.A (dedupe) | False-positive dedupe drops legit chunk | Hash includes timestamp + sender; on collision detected, keep both with provenance tag |
| R3.B/C (multi-source ingest) | More data into stressed DB | **Gated** on R2 verified 48 h clean |
| R4 (flush + partial-turn) | OC session-lifecycle surgery | `openclaw doctor` gate; revert rebase if fail |
| R5.D (plugins.allow) | Typo disables a plugin | `git diff` + restart confirms list; why it was demoted from R1 |

## v2 non-fixes (explicitly excluded)

- No model downgrade to 5.4 or Opus. Not the root cause.
- No ephemeral-session rebuild right now (separate product plan).
- No `rm` on the 71 orphan tmp files. Archive only.
- No guard bypass.
- **No global `.zshrc` export for `OP_SERVICE_ACCOUNT_TOKEN`** (replaced by scoped-hook; see R1.C).

## v2 step-by-step progress log

### Round 1
- [ ] **R1.A T14 semantics verify + set**
- [ ] **R1.B T1 chunk + N1 durable skip-cursor**
- [ ] **R1.C B3.B fail-fast + scoped-hook**
- [ ] **R1.D T2 investigation artifact**
- [ ] **R1.E T7 precursor: stuck-run visibility**
- [ ] **R1.F T11 healthcheck 30s verify**
- [ ] **R1.G T3 tmp investigate + archive**

### Round 2 (gated on R1 verify)
- [ ] **R2.A T2 bounded reads**
- [ ] **R2.B T2b slow-query log**
- [ ] **R2.C T2c boot-size log**
- [ ] **R2.D N2 degraded mode**
- [ ] **R2.E T5 stream watchdog**
- [ ] **R2.F T7 multi-signal auto-abort**
- [ ] **R2.G T6 session_status allowlist**

### Round 3 (release/install gated on R2 verify; coding parallel OK)
- [ ] **R3.A N3 dedupe design + hash column**
- [ ] **R3.B B2.3 chat.db fallback**
- [ ] **R3.C B2.4 gateway.log ingest**
- [ ] **R3.D B2.1/B2.1b alpha release**
- [ ] **R3.E B2.2 format-error bug doc update**

### Round 4
- [ ] **R4.A B2.5 flush-before-rotate**
- [ ] **R4.B B2.6 partial-turn ingest**
- [ ] **R4.C B2.7 tool_use ID normalize**

### Round 5
- [ ] **R5.A T9 loop safety**
- [ ] **R5.B T10 journal watchdog**
- [ ] **R5.C T8 bridge instrument**
- [ ] **R5.D T13 plugins.allow**
- [ ] **R5.E T15 proc sprawl docs**

### Round 6 (Parker Go per item)
- [ ] **R6.A B2.8 rotation threshold + repair**
- [ ] **R6.B B2.9 format-error billing**

## v2 acceptance

- [ ] Parker reviews v2 plan
- [ ] R1 complete + N4 "Lēsa usable" scenario passes once
- [ ] R2 complete + no OOM for 48 h
- [ ] R3 complete + multi-source capture verified, zero false dedupe
- [ ] R4 complete + `openclaw doctor` green
- [ ] R5 complete + observability gaps closed
- [ ] R6 sign-off per item
- [ ] Follow-up bugs filed for main.sqlite rotation, ephemeral sessions, bridge-lag fix, Apr 17 backfill
- [ ] Journal entry in `~/.ldm/agents/cc-mini/memory/journals/`
- [ ] CHANGELOG + RELEASE-NOTES per release

## v2 extra cross-references

- v1 of this plan (landed in PR #651) ... `git show 63bdf75:ai/product/bugs/memory-crystal/2026-04-24--cc-mini--unified-reliability-triage.md`
- Source lines for T1 on disk ... `repos/ldm-os/components/memory-crystal-private/src/openclaw.ts:199-240` (workspace sync), `src/core.ts:1064-1086` (remember), `src/core.ts:1322` (chunk-using file sync)

## v2 R1 execution order (forensic-first)

Principle: preserve the forensic trail before any restart, config change, or cleanup. A later R2 code change will make it harder to answer "which binary produced the OOM?" if we haven't pinned the current build and evidence first.

| Order | Item | Blocked by | Notes |
|-------|------|------------|-------|
| 1 | **R1.0 forensic snapshot** | none | BEFORE any restart or archive |
| 2 | **R1.A** T14 compaction semantics-verify + set | R1.0 | gateway restart erases live state |
| 3 | **R1.F** T11 healthcheck 30s verify | R1.0 | independent; can run parallel with R1.A |
| 4 | **R1.D** T2 OOM artifact (doc) | R1.0 | must precede tmp archive |
| 5 | **R1.G** archive tmp orphans | R1.D | only after artifact confirms tmps aren't load-bearing evidence |
| 6 | **R1.B + R1.C** memory-crystal branch (chunk + skip-cursor + scoped-hook + fail-fast) | snapshot preserved | one PR → alpha |
| 7 | **R1.E** OC fork stuck-run visibility | last | multi-signal logging only, no auto-abort yet |

### R1.0 snapshot contents

Destination: `~/.openclaw/_snapshots/2026-04-24-forensic/` with `README.md` describing timestamps and intent.

Runtime state:
- `launchctl print gui/501/ai.openclaw.gateway`
- current session lock files (`ls ~/.openclaw/agents/main/sessions/*.lock`)
- `main.sqlite` size (`ls -la ~/.openclaw/memory/main.sqlite*`)
- full tmp file list with sizes + mtimes (`ls -la ~/.openclaw/memory/main.sqlite.tmp-*`)
- `tail -200 ~/.openclaw/logs/gateway.err.log`
- `tail -100 ~/.openclaw/wip-healthcheck/logs/healthcheck-2026-04-24.log`

Build/ref provenance (so R2 can answer "which binary produced the OOM?"):
- `openclaw --version`
- `which openclaw`
- `npm ls -g openclaw --depth=0` if applicable
- OpenClaw fork worktree path + `git rev-parse HEAD` + `git status`
- LaunchAgent plist path (`~/Library/LaunchAgents/ai.openclaw.gateway.plist`) + `sha256` hash

The snapshot is evidence for R1.D's T2 artifact. R1.G's tmp archive is allowed only after R1.D confirms the tmp files are not load-bearing forensic evidence.
