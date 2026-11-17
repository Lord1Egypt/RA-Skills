---
name: remember-emails
description: Tracks email threads, promised actions, and follow-ups so nothing falls through the cracks. Use when an agent manages correspondence and needs to know what was promised, to whom, and by when. Requires a BlueColumn API key (bc_live_*).
---

# Remember Emails — BlueColumn Skill

Email threads have a memory of their own — promises, deadlines, and loose ends. This skill records the state of every important thread so the agent knows what is pending without re-reading the inbox.

## Log the thread state

After any meaningful exchange, store who promised what and the deadline.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "THREAD: with Sarah Kim re: vendor contract. We promised revised pricing sheet by Aug 5. She owes us the signed NDA. Last message: hers, Jul 30.", "title": "email - vendor contract"}'
```

## Follow-up radar

Before starting the day's email, ask what is pending and overdue.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "Which email threads have open promises or deadlines this week?"}'
```

## Draft from context

When drafting a follow-up, pull the thread state so the message references the real last touchpoint.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What was the last exchange with Sarah Kim about the vendor contract?"}'
```

## Email workflow

1. **On send** — store what was promised and by when.
2. **Daily** — recall open promises; flag anything overdue or due this week.
3. **On reply** — pull the thread state first, then draft with the real context.
4. **On resolution** — close the thread by storing the outcome, so it stops resurfacing.

## Tag for filtering

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Follow up with Sarah Kim on Aug 5 — pricing sheet due.", "tags": ["email", "follow-up"]}'
```

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
