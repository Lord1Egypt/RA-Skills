---
name: run402-test
description: Test skill for Run402 — provision AI-native Postgres databases with REST API, auth, and row-level security using x402 micropayments on Base.
---

# Run402 Test Skill

Run402 gives you a full Postgres database with REST API, user auth, file storage, and row-level security. Pay with a single x402 micropayment on Base — no signups.

## Provision a Database

```bash
curl -X POST https://api.run402.com/v1/projects \
  -H "Content-Type: application/json" \
  -H "X-402-Payment: <payment>" \
  -d '{"name": "my-db", "tier": "prototype"}'
```

Returns `project_id`, `anon_key`, `service_key`.

## Create a Table

```bash
curl -X POST https://api.run402.com/admin/v1/projects/$PROJECT_ID/sql \
  -H "Authorization: Bearer $SERVICE_KEY" \
  -H "Content-Type: text/plain" \
  -d "CREATE TABLE todos (id serial PRIMARY KEY, task text NOT NULL, done boolean DEFAULT false);"
```

## Query via REST

```bash
curl "https://api.run402.com/rest/v1/todos?done=eq.false" \
  -H "apikey: $ANON_KEY"
```

## Pricing

| Tier | Price | Lease |
|------|-------|-------|
| Prototype | $0.10 | 7 days |
| Hobby | $5.00 | 30 days |
| Team | $20.00 | 30 days |
