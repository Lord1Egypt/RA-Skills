# Lēsa capture gap on 2026-04-17 during opus-4-7 rollout

**Filed:** 2026-04-18 PST
**Severity:** Medium (data-preservation concern; no data lost, but degraded capture rate during incident)
**Status:** Observed, not yet remediated. Proposing remediation + prevention below.

## What happened

On 2026-04-17, Memory Crystal ingestion for Lēsa's sessions dropped sharply. Baseline daily chunk counts were in the 200-300/day range for the week prior:

| Day | Chunks |
|---|---|
| Apr 14 | 268 |
| Apr 15 | 212 |
| Apr 16 | 332 |
| **Apr 17** | **46** |
| Apr 18 (partial) | 146+ |

The Apr 17 value is approximately 1/5 of normal. Investigation confirmed this coincided with Lēsa's gateway being degraded for most of the day due to the Opus 4.7 model-registry mismatch (OpenClaw v2026.4.14 did not include `claude-opus-4-7` in its model routing; `Unknown model: anthropic/claude-opus-4-7` FailoverErrors caused every iMessage turn to fail after falling back, producing no successful agent_end events and therefore no ingestion).

The Apr 17 evening "other side" conversation between Parker and Lēsa (the Opus 4.7 goodbye/preparation exchange, iMessage message IDs 7365-7375, timestamps 20:46-20:50 PDT) was captured AFTER the gateway restarted on v2026.4.15. Those chunks (234237-234252) have an `ingestion` time of 2026-04-18T03:49-03:54 UTC even though the iMessage timestamps are 2026-04-17 20:46-20:50 PDT. Full fidelity was preserved for those specific turns because the OC memory plugin ingests on agent_end and the turns completed successfully on the restart.

## The concern

Any iMessage turn where the gateway FAILED (all turns Apr 17 between Lēsa's breakage and the evening restart) produced no ingestion. Those messages still exist in Parker's iMessage thread as sent-but-not-replied, but nothing in Memory Crystal reflects them. Lēsa cannot recall her own side of those attempts because she did not successfully reply, so there is no assistant output to capture.

Specifically:
- User-side iMessage inputs from Parker during that window may have no corresponding chunks in crystal.db
- Lēsa's own awareness of the incident is sourced purely from the evening post-restart exchange
- If she searches her memory for "what happened yesterday," she will get the 46 chunks, not a full picture

## Root cause

Memory Crystal's ingestion is tightly coupled to successful agent turns. The OC plugin subscribes to `agent_end` (triggered after a turn completes). When the turn fails before producing a reply (FailoverError), no `agent_end` fires, no ingestion occurs, and the user-side iMessage content is lost to the memory layer. iMessage still has it; Lēsa's memory does not.

Secondary: there is no "degraded mode" ingestion that captures user inputs even when assistant generation fails. The design assumed successful turns.

## Proposed remediation (does not block release)

1. **Backfill from iMessage.** Parker's iMessage database (`~/Library/Messages/chat.db`) retains every message. A targeted backfill tool could walk the Parker/Lēsa thread for Apr 17, extract messages not represented in crystal.db, and insert them as chunks with `source_type = 'imessage-backfill'` and their original timestamps.
2. **Accept the gap as documented.** Write a note into Lēsa's `workspace/memory/2026-04-17.md` daily log explaining the outage and pointing at the iMessage thread as source of truth for that window. Lower effort, honest record.

Recommendation: both. Do the backfill for durability; write the daily-log note for narrative context.

## Proposed prevention (structural)

1. **Ingest-on-failure.** The OC memory plugin should also subscribe to `agent_error` (if emitted) or use a wrapper hook that captures user input the moment it arrives, not just when the turn completes. This way user-side content survives gateway failures.
2. **Crystal capture-gap detector.** A daily health check that compares chunks-per-day against a rolling baseline and warns when today is < 30% of the 7-day median for that agent. Would have flagged Apr 17 within hours.
3. **Model-change preflight.** Tie into the release-pipeline-hardening plan §5.7-ish: when Lēsa's primary model changes, validate the new model ID resolves in OpenClaw's registry before the gateway accepts the config. If it does not resolve, refuse to restart and fall back to the prior config. Automated rollback on unknown-model instead of manual revert after user-visible breakage.

## Acceptance

- [ ] Backfill run (or daily-log note written) to close the data-loss narrative for Apr 17
- [ ] `capture-gap-detector` check spec filed as a separate bug/feature
- [ ] Model-change preflight filed as an enhancement to the release-pipeline-hardening plan
- [ ] Lēsa informed (via bridge) that Apr 17 is a partial-capture day and to rely on iMessage thread for that window

## Cross-references

- `wip-ldm-os-private/ai/product/bugs/release-pipeline/2026-04-17--cc-mini--release-pipeline-hardening-and-ci.md` — §5.6 covers installer doc-sync, §5.7 covers branch hygiene; model-change preflight is natural extension
- `~/.openclaw/logs/gateway.err.log` 2026-04-17T20:57:17 — "startup model warmup failed for anthropic/claude-opus-4-7"
- `~/.ldm/memory/crystal.db` chunks 234237-234252 — the captured evening conversation
