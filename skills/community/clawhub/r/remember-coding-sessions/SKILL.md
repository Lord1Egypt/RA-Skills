---
name: remember-coding-sessions
description: Developer continuity across coding sessions — architecture decisions, TODOs, and handoffs stay searchable. Use when an agent assists on a codebase and needs to resume work exactly where it stopped. Requires a BlueColumn API key (bc_live_*).
---

# Remember Coding Sessions — BlueColumn Skill

The most expensive bug in software is "where was I?". This skill records architecture decisions and session state so every coding session starts from a clean handoff instead of a blank screen.

## Log the decision

When a meaningful choice is made (library, schema, pattern), store the decision, the reason, and the rejected alternatives.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "DECISION: use SQLite for the sync cache. Reason: zero-ops, local-first. Rejected: Postgres (too heavy for a client cache), Redis (extra process). Date: 2026-07-31.", "title": "arch - sync cache storage"}'
```

## Resume the session

At the start of a new session, recall the last state before touching any code.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What was the last in-progress task and open TODO on this project?"}'
```

## Handoff ritual

End every session with a short handoff note so the next session (or teammate) can pick up in seconds.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "HANDOFF: auth middleware refactor ~80% done. Next: finish token refresh test. Blocked on: deciding expiry window (open question in #backend).", "tags": ["coding", "handoff"]}'
```

## Coding workflow

1. **Resume** — recall last task, open TODOs, and the active branch context.
2. **Act** — make the change; when you hit a fork, store the decision before moving on.
3. **Record** — log commits, gotchas, and anything a future you would thank you for.
4. **Hand off** — write the handoff note; it doubles as the next session's brief.

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
