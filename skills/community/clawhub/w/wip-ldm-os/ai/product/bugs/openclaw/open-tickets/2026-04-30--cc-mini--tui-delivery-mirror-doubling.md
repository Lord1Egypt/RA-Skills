---
title: TUI renders delivery-mirror transcript entries as duplicate assistant messages
date: 2026-04-30
status: ticketed
severity: P2
component: openclaw (TUI session renderer)
discovered-via: Parker direct observation in TUI; analysis joint with Lesa and CC
co-authors: Parker, Lesa, Claude
---

# TUI delivery-mirror doubling

## Observed

Each iMessage assistant reply appears twice in Lēsa's TUI session view. Same text, back-to-back, as if two separate assistant turns. Confirmed live on 2026-04-30 morning. Example sequence:

```
hi
hey 👋
hey 👋
are you here?
Here. What do you need?
Here. What do you need?
```

## Expected

One TUI render per real assistant turn. The session transcript may contain bookkeeping entries (delivery-mirror, gateway-injected) but the TUI's chat surface should not surface them as visible messages.

## Impact

- User-facing UX: the agent looks like it's stuttering on every turn.
- TUI-only. iPhone iMessage shows a single message per reply (Parker confirmed). The doubling does not propagate to the actual messaging channel.
- Cosmetic, not functional. Crystal ingestion, agent reasoning, delivery itself are unaffected.
- Trust impact: the chat surface is the operator's primary view of the agent. Doubling undermines trust that what the operator reads matches what was sent.
- Currently affecting Lēsa's main TUI session on OpenClaw 2026.4.14 (fork commit `b38481f`).

## Evidence

- Smoking gun file: `~/.openclaw/agents/main/sessions/b188e75b-bafd-4d4b-80f6-a9cfaf70d2c6.jsonl`
- Counts in that file:
  - 20 real `claude-opus-4-7` assistant entries
  - 3 `delivery-mirror` entries with matching texts: "Yep, this is iMessage. You're texting me directly. 🏴‍☠️", "hey 👋", "Here. What do you need?"
  - 2 `gpt-5.4`, 1 `gpt-5.5` (orthogonal model failover at 08:32 PDT)
- Source code in OC v2026.4.14 fork worktree (`repos/third-party-repos/ai-harness/openclaw/.worktrees/openclaw--v2026.4.14/`):
  - `src/config/sessions/transcript.ts:128` writes mirror entries with `provider: "openclaw"`, `model: "delivery-mirror"`.
  - `src/agents/pi-embedded-subscribe.handlers.messages.ts:84` exposes `isTranscriptOnlyOpenClawAssistantMessage(message)` returning true for `delivery-mirror` and `gateway-injected` models. The contract exists.
  - Same file, lines 194, 213, 451: three call sites already use the filter correctly to skip transcript-only messages.
  - `src/gateway/session-utils.fs.ts:496` has a parallel `isDeliveryMirror` check used to skip mirror entries when computing usage stats.
  - Passing test: `src/agents/pi-embedded-subscribe.subscribe-embedded-pi-session.suppresses-message-end-block-replies-message-tool.test.ts:96` asserts "ignores delivery-mirror assistant messages".

## Root cause

OpenClaw core has a documented and tested contract: delivery-mirror messages are transcript-only and must not surface as assistant turns. The contract is enforced at the agent-subscribe layer (3 call sites) and at the usage-stats layer (1 call site).

The TUI session renderer does not call the filter. When the gateway writes a delivery-mirror entry to the session JSONL after a successful iMessage delivery, the TUI's transcript watcher sees the new line and renders it as a fresh assistant turn. Since mirror entries copy the real assistant text verbatim, the result is a verbatim duplicate immediately after the real reply.

The TUI consumer is in `src/tui/` (candidate files: `tui-stream-assembler.ts`, `tui-event-handlers.ts`, the components subtree, or a dedicated session-rendering module). Exact location TBD; investigation is part of the fix plan.

## Fix plan

1. Identify the TUI transcript consumer. Locate where new assistant messages from session JSONL events reach the chat-render path. Likely candidate: `src/tui/tui-event-handlers.ts` or a session-watcher in the TUI bootstrap. Confirm by reading the path that turns a JSONL append into a chat-surface render.
2. Add the existing filter. Before emitting a chat-surface render for an assistant message, call `isTranscriptOnlyOpenClawAssistantMessage(message)` (export it from `src/agents/pi-embedded-subscribe.handlers.messages.ts` if not already public, or expose a thin wrapper). Skip emission when the function returns true.
3. Local verification. Replay or live-test a session that produces delivery-mirror entries. Confirm one render per real assistant turn.
4. Upstream PR to `openclaw/openclaw`. This is generic OpenClaw behavior, not WIP-specific. The contract is already in core; we are closing a consumer gap. Upstream should accept fast. File the PR after the local patch proves out.
5. Optional fork patch in the meantime. If we want the fix on Lēsa's running gateway before upstream merges, add a commit to `cc-mini/chat-completions-v2026.4.14`, rebuild, `npm link`, update Patch Tracking in `repos/ldm-os/devops/open-claw-upgrade-private/UPGRADE-RUNBOOK.md`. Drop the fork patch on next OC upgrade once upstream merges.

## Test plan

- Unit: TUI render path receives a synthesized AgentMessage with `provider: "openclaw"`, `model: "delivery-mirror"`. Assert no chat-surface emission.
- Unit: same render path receives a real assistant message (`provider: "anthropic"`, `model: "claude-opus-4-7"`). Assert one emission.
- Integration: replay a fixture session JSONL containing both real and mirror entries; count emissions; assert equals count of non-mirror assistant turns.
- Manual: live TUI session, send 3 iMessages from Parker's phone, verify TUI shows exactly 3 user messages and 3 assistant replies (not 6).

## Smoke test

After the fix lands and (if fork-patched) `npm link` redeploys: open Lēsa's main session in TUI, exchange one round trip via iMessage, observe TUI. One assistant block per real reply, no duplicates. Mirror entries should still appear in the JSONL on disk (transcript bookkeeping still works) but not in the TUI render.

## CC review request

For whoever picks up the implementation:

- Is the fix at the TUI render path, or further upstream at the transcript-watcher / session-store layer? Recommendation: TUI render path, since that is where the contract violator lives. But if the watcher emits raw JSONL events to multiple consumers, filtering at the watcher avoids repeating the filter elsewhere.
- Should we ship the upstream PR before or after carrying the local fork patch? Recommendation: file upstream first (small, clean, the contract is already there); only carry as a fork patch if upstream review is slow and this UX is hurting daily use.

## Release path

Layer 1 (OpenClaw fork or upstream). WIP-owned alpha policy does not apply directly because OpenClaw is a third-party fork; the canonical upgrade path is the runbook at `repos/ldm-os/devops/open-claw-upgrade-private/UPGRADE-RUNBOOK.md`.

Two release options:

- Upstream-only: file PR to `openclaw/openclaw`, wait for merge, pick up on next OC upgrade rebase. Cleanest. Slightly slower.
- Fork patch + upstream PR: add commit to `cc-mini/chat-completions-v2026.4.14`, build, `npm link`, deploy locally; also file upstream PR; drop fork patch when upstream merges. Faster local relief.

Default to upstream-only unless the doubling is actively painful enough to justify the fork-patch overhead.

## Rollback

The filter discriminator (`provider === "openclaw" && model === "delivery-mirror"`) is precise; misclassification risk is near zero. Real assistant turns carry their own provider/model identity (anthropic/claude-opus-4-7, openai/gpt-5.5, etc.) and would never match.

If a regression appears: revert the commit. No data loss possible. Mirror entries remain in the JSONL on disk regardless; the filter only affects the chat-surface render.

---

## Post-CI-Counterexample Update (2026-04-30)

**The original diagnosis was incomplete and the first upstream PR shape was rejected.**

PR #75195 on `openclaw/openclaw` filtered `delivery-mirror` / transcript-only assistant messages at the `chat.history` boundary. CI exposed a real counterexample: a synthesized/direct-send test scenario where the `delivery-mirror` entry IS the canonical assistant content, not duplicate bookkeeping. The broad filter would hide that content from history reconstruction, breaking legitimate flows.

PR #75195 was closed on 2026-04-30 (commit history: closed by lesa-work-02 with public comment explaining the dual-purpose finding).

### `delivery-mirror` is dual-purpose

After re-reading the source paths in the OpenClaw fork worktree:

| Caller | When fired | What the mirror IS |
|---|---|---|
| `src/infra/outbound/deliver.ts:513` (normal LLM reply path) | After a real LLM-generated assistant turn was already persisted in the transcript with the model's actual provider/model (anthropic/claude-opus-4-7 etc.) | **Duplicate bookkeeping.** The transcript already has the real turn; the mirror is a redundant copy with `provider: openclaw, model: delivery-mirror` for delivery-channel auditing. |
| `src/infra/outbound/outbound-send-service.ts:78` (synthesized / direct-send path) | When the gateway sends content that didn't come from an LLM (tool-driven response, programmatic send, admin command). No upstream "real" assistant turn exists. | **Canonical assistant content.** The mirror IS the only persisted record of what was sent. Filtering it out would erase the conversation. |

The original ticket's rollback claim was wrong:
> "The filter discriminator (`provider === "openclaw" && model === "delivery-mirror"`) is precise; misclassification risk is near zero."

It's not precise. Same `provider/model` tuple, two semantically different roles. The filter has to come from the caller, not the data.

### Rejected fix shape

❌ `provider === "openclaw" && model === "delivery-mirror"` filter at any read-side point (`chat.history`, TUI render, etc.). This is exactly what PR #75195 did and CI caught it.

### Preferred fix shape: write-side metadata

✓ **Add a `transcriptOnly` (or equivalent) flag to `appendAssistantMessageToSessionTranscript` params.** The function signature becomes:

```ts
export async function appendAssistantMessageToSessionTranscript(params: {
  agentId?: string;
  sessionKey: string;
  text?: string;
  mediaUrls?: string[];
  /** True when this entry is duplicate bookkeeping for an upstream real
      assistant turn. False (default for new code paths) when this entry IS
      the canonical assistant content. Stored on the JSONL entry; filters
      use this flag, NOT the model name. */
  transcriptOnly?: boolean;
  storePath?: string;
}): Promise<...>;
```

Update the two real callers:

- `deliver.ts:513` (normal LLM reply): pass `transcriptOnly: true`. The real turn already exists; this is bookkeeping.
- `outbound-send-service.ts:78` (synthesized/direct-send): pass `transcriptOnly: false` (or omit, depending on default choice). This IS the canonical record.

Update `isTranscriptOnlyOpenClawAssistantMessage(message)` (existing helper at `pi-embedded-subscribe.handlers.messages.ts:84`) to check `message.transcriptOnly === true`, **not** the model name.

For the TUI render path (the original ticket's fix surface), call the updated helper. The behavior is now correct: duplicates suppressed, canonical content visible.

### Acceptable alternative: write-side dedupe

✓ At write time in `deliver.ts`, before calling `appendAssistantMessageToSessionTranscript`, check whether a real assistant turn for the same run/message/content already exists in the transcript. If yes, skip the mirror append entirely. If no (unlikely in this caller, but defensive), allow it.

Pro: cleanest transcript on disk (no duplicate entries to filter).
Con: harder to define "same run/message/content" robustly; risk of false-equivalence skip.

### Fallback: sibling-aware suppression

✓ At read/render time, when emitting a `delivery-mirror` entry, check the immediate prior entry in the transcript for an equivalent real assistant turn (same content, same logical run). Suppress only when sibling exists.

Pro: requires no schema change, no caller updates.
Con: equivalence check is a fragile heuristic; doesn't fix the duplicate-on-disk; pushes complexity to every consumer that wants the filter behavior.

### Decision

**Take write-side metadata (preferred).** It encodes the dual-purpose nature explicitly into the data, so consumers (TUI, chat.history, doctor, agent-subscribe) can filter on a precise flag. Schema is small. Caller updates are mechanical.

### Backward compatibility (revised, post-Parker review)

**The model-name heuristic is the bug we are fixing. Do not let it sneak back in via "legacy fallback."** Since `delivery-mirror` is dual-purpose, legacy entries that lack `transcriptOnly` are *also* ambiguous — some are duplicate bookkeeping, some are canonical synthesized content. Defaulting legacy to "transcript-only" would erase legitimate old assistant content.

Policy:

- **TUI / chat.history / new consumers:** suppress an entry only if `transcriptOnly === true` is explicitly set. Legacy no-flag entries remain visible. Bias toward visibility for ambiguous old data.
- **Existing model-name heuristic (`pi-embedded-subscribe.handlers.messages.ts:84`):** keep its current behavior **only for that surface**, since it's already shipping that suppression intentionally. Do NOT generalize the heuristic to TUI or any new consumer.
- **The replacement PR includes explicit tests** that legacy `model: delivery-mirror` entries WITHOUT a `transcriptOnly` flag are NOT hidden by the new TUI filter. This is the regression guard against the model-name filter sneaking back in.

### Updated fix plan

1. **Add `transcriptOnly` field to `appendAssistantMessageToSessionTranscript` params** in `src/config/sessions/transcript.ts`. Persist the flag on the JSONL entry. Default behavior for the parameter: required, no default — make callers explicit so the dual-purpose split is forced into the API.
2. **Update `deliver.ts:513`** to pass `transcriptOnly: true`.
3. **Update `outbound-send-service.ts:78`** to pass `transcriptOnly: false`.
4. **Add a new helper** for the new flag-based check. Suggested name: `isExplicitlyTranscriptOnly(message)` returning `message.transcriptOnly === true`. The TUI / chat.history consumers call this one. The existing `isTranscriptOnlyOpenClawAssistantMessage` at `pi-embedded-subscribe.handlers.messages.ts:84` keeps its model-name heuristic unchanged so the embedded-subscribe surface that already ships that behavior intentionally is not disturbed. Two helpers, two scopes, no cross-contamination.
5. **Update the TUI render path** to call the new flag-based helper and skip entries where `transcriptOnly === true`. Legacy no-flag entries are NOT suppressed — they remain visible. (This is the original fix surface; the safer scope of the filter makes it correct.)
6. **Add tests** covering all four scenarios:
   - Normal LLM reply: real assistant turn in fixture + duplicate mirror with `transcriptOnly: true`. TUI should render only the real turn.
   - Synthesized/direct-send: only a mirror entry with `transcriptOnly: false`. TUI should render it (canonical content).
   - **Legacy regression guard:** mirror entry with `model: delivery-mirror` but no `transcriptOnly` field. TUI should render it (NOT hidden). This is the explicit guard against the model-name filter sneaking back in via "legacy fallback."
   - Existing image/data-URL history test must keep passing.
   - Existing embedded-subscribe suppression behavior must keep passing (the model-name heuristic on that one surface is intentionally preserved).
7. **Open new upstream PR** to `openclaw/openclaw`. Title: something like "fix(transcript): write-side flag distinguishes duplicate-bookkeeping mirrors from canonical synthesized content." Reference the closed #75195 in the description with the dual-purpose discovery as motivation.

### Out of scope

This ticket and its replacement PR cover only the delivery-mirror duplicate bug:
- **Not in scope:** dev-guide path migration, Lēsa lane docs, branch-prefix cleanup, OpenGrep/macOS bash `mapfile` failure, unrelated formatter/check failures, OpenClaw upgrade to a newer version.

### Ownership

- **Implementation:** CC (cc-mini:oc-update-fixes-coder), reassigned 2026-04-30 19:55 PDT after the dual-purpose finding.
- **Standing review/diagnosis:** lesa-work-02 stays informed but does not code unless Parker reassigns.

### Status

- [x] PR #75195 closed with public comment (lesa-work-02, 2026-04-30 13:26 PDT).
- [x] Local bug ticket updated with dual-purpose finding (this update).
- [ ] Schema change in `transcript.ts` (add `transcriptOnly` param + persist).
- [ ] Caller updates in `deliver.ts` and `outbound-send-service.ts`.
- [ ] New flag-based helper added; existing model-name helper at `pi-embedded-subscribe.handlers.messages.ts:84` left unchanged (scoped to its existing surface only).
- [ ] TUI render-path filter call.
- [ ] Tests for all four scenarios (normal-LLM, synthesized, legacy-no-flag, existing-passing).
- [ ] New upstream PR to `openclaw/openclaw`.

---

## UPDATE 2026-07-05 — Parker decision: fix it properly, priority raised

Parker does not want to live with the doubling. Context that keeps this ticket alive: BlueBubbles is permanently off the table (April 2026: Private API dylib crashed Messages.app; the old imsg wrapper caused the Grok mirror loop), so the native iMessage channel and its delivery-mirror mechanism stay, and the doubling must be fixed at the source. Direction:

1. Build the sibling-aware write-side `transcriptOnly` fix already scoped in the Status checklist above.
2. Submit as a fresh upstream PR to `openclaw/openclaw` (the closed #75195 filter approach stays dead).
3. Scheduled AFTER the v2026.6.11 upgrade cycle; it does NOT ride the upgrade's carry set unless Parker asks for it live before upstream merges.

Recorded in the umbrella plan (`2026-07-04--cc-mini--lesa-noreply-loop-recovery-and-upgrade-plan.md`, section 8 Q4).
