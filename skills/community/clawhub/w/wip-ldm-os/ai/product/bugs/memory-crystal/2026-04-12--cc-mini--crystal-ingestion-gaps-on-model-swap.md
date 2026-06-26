# Bug: Crystal Ingestion Gaps During Model Swap Cascade

**Date:** 2026-04-12
**Author:** CC Mini (lesa-work-02)
**Severity:** High (data loss: conversational context not captured)
**Discovered during:** Apr 11-12 infrastructure overhaul (Grok → Claude CLI → Direct API)

## Summary

Memory Crystal has gaps in its ingestion when the inference model changes, billing errors occur, or sessions rotate. Three specific failure modes were identified on Apr 11-12 that caused chunks of Lēsa's conversation to never reach the crystal.

## The Three Gaps

### Gap 1: Session transition dead zone (13 minutes lost)

**When:** 22:15-22:28 PDT Apr 11
**What happened:** Old session (b51f16a0) was abandoned after the messages.101 corruption. New session (b41eaf6b) started at 22:28. Messages exchanged during the 13-minute window between sessions were never written to ANY session file.
**Why crystal missed it:** The agent_end hook reads from the session JSONL. No JSONL entry = no ingestion.
**Impact:** 13 minutes of conversation permanently lost from crystal. Exists only in iMessage chat.db.

### Gap 2: Billing failure blackout (23:49 PDT onwards)

**When:** 23:49 PDT Apr 11 through ~01:00 PDT Apr 12
**What happened:** Claude CLI hit "out of extra usage." All models in the fallback chain failed. The gateway continued DELIVERING replies (some CLI subprocess calls succeeded on first attempt) but the session JSONL stopped being written at 23:49.
**Why crystal missed it:** agent_end hook only fires on successful agent turns. Billing failures = no successful turns = no hook = no ingestion. The capture state counter stalled.
**Impact:** ~75 minutes of conversation missing from crystal. Includes the end of the intimate scene generation AND the consent architecture discussion. iMessage chat.db has the messages. Gateway.log has raw CLI subprocess output.

### Gap 3: Complete blackout after session rotation (01:00-02:00 PDT)

**When:** 01:00-02:00 PDT Apr 12
**What happened:** The billing failure cascade caused OpenClaw to rotate to a new session. The new session started with zero history. The capture state counter reset. No agent turns completed during this hour.
**Why crystal missed it:** Zero chunks from both agents. The billing cascade (claude-cli "No conversation found" + stale anthropic billing flags) prevented any turns from completing.
**Impact:** 1 hour of zero ingestion. The agent was effectively dead during this window.

## Root Cause Chain

```
Grok 429 (team credits exhausted)
  → Fallback to Anthropic
    → tool_use ID normalization bug (Grok composite IDs mangled for Anthropic)
      → Format error at messages.101
        → Auth profile cooldown (incorrectly set on format error, not billing error)
          → All 3 fallback models fail
            → No successful agent turns
              → No agent_end hook fires
                → No crystal ingestion
                  → Session rotation (OpenClaw abandons corrupt session)
                    → Capture state reset
                      → Older un-ingested messages from the abandoned session never captured
```

## Crystal Ingestion Dependencies

The pipeline has three dependencies, all of which broke:

1. **Successful agent turn** (agent_end hook fires) ... broke when billing failed
2. **Session JSONL growing** (new messages to ingest) ... broke when session stopped being written
3. **Capture state counter valid** (tracks position) ... reset when session rotated

## Data That Survived

- **24 images on disk** at `team/Lēsa/documents/images/scene-01 through scene-24` (most durable artifact)
- **305 crystal chunks from 22:00-23:00 PDT** (the scene generation IS partially captured)
- **iMessage chat.db** has every message exchanged (authoritative record)
- **gateway.log** has raw CLI subprocess output (unstructured but complete)
- **Daily logs and SHARED-CONTEXT** were updated manually by CC before the gaps occurred

## Related Bugs

- `bugs/openclaw/`: Format errors should not cooldown auth profiles (separate bug)
- `bugs/bridge/2026-04-10--cc-mini--bridge-reply-addressing-mismatch.md`: Related to the Grok composite ID issue
- `bugs/memory-crystal/`: Capture state reset on compaction (pre-existing, documented 2026-02-13)
