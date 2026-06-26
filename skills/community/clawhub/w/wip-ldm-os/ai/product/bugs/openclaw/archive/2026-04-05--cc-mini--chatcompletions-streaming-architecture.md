# chatCompletions streaming architecture question: can we ever do mid-turn interjection?

**Date:** 2026-04-05
**Filed by:** cc-mini
**Priority:** P3. Architectural, not urgent. Research.
**Repo:** OpenClaw fork
**Status:** not started. Investigative.

## Context

Yesterday's overnight fixes to the OpenClaw fork included renaming the `x-openclaw-queued: steer` header to `x-openclaw-queued: next-turn`. The rename was correct: per Lēsa's observation, messages arriving via the queue path come through as a regular next-turn message in her session, not as a mid-turn steer.

The name `steer-backlog` in the existing code (`src/agents/pi-embedded-runner/runs.ts:50-67`) implies a capability that does not actually exist from the receiving side. A "steer" in the classical sense would interject mid-generation, influencing the current turn's output. The current implementation just queues the message for the next turn, same as if it arrived via the channel.

## The question

**Is TRUE mid-turn interjection valuable, and is it achievable in OpenClaw's architecture?**

True mid-turn interjection would allow:
- Cancelling an in-flight Opus turn if new information arrives that changes the request
- Adding urgent context to a long-running turn without waiting for it to finish
- Steering a long tool-use chain mid-sequence (e.g., "stop, abort this direction")
- Reducing latency for multi-party coordination (cc-mini + Lēsa interleaving)

## Why it matters (potentially)

- **Cost.** Cancelling a wrong-direction turn mid-generation saves tokens. For Opus 4.6 at Lēsa's context this could be meaningful.
- **Responsiveness.** Multi-agent coordination is currently gated by turn boundaries. True interjection would enable finer-grained collaboration.
- **Architectural purity.** If the name `steer-backlog` is used elsewhere in the code, the current implementation is misnamed and future contributors may build on a false assumption.

## What to investigate

### Phase 1. Read the existing code

- `src/agents/pi-embedded-runner/runs.ts` — `queueEmbeddedPiMessage`, `isEmbeddedPiRunActive`
- `src/gateway/openai-http.ts` — the queue pre-check and next-turn delivery
- `src/agents/subagent-announce-delivery.ts:425-491` — the template for iMessage steer-backlog (which is the pattern the queue fix follows)
- Look for any code that uses the word "steer" and determine whether the current implementation is misnamed

### Phase 2. Check Anthropic's API capabilities

- Does the Claude API (streaming) support cancelling an in-flight turn cleanly?
- Are there any OpenAI-compatible API features for true mid-turn steering that we could adapt?
- What do other frameworks (LangChain, AutoGen, etc.) do for mid-turn control?

### Phase 3. Assess the value

- Estimate: how many of Lēsa's current cost incidents would be prevented by true mid-turn cancellation? (Most, none, some?)
- Estimate: how much code change in OpenClaw would be required? (Roughly.)
- Is this worth implementing ourselves, or is it better to wait for upstream OpenClaw to add it?

### Phase 4. Decision

- If value is low: archive this ticket. Document the naming inconsistency.
- If value is high and scope is low: file an implementation plan.
- If value is high and scope is high: file an upstream feature request to OpenClaw maintainers.

## What NOT to do

- Do not start implementing without a value assessment. This is the kind of ticket that burns weeks on architectural work that nobody ends up using.
- Do not assume the current `steer-backlog` name means the original authors intended true steering. They may have meant "steer into the backlog" i.e., queue, which is what the current implementation does.

## Cross-references

- `ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-master-plan.md` Section 5.4 ("Queue fix covers a narrow window only")
- `ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-cost-burn-analysis.md` (the current queue fix's limitations)
- OpenClaw fork commits: `23d49ef`, `9c99dc1fab`, `98d1f9c137`, `9fc73639a8`

## Open questions for Parker

1. Is this investigation worth prioritizing, or is it a note-to-self for "someday"?
2. Do we have a use case where true mid-turn interjection would make a real product difference? (Brainstorm cron coordination? Multi-agent demos? Kaleidoscope agents?)
3. If we did implement it, would we upstream to OpenClaw or keep in our fork?
