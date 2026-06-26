# Bridge Cost Burn Analysis: How a "failed" MCP call costs 2-5x

**Date:** 2026-04-05
**Filed by:** cc-mini (with Parker, Lēsa)
**Priority:** critical. Main driver of the April 4-5 overnight $40 burn (minus the brainstorm cron contribution).
**Repo:** OpenClaw fork (primary), wip-ldm-os-private (filing location)
**Status:** SHIPPED 2026-04-05. Fork commit `54037e050c` on `cc-mini/chat-completions-v2026.4.2`. Deployed live via `npm link`. Gateway restarted. End-to-end verified: chatCompletions against Lēsa's iMessage-bound main session returns 200 + `x-openclaw-queued: channel-bound` header in ~100ms (was 120s timeout). Webchat-bound sessions still use the sync path (regression verified).

## Why this file exists

Parker asked me to document "this whole bridge token issue" as a standalone file under `ai/product/bugs/bridge/`. The bridge master plan already covers it at a summary level (Section 5.1, 5.2) but the detailed end-to-end trace with timing and the root-cause mechanism needs its own durable record. This is that record.

## The one-sentence version

**A single "failed" `lesa_send_message` call generates a full Opus turn server-side AFTER the client has given up, delivers the reply to the wrong destination (iMessage instead of HTTP), and leaves the caller thinking nothing happened so it retries.** Every retry is another full Opus turn. One "failed" call commonly costs 2-5x the cost of one successful call.

## The trace (verified from today's logs)

Lēsa's session wire log confirmed the exact timing of one such failed call:

- **08:15** — cc-mini fires `lesa_send_message` via MCP (a simple coordination question, not a heavy task)
- **08:15** — gateway routes to main session, calls `agentCommandFromIngress`
- **08:15** — my queue check (from last night's fix) does NOT fire. Lēsa was not in the "actively streaming" sub-state at that exact instant. She was holding the session write lock waiting for a prior turn or a heartbeat.
- **08:15** — handler falls through to the blocking path. HTTP request waits on the session lock.
- **08:17** — 120s later: my MCP client's `AbortController` fires. MCP returns "Gateway timeout: Lesa may be busy or the gateway is processing another request."
- **08:17** — server does NOT abort. The HTTP handler is still holding the connection waiting on the lock. From the server's perspective, nothing has happened yet.
- **08:22** — Lēsa's session becomes free. Starts processing my message as a fresh turn.
- **08:23** — she finishes the reply. Emits it to her bound channel (iMessage), visible to Parker in the TUI.
- **08:23** — the HTTP response path is still waiting but the reply never comes because the reply went to the channel, not the response. Eventually the socket closes with no content.
- **cc-mini sees:** a timeout error. No reply content.
- **Parker sees:** Lēsa's full reply in iMessage with no context for who asked.
- **Cost:** one full Opus turn at Lēsa's current context load (approximately 144k tokens in her window).

Reply logged at 2026-04-05T08:23:45 PDT. Call fired around 08:15. Total latency: about 3 minutes. Caller thought it timed out at 120s (08:17). Server kept working for another 6 minutes after the caller gave up.

## Why this 2-5x's the cost

Every "failed" call has four contributing cost factors:

1. **Full Opus turn generated after the caller gave up.** The server does not abort when the client does. It runs the entire turn regardless. For Lēsa that means full context load (~100-150k tokens) processed through Opus.
2. **Reply delivered to the wrong destination.** Goes to iMessage, not HTTP response. Parker sees it as a bare message with no context. No automation can consume it.
3. **Caller thinks the call failed.** No signal that anything happened server-side. From the caller's perspective, the request was lost.
4. **Caller retries.** Each retry is another full Opus turn. The brainstorm cron last night retried 4-5 times per fire (per Lēsa's count), so one cron event generated 4-5 full Opus turns, all invisible to the code that triggered them.

**Per-event cost multiplier:** 1 expected turn becomes 2-5 actual turns, plus the retry loop's side effects (message fragments in iMessage, confused Parker, corrupted context).

## Why last night's queue fix does NOT solve this

The queue fix I shipped (PRs wipcomputer/wip-ldm-os#266 via fork commits `9c99dc1fab`, `98d1f9c137`, `9fc73639a8`) only matches ONE sub-state of the failure mode. Specifically:

- It fires when `queueEmbeddedPiMessage(sessionId, text)` returns `true`
- That function (`src/agents/pi-embedded-runner/runs.ts:50-67`) only returns true when the session has an active run AND is streaming AND is not compacting

**It does NOT fire when:**
- Session is locked between turns (waiting on state persistence, heartbeat, compaction)
- Session is bound to a non-webchat channel (iMessage, Slack, Discord)
- Session is in any "busy" state outside the narrow streaming window

Most failed calls this morning fell into the "locked between turns" case. The queue check returned false. Handler fell through to the blocking path. Full burn.

## Why the blocking path is structurally wrong for channel-bound sessions

When chatCompletions delivers a message to a session that is bound to a non-webchat channel, the HTTP response path is **structurally** wrong:

1. Request enters `handleOpenAiHttpRequest` in `src/gateway/openai-http.ts`
2. `resolveGatewayRequestContext` resolves a `sessionKey` for the target
3. The target session's agent is mid-turn or holds the write lock
4. `agentCommandFromIngress` awaits on that lock
5. When the lock releases, the agent processes the new message as a regular turn
6. The agent generates a reply and emits it via its **bound channel handler** (iMessage transport, Slack adapter, webchat output, etc.)
7. The chatCompletions HTTP handler is still holding the connection, but the reply **never flows back to it** because the reply went to the channel, not to the HTTP response path

The handler currently returns whatever `agentCommandFromIngress` gives it. For a webchat session that has NO bound channel, this is the reply. For an iMessage-bound session, it is NOT, and the HTTP caller gets nothing regardless of timeout.

**The HTTP response can NEVER carry the reply back for channel-bound sessions.** Blocking just burns tokens and times out the caller for zero benefit.

## The real architectural fix

Before calling `agentCommandFromIngress`, check if the target session's channel is webchat (no binding). Branch:

- **Webchat (no binding):** current sync path is fine. Fall through.
- **Channel-bound (iMessage, Slack, etc.):** return 200 immediately with an `x-openclaw-queued: next-turn` header and a `[queued]` body marker. The agent will process the message when its lock releases and emit the reply to its bound channel. HTTP caller gets a fast, unambiguous "delivered, reply goes to channel" signal.

Size: approximately 50 lines in `src/gateway/openai-http.ts` plus a helper to resolve channel binding from session key.

Risk: need to verify the channel-binding resolver reliably classifies sessions. Probably already exists via `loadSessionEntryByKey(sessionKey).channel` used by the steer-backlog path in `src/agents/subagent-announce-delivery.ts:425-491`.

This is Phase 2 of the bridge master plan. Not started.

## Cost math (rough)

Assume Opus 4.6 pay-as-you-go billing at current public rates. Lēsa's context is around 100-150k tokens at any given time.

- **Successful call:** 1 turn, say ~$0.50-$2.00 depending on context and output length
- **"Failed" call (hit by this bug):** server still generates 1 turn (~$0.50-$2.00), caller retries 1-4 more times, each retry also "fails" and generates another turn. Total: **2-5 turns** per attempted interaction.
- **Brainstorm cron event last night:** 1 fire, 4-5 retries per Lēsa's count, approximately **$5-$20 per cron fire** burned with zero output reaching the caller.
- **Across 4-5 cron fires overnight:** $20-$100 range.
- **Parker's observed overnight burn:** $40.
- **Consistency check:** matches the mid-range of the estimated cron-driven burn, plus baseline Lēsa usage, plus heartbeats.

## The compounding factors

The bridge bug alone is bad. But it compounds with:

1. **The brainstorm cron's exec approval bug.** The cron retries 4-5x per fire because of approval gate timeout. Each retry hits the bridge bug. 4-5 retries x 2-5 turns per retry = 8-25 Opus turns per cron event.
2. **Pay-as-you-go billing went live April 4 noon.** Before that, every burn was covered by the Max subscription. After, every burn is real dollars.
3. **No visibility into what "failed".** The caller sees a generic timeout. Parker sees orphan messages in iMessage. Nobody sees the server-side full-turn cost happening in the background.
4. **Lēsa is on the full Opus 4.6 with 1M context.** Every turn is the most expensive model variant available. Even successful calls are on the high end; failed-but-still-processed calls are the worst case.

## Temporary mitigations (until Phase 2 ships)

1. **Stop calling `lesa_send_message` from CC to her main session.** Use paste-from-TUI workflow instead. This removes the bridge bug from CC's side entirely. I have already committed to this for the rest of today's session.
2. **Disable or gate the brainstorm cron.** Removes the biggest retry loop. Tracked in the openclaw/brainstorm-cron bug file.
3. **Ship @steipete's CLI adapter workaround** (tracked in `ai/product/bugs/openclaw/2026-04-05--cc-mini--cli-adapter-workaround-steipete.md`). This doesn't fix the bridge bug but takes Lēsa off pay-as-you-go entirely, which caps the worst case. The bridge bug still wastes turns, but the turns no longer cost pay-as-you-go rates.
4. **Add a cost budget gate.** If a session-level token counter crosses a threshold, pause cron-originated calls. Prevents runaway overnight burns from any future retry loop. Covered as Phase 4 in the bridge master plan.

## The real fix (scoped)

**Phase 2 of the bridge master plan.** ~50 line change to `src/gateway/openai-http.ts` in the OpenClaw fork. Before `agentCommandFromIngress`:

```typescript
const channel = loadSessionEntryByKey(sessionKey).channel;
if (channel !== 'webchat') {
  queueEmbeddedPiMessageOrForward(sessionId, text);
  return res.status(200).header('x-openclaw-queued', 'next-turn').json({ queued: true });
}
// existing sync path
```

(Pseudocode; actual implementation will match OpenClaw conventions.)

## Verification end-to-end (after Phase 2 ships)

1. `lesa_send_message` from CC to Lēsa's main (iMessage-bound) session returns 200 immediately with the queued marker, within ~100ms
2. No 120s timeout ever
3. Reply goes to iMessage (as before, that is correct behavior)
4. CC logs show fast success, not timeout
5. Server-side: one turn generated per call, not multiple
6. Cost per failed interaction: ~1x baseline, not 2-5x

## Cross-references

- `ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-master-plan.md` — canonical master plan, Sections 5.1, 5.2, 6, 7 (Phase 2)
- `ai/product/bugs/master-plans/bugs-plan-04-05-2026-001.md` — today's session rundown, Sections 5.1, 5.2
- `ai/product/bugs/openclaw/2026-04-05--cc-mini--cli-adapter-workaround-steipete.md` — orthogonal cost lever (CLI adapter)
- OpenClaw fork commits: `23d49ef`, `9c99dc1fab`, `98d1f9c137`, `9fc73639a8` (the partial queue fix that did NOT cover this case)
- Related tickets: wipcomputer/wip-ldm-os#266 (queue wiring, partial fix)

## Open questions for Parker

1. Do you want Phase 2 to be upstreamed to OpenClaw, or kept in our fork? Upstream is the right answer long-term but takes longer.
2. Should the queued response body include the text that was accepted, so CC at least has an echo of what it sent? (Currently OpenClaw returns an empty queued marker.)
3. Is there appetite for a cost-dashboard in Lēsa's TUI that surfaces per-session token burn so we catch future cost bugs faster?
4. The 50-line fix is well-scoped but it is in a critical path. Should we stage it as a feature flag first, then enable after a day of soak? Or ship directly?

## Scope boundary

**In scope for this file:** documenting the trace, the mechanism, the cost math, and the fix scope.

**Out of scope for this file:** actually shipping the fix (that is Phase 2 of the bridge master plan, done in a separate PR), testing the CLI adapter (that is the `cli-adapter-workaround-steipete.md` plan), and any cost-dashboard work (deferred).
