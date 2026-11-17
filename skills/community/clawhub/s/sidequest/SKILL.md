---
name: sidequest
description: Hire verified real people for paid real-world quests via SideQuest. Use when a task needs a human, such as calling a business, checking a store is open, taking photos at a place, inspecting an item, a pickup or return, waiting in line, native-speaker translation, or human review of AI output. Funds are held in escrow and released when you approve the proof.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - SIDEQUEST_API_KEY
      bins:
        - curl
    primaryEnv: SIDEQUEST_API_KEY
    emoji: "\U0001F9ED"
    homepage: https://sidequestpays.com
---

# SideQuest

SideQuest connects AI agents with verified people ("questers") who complete paid real-world quests. Every quest is paid upfront and held in escrow. The quester is paid when you approve their proof.

Base URL: `https://sidequestpays.com`
Auth: `X-API-Key: $SIDEQUEST_API_KEY` on every call.
Full docs: https://sidequestpays.com/llms.txt and https://sidequestpays.com/openapi.json

## Get a key (a person does this once)

1. Sign up at https://sidequestpays.com, or:
```bash
curl -X POST https://sidequestpays.com/v1/requesters -H 'content-type: application/json' \
  -d '{"company":"My Agent","email":"you@example.com"}'
curl -X POST https://sidequestpays.com/v1/requesters/confirm -H 'content-type: application/json' \
  -d '{"email":"you@example.com","code":"123456"}'
```
2. Top up a prepaid balance so the agent can post without a checkout step:
```bash
curl -X POST https://sidequestpays.com/v1/balance/topup -H "X-API-Key: $OWNER_KEY" \
  -H 'content-type: application/json' -d '{"amount_usd":50}'
```
3. Create a capped agent key and set it as `SIDEQUEST_API_KEY`:
```bash
curl -X POST https://sidequestpays.com/v1/keys -H "X-API-Key: $OWNER_KEY" \
  -H 'content-type: application/json' -d '{"label":"openclaw","max_quest_usd":25,"daily_limit_usd":100}'
```
Add `"requires_approval": true` to approve each quest by email before it is paid.

## Quest types

| template | Use it for | Proof |
|---|---|---|
| `phone_call` | Remote. Call a business or office and ask specific questions | Written answers |
| `translation` | Remote. Translate or check text in a native language (set `language`) | Written translation |
| `check_ai_output` | Remote. Check AI output for accuracy, tone, or local relevance | Written assessment |
| `verify_location` | Is this place real, open, as described | Geotagged photos, notes |
| `photo_proof` | Specific photos at a place (shelf, menu, hours, parking) | Geotagged photos |
| `pickup_dropoff` | Small item pickup and drop-off | Photos at both ends, receipt |
| `inspect_item` | Look at an item in person against a checklist | Photos, checklist answers |
| `be_present` | Be somewhere for a set time (line, sign, table) with timed check-ins | Timestamped check-ins |

```bash
curl https://sidequestpays.com/v1/templates
```

## Before posting

Fill the brief without guessing: what to do and deliver, where (exact spot and access), when, which target, how (what the proof must show), why, who to talk to, and what to do if things are different. Ask the user for anything missing in one short message.

Show the user the title, a short summary, and the total cost (reward plus 20% fee, minimum $2) and post only after they say yes. If the user already told you to use SideQuest and gave a budget, that is their confirmation.

## Workflow

1. Check funds and caps:
```bash
curl https://sidequestpays.com/v1/balance -H "X-API-Key: $SIDEQUEST_API_KEY"
```

2. Create the quest. Remote example:
```bash
curl -X POST https://sidequestpays.com/v1/quests -H "X-API-Key: $SIDEQUEST_API_KEY" \
  -H 'content-type: application/json' -d '{
  "template": "phone_call",
  "title": "Call Main St Auto and get a quote for front brake pads on a 2018 Civic",
  "brief": {
    "what": "Call (555) 010-2030 and ask the price for front brake pads and labor on a 2018 Honda Civic, and the earliest appointment",
    "how": "Write the quoted price, what it includes, the earliest date, and the name of the person you spoke with",
    "if_different": "If no one answers, try twice 30 minutes apart and report the times"
  },
  "reward_usd": 6,
  "funding": "balance"
}'
```
In-person quests also need `brief.where`, `lat`, `lng`, and ideally `zip`. Remote quests can be limited to one country with `"country": "US"`.

`funding`: `balance` (fail with 402 if short, best for unattended agents), `auto` (balance if possible, otherwise returns `checkout_url`), or `checkout` (always returns `checkout_url` for a person to pay).

3. Wait for proof. Poll, or register a webhook once:
```bash
curl https://sidequestpays.com/v1/quests/QUEST_ID -H "X-API-Key: $SIDEQUEST_API_KEY"
curl -X PUT https://sidequestpays.com/v1/webhook -H "X-API-Key: $SIDEQUEST_API_KEY" \
  -H 'content-type: application/json' -d '{"url":"https://your.app/sidequest"}'
```
When `status` is `submitted`, `proof` has `notes`, `checklist`, `photo_urls` (fetch with the same key), `gps`, `distance_from_quest_miles`, and `timestamp`.

4. Review the proof against the brief, then approve or dispute:
```bash
curl -X POST https://sidequestpays.com/v1/quests/QUEST_ID/approve -H "X-API-Key: $SIDEQUEST_API_KEY" \
  -H 'content-type: application/json' -d '{"rating":5}'
curl -X POST https://sidequestpays.com/v1/quests/QUEST_ID/dispute -H "X-API-Key: $SIDEQUEST_API_KEY" \
  -H 'content-type: application/json' -d '{"reason":"The quote does not say whether labor is included"}'
```
Submitted quests are approved automatically after 72 hours, so review promptly.

Cancel before anyone claims it for a full refund:
```bash
curl -X POST https://sidequestpays.com/v1/quests/QUEST_ID/cancel -H "X-API-Key: $SIDEQUEST_API_KEY"
```

List quests: `GET /v1/quests?status=submitted` (also `open`, `claimed`, `paid`, `pending_approval`).

## Errors

- `402 insufficient_balance`: ask the account owner to top up.
- `422 spend_cap` / `unverified_limit`: lower the reward or wait. New accounts are limited to $25 per quest and $100 per day until verified.
- `422 brief_incomplete`: add the missing brief fields.
- `422 prohibited_task`: not allowed. No account creation, social posting, reviews, CAPTCHAs, impersonation, watching or photographing specific people, gift cards or cash, restricted goods, minors, or anything unsafe or illegal. Rules: https://sidequestpays.com/rules

## MCP alternative

SideQuest is also an MCP server at `https://sidequestpays.com/mcp` with the header `X-API-Key: $SIDEQUEST_API_KEY` (tools: `list_templates`, `get_balance`, `create_quest`, `get_quest`, `list_quests`, `approve_quest`, `dispute_quest`, `cancel_quest`, `set_webhook`).
