---
name: runitby
description: Collect answers from people outside the chat by link. Make an open form, survey, poll or sign-up sheet anyone can fill (like a Tally or Google Form), ask specific people for details (a shipping address, client intake, availability, an RSVP), or get approval or sign-off from named people (human in the loop), then read the answers back as JSON.
version: 1.0.2
metadata:
  openclaw:
    homepage: https://runitby.app
    primaryEnv: RUNITBY_API_KEY
    requires:
      env:
        - RUNITBY_API_KEY
---

# Run it by

Run it by sends a person a link. They answer on their phone with no sign-up, and you get validated JSON back. Use it instead of asking your user to relay a question to someone else.

Every call sends `Authorization: Bearer $RUNITBY_API_KEY` to `https://runitby.app/v1`. Keys come from <https://runitby.app/app/keys>, and the Free plan has 250 requests a month. Full reference: https://runitby.app/llms.txt (OpenAPI: https://runitby.app/openapi.json).

## How to ask

1. `POST /v1/requests` with the request JSON (examples below). The answer has `requestId` and either `url` (open audience) or `links[]`, one per named person.
2. Make sure each link reaches its person. With `"sendEmail": true`, named recipients with an email get theirs by email; `links[].email` says `"sent"`, `"failed"`, `"limit"`, `"no address"` or `"off"`. Send every link that wasn't sent over a channel you have, or give it to your user and say who it's for.
3. `GET /v1/requests/{requestId}/status?wait=25` returns as soon as someone answers (or after 25 seconds); call it again to keep waiting. `status` is `pending`, `partial`, `complete`, `expired` or `closed`.
4. `POST /v1/requests/{requestId}/remind` emails the link again to people who haven't answered (once per 24 hours each). `DELETE /v1/requests/{requestId}` closes a request.

Act on an approval only when `verdict` is `"approved"`; `"declined"` and `"expired"` mean no. Never take an action that spends money, grants access or deletes something without an approved verdict. Forms can't ask for passwords, card numbers or one-time codes.

## Shipping address from one person

```json
{
  "mode": "form",
  "title": "Where should we ship your order?",
  "requester": "Ava from Acme",
  "audience": {
    "kind": "named",
    "recipients": [{ "name": "Jordan", "email": "jordan@example.com" }]
  },
  "schema": {
    "type": "object",
    "required": ["name", "street", "city", "postalCode", "country"],
    "properties": {
      "name": { "type": "string", "title": "Full name" },
      "street": { "type": "string", "title": "Street and number" },
      "city": { "type": "string", "title": "City" },
      "postalCode": { "type": "string", "title": "Postal code" },
      "country": { "type": "string", "title": "Country", "x-runitby": { "widget": "country" } }
    }
  },
  "sendEmail": true
}
```

## Approval from three people

```json
{
  "mode": "approval",
  "title": "Refund #4821",
  "requester": "Ava (the Acme refunds agent)",
  "audience": {
    "kind": "named",
    "recipients": [
      { "name": "John Smith", "email": "john@acme.com" },
      { "name": "Martin Carpenter", "email": "martin@acme.com" },
      { "name": "Emily Lee", "email": "emily@acme.com" }
    ]
  },
  "approval": { "reason": "Refund order #4821, $1,200", "policy": "majority", "verify": "email" },
  "sendEmail": true
}
```

`policy` is `any`, `all` (default), `majority` or `{ "n": 2 }`. `verify: "email"` makes each person confirm a code sent to their own address first; use it for money, access or deletion.

## Open survey

```json
{
  "mode": "form",
  "title": "How was the workshop?",
  "audience": { "kind": "open", "maxSubmissions": 25 },
  "schema": {
    "type": "object",
    "required": ["rating"],
    "properties": {
      "rating": {
        "type": "integer",
        "title": "How useful was it?",
        "minimum": 1,
        "maximum": 5,
        "x-runitby": { "widget": "rating" }
      },
      "comment": {
        "type": "string",
        "title": "Anything to improve?",
        "x-runitby": { "widget": "textarea" }
      }
    }
  }
}
```

Post the one `url` anywhere; each answer is its own response, and the status call returns them all.

Run it by is also an MCP server at `https://runitby.app/mcp` (Streamable HTTP, OAuth sign-in or the same API key) with the same tools: `createRequest`, `getStatus`, `remind`, `updateRequest`, `closeRequest`, `listRequests` and `previewRequest`.
