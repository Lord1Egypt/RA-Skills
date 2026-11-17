---
name: remember-birthdays
description: A personal date radar for birthdays and anniversaries. Use when an agent should greet someone on time, never double-book a celebration, or answer "whose special day is coming up". Requires a BlueColumn API key (bc_live_*).
---

# Remember Birthdays — BlueColumn Skill

People remember you when you remember their day. This skill keeps a searchable calendar of the dates that matter — birthdays, anniversaries, memorial days — so an agent can greet the right person at the right moment.

## Capture the date

Save each date the moment you learn it. Include the person's name, the date, and what kind of day it is.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Jane Almeida — birthday March 14. Wedding anniversary November 2 (married 2019).", "title": "dates - Jane Almeida"}'
```

## Recall who is next

Before any greeting task, ask which dates are approaching so you never surprise a user with a missed one.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "Whose birthday or anniversary is in the next 14 days?"}'
```

## Greeting workflow

1. **Check the radar** — recall upcoming dates for the next two weeks.
2. **Confirm the person** — verify name and date before drafting anything.
3. **Draft warm, not generic** — mention the relationship or a past detail if one is stored.
4. **Mark it done** — store a short note that the greeting was sent, so it is not sent twice.

## Tag for filtering

Use the quick-note endpoint with the `birthday` tag for lightweight additions without a title:

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Marcus — birthday June 3, prefers no public mention.", "tags": ["birthday", "privacy"]}'
```

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
