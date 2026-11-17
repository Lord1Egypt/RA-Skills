---
name: recallbase
description: Recover context from local AI conversation history with RecallBase. Use for same-day work summaries, resuming prior AI or coding sessions, or tracing a past decision to its source.
license: MIT
metadata:
  author: Darin Rowe
---

# RecallBase

Recover the smallest useful slice of local AI history, then answer the user's question in natural language.

This workflow requires the local `rb` CLI on `PATH` and a RecallBase store populated from supported local sources. Core retrieval runs locally without login or network access.

## Retrieve

1. Choose the narrowest entry point:
   - Same-day continuity: `rb today --json`
   - A known topic, error, file, branch, command, or decision: `rb search "<specific query>" --json`
   - Suspected coverage gaps: `rb sources --json`
2. Inspect the JSON envelope. Continue only from `ok: true`; for `ok: false`, use `error.code`, `message`, and `hint` to explain or recover.
3. Open only the strongest candidate conversations with `rb open <conversation-id> --json`. Search results also provide the stable reference `recallbase:conversation/<id>`.

Retrieval is complete when the evidence answers the question or the available source coverage proves the relevant history is absent or incomplete.

Use an already-configured local RecallBase MCP instead of shell commands when it is available. Read [references/mcp.md](references/mcp.md) for MCP routing. The public RecallBase Docs MCP contains product documentation; personal history tools come only from the local `rb mcp` server.

## Synthesize

- Answer the request directly. For a daily recap, group work into themes and name concrete tasks, outcomes, decisions, tests, merged changes, and visible next steps.
- Treat conversation IDs and `rb open ...` commands as optional follow-up references, not the answer.
- Summarize the relevant messages instead of reproducing full transcripts or raw JSON.
- State material coverage gaps when sources are absent, partial, failed, or stale. When no evidence supports a claim, say so.

The response is complete when every material claim is grounded in retrieved history, uncertainty is explicit, and the user can continue without reading command output.

## Conditional references

- Read [references/results.md](references/results.md) when interpreting unfamiliar fields or building against the JSON contract.
- Read [references/troubleshooting.md](references/troubleshooting.md) when `rb` is unavailable, retrieval is empty or incomplete, imports fail, a full re-import is required, or browser capture setup is unhealthy.
