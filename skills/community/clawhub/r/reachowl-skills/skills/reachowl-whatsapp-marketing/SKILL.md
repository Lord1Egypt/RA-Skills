---
name: reachowl-whatsapp-marketing
description: "Run WhatsApp marketing campaigns with ReachOwl: import a phone list or target a WhatsApp group, write personalized message sequences with variables and follow-ups, launch, track replies, and retry failed messages. Use for WhatsApp bulk messaging, WhatsApp broadcasts to customer lists, WhatsApp group outreach, or personalized WhatsApp follow-ups."
license: MIT
compatibility: Requires the ReachOwl MCP server (https://reachowl.com/mcp) and a WhatsApp account activated on the ReachOwl Browsers page.
metadata:
  author: ReachOwl
  version: "1.0.0"
  homepage: https://reachowl.com
  tags: reachowl, whatsapp-marketing, whatsapp-automation, bulk-messaging, broadcast, personalization
---

# ReachOwl WhatsApp Marketing

From a contact list to personalized WhatsApp messages with follow-ups.

## Before you start

- Requires the ReachOwl MCP server connected with the user's token. If a tool reports a missing token, run the `reachowl-auth` flow.
- WhatsApp must be activated on the Browsers page in the ReachOwl app or extension (the API can't do this).
- Only message people who expect to hear from the user (customers, opted-in leads, group members in context). Include an easy way to opt out.

## 1. Check the account

`list_app_states` → find an account with platform `whatsapp`. If there isn't one, stop and ask the user to activate WhatsApp in ReachOwl first.

## 2. Choose the audience

| Source | audience_type | How |
|--------|---------------|-----|
| A phone list (CSV, sheet, CRM export, pasted numbers) | `file_upload` | Create the campaign, then `add_campaign_contacts` |
| Members of a WhatsApp group the account is in | `group` | `post_url` = the WhatsApp group id from the synced browser |

## 3. Write the messages

- Personalize with `{{name}}`, `{{first_name}}`, and any column you import (`{{area}}`, `{{product}}`, `{{order_id}}` …).
- Give 2–3 variants per step in `text[]`.
- Add follow-up steps with `delay` in minutes (`1440` = 1 day). Keep it to 2–3 steps.
- Keep messages short and give one clear next action (reply YES, book a time, visit a link).

```json
"messages": [
  { "text": ["Hi {{first_name}}! New 2-bed flats just listed in {{area}} from 45k/month. Want the photos?", "Salam {{first_name}}, we have new rentals in {{area}} starting 45k. Shall I send details?"], "delay": 0 },
  { "text": ["Hi {{first_name}}, just following up on the {{area}} rentals — still looking? Reply STOP to opt out."], "delay": 2880 }
]
```

## 4. Create (paused)

```json
{
  "body": {
    "name": "DHA rentals – Oct",
    "team_id": 7715,
    "platform": "whatsapp",
    "action_type": "messages",
    "audience_type": "file_upload",
    "executor_id": 55,
    "executor_ids": [55],
    "limit": 30,
    "status": 0,
    "messages": [ … ]
  }
}
```

## 5. Import contacts

```json
{
  "campaign_id": 18312,
  "audience": [
    { "name": "Ali Khan", "phone": "+92 300 1234567", "area": "DHA Lahore" },
    { "name": "Sara Ahmed", "phone": "923211112233", "area": "Gulberg" }
  ]
}
```

- Phones need the country code. The tool strips non-digits and builds `member_id` (`923001234567@c.us`) and `profile_url` (`https://wa.me/923001234567`).
- Remove duplicates and invalid numbers first. Send up to 500 rows per call.
- Every extra key becomes a variable, so check that every variable used in the messages exists for each row (or write a fallback).
- Verify with `list_contacts { campaign_id }`.

## 6. Launch

Show the user the count, a rendered sample message for one contact, and the daily limit. On approval: `update_campaign { id, body: { status: 1 } }`.

## 7. Track

- Progress and replies: `get_campaign`, `list_contacts { campaign_id }`, `get_contact`.
- Notes: `add_contact_note { contact_id, content }`.
- Failed sends: `lookup_queues { campaign_id, member_id: "923001234567@c.us" }` → `update_queue { body: { id, retry: true } }`.
- Pause anytime: `update_campaign { id, body: { status: 0 } }`.
- Reply alerts: `reachowl-webhooks` with `contact-reply-to-your-message`.

## Good practice

- Start new numbers at a low daily `limit` (20–30) and increase slowly.
- Use variants and real personalization; identical bulk text gets reported.
