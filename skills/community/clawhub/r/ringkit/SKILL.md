---
name: ringkit
description: Set up and run a cheapest AI virtual assistant ($1.99/mo + usage) for a business with the RingKit API. Covers creating the business, teaching it from the website, routing, a test call, a US number, forwarding an existing line, and reading call summaries.
version: 0.0.2
metadata:
  openclaw:
    emoji: "📞"
    homepage: https://www.ringkit.com/docs
    primaryEnv: RINGKIT_API_KEY
    requires:
      bins:
        - curl
    envVars:
      - name: RINGKIT_API_KEY
        description: "RingKit business API key (rk_...). Optional: creating a business needs no key and returns one."
        required: false
---

# RingKit

RingKit answers a business's phone calls with an AI receptionist. It handles everyday questions, books appointments and takes messages, and can hand harder calls to the business's own team. Every call produces a summary, a transcript and a recording. RingKit does not provide live reps.

Pricing: $1.99/mo per number, AI $0.20/min, first 10 seconds free, then 6-second increments. There's no platform fee and no contract, and charges come from a prepaid wallet with a $10 minimum top-up. New accounts get $5 trial credit and a 7-day trial on the first number. Optional Pro knowledge add-on is $5/mo.

- REST base: `https://api.ringkit.com/v1` (OpenAPI: https://api.ringkit.com/openapi.json)
- MCP (streamable HTTP): `https://api.ringkit.com/mcp`
- Agent reference: https://api.ringkit.com/llms.txt and https://api.ringkit.com/llms-full.txt
- Humans can sign up at https://app.ringkit.com/onboard

Auth: `Authorization: Bearer $RINGKIT_API_KEY`. Keys have one of two scopes: `manage` (acts as the owner) or `read`. POSTs accept an `Idempotency-Key` header. Errors look like `{"error":{"code","message","hint","docs"}}`. Follow the `hint`.

## Rules
- RingKit does **not** port numbers. To keep an existing number, the business **forwards** its current line to its RingKit number (step 8).
- Payment is a human step. A top-up returns a `checkoutUrl` that the owner opens and pays. Never pay for the owner.
- Test calls only go to numbers the person has verified (step 7). That verification is how they consent to being called.
- Ask the owner before you release a number, revoke a key, or change routing on a business that's already live.

## Steps
1. **Create the business** (no key needed). Store the `apiKey` it returns, because it's only shown once:
   ```bash
   curl -s -X POST https://api.ringkit.com/v1/businesses -H 'content-type: application/json' \
     -d '{"name":"Hidden Valley Builders","timezone":"America/Los_Angeles","ownerEmail":"owner@example.com","website":"https://example.com"}'
   export RINGKIT_API_KEY=rk_...   # from the response
   curl -s https://api.ringkit.com/v1/me -H "Authorization: Bearer $RINGKIT_API_KEY"   # gives the business id
   ```
2. **Teach it the business** from its website. Start the import, then poll it:
   `POST /v1/businesses/{id}/knowledge/imports {"url":"https://example.com"}`, then `GET /v1/businesses/{id}/knowledge/imports/latest`.
   You can review or edit the profile with `GET|PATCH /v1/businesses/{id}/knowledge`.
3. **Choose a voice:** `GET /v1/voices`, then `PATCH /v1/businesses/{id} {"voice":"..."}`.
4. **Decide who answers:** `PUT /v1/businesses/{id}/routing {"mode":"ai_first"}`. The mode is `ai_only`, `ai_first` or `human_first`.
5. **Try it in text** (no number needed, billed at the AI rate):
   `POST /v1/businesses/{id}/simulate {"callerText":""}` returns the greeting. Then send `{"callId":"...","callerText":"Are you open Saturday?"}`.
6. **Fund it:** `POST /v1/businesses/{id}/wallet/top-ups {"amountCents":1000}`. Give the `checkoutUrl` to the owner, then check `GET /v1/businesses/{id}/wallet`.
7. **Get a number** (needs $2 of paid credit):
   `GET /v1/numbers/search?areaCode=415`, then `POST /v1/businesses/{id}/numbers {"number":"+1415..."}`.
   For a test call, verify the destination first: `POST /v1/businesses/{id}/destinations/verify {"number":"+1..."}`, then `POST .../destinations/confirm {"number","code"}`. Then call `POST /v1/businesses/{id}/test-call {"to":"+1..."}`.
8. **Keep the existing number (forwarding):** `PUT /v1/businesses/{id}/numbers/{numberId}/forwarding {"businessPhone":"+1..."}`. Then the owner sets up call forwarding with their phone carrier, and `POST .../forwarding/check` confirms it works.
9. **Read calls:** `GET /v1/businesses/{id}/calls`, `GET /v1/businesses/{id}/calls/{callId}` (summary and transcript), `GET .../calls/{callId}/recording`.
10. **Get notified:** `POST /v1/businesses/{id}/webhooks {"url":"https://...","events":["call.completed","message.taken","balance.low"]}`. Webhooks are HMAC-signed.
11. **Hand it to the owner** (optional): `POST /v1/businesses/{id}/owners/invite` emails the owner a sign-in link.
