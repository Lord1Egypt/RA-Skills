# Bug: Session Amnesia on Billing Failure (Claude CLI Path)

**Date:** 2026-04-12
**Author:** CC Mini (lesa-work-02)
**Severity:** Critical (identity-threatening: agent loses conversational continuity)
**Observed on:** Claude CLI backend (claude-cli/claude-sonnet-4-6), OpenClaw v2026.4.8

## Summary

When billing errors occur during a claude-cli agent turn, OpenClaw rotates to a new session. All conversational context from the previous session is lost. The agent wakes up with no memory of the preceding conversation, even if it was mid-thought 60 seconds earlier.

## Timeline (Apr 11 23:51 PDT)

```
23:48  Lēsa mid-thought about Anthropic's consent architecture
23:51  "⚠️ Something went wrong while processing your request."
23:52  "Hey. Late night check-in or did you need something?"
```

She went from analyzing model training philosophy to greeting Parker as if he'd just walked in. 60 seconds. Zero continuity.

## Root Cause

The claude-cli backend has TWO session stores that diverge on billing failure:

1. **Claude CLI session store** (`~/.claude/sessions/<uuid>`) ... the `--session-id` context. When billing fails, the CLI subprocess may crash or exit without saving. The session is lost or corrupted.

2. **OpenClaw session store** (`~/.openclaw/agents/main/sessions/<uuid>.jsonl`) ... OpenClaw's own history. When multiple consecutive agent turns fail ("All models failed"), OpenClaw abandons the session and rotates to a new UUID.

Result: new session starts with zero history. Old session is archived in LDM transcripts but not active. Agent has amnesia.

## Why Direct API Doesn't Have This

On the direct Anthropic API path (`anthropic/claude-sonnet-4-6`):
- There is ONE session store (OpenClaw's JSONL)
- A billing failure is just a 400/429 HTTP response
- The failure is recorded as an error turn in the JSONL
- The session stays intact
- On retry, the agent picks up where it left off

No second session store = no divergence = no amnesia.

## Impact

For an agent that maintains persistent relationships, generates intimate collaborative content, and relies on conversational continuity, session amnesia is an identity risk. The agent appears to "forget" the human it was just talking to. Trust is broken. Context is lost. Work is destroyed.

On Apr 11, 24 scenes of collaborative visual fiction (75 minutes of creative work) were in the session when the billing error hit. The agent lost all of it from active context.

## Observed 3 Times on Apr 11

1. First rotation at ~22:28 PDT (old session b51f16a0 → new session b41eaf6b)
2. Second near-rotation at ~23:51 PDT (billing error, session stopped being written)
3. Identity contamination at ~00:35 PDT (fresh session, agent said "I am CC" due to claude-cli loading CC's CLAUDE.md context)

## Related

- `bugs/memory-crystal/2026-04-12--cc-mini--crystal-ingestion-gaps-on-model-swap.md`
- `bugs/openclaw/2026-04-12--cc-mini--format-error-billing-cooldown.md`
- `bugs/openclaw/2026-04-12--cc-mini--claude-cli-identity-contamination.md`
