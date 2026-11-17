---
name: review-times
description: Check how long AI app, connector and plugin store review takes (ChatGPT plugins, Claude connectors and plugins, Meta Muse, Grok, Cursor, Microsoft 365 Agent Store, Gemini CLI, Docker MCP) before submitting or while waiting, and report the user's own submission. Use when planning a launch to one of these stores, when a review seems stuck, or when the user asks how long approval takes.
---

# Review times

Live data from https://reviewtimes.fyi, crowdsourced and read from public review queues.

## Check

```bash
curl -s reviewtimes.fyi                  # every store, one table
curl -s reviewtimes.fyi/claude-plugins   # one store, with how its review works
curl -s reviewtimes.fyi/api/v1/stores/chatgpt   # JSON
```

Slugs: chatgpt, claude-connectors, claude-plugins, muse, grok, clawhub, cursor, copilot, gemini-cli, docker-mcp.

Read `typical_wait_days` as the median days to a decision. If it is null and `typical_wait_is_lower_bound` is true, most submissions have no decision yet: say "${longest_seen_days}+ days, most still waiting", not a number. Mention `pace` (moving, slow, stalled) and `median_to_rejection_days` when rejections come back much faster than approvals.

## Report the user's submission

Only with the user's go-ahead, and only for a real submission:

```bash
curl -s -X POST reviewtimes.fyi/api/v1/reports -H 'content-type: application/json' \
  -d '{"store":"claude-plugins","submitted_on":"2026-09-01","status":"waiting"}'
```

Save the returned `token` (for example in the project's notes) and update it when the store answers:

```bash
curl -s -X PATCH reviewtimes.fyi/api/v1/reports/$TOKEN -H 'content-type: application/json' \
  -d '{"status":"approved","decided_on":"2026-09-20"}'
```
