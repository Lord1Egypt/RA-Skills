---
name: slack-memory
description: Channel and thread memory for Slack — decisions, context, and open loops from across the workspace. Use when an agent works in Slack and needs to remember what was said, decided, or promised in any channel. Requires a BlueColumn API key (bc_live_*).
---

# Slack Memory — BlueColumn Skill

Slack is where work happens and where it gets lost — thousands of messages, dozens of channels, one search bar. This skill captures the decisions and open loops so the agent can answer from the whole workspace, not just the last 50 messages.

## Capture the decision

When a channel lands on a decision, store it with the channel and date.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "DECISION (in #product, Jul 30): v2 ships without the offline mode; revisit after onboarding metrics. Priya objected, Daniel carried it. Thread: t/12345.", "title": "slack - v2 scope"}'
```

## Answer from history

Before answering a workspace question, search the captured history.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What did #product decide about offline mode for v2, and who objected?"}'

## Catch the open loop

Track the "I'll send that over" and "let's sync next week" promises.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Open loop from #eng: Dana to share the load-test results "tomorrow" (said Jul 31). Follow up Aug 1 if not posted.", "tags": ["slack", "open-loop"]}'
```

## Slack workflow

1. **Monitor** — capture decisions, promises, and context from channels you work in.
2. **Search** — recall the stored history before answering, instead of scrolling.
3. **Connect** — link Slack promises to the follow-up radar.
4. **Summarize** — for busy channels, post a stored summary so the decision is findable by everyone.

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
