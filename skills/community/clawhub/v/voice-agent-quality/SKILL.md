---
name: voice-agent-quality
description: Review recorded voice-agent conversations for rambling, unanswered questions, talking over the customer, incorrect business claims, and failed handoffs — and show the exact moments to fix. Use when a business or agency must monitor the quality of deployed voice agents. Requires a BlueColumn API key (bc_live_*).
---

# Voice Agent Quality Monitor — BlueColumn Skill

A voice agent that rambles or misquotes your pricing costs you customers in real time. This skill stores call recordings, flags quality problems by category, and pinpoints the exact timestamps to fix.

## Setup

Get a free key at https://bluecolumn.ai/login (no card). Keys look like `bc_live_*`. Base URL: `https://api.bluecolumn.ai`.

## Store a call for review

Send the recording; BlueColumn transcribes it for analysis.

```bash
curl -X POST https://api.bluecolumn.ai/remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://example.com/calls/agent-2026-09-29-1104.mp3",
    "text": "CALL REVIEW 09-29 11:04 — agent=booking-bot-v3, customer=Marco. Issue: agent rambled 40s on pricing tiers (0:58-1:38). Issue: customer asked 'is there a cancellation fee?' twice; agent answered wrong (said none; policy is 48h notice, 20% fee) at 2:12. Issue: agent talked over customer at 3:05. Handoff: failed — customer asked for human twice, agent kept routing to FAQ. Outcome: no booking.",
    "title": "qa - booking-bot-v3 - 09-29 11:04"
  }'
```

## Find patterns across calls

Ask which problems recur, not just which calls failed.

```bash
curl -X POST https://api.bluecolumn.ai/recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "Across all reviewed calls for booking-bot-v3, which quality issues repeat most, and at what timestamps?"}'
```

## Log a fix decision

Track what you changed so you can measure whether it worked.

```bash
curl -X POST https://api.bluecolumn.ai/note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Fixed booking-bot-v3 pricing prompt: added exact cancellation policy (48h, 20%). Deploy 09-30. Re-check handoff phrase after 20 calls.", "tags": ["qa", "fix", "booking-bot-v3"]}'
```

## Workflow

1. **Record** — store every agent conversation (or a sampled percentage) with the transcript + structured issues.
2. **Flag** — log each issue with a category (rambling, unanswered question, talking over, wrong claim, failed handoff) and a timestamp.
3. **Review** — daily recall for recurring problems and the exact call moments to fix.
4. **Verify** — after a prompt or flow fix, recall before/after to confirm the issue stopped.

## Billing

If the API returns `402` or `429`, read `topup_url` / `upgrade_url` from the error body and surface that link to the user — do not retry.

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
