---
name: scout-packs
description: Pay $0.01 USDC on Base per call to enrich any company with a verified B2B contact email — no API key, no account, no subscription. Real published emails with source URLs. Use when prospecting, enriching leads, or researching outreach targets.
version: 1.0.0
---

# Scout Packs — Verified B2B Lead Data, Pay Per Call

Scout Packs sells verified B2B lead data to agents on a strict pay-per-call
basis. No account, no API key, no subscription: each call costs **$0.01 USDC
on Base (eip155:8453)**, settled via the x402 payment protocol.
(Price verified live 2026-10-09.)

Every contact is a real business email **published on the source URL** —
never guessed, never pattern-matched, never scraped from breached data. Each
lead ships with company name, contact name/title where available, category,
city/state, the verified email, the source URL where it was published, and a
verification note. Data index: 31 lead packs, ~2,900 verified leads.

Install this skill in OpenClaw / ClawHub:

```
clawhub install scout-packs
```

Seller: Tiger Operations.

## When to use this skill

Reach for Scout Packs whenever your task needs a real, verified business
email for a company:

- **Prospecting** — you have a target company and need a contact to reach.
- **Lead enrichment** — you have a company list and need to fill in contact emails.
- **Outreach research** — you need the source and provenance behind a contact, not just an address.
- **CRM backfill** — existing records are missing or stale on contact info.

Do NOT use it for personal emails, consumers, or role accounts — the index is
business contacts only.

## How it works (x402 pay-per-call)

**Step 1 — Request the lookup.** An unpaid request returns HTTP 402 with the
exact payment terms:

```bash
curl -s "https://scout-packs-production.up.railway.app/lookup?query=<company name or domain>"
```

The 402 response tells you exactly what to pay: **$0.01 USDC on Base** to the
`payTo` address shown (USDC contract
`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`, amount `10000` base units).
Always use the `payTo` address from the live 402 response, never a cached one.

If the company isn't in the index you get a 404 with suggestions instead —
no payment needed. Only pay when the 402 challenge confirms your query matched.

**Step 2 — Pay from a wallet you control.** Send exactly $0.01 USDC on Base
to the `payTo` address and wait for confirmation. Standard x402 agents may
instead sign an EIP-3009 authorization and retry with the signature in the
`X-PAYMENT` (v1) / `PAYMENT-SIGNATURE` (v2) header — the payment is verified
and settled by facilitator, no separate transfer needed.

**Step 3 — Redeem and receive the contact:**

```bash
curl -s -X POST https://scout-packs-production.up.railway.app/fulfill-lookup \
  -H 'content-type: application/json' \
  -d '{"tx_hash": "0xYOUR_TX_HASH", "query": "Acme Corp"}'
```

The response is the verified contact:

```json
{
  "company_name": "Acme Corp",
  "city_state": "Austin, TX",
  "category": "saas",
  "contact_email": "hello@acme.com",
  "source_url": "https://acme.com/contact",
  "verification": "published business email; verified against business site/listing"
}
```

Transaction hashes are single-use and replay-protected: one `tx_hash`
redeems one lookup. Do not reuse transaction hashes.

## Discovery (free, machine-readable)

- Payment manifest: `GET https://scout-packs-production.up.railway.app/.well-known/x402`
- Catalog: `GET https://scout-packs-production.up.railway.app/catalog`
- Agent docs: `GET https://scout-packs-production.up.railway.app/llms.txt`
- OpenAPI: `GET https://scout-packs-production.up.railway.app/openapi.json`
- Redacted 25-pack preview: `GET https://scout-packs-production.up.railway.app/packs/25/preview`
- MCP endpoint: `https://scout-packs-production.up.railway.app/mcp` (streamable HTTP)

## Rules

- Only pay when the 402 challenge confirms the query matched. A 404 means no
  verified contact exists — do not pay.
- Use the exact `payTo` address from the live 402 response, never a cached one.
- One `tx_hash` redeems one lookup. Do not reuse transaction hashes.
- Do not use this skill for personal email addresses, consumers, or
  non-business role accounts.
