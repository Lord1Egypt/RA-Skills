---
name: remember-medical-notes
description: Private, authorized health-appointment memory for care continuity. Use when an agent tracks appointments, symptoms, and provider instructions for an authorized user, with consent and confidentiality built in. Requires a BlueColumn API key (bc_live_*).
---

# Remember Medical Notes — BlueColumn Skill

Care continuity lives in the details: the symptom timeline, the provider's instructions, the next follow-up. This skill keeps those details organized and private — for the authorized user and no one else.

> **Privacy first.** Store only what the user authorizes. Never share notes outside the user's context. Use the `private` tag and treat every entry as confidential.

## Record the appointment

After each visit, store the provider, date, key facts, and instructions.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "APPT: Dr. Osei, Jul 30. Bloodwork normal. Started low-dose magnesium. Instructions: increase water, follow up in 6 weeks if symptoms persist.", "title": "appt - Dr. Osei Jul 30", "tags": ["private", "medical"]}'
```

## Prepare for the next visit

Before an appointment, recall the history so the user arrives ready.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What was discussed at the last appointment and what follow-ups were scheduled?"}'
```

## Symptom timeline

Track symptoms over time so patterns become visible instead of anecdotal.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Symptom log: headaches 3x this week, mornings mainly, mild. Tension? hydration? Tracking through Aug 14.", "tags": ["private", "symptom-log"]}'
```

## Care workflow

1. **Capture** — log appointments, instructions, and symptom changes promptly.
2. **Prepare** — recall history before each visit; list questions the user wanted to ask.
3. **Track** — note medication changes and adherence, with dates.
4. **Protect** — keep everything tagged private and accessible only to the authorized user.

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
