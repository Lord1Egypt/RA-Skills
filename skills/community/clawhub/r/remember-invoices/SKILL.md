---
name: remember-invoices
description: Billing memory that tracks invoices, payment status, and follow-ups so revenue is never lost in a thread. Use when an agent handles billing, chases payments, or answers "what is outstanding". Requires a BlueColumn API key (bc_live_*).
---

# Remember Invoices — BlueColumn Skill

An unpaid invoice is a conversation, not a number. This skill keeps the full billing picture — issued, paid, overdue, disputed — so the agent can chase money without ever chasing context.

## Record the invoice

Store every invoice the moment it is issued: amount, client, due date, status, and the payment channel.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "INVOICE INV-1042: $4,800 to Acme Corp, issued Jul 28, due Aug 27, status OPEN. Sent via Stripe; client pays by ACH.", "title": "invoice - INV-1042 Acme"}'
```

## Check what is outstanding

Before any billing conversation, pull the open and overdue list.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "Which invoices are unpaid or past due, and who owes what?"}'
```

## Chasing workflow

1. **Context first** — recall the client's payment history and any prior promises.
2. **Gentle first touch** — reference the invoice number and due date, assume it slipped.
3. **Escalate with evidence** — if overdue, pull the original terms and prior messages.
4. **Record the outcome** — mark paid, or store the new promised date.

```bash
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "INV-1042: Acme confirmed payment routed, ETA Aug 5. Note: they asked for net-30 terms going forward.", "tags": ["invoice", "update"]}'
```

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
