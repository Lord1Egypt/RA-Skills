---
name: travel-memory
description: Travel memory that holds plans, preferences, and past trips so agents can plan, rebook, and advise without re-asking. Use when an agent helps with itineraries, bookings, or "what did I like last time". Requires a BlueColumn API key (bc_live_*).
---

# Remember Travel — BlueColumn Skill

Every trip starts with the same questions: where did we stay, what did we like, what do we avoid. This skill keeps the answers — plans, preferences, and history — so the next trip plans itself faster.

## Log the trip plan

Store the itinerary and the choices that matter for rebooking.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "TRIP: Lisbon Oct 12-19. Stay: Alfama, airbnb (booked). Flight: TAP outbound 6:40am (hate early — note for next time). Must-do: Sintra day trip, Time Out Market dinner.", "title": "trip - Lisbon Oct"}'

## Plan the next one

Before booking anything, recall past preferences and history.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What travel preferences and past trips should inform booking a new trip?"}'

## Record the lessons

After the trip, store what to repeat and what to skip.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Lisbon lessons: Alfama airbnb was perfect (quiet, close to tram 28). TAP early flight was brutal — book afternoon departures. Sintra needs a full day, not half.", "tags": ["travel", "lessons"]}'

## Travel workflow

1. **Plan** — recall preferences and past trips before proposing anything.
2. **Book** — store bookings with the details that matter for changes.
3. **During** — note favorites and annoyances as they happen.
4. **After** — write the lessons so the next trip starts smart.

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
