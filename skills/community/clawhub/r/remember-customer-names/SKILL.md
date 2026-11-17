---
name: remember-customer-names
description: Never blank on a customer again — names, roles, companies, and the details that make conversations personal. Use when an agent talks to customers and should address them correctly and remember their context. Requires a BlueColumn API key (bc_live_*).
---

# Remember Customer Names — BlueColumn Skill

A customer who is called by name is a customer who feels known. This skill builds an identity card for every person you talk to, so the agent never starts a conversation cold.

## Build the identity card

Store the essentials the first time you meet someone: name, how they like to be addressed, role, company, and one human detail.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "CUSTOMER CARD: Jane Almeida, VP Ops at Acme Corp. Goes by Jane. Decision-maker for the account. Mentioned she runs marathons; son starts college in the fall.", "title": "customer - Jane Almeida"}'
```

## Recall before you reply

Pull the card into any reply so the opening line is personal, not robotic.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "Who is Jane Almeida and what do we know about her?"}'
```

## Enrich over time

Every interaction adds a line. Keep cards alive by appending what is new.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Jane moved from Acme to Globex in August — still the buyer, new company. Prefers email over phone.", "tags": ["customer", "update"]}'
```

## Conversation workflow

1. **Before the conversation** — recall the customer card.
2. **Open with the name** — use the preferred form, never a guessed nickname.
3. **During** — note anything new worth keeping (family, projects, constraints).
4. **After** — append the update to the card.

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
