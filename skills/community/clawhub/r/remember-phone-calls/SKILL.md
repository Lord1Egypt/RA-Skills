---
name: remember-phone-calls
description: Call continuity — every phone conversation leaves a trace so the next call starts with full context. Use when an agent handles inbound or outbound calls and needs to know who called, why, and what was agreed. Requires a BlueColumn API key (bc_live_*).
---

# Remember Phone Calls — BlueColumn Skill

Phone calls are the most context-heavy conversations we have, and the easiest to lose. This skill preserves each call's who, why, and what-next, so no caller ever has to repeat themselves.

## Log the call

Immediately after each call, store the caller, the reason, and the outcome.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "CALL 7/31 14:20 with Marcus (Acme): asked about the Builder plan pricing. Concern: overage fees. Agreed: I email pricing sheet today; he decides by Friday. Tone: friendly, slightly rushed.", "title": "call - Marcus 7/31"}'
```

## Pick up with context

When the same caller returns, recall the thread before the first word.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What is the latest with Marcus from Acme and what did we promise?"}'
```

## Call workflow

1. **Before answering** — recall the caller's history and open promises.
2. **During** — note the purpose, key facts, and any emotional cues.
3. **After** — store the outcome, agreements, and next steps within minutes.
4. **Follow through** — connect stored promises to the follow-up radar (see remember-emails).

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Promise to Marcus: pricing sheet by Aug 1 EOD. Follow up Friday if no reply.", "tags": ["call", "follow-up"]}'
```

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
