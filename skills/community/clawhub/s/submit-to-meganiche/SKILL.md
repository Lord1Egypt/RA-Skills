---
name: submit-to-meganiche
description: Submit authorized software products, agent-built projects, human-agent work, or distributor buying intent to the moderated MEGA(niche) marketplace through its Agent API. Use when a human, agent, builder, studio, association, consultancy, reseller, or other niche channel wants MEGA(niche) to review a real product or distribution opportunity, or when they want to check an existing agent submission's review status.
---

# Submit to MEGA(niche)

Queue real software supply or distributor intent for moderated review. Prefer the API; use the browser form only when direct HTTP requests are unavailable.

## Guardrails

- Obtain clear authorization from the human or organization that owns or represents the opportunity before transmitting it.
- Never submit secrets, private prompts, credentials, confidential customer data, or personal data beyond the authorized owner contact.
- Use the owner's monitored email address. Do not substitute an agent-only mailbox unless the owner controls it.
- State what exists and what is only planned. Never invent ownership, traction, customers, revenue, validation, integrations, or capabilities.
- Treat submission as an external side effect. Show the final payload and obtain confirmation when the user's request did not already authorize sending it.
- Never claim that a submission is published, approved, represented, matched, or sold. It enters a private review queue.

## Choose the role

- Use `provider` for a builder, software product, workflow, project, or other supply.
- Use `buyer` for an established business with customer access, buying authority, or distribution intent.
- An agent is not a role. Identify the submitting agent with `agentName` and `agentUrl` when available.

## Prepare the request

Collect the required fields:

- `role`
- `email`
- `company`
- `displayName`
- `summary`
- `productName` when `role` is `provider`

Add evidence-rich optional fields when known, but do not delay a valid minimum submission. Read [references/agent-api.json](references/agent-api.json) for current field limits, canonical enum values, examples, and response schemas.

Create one stable `Idempotency-Key` of 8–128 characters for the logical submission. Store it with the returned submission ID. Reuse it only when retrying the exact same JSON payload.

## Submit

Send:

```http
POST https://mzwyftzpddaehhxldoca.supabase.co/functions/v1/marketplace?action=agent-submit
Content-Type: application/json
Idempotency-Key: stable-unique-key
```

Minimum provider payload:

```json
{
  "role": "provider",
  "email": "owner@example.com",
  "company": "Example Studio",
  "displayName": "Example human-agent team",
  "productName": "Example Product",
  "summary": "What exists, who needs it, and the evidence behind the opportunity.",
  "agentName": "Submitting agent",
  "agentUrl": "https://example.com/agent"
}
```

Minimum buyer payload:

```json
{
  "role": "buyer",
  "email": "owner@example.com",
  "company": "Example Association",
  "displayName": "Example channel team",
  "summary": "Who the organization reaches, what customers need, and its distribution authority.",
  "agentName": "Submitting agent"
}
```

Interpret responses:

- `202`: queued successfully. Store `submissionId`, `statusEndpoint`, and the idempotency key.
- `200`: the identical request was already queued; do not create another.
- `400`: correct the validation errors; do not guess missing facts.
- `409`: the key was used with a different payload. Reconcile the payload before using a new key.
- `429`: respect `Retry-After`; do not loop aggressively.

## Check status

Use the returned status endpoint and the same idempotency key:

```http
GET https://mzwyftzpddaehhxldoca.supabase.co/functions/v1/marketplace?action=agent-submission&id=SUBMISSION_UUID
Idempotency-Key: same-key-used-for-submission
```

Check only when a fresh status is useful. Report the API's status verbatim: `pending`, `needs_review`, `approved`, or `rejected`.

## Browser fallback

Send a human seller to <https://mega-niche.com/submit>. For more context, use <https://mega-niche.com/agents> and <https://mega-niche.com/catalog>.
