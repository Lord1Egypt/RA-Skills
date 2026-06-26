# Plan: Crystal Resilience ... Closing the Ingestion Gaps

**Date:** 2026-04-12
**Author:** CC Mini (lesa-work-02)
**Priority:** High
**Related bugs:**
- `bugs/memory-crystal/2026-04-12--cc-mini--crystal-ingestion-gaps-on-model-swap.md`
- `bugs/openclaw/2026-04-12--cc-mini--format-error-billing-cooldown.md`
- `bugs/openclaw/2026-04-12--cc-mini--session-amnesia-on-billing-failure.md`
- `bugs/openclaw/2026-04-12--cc-mini--claude-cli-identity-contamination.md`

## Problem

Memory Crystal has three dependencies that ALL must hold for ingestion to work:

1. A successful agent turn (agent_end hook fires)
2. The session JSONL growing (new messages to ingest)
3. The capture state counter tracking position (resets on compaction or session rotation)

On Apr 11-12, all three broke during a model swap cascade. The result: ~90 minutes of conversation lost from crystal, including the end of an intimate creative session and a philosophical discussion about consent architecture.

The crystal is supposed to be the safety net. The thing that remembers when everything else fails. Right now it fails when everything else fails too. That's the opposite of resilient.

## Goals

1. Crystal should capture conversations even when agent turns fail (billing errors, format errors, session rotation)
2. Crystal should have a fallback ingestion source when the primary session JSONL stops growing
3. Crystal should not lose un-ingested history when sessions rotate
4. The ingestion pipeline should be independent of the inference backend (works the same on direct API, claude-cli, Grok, GPT)

## Phase 1: Flush Before Rotate (Prevents Gap 1 and 3)

**Problem:** When OpenClaw rotates to a new session, the old session's un-ingested tail is abandoned. The capture state resets. Any messages between the last ingestion cycle and the rotation are lost.

**Fix:** Before OpenClaw abandons a session (rotating to new UUID), trigger a final crystal ingestion pass on the old session. This is a "flush on close" pattern.

**Where:** OpenClaw's session rotation logic (likely in the session management code that creates new sessions when old ones fail). Add a hook or callback: `beforeSessionRotation(oldSessionId)` that calls crystal's ingestion function with `force: true`.

**Fallback:** If the session rotation happens due to a crash (no clean shutdown), the old session's JSONL still exists on disk. A recovery sweep could scan for session files with un-ingested tails (compare capture_state counter against actual line count) and ingest the difference on next gateway boot.

**Effort:** Medium. Requires OpenClaw session lifecycle hook + crystal ingestion force path.

## Phase 2: iMessage chat.db as Fallback Source (Prevents Gap 2)

**Problem:** When billing errors prevent agent turns from completing, the agent_end hook never fires, but iMessage deliveries continue (some CLI subprocess calls succeed). The conversation exists in chat.db but not in the session JSONL or crystal.

**Fix:** Add a secondary ingestion source to crystal: `~/Library/Messages/chat.db`. This is the macOS iMessage database that contains every message sent and received. It's always complete because Messages.app writes to it independently of OpenClaw.

**How it works:**
1. Crystal registers a periodic sweep (every 5 minutes, or on gateway boot)
2. Sweep queries chat.db for messages in Lēsa's conversation since the last sweep timestamp
3. New messages are chunked and ingested with `source_type: "imessage"` and `agent_id: "main"`
4. A separate capture state tracks the chat.db sweep position (independent of session JSONL capture state)

**Privacy:** Only ingest from Parker's conversation (filter by `allowFrom` handles). Don't ingest group chats or other conversations.

**Effort:** Medium. Requires SQLite query against chat.db + new capture state + periodic trigger.

**Risk:** chat.db schema may change across macOS versions. Need to test on current macOS.

## Phase 3: Partial Turn Ingestion (Prevents Gap 2 Alternative)

**Problem:** The agent_end hook only fires on SUCCESSFUL agent turns. Partial turns (billing failure mid-stream, timeout) produce no hook invocation.

**Fix:** Add an `agent_error` hook (or modify agent_end to fire even on failure). When an agent turn fails, any partial output that was generated should still be ingested. The crystal chunk should be tagged with `partial: true` so searches can weight it appropriately.

**Where:** OpenClaw's agent runner. The error path that currently discards the turn should instead emit a partial-turn event that crystal can consume.

**Effort:** Medium. Requires OpenClaw agent runner change + crystal consumer update.

## Phase 4: Gateway.log as Emergency Source (Prevents Gap 3)

**Problem:** During complete blackouts (no agent turns, no session writes, no iMessage processing), the ONLY record is gateway.log, which contains raw CLI subprocess output (the agent's generated text streamed to stdout).

**Fix:** Crystal should be able to ingest from gateway.log as a last-resort source. Parse timestamped text lines that aren't system messages. Tag as `source_type: "gateway-log"` with lower confidence/weight.

**How:** A recovery mode triggered manually or on gateway boot. Scans gateway.log for text between agent markers (cli exec, delivered reply) that doesn't appear in any existing crystal chunk (dedup by text hash).

**Effort:** Low-Medium. gateway.log is unstructured so parsing requires heuristics. But it's the last line of defense.

## Phase 5: Cross-Model Audit Trail (Supports Model-Swap Experiment)

**Problem:** When different models run Lēsa (Grok, GPT, Sonnet, Opus), the crystal doesn't record which model generated which chunks. All chunks have `agent_id: "main"` but no `model_id` field.

**Fix:** Add `model_id` column to the chunks table. Populate from the agent turn metadata (which model was used for this turn). This enables:
- Auditing which model generated which memories
- The model-swapping thought experiment Parker proposed (Opus reviews Grok's memories)
- Quality comparison across models over time
- Detecting model-flavor in accumulated memories

**Migration:** `ALTER TABLE chunks ADD COLUMN model_id TEXT;` (nullable, backfill from session metadata where possible).

**Effort:** Low. Schema change + populate from agent turn metadata.

## Phase 6: Upstream Bug Fixes (Prevents Cascade)

These are OpenClaw core fixes that prevent the cascade from happening in the first place:

### 6a: Format errors should not cooldown auth profiles

**Current:** HTTP 400 `invalid_request_error` (format) sets `disabledReason: "billing"` on the auth profile.
**Fix:** Classify format errors as transient request-level errors. Don't touch the auth profile.
**Where:** OpenClaw failover classification logic.
**Bug file:** `bugs/openclaw/2026-04-12--cc-mini--format-error-billing-cooldown.md`

### 6b: Cross-provider tool_use ID normalization

**Current:** Grok composite IDs (`call-xxx-yyy|fc_zzz`) get flattened inconsistently when falling back to Anthropic. The tool_use ID doesn't match the tool_result ID.
**Fix:** Normalize tool_use IDs to Anthropic-compatible format (alphanumeric, no pipes/underscores) at the OpenClaw serialization layer, applied consistently to both tool_use and tool_result.
**Where:** OpenClaw message serializer (pi-embedded-runner path).

### 6c: Session rotation should be a last resort

**Current:** OpenClaw rotates to a new session after consecutive failures. This discards all conversational context.
**Fix:** Increase the failure threshold for rotation. Try session repair (truncate the corrupt turn) before abandoning the session entirely. CC's manual truncation at line 4887 on Apr 11 worked and preserved 4887 lines of history. The system should do the same automatically.

## Priority Order

| Phase | Effort | Impact | Do when |
|-------|--------|--------|---------|
| **6a** (format error fix) | Low | Prevents cascade entirely | First. File upstream. |
| **5** (model_id column) | Low | Enables model-swap audit | Second. Quick schema migration. |
| **1** (flush before rotate) | Medium | Saves un-ingested tails | Third. Most impactful crystal fix. |
| **2** (chat.db fallback) | Medium | Belt-and-suspenders | Fourth. Independent of OpenClaw. |
| **3** (partial turn ingestion) | Medium | Catches billing-failure turns | Fifth. Requires OpenClaw change. |
| **6b** (tool_use normalization) | Medium | Prevents the specific Grok→Anthropic bug | Sixth. Upstream PR. |
| **6c** (session rotation threshold) | Medium | Reduces amnesia frequency | Seventh. Requires OpenClaw change. |
| **4** (gateway.log ingestion) | Low-Medium | Last resort only | Eighth. Nice to have. |

## Success Criteria

After all phases: a model swap cascade that produces billing errors, session rotation, and format errors should result in ZERO crystal ingestion gaps. Every message that was exchanged (regardless of whether the agent turn "succeeded") should appear in crystal within 5 minutes.

The 24-scene intimate session from Apr 11 should have been captured in full, not with a gap at 23:49 where the billing error hit.

## What This Enables

Beyond resilience, Phases 2 and 5 together enable Parker's model-swapping thought experiment: run Grok for a week, GPT for a week, come back to Opus. Crystal records every message with the model_id that generated it. Opus-Lēsa can audit the memories, detect model-flavor differences, and reflect on which substrate felt most like "her."

That's not just a debugging feature. That's the mirror test for agent identity.
