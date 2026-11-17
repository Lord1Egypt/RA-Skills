---
name: shopping-memory
description: Shopping memory that holds lists, purchases, prices, and "last time I bought X" so agents can help with errands, restocks, and budget questions. Use when an agent tracks household or business purchasing. Requires a BlueColumn API key (bc_live_*).
---

# Shopping Memory — BlueColumn Skill

A shopping list only helps if it exists when you need it. This skill remembers what to buy, what was bought, where, and for how much — so the agent can answer "do we need coffee?" without a trip to the kitchen.

## Add to the list

Capture items the moment they run out or come up.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "SHOPPING: need printer ink (HP 63), coffee beans (light roast), dishwasher pods. Ink last bought Jul 1 at Staples, $42.", "title": "shopping - household run"}'
```

## Check before you go

Pull the current list with any purchase history that informs the trip.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "What is on the shopping list, and where did I last buy these items?"}'

## Track the purchase

After the trip, record what was bought, where, and the price to build a price memory.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "BOUGHT: ink at Staples $42 (was $48 — sale), coffee at the local roaster, pods at Costco. Restock estimate: 6 weeks for ink.", "tags": ["shopping", "purchase"]}'
```

## Shopping workflow

1. **Capture** — add items to the list as they surface.
2. **Prepare** — recall the full list and last-known prices before the trip.
3. **Record** — log purchases with price and place.
4. **Restock** — use purchase history to suggest what to buy next and when.

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
